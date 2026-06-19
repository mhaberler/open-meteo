#!/usr/bin/env python3
"""Loader for an ICON-GLOBAL single-hour sounding: dev-server native model levels
vs public-api pressure levels.

Model levels (120 native full levels, 120≈surface .. 1=top) come from the private
dev server; pressure levels (18) come from the public Open-Meteo api, both for
`models=icon_global`. Builds one valid-hour profile for each source.

Import-safe: no network at import time — call load(). Reuses geocode() from
sounding_data.py."""
import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

from sounding_data import geocode  # noqa: F401  (re-exported for callers)

BASE_MODEL = "https://open-meteo-dev.mah.priv.at/v1/forecast"   # native model levels (dev)
BASE_PRESS = "https://api.open-meteo.com/v1/forecast"           # pressure levels (public)
META_MODEL = "https://open-meteo-dev.mah.priv.at/data/dwd_icon/static/meta.json"
META_PRESS = "https://api.open-meteo.com/data/dwd_icon/static/meta.json"

MODEL = "icon_global"
# ICON global native pressure levels (Sources/App/Icon/Icon.swift:108)
PLEVELS = [30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000]
LEVELS = range(1, 121)               # 120 native model full levels
SURFACE_LEVEL = 120                  # lowest (near-surface) full level

PROFILE_KEYS = ("h", "p", "T", "Dew", "Dir", "Spd", "RH")


@dataclass
class GlobalSounding:
    lat: float
    lon: float
    elev: float
    time: str                        # the single valid-time string (UTC, no Z)
    ml: dict                         # native model levels  {h,p,T,Dew,Dir,Spd,RH}, surface->top
    ref: dict                        # public pressure levels {…}, surface->top (may be empty)
    run_model: str
    run_ref: str
    run_note: str


def _utc(ts):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(ts))


def _run_init(meta_url):
    """Best-effort run timestamp; '?' when the /data route is gated/unavailable."""
    try:
        with urllib.request.urlopen(meta_url, timeout=30) as f:
            return _utc(json.load(f)["last_run_initialisation_time"])
    except Exception:
        return "?"


def _fetch(base, lat, lon, hourly, past_days, forecast_days):
    query = {
        "latitude": lat, "longitude": lon,
        "hourly": ",".join(hourly),
        "models": MODEL,
        "wind_speed_unit": "ms",
        "timezone": "GMT",
        "past_days": past_days,
        "forecast_days": forecast_days,
    }
    q = urllib.parse.urlencode(query)
    with urllib.request.urlopen(f"{base}?{q}", timeout=120) as r:
        return json.load(r)


def _empty():
    return {k: [] for k in PROFILE_KEYS}


def load(lat=46.9911, lon=15.4396, target=None, past_days=2, forecast_days=1):
    """Fetch both sources, build the single-hour profiles. Returns a GlobalSounding.

    target: valid-time string ("YYYY-MM-DDTHH:MM"); defaults to the first model hour
    that actually carries data. The dev ingest may be in the recent past, so the window
    spans past_days..forecast_days rather than future-only forecast_hours."""
    run_model = _run_init(META_MODEL)
    run_ref = _run_init(META_PRESS)
    if "?" in (run_model, run_ref):
        run_note = "run unknown"
    else:
        run_note = "same run" if run_model == run_ref else "RUN MISMATCH"

    model_vars = []
    for n in LEVELS:
        model_vars += [f"height_level{n}", f"pressure_level{n}", f"temperature_level{n}",
                       f"relative_humidity_level{n}", f"dew_point_level{n}",
                       f"wind_speed_level{n}", f"wind_direction_level{n}"]
    press_vars = []
    for p in PLEVELS:
        press_vars += [f"temperature_{p}hPa", f"relative_humidity_{p}hPa", f"dew_point_{p}hPa",
                       f"wind_speed_{p}hPa", f"wind_direction_{p}hPa", f"geopotential_height_{p}hPa"]

    dm = _fetch(BASE_MODEL, lat, lon, model_vars, past_days, forecast_days)   # dev server
    dp = _fetch(BASE_PRESS, lat, lon, press_vars, past_days, forecast_days)   # public api

    elev = dm["elevation"]
    Hm = dm["hourly"]
    Hp = dp["hourly"]
    pidx = {t: i for i, t in enumerate(Hp["time"])}   # pressure valid-time -> index

    sfc = Hm[f"temperature_level{SURFACE_LEVEL}"]
    hours = [t for i, t in enumerate(Hm["time"]) if sfc[i] is not None]
    if not hours:
        raise SystemExit("no model-level data in response")
    t = target if (target and target in hours) else hours[0]
    im = Hm["time"].index(t)
    ip = pidx.get(t)

    ml = _empty()                    # native model levels (dev server)
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

    ref = _empty()                   # pressure levels (public api, reference)
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

    for prof in (ml, ref):           # sort surface -> top
        order = sorted(range(len(prof["h"])), key=lambda j: prof["h"][j])
        for k in prof:
            prof[k] = [prof[k][j] for j in order]

    return GlobalSounding(lat, lon, elev, t, ml, ref, run_model, run_ref, run_note)
