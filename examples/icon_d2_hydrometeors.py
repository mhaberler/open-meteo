#!/usr/bin/env python3
"""Fetch ICON-D2 rain, snow, and graupel water on full levels 63..65.

These are specific content in g/kg (`qr`, `qs`, `qg`), packed like
`cloud_water`. Level 65 is the full level nearest the surface. `visibility`
is the surface field in metres, so the two can be compared on one run.
Only `models=icon_d2` publishes them; other models reject the names.

The files appear after the next icon-d2 `hiresTemp` run following deploy.
Until then the hydrometeor columns are null.

Usage:
    python3 icon_d2_hydrometeors.py [lat] [lon]

Env:
    OM_API  base URL of the open-meteo server (default https://open-meteo.wetterheidi.de)
            point it at a local instance with e.g. OM_API=http://127.0.0.1:8080
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("OM_API", "https://open-meteo.wetterheidi.de").rstrip("/")
LAT = float(sys.argv[1]) if len(sys.argv) > 1 else 52.52
LON = float(sys.argv[2]) if len(sys.argv) > 2 else 13.41

LEVELS = (63, 64, 65)
HYDROMETEORS = ("rain_water", "snow_water", "graupel_water")
VARIABLES = ["visibility"] + [f"{name}_level{level}" for name in HYDROMETEORS for level in LEVELS]

url = f"{BASE}/v1/dwd-icon?" + urllib.parse.urlencode({
    "latitude": LAT,
    "longitude": LON,
    "hourly": ",".join(VARIABLES),
    "forecast_hours": 6,
    "models": "icon_d2",
    # Pin to model-grid elevation; no DEM downscaling regardless of instance.
    "elevation": "nan",
})


def fail_with_body(prefix, status, content_type, body):
    snippet = body.decode("utf-8", "replace")[:2000]
    sys.exit(
        f"{prefix}\n"
        f"HTTP {status}  Content-Type: {content_type or '(none)'}  {len(body)} bytes\n"
        f"--- body ---\n{snippet}"
    )


print(f"GET {url}\n")
try:
    with urllib.request.urlopen(url, timeout=30) as r:
        status, content_type, body = r.status, r.headers.get("Content-Type", ""), r.read()
except urllib.error.HTTPError as e:
    fail_with_body(f"Request failed: HTTP error from {BASE}", e.code, e.headers.get("Content-Type", ""), e.read())
except urllib.error.URLError as e:
    sys.exit(f"Could not reach {BASE}: {e.reason}")

try:
    data = json.loads(body)
except json.JSONDecodeError as e:
    fail_with_body(f"Response was not valid JSON ({e})", status, content_type, body)

hourly = data["hourly"]
missing = [name for name in VARIABLES if name not in hourly]
if missing:
    sys.exit(f"Response is missing {', '.join(missing)}")

units = data.get("hourly_units", {})
print(
    f"{data['latitude']},{data['longitude']}  elevation={data.get('elevation')} m  "
    f"visibility [{units.get('visibility', 'm')}]  "
    f"hydrometeors [{units.get('rain_water_level65', 'g/kg')}]\n"
)
header = f"{'time':<16} {'vis':>8}" + "".join(f" {name[:1]}{level:>2}" for name in HYDROMETEORS for level in LEVELS)
print(header)
for i, time in enumerate(hourly["time"]):
    cells = [f"{hourly['visibility'][i]:8.0f}" if hourly["visibility"][i] is not None else f"{'null':>8}"]
    for name in HYDROMETEORS:
        for level in LEVELS:
            value = hourly[f"{name}_level{level}"][i]
            cells.append(f"{value:8.5f}" if value is not None else f"{'null':>8}")
    print(f"{time:<16} " + " ".join(cells))
