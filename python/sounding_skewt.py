#!/usr/bin/env python3
"""MetPy Skew-T log-p variant: ICON-D2 pressure levels vs native model levels.

Single overlaid Skew-T — pressure-level T/Td solid, model-level T/Td dashed.
Wind barbs, surface-based parcel ascent, LCL and CAPE/CIN shading are computed
from the (denser) model-level profile. ◀ Prev / Next ▶ buttons + arrow keys
step through forecast hours. Data via the shared loader in sounding_data.py.

Modelled on https://unidata.github.io/MetPy/latest/examples/Advanced_Sounding.html
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units

from sounding_data import load, geocode

LAT, LON = 46.9911, 15.4396          # LOWG — Graz Airport (Graz-Thalerhof)
LABEL = "LOWG / Graz"                 # resolved place name (updated via the location box)
TARGET = "2026-06-17T18:00"

data = load(LAT, LON)
times = data.times
profiles = data.profiles
note_color = 'green' if data.run_note == "same run" else 'red'

idx = times.index(TARGET) if TARGET in times else 0

fig = plt.figure(figsize=(11, 11))
skew = SkewT(fig, rotation=45, rect=(0.07, 0.12, 0.86, 0.78))

# --- static setup (built ONCE; clearing the SkewT axis would destroy its
#     projection + log-p scale, so we never cla() — only swap dynamic artists) ---
skew.plot_dry_adiabats(alpha=0.25)
skew.plot_moist_adiabats(alpha=0.25)
skew.plot_mixing_lines(alpha=0.25)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)
skew.ax.set_xlabel('Temperatur (°C)')
skew.ax.set_ylabel('Druck (hPa)')

title_txt = fig.suptitle("", fontsize=13, fontweight='bold', y=0.99)
sub_txt = fig.text(0.5, 0.945, "", ha='center', fontsize=9, color=note_color)
dynamic = []                          # per-hour artists, removed before each redraw
CAPE_SRC = 'model'                    # which profile drives parcel + CAPE/CIN shading


def _q(seq, unit):
    return np.array(seq, dtype=float) * unit


def draw(i):
    t = times[i]
    ml, ref = profiles[t]

    for a in dynamic:                 # drop previous hour's artists
        a.remove()
    dynamic.clear()

    # draw both profiles' T/Td and stash arrays for the parcel calc
    arr = {}                          # 'pressure'/'model' -> (p, T, Td) with units
    if ref['p']:
        p = _q(ref['p'], units.hPa)
        dynamic.extend(skew.plot(p, _q(ref['T'], units.degC),   'r', linewidth=2, label='T (pressure)'))
        dynamic.extend(skew.plot(p, _q(ref['Dew'], units.degC), 'g', linewidth=2, label='Td (pressure)'))
        arr['pressure'] = (p, _q(ref['T'], units.degC), _q(ref['Dew'], units.degC))
    if ml['p']:
        pm = _q(ml['p'], units.hPa)
        dynamic.extend(skew.plot(pm, _q(ml['T'], units.degC),   color='darkred',  linestyle='--', linewidth=1.5, label='T (model)'))
        dynamic.extend(skew.plot(pm, _q(ml['Dew'], units.degC), color='darkblue', linestyle='--', linewidth=1.5, label='Td (model)'))
        arr['model'] = (pm, _q(ml['T'], units.degC), _q(ml['Dew'], units.degC))
        # wind barbs always from the (denser) model levels
        u, v = mpcalc.wind_components(_q(ml['Spd'], units('m/s')), _q(ml['Dir'], units.deg))
        k = max(1, len(pm) // 25)
        dynamic.append(skew.plot_barbs(pm[::k], u[::k].to('knots'), v[::k].to('knots')))

    # CAPE/CIN for BOTH profiles (reported in title)
    cc = {}
    for src, (P, T, Td) in arr.items():
        try:
            pr = mpcalc.parcel_profile(P, T[0], Td[0]).to('degC')
            cc[src] = mpcalc.cape_cin(P, T, Td, pr)
        except Exception:
            cc[src] = None

    # parcel ascent + LCL + red/blue shading for the SELECTED source only
    sel = CAPE_SRC if CAPE_SRC in arr else (next(iter(arr), None))
    if sel:
        P, T, Td = arr[sel]
        try:
            pr = mpcalc.parcel_profile(P, T[0], Td[0]).to('degC')
            dynamic.extend(skew.plot(P, pr, 'k', linewidth=1.6, label=f'parcel ({sel})'))
            dynamic.append(skew.shade_cin(P, T, pr, Td, facecolor='tab:blue', alpha=0.3))
            dynamic.append(skew.shade_cape(P, T, pr, facecolor='tab:red', alpha=0.3))
            lcl_p, lcl_t = mpcalc.lcl(P[0], T[0], Td[0])
            dynamic.extend(skew.plot(lcl_p, lcl_t, 'ko', markerfacecolor='black'))
            dynamic.append(skew.ax.text(0.02, lcl_p.m, ' LCL', va='center', fontsize=8,
                                        transform=skew.ax.get_yaxis_transform()))
        except Exception as e:        # short/degenerate profile, etc.
            dynamic.append(skew.ax.text(0.02, 0.02, f'parcel calc failed: {e}', fontsize=8,
                                        color='red', transform=skew.ax.transAxes))

    dynamic.append(skew.ax.legend(loc='upper right', fontsize='small'))

    def _fmt(src):
        v = cc.get(src)
        tag = '◀shaded' if src == sel else ''
        return (f'{src} CAPE {v[0].m:.0f}/CIN {v[1].m:.0f}{tag}'
                if v is not None else f'{src} n/a')
    title_txt.set_text(
        f'ICON-D2 Skew-T  pressure (solid) vs model (dashed) @ {LABEL} ({LAT:.3f},{LON:.3f})\n'
        f'{t}Z  [{i + 1}/{len(times)}]   ' + '   '.join(_fmt(s) for s in ('model', 'pressure')))
    sub_txt.set_text(
        f'pressure run {data.run_press} (public) | model run {data.run_model} (private) '
        f'[{data.run_note}]   ref={len(ref["p"])} p-levels, model={len(ml["p"])} levels')
    sub_txt.set_color(note_color)
    fig.canvas.draw_idle()


def step(delta):
    global idx
    idx = max(0, min(len(times) - 1, idx + delta))
    draw(idx)


def relocate(lat, lon, label):
    """Re-fetch profiles for a new location and redraw."""
    global LAT, LON, LABEL, data, times, profiles, note_color, idx
    LAT, LON, LABEL = lat, lon, label
    data = load(lat, lon)
    times = data.times
    profiles = data.profiles
    note_color = 'green' if data.run_note == "same run" else 'red'
    idx = times.index(TARGET) if TARGET in times else 0
    draw(idx)


def on_submit(name):
    r = geocode(name)
    if r:
        relocate(*r)
    else:
        sub_txt.set_text(f"'{name}' not found")
        fig.canvas.draw_idle()


ax_prev = fig.add_axes([0.40, 0.02, 0.08, 0.045])
ax_next = fig.add_axes([0.52, 0.02, 0.08, 0.045])
b_prev = mwidgets.Button(ax_prev, '◀ Prev')
b_next = mwidgets.Button(ax_next, 'Next ▶')
b_prev.on_clicked(lambda _evt: step(-1))
b_next.on_clicked(lambda _evt: step(+1))

# CAPE/CIN source switch (model <-> pressure); drives parcel + red/blue shading
ax_src = fig.add_axes([0.66, 0.015, 0.13, 0.07])
ax_src.set_title('CAPE/CIN from', fontsize=8)
radio = mwidgets.RadioButtons(ax_src, ('model', 'pressure'),
                              active=('model', 'pressure').index(CAPE_SRC))


def on_src(label):
    global CAPE_SRC
    CAPE_SRC = label
    draw(idx)
radio.on_clicked(on_src)

# location picker: type a place name -> geocode -> relocate
ax_loc = fig.add_axes([0.10, 0.018, 0.20, 0.04])
tb_loc = mwidgets.TextBox(ax_loc, 'Ort ', initial='Graz')
tb_loc.on_submit(on_submit)


def on_key(evt):
    if evt.key == 'left':
        step(-1)
    elif evt.key == 'right':
        step(+1)
fig.canvas.mpl_connect('key_press_event', on_key)

print(f"# pressure run {data.run_press} (public) | model run {data.run_model} (private) "
      f"[{data.run_note}]")
print(f"# ICON-D2 Skew-T ({LAT},{LON}) elev={data.elev:.0f}m  "
      f"hours: {times[0]}Z .. {times[-1]}Z ({len(times)})")

draw(idx)
plt.show()
