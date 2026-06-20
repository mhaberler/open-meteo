#!/usr/bin/env python3
"""Overlay ICON-D2 pressure-level (reference) vs native model-level soundings.

Both profiles are fetched live from open-meteo for the same point/run/time and
plotted against height-AGL across 5 panels (p, T+Dew, RH, Spd, Dir)."""
import matplotlib.pyplot as plt
from sounding_data import load, geocode

LAT, LON = 46.9911, 15.4396          # LOWG — Graz Airport (Graz-Thalerhof)
LABEL = "LOWG / Graz"                 # resolved place name (updated via the location box)
TARGET = "2026-06-20T09:00"

# --- fetch + build all hours once (shared loader) ---
print(f"Fetching ICON-D2 soundings for {LAT},{LON} …", flush=True)
data = load(LAT, LON)
elev = data.elev
times = data.times
profiles = data.profiles
RUN_MODEL = data.run_model
RUN_PRESS = data.run_press
run_note = data.run_note

# --- fixed axis limits over the whole forecast (so stepping is steady) ---
plots_config = [
    ('p',   'Druck',                 'Druck (hPa)',           'grey'),
    ('T',   'Temperatur & Taupunkt', 'Temperatur (°C)',       'red'),
    ('RH',  'Relative Feuchte',      'Feuchtigkeit (%)',      'green'),
    ('Spd', 'Windgeschwindigkeit',   'Geschwindigkeit (m/s)', 'blue'),
    ('Dir', 'Windrichtung',          'Richtung (°)',          'orange'),
]

def _pad(lo, hi, frac=0.05):
    if lo == hi:
        return lo - 1, hi + 1
    m = (hi - lo) * frac
    return lo - m, hi + m

xlim, ylim = {}, (0, 1)

def compute_limits():
    """(Re)compute fixed axis limits from the current profiles."""
    global xlim, ylim
    xlim = {}
    for key, *_ in plots_config:
        vals = [v for ml, ref in profiles.values() for prof in (ml, ref) for v in prof[key]]
        if key == 'T':               # T panel also shows Dew
            vals += [v for ml, ref in profiles.values() for prof in (ml, ref) for v in prof['Dew']]
        xlim[key] = _pad(min(vals), max(vals)) if vals else (0, 1)
    xlim['Dir'] = (0, 360)
    hvals = [v for ml, ref in profiles.values() for prof in (ml, ref) for v in prof['h']]
    ylim = _pad(min(hvals), max(hvals))

compute_limits()

print(f"# pressure run {RUN_PRESS} (public)  |  model run {RUN_MODEL} (private)  [{run_note}]")
print(f"# ICON-D2 ({LAT},{LON}) elev={elev:.0f}m  steppable hours: {times[0]}Z .. {times[-1]}Z "
      f"({len(times)})")

# --- figure with Prev/Next buttons + arrow keys ---
import matplotlib.widgets as mwidgets

fig, axs = plt.subplots(2, 3, figsize=(16, 10), sharey=True)
axs = axs.flatten()
plt.subplots_adjust(bottom=0.12, top=0.90)

idx = times.index(TARGET) if TARGET in times else 0

def draw(i):
    t = times[i]
    ml, ref = profiles[t]
    for ax, (key, title, xlabel, color) in zip(axs, plots_config):
        ax.clear()
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
        ax.set_xlim(*xlim[key])
        ax.set_ylim(*ylim)
        ax.grid(True, linestyle=':', alpha=0.6)
    axs[0].set_ylabel('Höhe (m AGL)', fontsize=11)
    axs[3].set_ylabel('Höhe (m AGL)', fontsize=11)
    axs[5].axis('off')
    axs[5].text(0.5, 0.5,
                f'pressure (public)\n  run {RUN_PRESS}\n\nmodel (private)\n  run {RUN_MODEL}\n\n'
                f'valid {t}Z\n[{run_note}]\n\n'
                f'ref={len(ref["h"])} p-levels, model={len(ml["h"])} levels',
                ha='center', va='center', fontsize=11,
                color=('green' if RUN_PRESS == RUN_MODEL else 'red'),
                transform=axs[5].transAxes)
    fig.suptitle(f'ICON-D2 pressure vs model levels @ {LABEL} ({LAT:.3f},{LON:.3f}) — {t}Z   '
                 f'[{i + 1}/{len(times)}]',
                 fontsize=16, fontweight='bold', y=0.985)
    fig.canvas.draw_idle()

def step(delta):
    global idx
    idx = max(0, min(len(times) - 1, idx + delta))
    draw(idx)

def relocate(lat, lon, label):
    """Re-fetch profiles for a new location, recompute limits and redraw."""
    global LAT, LON, LABEL, data, elev, times, profiles, RUN_MODEL, RUN_PRESS, run_note, idx
    LAT, LON, LABEL = lat, lon, label
    data = load(lat, lon)
    elev = data.elev
    times = data.times
    profiles = data.profiles
    RUN_MODEL, RUN_PRESS, run_note = data.run_model, data.run_press, data.run_note
    compute_limits()
    idx = times.index(TARGET) if TARGET in times else 0
    draw(idx)

def on_submit(name):
    r = geocode(name)
    if r:
        relocate(*r)

ax_prev = plt.axes([0.40, 0.02, 0.08, 0.045])
ax_next = plt.axes([0.52, 0.02, 0.08, 0.045])
b_prev = mwidgets.Button(ax_prev, '◀ Prev')
b_next = mwidgets.Button(ax_next, 'Next ▶')
b_prev.on_clicked(lambda _evt: step(-1))
b_next.on_clicked(lambda _evt: step(+1))

# location picker: type a place name -> geocode -> relocate
ax_loc = plt.axes([0.10, 0.02, 0.18, 0.045])
tb_loc = mwidgets.TextBox(ax_loc, 'Ort ', initial='Graz')
tb_loc.on_submit(on_submit)

def on_key(evt):
    if evt.key == 'left':
        step(-1)
    elif evt.key == 'right':
        step(+1)
fig.canvas.mpl_connect('key_press_event', on_key)

draw(idx)
plt.show()
