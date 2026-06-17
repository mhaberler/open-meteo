#!/usr/bin/env python3
"""Overlay ICON-D2 pressure-level (reference) vs native model-level soundings.

Both profiles are fetched live from open-meteo for the same point/run/time and
plotted against height-AGL across 5 panels (p, T+Dew, RH, Spd, Dir)."""
import json, time, urllib.parse, urllib.request
import matplotlib.pyplot as plt

BASE_MODEL = "https://open-meteo.mah.priv.at/v1/forecast"   # native model levels
BASE_PRESS = "https://api.open-meteo.com/v1/forecast"        # pressure levels (public)
META_MODEL = "https://open-meteo.mah.priv.at/data/dwd_icon_d2/static/meta.json"
META_PRESS = "https://api.open-meteo.com/data/dwd_icon_d2/static/meta.json"
LAT, LON = 48.717, 8.750
TARGET = "2026-06-17T18:00"

# ICON-D2 native pressure levels (Sources/App/Icon/Icon.swift:111)
PLEVELS = [1000, 975, 950, 850, 700, 600, 500, 400, 300, 250, 200]
LEVELS = range(1, 66)                # 65 native model full levels

# --- run init per source, from each meta.json ---
def _utc(ts):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(ts))
def run_init(meta_url):
    with urllib.request.urlopen(meta_url, timeout=30) as f:
        return _utc(json.load(f)["last_run_initialisation_time"])
RUN_MODEL = run_init(META_MODEL)     # private server (model levels)
RUN_PRESS = run_init(META_PRESS)     # public api (pressure levels)

# --- two requests: model levels (private) + pressure levels (public) ---
def fetch(base, hourly):
    query = {
        "latitude": LAT, "longitude": LON,
        "hourly": ",".join(hourly),
        "models": "icon_d2",
        "wind_speed_unit": "ms",
        "timezone": "GMT",
        "start_date": TARGET[:10], "end_date": TARGET[:10],
    }
    q = urllib.parse.urlencode(query)
    with urllib.request.urlopen(f"{base}?{q}", timeout=120) as r:
        return json.load(r)

model_vars = []
for n in LEVELS:
    model_vars += [f"height_level{n}", f"pressure_level{n}", f"temperature_level{n}",
                   f"relative_humidity_level{n}", f"dew_point_level{n}",
                   f"wind_speed_level{n}", f"wind_direction_level{n}"]
press_vars = []
for p in PLEVELS:
    press_vars += [f"temperature_{p}hPa", f"relative_humidity_{p}hPa", f"dew_point_{p}hPa",
                   f"wind_speed_{p}hPa", f"wind_direction_{p}hPa", f"geopotential_height_{p}hPa"]

dm = fetch(BASE_MODEL, model_vars)   # native model levels (private server)
dp = fetch(BASE_PRESS, press_vars)   # pressure levels (public api)

elev = dm["elevation"]               # common ground datum (same icon_d2 grid)
Hm = dm["hourly"]; im = Hm["time"].index(TARGET)
Hp = dp["hourly"]; ip = Hp["time"].index(TARGET)

# --- build two profiles in the {h,p,T,Dew,Dir,Spd,RH} shape ---
def empty():
    return {k: [] for k in ("h", "p", "T", "Dew", "Dir", "Spd", "RH")}

ml = empty()                         # native model levels (private server)
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

ref = empty()                        # pressure levels (public api, reference)
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

# sort surface -> top
for prof in (ml, ref):
    order = sorted(range(len(prof["h"])), key=lambda j: prof["h"][j])
    for k in prof:
        prof[k] = [prof[k][j] for j in order]

run_note = "same run" if RUN_PRESS == RUN_MODEL else "RUN MISMATCH"
print(f"# pressure run {RUN_PRESS} (public)  |  model run {RUN_MODEL} (private)  [{run_note}]")
print(f"# {TARGET}Z  ICON-D2  ({LAT},{LON}) elev={elev:.0f}m  "
      f"ref={len(ref['h'])} pressure levels, model={len(ml['h'])} levels")

# --- plot: reference (solid) vs model levels (dashed) ---
fig, axs = plt.subplots(2, 3, figsize=(16, 10), sharey=True)
axs = axs.flatten()

plots_config = [
    ('p',   'Druck',               'Druck (hPa)',           'grey'),
    ('T',   'Temperatur & Taupunkt', 'Temperatur (°C)',     'red'),
    ('RH',  'Relative Feuchte',    'Feuchtigkeit (%)',      'green'),
    ('Spd', 'Windgeschwindigkeit', 'Geschwindigkeit (m/s)', 'blue'),
    ('Dir', 'Windrichtung',        'Richtung (°)',          'orange'),
]

for ax, (key, title, xlabel, color) in zip(axs, plots_config):
    # 'P' = thin crosshair marker at each pressure-level sample
    if key == 'T':
        ax.plot(ref['T'],   ref['h'], color='red',      linestyle='-',  marker='P', markersize=7, label='T (pressure)')
        ax.plot(ref['Dew'], ref['h'], color='blue',     linestyle='-',  marker='P', markersize=7, label='Dew (pressure)')
        ax.plot(ml['T'],    ml['h'],  color='darkred',  linestyle='--', label='T (model)')
        ax.plot(ml['Dew'],  ml['h'],  color='darkblue', linestyle='--', label='Dew (model)')
    else:
        ax.plot(ref[key], ref['h'], color=color, linestyle='-',  marker='P', markersize=7, label='pressure levels')
        ax.plot(ml[key],  ml['h'],  color=color, linestyle='--', label='model levels')
    ax.legend(loc='best', fontsize='small')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.grid(True, linestyle=':', alpha=0.6)

axs[0].set_ylabel('Höhe (m AGL)', fontsize=11)
axs[3].set_ylabel('Höhe (m AGL)', fontsize=11)
axs[5].axis('off')

plt.suptitle(f'ICON-D2 pressure levels vs model levels @ ({LAT},{LON}) — {TARGET}Z',
             fontsize=16, fontweight='bold', y=0.99)
fig.text(0.5, 0.945,
         f'pressure run {RUN_PRESS} (public)   |   model run {RUN_MODEL} (private)   [{run_note}]',
         ha='center', fontsize=11,
         color=('green' if RUN_PRESS == RUN_MODEL else 'red'))
# also annotate the unused 6th panel
axs[5].text(0.5, 0.5,
            f'pressure (public)\n  run {RUN_PRESS}\n\nmodel (private)\n  run {RUN_MODEL}\n\nvalid {TARGET}Z\n[{run_note}]',
            ha='center', va='center', fontsize=11,
            color=('green' if RUN_PRESS == RUN_MODEL else 'red'),
            transform=axs[5].transAxes)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
