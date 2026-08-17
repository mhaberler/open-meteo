#!/usr/bin/env python3
"""Check the `heidiVars` surface variables served by an open-meteo instance.

Exercises the second batch added to the ICON `--group heidiVars` downloader —
`cloud_base` (DWD CEILING), `cloud_cover{,_low,_mid,_high}` (CLCT/CLCL/CLCM/CLCH),
`freezing_level_height` (HZEROCL), `convective_inhibition` (CIN_ML),
`snowfall_height` (SNOWLMT) and `wind_speed_10m`/`wind_direction_10m` (derived
from U_10M/V_10M) — and asserts the properties that are easy to regress silently:

  * `cloud_base` is metres above MSL, not AGL, so it never sits below the grid
    cell elevation. Verified against DWD GRIB: CEILING - HSURF is never negative
    over 525,072 icon-d2 cells (min +9.8 m) across terrain reaching 4080 m.
  * Clear sky is a large value, not null and not 0. DWD fills "no ceiling" with
    the top of the scan range (~16 km) rather than bitmap-missing it, so a
    `cloud_base < threshold` test needs no special casing. Conversely, solid low
    cloud (CLCL >= 80%) always yields a low ceiling. Note that *total* cover is
    not a usable predictor — CLCT >= 50% is frequently cirrus alone, and a
    quarter of those grid points have a ceiling above 10 km.
  * `convective_inhibition` never leaks DWD's -999.9 fill value; the ingest maps
    it to 0, leaving a non-negative J/kg magnitude.
  * `snowfall_height` (wet bulb 1.3 °C) stays at or below `freezing_level_height`
    (dry bulb 0 °C).

Also exercises the third batch — raw `surface_pressure_model` (DWD PS) and
`model_elevation` (DWD HSURF, unmasked) — and measures the gap this change was
built to quantify: how far the existing *derived* `surface_pressure` (a
barometric reduction of `pressure_msl` through `temperature_2m` and the
requested `elevation=`) drifts from the raw model value at a mountain grid
cell. See HEIDIVARS.md, "surface_pressure_model sits alongside the existing
derived surface_pressure, it does not replace it."

Pinned to `models=icon_d2` — CEILING and CIN_ML are only published for icon-eu
and icon-d2, so a seamless query could silently fall back to global ICON, where
these variables do not exist.

Usage:
    python3 heidivars.py [lat] [lon]

Env:
    OM_API  base URL of the open-meteo server (default https://open-meteo-temp.mah.priv.at)
            point it at a local instance with e.g. OM_API=http://127.0.0.1:8080
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

#BASE = os.environ.get("OM_API", "https://open-meteo-temp.mah.priv.at").rstrip("/")
BASE = os.environ.get("OM_API", "https://open-meteo.mah.priv.at").rstrip("/")
# Default to the Zugspitze massif: a ~2000 m grid cell makes the MSL check
# discriminating (over lowland the ceiling clears the terrain trivially) and puts
# cloud_base, CAPE and CIN into interesting ranges.
LAT = float(sys.argv[1]) if len(sys.argv) > 1 else 47.42
LON = float(sys.argv[2]) if len(sys.argv) > 2 else 10.98

VARIABLES = [
    "cloud_base",
    "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
    "freezing_level_height", "snowfall_height",
    "cape", "convective_inhibition",
    "wind_speed_10m", "wind_direction_10m",
    "temperature_2m",
    "surface_pressure", "surface_pressure_model", "model_elevation", "pressure_msl",
]

# DWD fills "no ceiling" with the top of the scan range. Measured on icon-d2 where
# CLCT == 0: 5th percentile 16,000 m, median 16,164 m over 358k clear grid points.
CLEAR_SKY_FLOOR = 10_000.0
# Ceiling ceiling, so to speak, when the low layer (800 hPa to ground) is solid.
# Measured on icon-d2 where CLCL >= 80%: max 4949 m over 5430 grid points.
LOW_CEILING_MAX = 6_000.0
# DWD's CIN_ML undefined marker; the ingest must have replaced it with 0.
CIN_FILL = -999.0

url = f"{BASE}/v1/dwd-icon?" + urllib.parse.urlencode({
    "latitude": LAT,
    "longitude": LON,
    "hourly": ",".join(VARIABLES),
    "forecast_hours": 24,
    "models": "icon_d2",
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
        status, content_type, body = r.status, r.headers.get("Content-Type", ""), r.read()
except urllib.error.HTTPError as e:
    fail_with_body(f"Request failed: HTTP error from {BASE}", e.code, e.headers.get("Content-Type", ""), e.read())
except urllib.error.URLError as e:
    sys.exit(f"Could not reach {BASE}: {e.reason}")

try:
    data = json.loads(body)
except json.JSONDecodeError as e:
    fail_with_body(f"Response was not valid JSON ({e})", status, content_type, body)

h = data["hourly"]
elevation = data["elevation"]
units = data.get("hourly_units", {})

missing = [v for v in VARIABLES if v not in h]
if missing:
    sys.exit(f"Server did not return: {', '.join(missing)}\n"
             f"Is it running a build with these variables, and has `--group heidiVars` been ingested?")

null_only = [v for v in VARIABLES if all(x is None for x in h[v])]
if null_only:
    sys.exit(f"All-null variables: {', '.join(null_only)}\n"
             f"The variable is known to the API but has no ingested data for this run.")

failures = []
notes = []


def check(name, ok, detail):
    (notes if ok else failures).append(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")


n = len(h["time"])
print(f"{data['latitude']},{data['longitude']}  grid elevation {elevation} m  "
      f"{n} hours from {h['time'][0]}\n")

hdr = f"{'time':>16} {'cld_base':>9} {'clct':>5} {'low':>4} {'mid':>4} {'high':>4} " \
      f"{'frzlvl':>7} {'snowlmt':>8} {'cape':>6} {'cin':>6} {'wind':>6} {'dir':>4}"
print(hdr)
for i in range(min(n, 12)):
    def g(v, fmt=">9.0f"):
        x = h[v][i]
        return "null".rjust(int(fmt.split('.')[0].lstrip('>'))) if x is None else format(x, fmt)
    print(f"{h['time'][i]:>16} {g('cloud_base')} {g('cloud_cover', '>5.0f')} "
          f"{g('cloud_cover_low', '>4.0f')} {g('cloud_cover_mid', '>4.0f')} {g('cloud_cover_high', '>4.0f')} "
          f"{g('freezing_level_height', '>7.0f')} {g('snowfall_height', '>8.0f')} "
          f"{g('cape', '>6.0f')} {g('convective_inhibition', '>6.0f')} "
          f"{g('wind_speed_10m', '>6.1f')} {g('wind_direction_10m', '>4.0f')}")
if n > 12:
    print(f"{'...':>16} ({n - 12} more hours)")
print()

# --- units -------------------------------------------------------------------
for v, want in [("cloud_base", "m"), ("freezing_level_height", "m"), ("snowfall_height", "m"),
                ("cloud_cover", "%"), ("convective_inhibition", "J/kg"), ("wind_speed_10m", "m/s"),
                ("surface_pressure", "hPa"), ("surface_pressure_model", "hPa"), ("model_elevation", "m")]:
    got = units.get(v)
    check(f"unit {v}", got == want, f"{got!r} (want {want!r})")

# --- cloud_base is MSL, never below the grid cell ------------------------------
base = [(t, x) for t, x in zip(h["time"], h["cloud_base"]) if x is not None]
below = [(t, x) for t, x in base if x < elevation - 50]
check("cloud_base >= grid elevation (MSL, not AGL)", not below,
      f"min {min(x for _, x in base):.0f} m vs elevation {elevation} m"
      + (f" — {len(below)} hours below, first {below[0]}" if below else ""))

# --- clear sky is a large sentinel, not 0 and not null -------------------------
clear = [(t, cb) for t, cc, cb in zip(h["time"], h["cloud_cover"], h["cloud_base"]) if cc == 0]
if clear:
    bad = [(t, cb) for t, cb in clear if cb is None or cb < CLEAR_SKY_FLOOR]
    check("clear sky -> ~16 km, not 0/null", not bad,
          f"{len(clear)} clear hours, cloud_base min {min(cb for _, cb in clear if cb is not None):.0f} m"
          + (f" — {len(bad)} suspect, first {bad[0]}" if bad else ""))
else:
    notes.append("skip clear-sky check: no hour with cloud_cover == 0 in this window")

# Solid *low* cloud implies a low ceiling. Total cover is not a usable predictor:
# CLCT >= 50% is often cirrus alone, and 26% of those grid points have a ceiling
# above 10 km. Measured on icon-d2 where CLCL >= 80%: max ceiling 4949 m, p99
# 4419 m, none above 10 km — versus CLCL >= 50%, where 19% still exceed 10 km.
overcast = [(t, cb) for t, cl, cb in zip(h["time"], h["cloud_cover_low"], h["cloud_base"])
            if cl is not None and cl >= 80 and cb is not None]
if overcast:
    check("solid low cloud -> low ceiling", all(cb < LOW_CEILING_MAX for _, cb in overcast),
          f"{len(overcast)} hours with cloud_cover_low >= 80%, "
          f"cloud_base max {max(cb for _, cb in overcast):.0f} m (want < {LOW_CEILING_MAX:.0f})")
else:
    notes.append("skip low-ceiling check: no hour with cloud_cover_low >= 80% in this window")

# --- cloud cover layers --------------------------------------------------------
layers = ["cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"]
oob = [(v, t, x) for v in layers for t, x in zip(h["time"], h[v]) if x is not None and not 0 <= x <= 100]
check("cloud cover in 0..100%", not oob, f"all 4 layers over {n} hours" + (f" — {oob[:1]}" if oob else ""))

# maximum-random overlap: the total is at least the largest single layer
viol = [(t, tot, lo, mi, hi) for t, tot, lo, mi, hi in
        zip(h["time"], h["cloud_cover"], h["cloud_cover_low"], h["cloud_cover_mid"], h["cloud_cover_high"])
        if None not in (tot, lo, mi, hi) and tot < max(lo, mi, hi) - 1]
check("cloud_cover >= max(low, mid, high)", not viol,
      f"{n} hours" + (f" — {len(viol)} violations, first {viol[0]}" if viol else ""))

# --- convective_inhibition: the -999.9 fill must not survive ingest -------------
cin = [(t, x) for t, x in zip(h["time"], h["convective_inhibition"]) if x is not None]
leaked = [(t, x) for t, x in cin if x <= CIN_FILL]
check("convective_inhibition fill mapped to 0", not leaked,
      f"range {min(x for _, x in cin):.1f}..{max(x for _, x in cin):.1f} J/kg"
      + (f" — {len(leaked)} hours at the -999.9 fill" if leaked else ""))

cape = [x for x in h["cape"] if x is not None]
check("cape >= 0", all(x >= 0 for x in cape), f"max {max(cape):.0f} J/kg")

# --- snowfall_height (wet bulb 1.3 C) sits at or below freezing level (0 C) -----
# Only where the freezing level is above ground: below the grid cell both fields are
# rewritten from temperature_2m by the ingest and the ordering no longer applies.
pairs = [(t, f, s) for t, f, s in zip(h["time"], h["freezing_level_height"], h["snowfall_height"])
         if None not in (f, s) and f > elevation + 50]
if pairs:
    viol = [(t, f, s) for t, f, s in pairs if s > f + 100]
    check("snowfall_height <= freezing_level_height", not viol,
          f"{len(pairs)} hours with the freezing level above ground"
          + (f" — {len(viol)} violations, first {viol[0]}" if viol else ""))
else:
    notes.append("skip snowfall/freezing order check: freezing level never above the grid cell")

# --- wind derived from U_10M/V_10M ---------------------------------------------
spd = [x for x in h["wind_speed_10m"] if x is not None]
dirs = [x for x in h["wind_direction_10m"] if x is not None]
check("wind_speed_10m >= 0", all(x >= 0 for x in spd), f"max {max(spd):.1f} m/s")
check("wind_direction_10m in 0..360", all(0 <= x <= 360 for x in dirs), f"{len(dirs)} hours")

# --- model_elevation: raw HSURF, finite, matches the (masked) elevation on land ---
# On land the mask never applies (elevation only drops to -999 over open sea), so
# the unmasked time series and the static, sea-masked `elevation` field should agree.
# Present-hours count, not ==n: only the ingested forecast window has to carry it,
# same as every other heidiVars field checked above.
me = [x for x in h["model_elevation"] if x is not None]
check("model_elevation has data", len(me) > 0, f"{len(me)}/{n} hours present")
if me:
    spread = max(me) - min(me)
    check("model_elevation is constant over the run (time-invariant field)", spread < 1.0,
          f"range {min(me):.1f}..{max(me):.1f} m")
    check("model_elevation matches response elevation on land", abs(me[0] - elevation) < 5.0,
          f"model_elevation={me[0]:.1f} m vs elevation={elevation} m")

# --- surface_pressure_model: sane magnitude, and the gap vs the derived value ------
psfc = [x for x in h["surface_pressure_model"] if x is not None]
check("surface_pressure_model is a sane hPa magnitude", all(300 <= x <= 1100 for x in psfc),
      f"range {min(psfc):.1f}..{max(psfc):.1f} hPa" if psfc else "no data")

derived = [x for x in h["surface_pressure"] if x is not None]
raw = [x for x in h["surface_pressure_model"] if x is not None]
if derived and raw and len(derived) == len(raw):
    deltas = [d - r for d, r in zip(derived, raw)]
    mean_delta = sum(deltas) / len(deltas)
    max_abs_delta = max(abs(x) for x in deltas)
    print(f"surface_pressure (derived) - surface_pressure_model (raw): "
          f"mean {mean_delta:+.2f} hPa, max |delta| {max_abs_delta:.2f} hPa over {len(deltas)} hours "
          f"at grid elevation {elevation} m")
    notes.append(f"pressure delta: mean {mean_delta:+.2f} hPa, max |delta| {max_abs_delta:.2f} hPa "
                 f"(informational -- see HEIDIVARS.md on which field should be authoritative)")
else:
    notes.append("skip pressure delta: surface_pressure/surface_pressure_model not both fully present")

# --- report --------------------------------------------------------------------
for line in notes:
    print(line)
for line in failures:
    print(line)
print()
if failures:
    sys.exit(f"{len(failures)} check(s) failed")
print(f"all {len(notes)} checks passed")
