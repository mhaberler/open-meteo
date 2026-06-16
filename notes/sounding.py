#!/usr/bin/env python3
"""Full ICON-D2 native model-level sounding from local open-meteo (port 8085).
Reformat like the Stiwoll table: h(mAGL) p(hPa) T(C) Dew(C) Dir(deg) Spd(m/s) RH(%)."""
import json, time, urllib.parse, urllib.request

BASE = "http://127.0.0.1:8085/v1/forecast"
META = "/var/lib/openmeteo-api/data/dwd_icon_d2/static/meta.json"
LAT, LON = 47.105, 15.215          # Stiwoll Heidi Startplatz
LEVELS = range(1, 66)              # ICON-D2: 65 native full levels (65=surface,1=top)
TARGET = "2026-06-16T00:00"

# Last ICON-D2 model run + forecast end (read from the domain meta.json).
def _utc(ts):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(ts))
with open(META) as f:
    _m = json.load(f)
RUN_INIT = _utc(_m["last_run_initialisation_time"])   # e.g. 2026-06-15T09:00Z
FCST_END = _utc(_m["data_end_time"])                  # e.g. 2026-06-17T10:00Z

# Dew(C), Dir(deg), Spd(m/s) now come straight from the server-side derived
# model-level vars dew_point/wind_direction/wind_speed (no client-side math).
vars = []
for n in LEVELS:
    vars += [f"height_level{n}", f"pressure_level{n}", f"temperature_level{n}",
             f"relative_humidity_level{n}", f"dew_point_level{n}",
             f"wind_speed_level{n}", f"wind_direction_level{n}"]

q = urllib.parse.urlencode({
    "latitude": LAT, "longitude": LON,
    "hourly": ",".join(vars),
    "models": "icon_d2",
    "wind_speed_unit": "ms",
    "timezone": "GMT",
    "start_date": "2026-06-16", "end_date": "2026-06-16",
})
with urllib.request.urlopen(f"{BASE}?{q}", timeout=120) as r:
    d = json.load(r)

elev = d["elevation"]
H = d["hourly"]
i = H["time"].index(TARGET)

rows = []
for n in LEVELS:
    h  = H[f"height_level{n}"][i]
    p  = H[f"pressure_level{n}"][i]
    T  = H[f"temperature_level{n}"][i]
    rh = H[f"relative_humidity_level{n}"][i]
    td = H[f"dew_point_level{n}"][i]
    spd = H[f"wind_speed_level{n}"][i]
    dr  = H[f"wind_direction_level{n}"][i]
    if None in (h, p, T, rh, td, spd, dr):
        continue
    rows.append((h-elev, p, T, td, dr, spd, rh))

rows.sort(key=lambda r: r[0])      # surface -> top
print(f"# run {RUN_INIT} (init), forecast to {FCST_END}")
print(f"# {TARGET}Z  ICON-D2 native levels  Stiwoll ({LAT},{LON}) elev={elev:.0f}m")
print("h(mAGL) p(hPa) T(C) Dew(C) Dir(°) Spd(m/s) RH(%)")
for h,p,T,td,dr,sp,rh in rows:
    print(f"{h:.0f} {p:.1f} {T:.1f} {td:.1f} {dr:.0f} {sp:.1f} {rh:.0f}")
