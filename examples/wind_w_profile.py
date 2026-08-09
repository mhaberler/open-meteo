#!/usr/bin/env python3
"""Query ICON global vertical wind (W) on native model half levels.

W (`wind_w_level<N>`) lives on DWD half levels 1..nFull+1 (icon global: 1..121;
icon-eu: 1..75; icon-d2: 1..66 — not used here). Half level N sits exactly at
hhl[N]; its height is exposed as `height_half_level<N>` (ASL) /
`height_half_agl_level<N>`.

Pinned to `models=icon_global` so the server never falls back to icon-eu/icon-d2
via the seamless mixer — useful on boxes that only ingest the global domain.

Usage:
    python3 wind_w_profile.py [lat] [lon]

Env:
    OM_API  base URL of the open-meteo server (default https://open-meteo.mah.priv.at)
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("OM_API", "https://open-meteo-temp.mah.priv.at").rstrip("/")
LAT = float(sys.argv[1]) if len(sys.argv) > 1 else 47.8
LON = float(sys.argv[2]) if len(sys.argv) > 2 else 16.2

N_HALF = 121  # icon global half levels; lowest ~20 cover the boundary layer + low troposphere
LEVELS = range(N_HALF - 20, N_HALF + 1)

hourly = [f"wind_w_level{n}" for n in LEVELS]
hourly += [f"height_half_agl_level{n}" for n in LEVELS]

# 2 timesteps starting at current hour; index 1 = one hour ahead
url = f"{BASE}/v1/dwd-icon?" + urllib.parse.urlencode({
    "latitude": LAT,
    "longitude": LON,
    "hourly": ",".join(hourly),
    "forecast_hours": 2,
    "models": "icon_global",
    # explicit m/s: older servers apply the default kmh wind unit to wind_w as well
    "windspeed_unit": "ms",
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
        status = r.status
        content_type = r.headers.get("Content-Type", "")
        body = r.read()
except urllib.error.HTTPError as e:
    fail_with_body(f"Request failed: HTTP error from {BASE}", e.code, e.headers.get("Content-Type", ""), e.read())
except urllib.error.URLError as e:
    sys.exit(f"Could not reach {BASE}: {e.reason}")

try:
    data = json.loads(body)
except json.JSONDecodeError as e:
    fail_with_body(f"Response was not valid JSON ({e})", status, content_type, body)

h = data["hourly"]
hour_idx = 1  # one hour ahead
print(f"Vertical wind profile at {data['latitude']},{data['longitude']} "
      f"time={h['time'][hour_idx]} (icon global half levels)\n")
print(f"{'level':>5} {'height AGL [m]':>15} {'w [m/s]':>8}")

prev_height = None
missing_w = False
for n in LEVELS:
    height = h[f"height_half_agl_level{n}"][hour_idx]
    w = h[f"wind_w_level{n}"][hour_idx]
    missing_w |= w is None
    print(f"{n:>5} {height:>15.1f} {'n/a' if w is None else f'{w:.2f}':>8}")
    # sanity: heights strictly decrease with level index (1 = model top)
    assert prev_height is None or height < prev_height, f"height not monotonic at level {n}"
    prev_height = height

if missing_w:
    sys.exit("\nwind_w is null — server has no ingested w data yet (re-run hires-temp download)")

# sanity: surface half level — AGL ≈ 0 and w ≈ 0 (lower boundary condition)
surf_agl = h[f"height_half_agl_level{N_HALF}"][hour_idx]
surf_w = h[f"wind_w_level{N_HALF}"][hour_idx]
assert abs(surf_agl) < 1.0, f"surface half level AGL should be ~0, got {surf_agl}"
assert abs(surf_w) < 0.5, f"surface w should be ~0, got {surf_w}"
print("\nsanity OK: heights monotonic, surface AGL≈0, surface w≈0")
