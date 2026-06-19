#!/usr/bin/env python3
"""MetPy Skew-T log-p for a single ICON-GLOBAL hour: dev-server native model levels
(120) overlaid with public-api pressure levels (18).

Model-level T/Td solid + wind barbs; public pressure-level T/Td as 'P' markers.
Surface-based parcel ascent, shaded CAPE/CIN and LCL/LFC/EL markers are computed
from the (denser) model-level profile. The dev ingest only covers a 1-2 h window so
there is nothing to step through, but a geocode text box relocates the point. Data
via sounding_global_data.py.

Modelled on https://unidata.github.io/MetPy/latest/examples/Advanced_Sounding.html
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units

from sounding_global_data import load, geocode

LAT, LON = 46.9911, 15.4396          # Graz
LABEL = "Graz"
TARGET = "2026-06-19T00:00"          # the dev ingest window (00..01Z); None -> first hour

data = load(LAT, LON, TARGET)


def _q(seq, unit):
    return np.array(seq, dtype=float) * unit


fig = plt.figure(figsize=(11, 11))
skew = SkewT(fig, rotation=45, rect=(0.08, 0.10, 0.84, 0.82))
# static guides — built ONCE; clearing the SkewT axis would destroy its projection.
skew.plot_dry_adiabats(alpha=0.25)
skew.plot_moist_adiabats(alpha=0.25)
skew.plot_mixing_lines(alpha=0.25)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)
skew.ax.set_xlabel('Temperatur (°C)')
skew.ax.set_ylabel('Druck (hPa)')

title_txt = fig.suptitle("", fontsize=13, fontweight='bold', y=0.99)
sub_txt = fig.text(0.5, 0.945, "", ha='center', fontsize=9)
dynamic = []                          # per-location artists, removed before each redraw


def draw():
    ml, ref = data.ml, data.ref
    note_color = 'green' if data.run_note == "same run" else 'red'

    for a in dynamic:
        try:
            a.remove()
        except (NotImplementedError, ValueError):
            pass
    dynamic.clear()

    P  = _q(ml['p'], units.hPa)
    T  = _q(ml['T'], units.degC)
    Td = _q(ml['Dew'], units.degC)
    u, v = mpcalc.wind_components(_q(ml['Spd'], units('m/s')), _q(ml['Dir'], units.deg))

    dynamic.extend(skew.plot(P, T,  'r', linewidth=2, label='T (model)'))
    dynamic.extend(skew.plot(P, Td, 'g', linewidth=2, label='Td (model)'))
    k = max(1, len(P) // 25)
    dynamic.append(skew.plot_barbs(P[::k], u[::k].to('knots'), v[::k].to('knots')))

    if ref['p']:                      # public pressure levels: 'P' markers
        rp = _q(ref['p'], units.hPa)
        dynamic.extend(skew.plot(rp, _q(ref['T'], units.degC),   'r', marker='P',
                                 markersize=8, linestyle='none', label='T (pressure)'))
        dynamic.extend(skew.plot(rp, _q(ref['Dew'], units.degC), 'g', marker='P',
                                 markersize=8, linestyle='none', label='Td (pressure)'))

    cape = cin = None
    try:
        prof = mpcalc.parcel_profile(P, T[0], Td[0]).to('degC')
        dynamic.extend(skew.plot(P, prof, 'k', linewidth=1.6, label='parcel (model)'))
        dynamic.append(skew.shade_cin(P, T, prof, Td, facecolor='tab:blue', alpha=0.3))
        dynamic.append(skew.shade_cape(P, T, prof, facecolor='tab:red', alpha=0.3))
        cape, cin = mpcalc.cape_cin(P, T, Td, prof)

        lcl_p, lcl_t = mpcalc.lcl(P[0], T[0], Td[0])
        dynamic.extend(skew.plot(lcl_p, lcl_t, 'ko', markerfacecolor='black'))
        dynamic.append(skew.ax.text(0.02, lcl_p.m, ' LCL', va='center', fontsize=8,
                                    transform=skew.ax.get_yaxis_transform()))
        for name, fn, col in (('LFC', mpcalc.lfc, 'tab:purple'), ('EL', mpcalc.el, 'tab:brown')):
            lp, lt = fn(P, T, Td, prof)
            if lp is not None and np.isfinite(lp.m):
                dynamic.extend(skew.plot(lp, lt, 'o', color=col))
                dynamic.append(skew.ax.text(0.02, lp.m, f' {name}', va='center', fontsize=8,
                                            color=col, transform=skew.ax.get_yaxis_transform()))
    except Exception as e:
        dynamic.append(skew.ax.text(0.02, 0.02, f'parcel calc failed: {e}', fontsize=8,
                                    color='red', transform=skew.ax.transAxes))

    dynamic.append(skew.ax.legend(loc='upper right', fontsize='small'))

    cape_s = f'CAPE {cape.m:.0f} CIN {cin.m:.0f}' if cape is not None else 'CAPE n/a'
    title_txt.set_text(f'ICON global Skew-T @ {LABEL} ({LAT:.3f},{LON:.3f}) — {data.time}Z\n'
                       f'dev model({len(ml["p"])}) vs public pressure({len(ref["p"])})   {cape_s}')
    sub_txt.set_text(f'model run {data.run_model} (dev) | pressure run {data.run_ref} (public) '
                     f'[{data.run_note}]   elev={data.elev:.0f}m')
    sub_txt.set_color(note_color)
    fig.canvas.draw_idle()
    return cape_s


def relocate(lat, lon, label):
    global LAT, LON, LABEL, data
    LAT, LON, LABEL = lat, lon, label
    data = load(lat, lon, TARGET)
    draw()


def on_submit(name):
    r = geocode(name)
    if r:
        relocate(*r)
    else:
        sub_txt.set_text(f"'{name}' not found")
        fig.canvas.draw_idle()


# location picker: type a place name -> geocode -> relocate
ax_loc = fig.add_axes([0.12, 0.02, 0.22, 0.04])
tb_loc = mwidgets.TextBox(ax_loc, 'Ort ', initial=LABEL)
tb_loc.on_submit(on_submit)

cape_s = draw()
print(f"# ICON global ({LAT},{LON}) elev={data.elev:.0f}m  valid {data.time}Z  "
      f"[{data.run_note}]  model={len(data.ml['p'])} levels, pressure={len(data.ref['p'])} levels")
print(f"# model run {data.run_model} (dev) | pressure run {data.run_ref} (public)  {cape_s}")

plt.show()
