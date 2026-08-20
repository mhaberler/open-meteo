#!/usr/bin/env python3
"""Compare DEM90 elevation against raw ICON model orography (HSURF) at named places.

Geocodes each place via OpenStreetMap Nominatim (handles street addresses with
house numbers, unlike Open-Meteo's own place-name geocoder), then queries:

  * `/v1/elevation` -- the DEM90 value (Dem90.read, see DownloadDem.swift). This
    is what an unset `elevation=` request parameter resolves to (or what a
    DEM_DOWNSCALING=false instance ignores in favour of the model grid).
  * `model_elevation` (raw DWD HSURF) via `/v1/dwd-icon`, once per model. This
    is the elevation the model's own grid actually sits at -- can differ from
    DEM90 by hundreds of metres where the grid smooths terrain (e.g. valleys
    under a coarse ICON-EU cell, see the HSURF/PS/surface_pressure analysis).

`elevation=nan` is passed on the model_elevation request so the result reflects
the model's own grid regardless of whether this instance downscales to DEM.

Usage:
    python3 elevation_compare.py ["place 1"] ["place 2"] ...
    (defaults to Stiwoll 75, Austria and Herrsching am Ammersee, Germany)

Env:
    OM_API  base URL of the open-meteo server (default https://open-meteo.mah.priv.at)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("OM_API", "https://open-meteo.mah.priv.at").rstrip("/")
MODELS = ["icon_d2", "icon_eu"]

PLACES = sys.argv[1:] or ["Stiwoll 75, Austria", "Herrsching am Ammersee, Germany"]


def fail_with_body(prefix, status, content_type, body):
    snippet = body.decode("utf-8", "replace")[:2000]
    sys.exit(
        f"{prefix}\n"
        f"HTTP {status}  Content-Type: {content_type or '(none)'}  {len(body)} bytes\n"
        f"--- body ---\n{snippet}"
    )


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status, content_type, body = r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        fail_with_body(f"Request failed: HTTP error from {url}", e.code, e.headers.get("Content-Type", ""), e.read())
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {url}: {e.reason}")
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        fail_with_body(f"Response was not valid JSON ({e})", status, content_type, body)


def geocode(place):
    # Nominatim usage policy: identify with a real User-Agent, max 1 req/s.
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": place,
        "format": "json",
        "limit": 1,
    })
    results = get_json(url, headers={"User-Agent": "open-meteo-examples/elevation_compare.py"})
    if not results:
        sys.exit(f"Nominatim found nothing for {place!r}")
    r = results[0]
    return float(r["lat"]), float(r["lon"]), r["display_name"]


def dem_elevation(lat, lon):
    url = f"{BASE}/v1/elevation?" + urllib.parse.urlencode({"latitude": lat, "longitude": lon})
    data = get_json(url)
    return data["elevation"][0]


def model_elevation(lat, lon, model):
    url = f"{BASE}/v1/dwd-icon?" + urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "hourly": "model_elevation",
        "forecast_hours": 1,
        "models": model,
        # Pin to model-grid elevation; no DEM downscaling regardless of instance.
        "elevation": "nan",
    })
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        # e.g. point outside this model's domain -> treat as unavailable, not fatal
        return None
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {BASE}: {e.reason}")
    data = json.loads(body)
    values = data.get("hourly", {}).get("model_elevation")
    if not values or values[0] is None:
        return None
    return values[0]


rows = []
for i, place in enumerate(PLACES):
    if i:
        time.sleep(1)  # Nominatim rate limit
    lat, lon, resolved = geocode(place)
    dem = dem_elevation(lat, lon)
    models = {m: model_elevation(lat, lon, m) for m in MODELS}
    rows.append((place, resolved, lat, lon, dem, models))

for place, resolved, lat, lon, dem, models in rows:
    print(f"{place}")
    print(f"  -> {resolved}")
    print(f"  {lat:.5f},{lon:.5f}")
    dem_str = f"{dem:.0f} m" if dem is not None else "n/a"
    print(f"  DEM90 elevation:        {dem_str}")
    for m in MODELS:
        v = models[m]
        if v is None:
            print(f"  {m:<9} model_elevation:  n/a (outside domain or not ingested)")
            continue
        delta = f" (Δ {v - dem:+.0f} m vs DEM)" if dem is not None else ""
        print(f"  {m:<9} model_elevation:  {v:.0f} m{delta}")
    print()
