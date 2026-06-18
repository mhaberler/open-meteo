#!/usr/bin/env python3
"""Shared loader for ICON-D2 pressure-level vs native model-level soundings.

Fetches both sources once (model levels from the private server, pressure levels
from the public api), builds per-hour profiles, and returns them for plotting.
Import-safe: no network or matplotlib at import time — call load()."""
import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

BASE_MODEL = "https://open-meteo.mah.priv.at/v1/forecast"   # native model levels
BASE_PRESS = "https://api.open-meteo.com/v1/forecast"        # pressure levels (public)
META_MODEL = "https://open-meteo.mah.priv.at/data/dwd_icon_d2/static/meta.json"
META_PRESS = "https://api.open-meteo.com/data/dwd_icon_d2/static/meta.json"

# ICON-D2 native pressure levels (Sources/App/Icon/Icon.swift:111)
PLEVELS = [1000, 975, 950, 850, 700, 600, 500, 400, 300, 250, 200]
LEVELS = range(1, 66)                # 65 native model full levels

PROFILE_KEYS = ("h", "p", "T", "Dew", "Dir", "Spd", "RH")


@dataclass
class Sounding:
    lat: float
    lon: float
    elev: float
    times: list                      # steppable valid-time strings (model hours with data)
    profiles: dict                   # t -> (ml, ref); each {h,p,T,Dew,Dir,Spd,RH} lists, surface->top
    run_model: str
    run_press: str
    run_note: str


def geocode(name, count=1):
    """Resolve a place name to (lat, lon, label) via the Open-Meteo geocoding API.

    Returns None if there is no match."""
    q = urllib.parse.urlencode({"name": name, "count": count,
                                "language": "en", "format": "json"})
    url = f"https://geocoding-api.open-meteo.com/v1/search?{q}"
    with urllib.request.urlopen(url, timeout=30) as r:
        results = json.load(r).get("results")
    if not results:
        return None
    g = results[0]
    label = ", ".join(str(g[k]) for k in ("name", "admin1", "country_code") if g.get(k))
    return g["latitude"], g["longitude"], label


def _utc(ts):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(ts))


def _run_init(meta_url):
    with urllib.request.urlopen(meta_url, timeout=30) as f:
        return _utc(json.load(f)["last_run_initialisation_time"])


def _fetch(base, lat, lon, hourly, forecast_days):
    query = {
        "latitude": lat, "longitude": lon,
        "hourly": ",".join(hourly),
        "models": "icon_d2",
        "wind_speed_unit": "ms",
        "timezone": "GMT",
        "forecast_days": forecast_days,
    }
    q = urllib.parse.urlencode(query)
    with urllib.request.urlopen(f"{base}?{q}", timeout=120) as r:
        return json.load(r)


def _empty():
    return {k: [] for k in PROFILE_KEYS}


def load(lat=48.717, lon=8.750, forecast_days=2):
    """Fetch both sources and build per-hour profiles. Returns a Sounding."""
    run_model = _run_init(META_MODEL)
    run_press = _run_init(META_PRESS)
    run_note = "same run" if run_press == run_model else "RUN MISMATCH"

    model_vars = []
    for n in LEVELS:
        model_vars += [f"height_level{n}", f"pressure_level{n}", f"temperature_level{n}",
                       f"relative_humidity_level{n}", f"dew_point_level{n}",
                       f"wind_speed_level{n}", f"wind_direction_level{n}"]
    press_vars = []
    for p in PLEVELS:
        press_vars += [f"temperature_{p}hPa", f"relative_humidity_{p}hPa", f"dew_point_{p}hPa",
                       f"wind_speed_{p}hPa", f"wind_direction_{p}hPa", f"geopotential_height_{p}hPa"]

    dm = _fetch(BASE_MODEL, lat, lon, model_vars, forecast_days)   # private server
    dp = _fetch(BASE_PRESS, lat, lon, press_vars, forecast_days)   # public api

    elev = dm["elevation"]           # common ground datum (same icon_d2 grid)
    Hm = dm["hourly"]
    Hp = dp["hourly"]
    pidx = {t: i for i, t in enumerate(Hp["time"])}   # pressure valid-time -> index

    # master timeline: model hours that actually carry data
    times = [t for i, t in enumerate(Hm["time"]) if Hm["temperature_level65"][i] is not None]
    if not times:
        raise SystemExit("no model-level data in response")

    def build(t):
        im = Hm["time"].index(t)
        ip = pidx.get(t)

        ml = _empty()                # native model levels (private server)
        for n in LEVELS:
            h  = Hm[f"height_level{n}"][im]
            p  = Hm[f"pressure_level{n}"][im]
            T  = Hm[f"temperature_level{n}"][im]
            rh = Hm[f"relative_humidity_level{n}"][im]
            td = Hm[f"dew_point_level{n}"][im]
            sp = Hm[f"wind_speed_level{n}"][im]
            dr = Hm[f"wind_direction_level{n}"][im]
            if None in (h, p, T, rh, td, sp, dr):
                continue
            for k, v in zip(ml, (h - elev, p, T, td, dr, sp, rh)):
                ml[k].append(v)

        ref = _empty()               # pressure levels (public api, reference)
        if ip is not None:
            for p in PLEVELS:
                gz = Hp[f"geopotential_height_{p}hPa"][ip]
                T  = Hp[f"temperature_{p}hPa"][ip]
                rh = Hp[f"relative_humidity_{p}hPa"][ip]
                td = Hp[f"dew_point_{p}hPa"][ip]
                sp = Hp[f"wind_speed_{p}hPa"][ip]
                dr = Hp[f"wind_direction_{p}hPa"][ip]
                if None in (gz, T, rh, td, sp, dr):
                    continue
                for k, v in zip(ref, (gz - elev, p, T, td, dr, sp, rh)):
                    ref[k].append(v)

        for prof in (ml, ref):       # sort surface -> top
            order = sorted(range(len(prof["h"])), key=lambda j: prof["h"][j])
            for k in prof:
                prof[k] = [prof[k][j] for j in order]
        return ml, ref

    profiles = {t: build(t) for t in times}
    return Sounding(lat, lon, elev, times, profiles, run_model, run_press, run_note)
