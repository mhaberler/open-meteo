#!/usr/bin/env python3
"""Verify an Open-Meteo server's ICON model-level output against the original DWD GRIBs.

Generic verification client: parameterised by --server, --model, --run and --time.
The run must already be ingested on the target server (operator's job) — this script
does NOT ingest anything, it only compares.

For each sampled (variable, level) it
  1. downloads the matching DWD model-level GRIB, decodes it with eccodes and reads the
     value nearest to the test point, and
  2. asks the Open-Meteo server for `<var>_level<N>` at the same point (cell_selection=nearest)
     for the valid time `--time`,
then compares with unit conversion and a per-variable tolerance.

Exact agreement is expected only for regular-lat-lon models (icon-d2, icon-eu): the server
ingests those grids verbatim. The global `icon` model ships icosahedral GRIBs which the server
remaps via CDO, so the comparison there is approximate (looser tolerance, nearest on the
native icosahedral grid).

Requires: `pip install eccodes` plus the system ecCodes library (brew install eccodes).

Examples:
  python test_modellevel_vs_dwd.py --server https://open-meteo.mah.priv.at --model icon-d2 \
      --run 2026062000 --time 2026-06-20T03:00
  python test_modellevel_vs_dwd.py --server https://open-meteo.mah.priv.at --model icon-eu \
      --run 2026062000 --time 2026-06-20T06:00 --lat 48.2 --lon 16.4
"""
import argparse
import bz2
import json
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# Per-variable mapping: DWD GRIB token, Open-Meteo api type, GRIB->API unit conversion, tolerance.
# NOTE: the api already converts at ingest — temperature K->°C, pressure Pa->hPa,
# specific_humidity kg/kg->g/kg (×1000). u/v stay m/s. Conversions below mirror that.
VARS = {
    "t":  dict(dwd="t",  api="temperature",       conv=lambda x: x - 273.15, atol=0.1,  rtol=None, unit="°C"),
    "p":  dict(dwd="p",  api="pressure",          conv=lambda x: x / 100.0,  atol=0.2,  rtol=None, unit="hPa"),
    "u":  dict(dwd="u",  api="wind_u_component",  conv=lambda x: x,          atol=0.1,  rtol=None, unit="m/s"),
    "v":  dict(dwd="v",  api="wind_v_component",  conv=lambda x: x,          atol=0.1,  rtol=None, unit="m/s"),
    "qv": dict(dwd="qv", api="specific_humidity", conv=lambda x: x * 1000.0, atol=None, rtol=0.01, unit="g/kg"),
}

# Per-model: DWD path == api download domain id, region + grid in the GRIB filename,
# number of native full levels, Open-Meteo api model id, and whether the filename variable
# token is upper-cased (DownloadIconCommand.swift:315 — only icon-d2/eps use lower-case).
MODELS = {
    "icon-d2": dict(path="icon-d2", region="germany", grid="regular-lat-lon", nlev=65,  api="icon_d2",     fname_upper=False, lat=48.0, lon=11.0),
    "icon-eu": dict(path="icon-eu", region="europe",  grid="regular-lat-lon", nlev=74,  api="icon_eu",     fname_upper=True,  lat=48.0, lon=11.0),
    "icon":    dict(path="icon",    region="global",  grid="icosahedral",     nlev=120, api="icon_global", fname_upper=True,  lat=48.0, lon=11.0),
}

DWD_BASE = "https://opendata.dwd.de/weather/nwp"


def sample_levels(nlev, n_mid=4):
    """Boundaries (1=top, nlev=surface) + ~n_mid evenly spaced interior levels."""
    pts = {1, nlev}
    for i in range(1, n_mid + 1):
        pts.add(round(1 + i * (nlev - 1) / (n_mid + 1)))
    return sorted(pts)


def dwd_url(m, run, h3, level, dwd_var):
    fname_var = dwd_var.upper() if m["fname_upper"] else dwd_var
    fname = f"{m['path']}_{m['region']}_{m['grid']}_model-level_{run}_{h3}_{level}_{fname_var}.grib2.bz2"
    return f"{DWD_BASE}/{m['path']}/grib/{run[8:10]}/{dwd_var}/{fname}"


def dwd_value(url, lat, lon):
    """Download + bunzip2 a single-message GRIB, return value nearest (lat,lon) via eccodes."""
    import eccodes
    with urllib.request.urlopen(url, timeout=120) as r:
        raw = bz2.decompress(r.read())
    with tempfile.NamedTemporaryFile(suffix=".grib2") as tf:
        tf.write(raw)
        tf.flush()
        with open(tf.name, "rb") as f:
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                raise RuntimeError("empty GRIB")
            try:
                near = eccodes.codes_grib_find_nearest(gid, lat, lon)[0]
                return near.value, near.lat, near.lon
            finally:
                eccodes.codes_release(gid)


def server_values(server, api_model, lat, lon, levels, valid_iso, day):
    """One request for all sampled vars×levels; return {(grib_token, level): value} at valid_iso."""
    hourly = []
    for level in levels:
        for spec in VARS.values():
            hourly.append(f"{spec['api']}_level{level}")
    query = {
        "latitude": lat, "longitude": lon,
        "hourly": ",".join(hourly),
        "models": api_model,
        "wind_speed_unit": "ms",
        "cell_selection": "nearest",
        "timezone": "GMT",
        "start_date": day, "end_date": day,
    }
    url = f"{server.rstrip('/')}/v1/forecast?{urllib.parse.urlencode(query)}"
    with urllib.request.urlopen(url, timeout=120) as r:
        js = json.load(r)
    H = js["hourly"]
    times = H["time"]
    want = valid_iso[:16]
    if want not in times:
        raise SystemExit(f"valid time {want} not in server response (have {times[0]}..{times[-1]})")
    i = times.index(want)
    out = {}
    for level in levels:
        for tok, spec in VARS.items():
            col = H.get(f"{spec['api']}_level{level}")
            out[(tok, level)] = (col[i] if col is not None else None)
    return out, js.get("elevation")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default="https://open-meteo.mah.priv.at",
                    help="Open-Meteo base URL (default: https://open-meteo.mah.priv.at)")
    ap.add_argument("--model", required=True, choices=sorted(MODELS), help="icon-d2 | icon-eu | icon")
    ap.add_argument("--run", required=True, help="model run YYYYMMDDHH (UTC)")
    ap.add_argument("--time", required=True, help="valid time YYYY-MM-DDTHH:MM (UTC); step = time - run")
    ap.add_argument("--lat", type=float, help="test point latitude (default: model centre)")
    ap.add_argument("--lon", type=float, help="test point longitude (default: model centre)")
    ap.add_argument("--levels", help="comma-separated levels (default: boundaries + 4 evenly spaced)")
    ap.add_argument("--vars", default="t,p,u,v,qv", help="comma-separated subset of t,p,u,v,qv")
    args = ap.parse_args()

    m = MODELS[args.model]
    lat = args.lat if args.lat is not None else m["lat"]
    lon = args.lon if args.lon is not None else m["lon"]
    levels = ([int(x) for x in args.levels.split(",")] if args.levels else sample_levels(m["nlev"]))
    tokens = [t.strip() for t in args.vars.split(",") if t.strip() in VARS]

    run_dt = datetime.strptime(args.run, "%Y%m%d%H").replace(tzinfo=timezone.utc)
    valid_dt = datetime.strptime(args.time, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
    step = int((valid_dt - run_dt).total_seconds() // 3600)
    if step < 0:
        raise SystemExit("--time is before --run")
    h3 = f"{step:03d}"
    day = valid_dt.strftime("%Y-%m-%d")

    print(f"# {args.model} run {args.run} +{h3}h  valid {args.time}Z  point ({lat},{lon})")
    print(f"# server {args.server}  levels {levels}  vars {tokens}")
    if m["grid"] != "regular-lat-lon":
        print(f"# NOTE: {args.model} is {m['grid']} → server CDO-remaps; comparison is APPROXIMATE")

    srv, elev = server_values(args.server, m["api"], lat, lon, levels, args.time, day)
    print(f"# server elevation {elev} m\n")

    hdr = f"{'var':>4} {'lvl':>4} {'DWD':>12} {'server':>12} {'diff':>10} {'tol':>8}  result"
    print(hdr)
    print("-" * len(hdr))
    failures = 0
    for level in levels:
        for tok in tokens:
            spec = VARS[tok]
            url = dwd_url(m, args.run, h3, level, spec["dwd"])
            try:
                raw, nlat, nlon = dwd_value(url, lat, lon)
            except Exception as e:
                print(f"{tok:>4} {level:>4}  DWD fetch/decode failed: {e}")
                failures += 1
                continue
            ref = spec["conv"](raw)
            got = srv.get((tok, level))
            if got is None:
                print(f"{tok:>4} {level:>4} {ref:12.4f} {'null':>12} {'—':>10} {'—':>8}  FAIL (no server value)")
                failures += 1
                continue
            diff = got - ref
            if spec["rtol"] is not None:
                tol = spec["rtol"] * max(abs(ref), 1e-9)
                tol_s = f"{spec['rtol']*100:.0f}%"
            else:
                tol = spec["atol"]
                tol_s = f"{spec['atol']:.2g}"
            ok = abs(diff) <= tol
            failures += not ok
            print(f"{tok:>4} {level:>4} {ref:12.4f} {got:12.4f} {diff:10.4f} {tol_s:>8}  {'ok' if ok else 'FAIL'}")

    print()
    if failures:
        print(f"FAILED: {failures} mismatch(es)")
        sys.exit(1)
    print("PASSED: all samples within tolerance")


if __name__ == "__main__":
    main()
