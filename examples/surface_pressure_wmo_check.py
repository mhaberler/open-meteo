#!/usr/bin/env python3
"""Compare `surface_pressure` (ICAO standard atmosphere) against the new
`surface_pressure_wmo` (WMO/ICAO reduction anchored on layer-mean temperature)
for the current ICON run, across all three DWD ICON domains.

Usage:
    python3 surface_pressure_wmo_check.py [lat] [lon]

Env:
    OM_API  base URL of the open-meteo server (default https://open-meteo-temp.mah.priv.at)
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

#BASE = os.environ.get("OM_API", "https://open-meteo-temp.mah.priv.at").rstrip("/")
BASE = os.environ.get("OM_API", "https://open-meteo.mah.priv.at").rstrip("/")
LAT = float(sys.argv[1]) if len(sys.argv) > 1 else 47.8
LON = float(sys.argv[2]) if len(sys.argv) > 2 else 16.2

# MODELS = ["icon_global", "icon_eu", "icon_d2"]
MODELS = [ "icon_eu", "icon_d2"]
HOURLY = ["surface_pressure", "surface_pressure_wmo", "pressure_msl", "temperature_2m"]


def fail_with_body(prefix, status, content_type, body):
    snippet = body.decode("utf-8", "replace")[:2000]
    sys.exit(
        f"{prefix}\n"
        f"HTTP {status}  Content-Type: {content_type or '(none)'}  {len(body)} bytes\n"
        f"--- body ---\n{snippet}"
    )


def fetch(model):
    url = f"{BASE}/v1/dwd-icon?" + urllib.parse.urlencode({
        "latitude": LAT,
        "longitude": LON,
        "hourly": ",".join(HOURLY),
        "forecast_hours": 2,
        "models": model,
    })
    print(f"GET {url}")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            content_type = r.headers.get("Content-Type", "")
            body = r.read()
            status = r.status
    except urllib.error.HTTPError as e:
        fail_with_body(f"Request failed for {model}: HTTP error from {BASE}", e.code, e.headers.get("Content-Type", ""), e.read())
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {BASE}: {e.reason}")

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        fail_with_body(f"Response for {model} was not valid JSON ({e})", status, content_type, body)


hour_idx = 1  # one hour ahead
any_missing = False
print(f"{'model':>12} {'elevation':>10} {'pressure_msl':>13} {'surf_press':>11} {'surf_press_wmo':>15} {'diff':>7}")

for model in MODELS:
    data = fetch(model)
    elevation = data.get("elevation")
    h = data["hourly"]
    time = h["time"][hour_idx]
    pmsl = h["pressure_msl"][hour_idx]
    sp = h["surface_pressure"][hour_idx]
    spw = h["surface_pressure_wmo"][hour_idx]

    if sp is None or spw is None or pmsl is None:
        any_missing = True
        print(f"{model:>12} {elevation!s:>10} {'n/a':>13} {'n/a':>11} {'n/a':>15} {'n/a':>7}   time={time}")
        continue

    diff = spw - sp
    print(f"{model:>12} {elevation:>10.1f} {pmsl:>13.2f} {sp:>11.2f} {spw:>15.2f} {diff:>7.2f}   time={time}")

    # sanity: at (near) sea level both reductions should collapse close to pressure_msl
    if abs(elevation) < 5:
        assert abs(sp - pmsl) < 1.0, f"{model}: surface_pressure should be ~pressure_msl at elevation {elevation}, got {sp} vs {pmsl}"
        assert abs(spw - pmsl) < 1.0, f"{model}: surface_pressure_wmo should be ~pressure_msl at elevation {elevation}, got {spw} vs {pmsl}"

if any_missing:
    sys.exit("\nsome values were null — server may not have ingested this run yet")

print("\nsanity OK: sea-level reductions collapse to pressure_msl")
