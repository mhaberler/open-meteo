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
from metpy.plots import SkewT, Hodograph
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

# --- complex layout (after MetPy Advanced_Sounding_With_Complex_Layout):
#     Skew-T fills the tall left column; right column stacks hodograph, the
#     convective strip and the index table; compact widgets sit bottom-right. ---
fig = plt.figure(figsize=(18, 12))
skew = SkewT(fig, rotation=45, rect=(0.04, 0.05, 0.46, 0.84))
hodo_ax = fig.add_axes((0.57, 0.64, 0.39, 0.31))   # hodograph (rebuilt each redraw)
ax_conv = fig.add_axes((0.57, 0.46, 0.39, 0.13))   # convective CCL->BL time-series strip
ax_tbl  = fig.add_axes((0.55, 0.15, 0.42, 0.27))   # index table (text, axis off)
ax_tbl.axis('off')

# --- static setup (built ONCE; clearing the SkewT axis would destroy its
#     projection + log-p scale, so we never cla() — only swap dynamic artists) ---
skew.plot_dry_adiabats(alpha=0.25)
skew.plot_moist_adiabats(alpha=0.25)
skew.plot_mixing_lines(alpha=0.25)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)
skew.ax.set_xlabel('Temperatur (°C)')
skew.ax.set_ylabel('Druck (hPa)')

# titles centered over the left Skew-T column only (x≈0.27), clear of the hodograph
title_txt = fig.suptitle("", fontsize=11, fontweight='bold', x=0.27, y=0.985)
sub_txt = fig.text(0.27, 0.925, "", ha='center', fontsize=8, color=note_color)
dynamic = []                          # per-hour artists, removed before each redraw
CAPE_SRC = 'model'                    # which profile drives parcel + CAPE/CIN + panels

HODO_MAX_KM = 12                      # height cap for the hodograph color / Bunkers


def _q(seq, unit):
    return np.array(seq, dtype=float) * unit


def _uvz(prof):
    """(P, T, Td, z, u, v) with units for a {p,T,Dew,h,Spd,Dir} profile, or None."""
    if not prof['p']:
        return None
    P  = _q(prof['p'], units.hPa)
    T  = _q(prof['T'], units.degC)
    Td = _q(prof['Dew'], units.degC)
    z  = _q(prof['h'], units.meter)
    u, v = mpcalc.wind_components(_q(prof['Spd'], units('m/s')), _q(prof['Dir'], units.deg))
    return P, T, Td, z, u, v


def _na(fn):
    """Run fn() returning a formatted str; 'n/a' on any failure / non-finite."""
    try:
        v = fn()
        return v if v is not None else 'n/a'
    except Exception:
        return 'n/a'


def draw_hodograph(data6, src):
    """Rebuild the hodograph from (P,T,Td,z,u,v); height-colored 0..HODO_MAX_KM + Bunkers."""
    hodo_ax.cla()
    P, T, Td, z, u, v = data6
    m = z.to('km').m <= HODO_MAX_KM
    uu, vv, zz = u[m], v[m], z[m]
    spd = np.hypot(uu.to('m/s').m, vv.to('m/s').m)
    cr = max(40.0, np.ceil((spd.max() if spd.size else 0) / 10.0) * 10.0)
    h = Hodograph(hodo_ax, component_range=cr)
    h.add_grid(increment=20, ls='-', lw=1.2, alpha=0.5)
    h.add_grid(increment=10, ls='--', lw=0.8, alpha=0.2)
    if uu.size:
        h.plot_colormapped(uu, vv, c=zz.to('km'), linewidth=5,
                           label=f'0-{HODO_MAX_KM}km wind')
    try:                                  # Bunkers storm motion (needs full column)
        rm, lm, mw = mpcalc.bunkers_storm_motion(P, u, v, z)
        for vec, col, lab in ((rm, 'r', 'RM'), (lm, 'b', 'LM'), (mw, 'g', 'MW')):
            hodo_ax.plot(vec[0].to('m/s').m, vec[1].to('m/s').m, 'o', color=col, markersize=6)
            hodo_ax.annotate(lab, (vec[0].to('m/s').m, vec[1].to('m/s').m),
                             color=col, fontsize=8, xytext=(4, 4), textcoords='offset points')
    except Exception:
        pass
    hodo_ax.set_title(f'Hodograph (m/s, {src})', fontsize=10)


def draw_table(data6, src):
    """Rebuild the index table from (P,T,Td,z,u,v); thermo follows src, kinematic guarded."""
    ax_tbl.cla()
    ax_tbl.axis('off')
    P, T, Td, z, u, v = data6

    def cc(fn):
        c, i = fn()
        return f'{c.m:.0f} / {i.m:.0f}'
    sb = _na(lambda: cc(lambda: mpcalc.surface_based_cape_cin(P, T, Td)))
    ml_ = _na(lambda: cc(lambda: mpcalc.mixed_layer_cape_cin(P, T, Td)))
    mu = _na(lambda: cc(lambda: mpcalc.most_unstable_cape_cin(P, T, Td)))
    ki = _na(lambda: f"{mpcalc.k_index(P, T, Td).m:.0f}")
    tt = _na(lambda: f"{mpcalc.total_totals_index(P, T, Td).m:.0f}")
    pw = _na(lambda: f"{mpcalc.precipitable_water(P, Td).to('mm').m:.0f} mm")

    def srh(depth):
        rm, _lm, _mw = mpcalc.bunkers_storm_motion(P, u, v, z)
        _p, _n, tot = mpcalc.storm_relative_helicity(z, u, v, depth=depth * units.km,
                                                     storm_u=rm[0], storm_v=rm[1])
        return f"{tot.m:.0f}"
    def shr(depth):
        us, vs = mpcalc.bulk_shear(P, u, v, height=z, depth=depth * units.km)
        return f"{mpcalc.wind_speed(us, vs).to('m/s').m:.0f} m/s"
    srh1, srh3 = _na(lambda: srh(1)), _na(lambda: srh(3))
    shr1, shr6 = _na(lambda: shr(1)), _na(lambda: shr(6))

    left = [('SBCAPE/CIN', sb), ('MLCAPE/CIN', ml_), ('MUCAPE/CIN', mu),
            ('K-Index', ki), ('Totals-Totals', tt), ('PW', pw)]
    right = [('SRH 0-1 km', srh1), ('SRH 0-3 km', srh3),
             ('Shear 0-1 km', shr1), ('Shear 0-6 km', shr6)]
    ax_tbl.text(0.0, 1.0, f'Indices ({src})', fontsize=11, fontweight='bold',
                va='top', transform=ax_tbl.transAxes)
    for col, items, x in ((0, left, 0.0), (1, right, 0.55)):
        for r, (k, val) in enumerate(items):
            y = 0.85 - r * 0.14
            colr = 'orangered' if 'CAPE' in k else 'navy' if ('SRH' in k or 'Shear' in k) else 'black'
            ax_tbl.text(x, y, k, fontsize=10, va='top', transform=ax_tbl.transAxes)
            ax_tbl.text(x + 0.30, y, val, fontsize=10, fontweight='bold', color=colr,
                        va='top', transform=ax_tbl.transAxes)


def model_arrays(t):
    """(p, T, Td) with units for the model-level profile at valid time t, or None."""
    ml = profiles[t][0]
    if not ml['p']:
        return None
    return (_q(ml['p'], units.hPa), _q(ml['T'], units.degC), _q(ml['Dew'], units.degC))


def convective(arrays):
    """CCL / convective temperature / BL (=EL) + SBCAPE for a model profile.

    Returns dict {ccl_p, tcon, bl_p, cape, triggered} or None when undefined."""
    if arrays is None:
        return None
    P, T, Td = arrays
    try:
        ccl_p, _ccl_t, tcon = mpcalc.ccl(P, T, Td)
        prof_c = mpcalc.parcel_profile(P, tcon, Td[0])
        bl_p, _ = mpcalc.el(P, T, Td, prof_c)
        prof_s = mpcalc.parcel_profile(P, T[0], Td[0]).to('degC')
        cape, cin = mpcalc.cape_cin(P, T, Td, prof_s)
        if not (np.isfinite(ccl_p.m) and np.isfinite(bl_p.m) and bl_p.m < ccl_p.m):
            return None
        # convection expected if there is CAPE AND the surface parcel can reach the
        # LFC: either the cap is already weak (CIN ~ 0) or surface heating reaches TCON.
        triggered = cape.m > 100 and (cin.m > -25 or float(T[0].m) >= float(tcon.m))
        return {'ccl_p': ccl_p.m, 'tcon': tcon.m, 'bl_p': bl_p.m,
                'cape': cape.m, 'cin': cin.m, 'triggered': triggered}
    except Exception:
        return None


def _cape_color(cape):
    return 'gold' if cape < 300 else 'orange' if cape < 1000 else 'red'


def draw_strip():
    """(Re)draw the per-hour CCL->BL convective bars; persists across stepping."""
    import matplotlib.lines as mlines
    ax_conv.clear()
    ax_conv.set_yscale('log')
    ax_conv.set_ylim(1000, 100)
    ax_conv.set_xlim(-0.5, len(times) - 0.5)
    for i, t in enumerate(times):
        c = conv.get(t)
        if c and c['triggered']:
            ax_conv.plot([i, i], [c['ccl_p'], c['bl_p']], lw=3,
                         color=_cape_color(c['cape']), solid_capstyle='butt')
    s = max(1, len(times) // 8)
    ticks = list(range(0, len(times), s))
    ax_conv.set_xticks(ticks)
    ax_conv.set_xticklabels([times[j][5:13] for j in ticks], rotation=90, fontsize=7)
    ax_conv.set_yticklabels([])           # pressure rows already labelled on the Skew-T
    ax_conv.set_title('convective CCL→BL', fontsize=9)
    ax_conv.grid(True, axis='x', linestyle=':', alpha=0.4)
    handles = [mlines.Line2D([], [], color=c, lw=3, label=l) for c, l in
               (('gold', '<300'), ('orange', '300–1000'), ('red', '>1000'))]
    ax_conv.legend(handles=handles, fontsize=7, loc='upper right',
                   title='SBCAPE J/kg', title_fontsize=7)


conv = {}                             # valid-time -> convective() dict (or None)


def build_convective():
    global conv
    conv = {t: convective(model_arrays(t)) for t in times}
    draw_strip()


def draw(i):
    t = times[i]
    ml, ref = profiles[t]

    for a in dynamic:                 # drop previous hour's artists
        try:
            a.remove()
        except (NotImplementedError, ValueError):
            pass                      # already gone (e.g. ax_conv was cleared)
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

    # hodograph + index table from the SELECTED source (kinematic guarded inside)
    src6 = {'model': _uvz(ml), 'pressure': _uvz(ref)}
    psel = sel if (sel and src6.get(sel)) else next((s for s in ('model', 'pressure') if src6.get(s)), None)
    if psel:
        draw_hodograph(src6[psel], psel)
        draw_table(src6[psel], psel)

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
    dynamic.append(ax_conv.axvline(i, color='black', lw=1.2, alpha=0.8))   # current hour
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
    build_convective()
    draw(idx)


def on_submit(name):
    r = geocode(name)
    if r:
        relocate(*r)
    else:
        sub_txt.set_text(f"'{name}' not found")
        fig.canvas.draw_idle()


# compact controls, bottom-right (keep the left column free for the tall Skew-T)
ax_prev = fig.add_axes([0.70, 0.075, 0.05, 0.03])
ax_next = fig.add_axes([0.755, 0.075, 0.05, 0.03])
b_prev = mwidgets.Button(ax_prev, '◀')
b_next = mwidgets.Button(ax_next, '▶')
b_prev.on_clicked(lambda _evt: step(-1))
b_next.on_clicked(lambda _evt: step(+1))

# CAPE/CIN source switch (model <-> pressure); drives parcel + red/blue shading
ax_src = fig.add_axes([0.84, 0.045, 0.11, 0.065])
ax_src.set_title('CAPE/CIN from', fontsize=7)
radio = mwidgets.RadioButtons(ax_src, ('model', 'pressure'),
                              active=('model', 'pressure').index(CAPE_SRC))


def on_src(label):
    global CAPE_SRC
    CAPE_SRC = label
    draw(idx)
radio.on_clicked(on_src)

# location picker: type a place name -> geocode -> relocate
ax_loc = fig.add_axes([0.60, 0.075, 0.09, 0.03])
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

build_convective()
draw(idx)
plt.show()
