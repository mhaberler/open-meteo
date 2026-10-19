#!/usr/bin/env python3
"""Compare ICON-D2 on the native host with open-meteo.wetterheidi.de.

The candidate is the native grid (dwd_icon_d2_native). The oracle is the
lat-lon host (icon_d2). Shared names are compared on overlapping hours.
Lake cells are checked only on the candidate: elevation must equal
model_elevation and stay well above sea level.

Writes an HTML summary to /var/www/vpsmon/regression/index.html and prints
https://vpsmon.meteo.mah.priv.at/regression/
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CANDIDATE = "https://open-meteo-next.mah.priv.at"
ORACLE = "https://open-meteo.wetterheidi.de"
CANDIDATE_MODEL = "dwd_icon_d2_native"
ORACLE_MODEL = "icon_d2"
REPORT_PATH = "/var/www/vpsmon/regression/index.html"
REPORT_URL = "https://vpsmon.meteo.mah.priv.at/regression/"

POINTS = [
    {"name": "Munich", "latitude": 48.14, "longitude": 11.58, "lake": False},
    {"name": "Zugspitze", "latitude": 47.42, "longitude": 10.98, "lake": False},
    {"name": "Starnberger See", "latitude": 47.86, "longitude": 11.29, "lake": True},
    {"name": "Ammersee", "latitude": 47.99, "longitude": 11.12, "lake": True},
    {"name": "Chiemsee", "latitude": 47.88, "longitude": 12.45, "lake": True},
]

# snowfall_convective_water_equivalent is ingest-only. It is not a VariableHourly
# case, and one unknown name rejects the whole hourly list.
SURFACE = [
    "wind_gusts_10m", "wind_u_component_10m", "wind_v_component_10m",
    "visibility", "pressure_msl", "surface_pressure_model", "model_elevation", "weather_code",
    "precipitation", "rain", "showers",
    "snowfall_water_equivalent", "snowfall_height",
    "temperature_2m", "relative_humidity_2m",
    "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm",
    "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
    "cloud_base", "freezing_level_height",
    "cape", "convective_inhibition", "lightning_potential",
    "convective_cloud_base", "convective_cloud_top",
]

FULL_LEVELS = (1, 30, 65)
FULL_VARS = (
    "temperature", "wind_u_component", "wind_v_component",
    "specific_humidity", "pressure", "cloud_cover",
)
HALF_LEVELS = (64, 65, 66)

PROFILE = (
    [f"{name}_level{level}" for name in FULL_VARS for level in FULL_LEVELS]
    + [f"wind_w_level{level}" for level in HALF_LEVELS]
    + [f"height_half_agl_level{level}" for level in HALF_LEVELS]
    + ["height_agl_level65"]
)

OPTIONAL_NULLS = {"visibility"}


def profile_names():
    return list(PROFILE)


def get(base, params):
    url = base.rstrip("/") + "/v1/dwd-icon?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=90) as response:
            raw = response.read().decode()
            status = response.status
    except urllib.error.HTTPError as error:
        raw = error.read().decode(errors="replace")
        status = error.code
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        body = {"reason": raw}
    return status, body, raw, url


def finite(values):
    return [value for value in values if isinstance(value, (int, float))]


def fail(failures, message):
    failures.append(message)
    print("FAIL", message)


def note(notes, message):
    notes.append(message)
    print("note", message)


def gate_for(name):
    if name.startswith("temperature") or name.startswith("soil_temperature"):
        return 3.0, "K"
    if name.startswith("specific_humidity"):
        return 2.0, "g/kg"
    if name.startswith("wind_"):
        return 2.0, "m/s"
    if name in {"pressure_msl", "surface_pressure", "surface_pressure_model"} or name.startswith("pressure_level"):
        return 2.0, "hPa"
    return None, None


def max_abs(left_times, left_values, right_times, right_values):
    right = dict(zip(right_times, right_values))
    diffs = []
    for moment, left in zip(left_times, left_values):
        other = right.get(moment)
        if isinstance(left, (int, float)) and isinstance(other, (int, float)):
            diffs.append(abs(left - other))
    if not diffs:
        return None
    return max(diffs)


def shared_times(left, right):
    return [moment for moment in left if moment in set(right)]


def qv_decimals(raw, level):
    needle = f'"specific_humidity_level{level}":['
    if needle not in raw:
        return None
    snippet = raw.split(needle, 1)[1].split("]", 1)[0]
    first = snippet.split(",")[0].strip()
    if "." not in first:
        return 0
    return len(first.split(".", 1)[1])


def check_units(failures, where, units):
    expected = {
        "model_elevation": "m",
        "pressure_msl": "hPa",
        "surface_pressure": "hPa",
        "surface_pressure_model": "hPa",
        "wind_gusts_10m": "m/s",
        "wind_u_component_10m": "m/s",
        "wind_v_component_10m": "m/s",
        "wind_w_level64": "m/s",
        "wind_w_level65": "m/s",
        "wind_w_level66": "m/s",
        "pressure_level1": "hPa",
        "pressure_level30": "hPa",
        "pressure_level65": "hPa",
    }
    for name, want in expected.items():
        if name not in units:
            continue
        if units.get(name) != want:
            fail(failures, f"{where} unit {name}={units.get(name)!r}, want {want!r}")


def check_series(failures, notes, where, names, hourly):
    for name in names:
        if name not in hourly:
            fail(failures, f"{where} missing {name}")
            continue
        if name in OPTIONAL_NULLS:
            if not finite(hourly[name]):
                note(notes, f"{where} {name} is all null")
            continue
        if not finite(hourly[name]):
            fail(failures, f"{where} {name} is all null")


def check_agl(failures, where, hourly):
    values = finite(hourly.get("height_agl_level65", []))
    if not values:
        fail(failures, f"{where} height_agl_level65 has no values")
        return
    worst = max(values, key=lambda value: abs(value - 10.0))
    if abs(worst - 10.0) > 1.0:
        fail(failures, f"{where} height_agl_level65={worst}, expected 10 m")


def check_half_levels(failures, where, hourly):
    columns = [hourly.get(f"height_half_agl_level{level}") for level in HALF_LEVELS]
    if any(column is None for column in columns):
        fail(failures, f"{where} missing a half-level height")
        return
    checked = 0
    for index in range(len(columns[0])):
        sample = [column[index] if index < len(column) else None for column in columns]
        if not all(isinstance(value, (int, float)) for value in sample):
            continue
        checked += 1
        if not (sample[0] > sample[1] > sample[2]):
            fail(failures, f"{where} half-level AGL not decreasing toward the surface: {sample}")
            return
    if checked == 0:
        fail(failures, f"{where} half-level heights have no finite hour")


def check_candidate_surface(failures, point, body):
    hourly = body.get("hourly", {})
    elevation = body.get("elevation")
    times = hourly.get("time", [])
    if not isinstance(elevation, (int, float)):
        fail(failures, f"{point} candidate elevation missing")
        return
    bases = hourly.get("cloud_base", [])
    below = [
        (moment, value)
        for moment, value in zip(times, bases)
        if isinstance(value, (int, float)) and value < elevation - 50
    ]
    if below:
        fail(failures, f"{point} cloud_base {below[0][1]} m is more than 50 m below elevation {elevation} m")
    cin = [value for value in hourly.get("convective_inhibition", []) if isinstance(value, (int, float))]
    if any(value < 0 for value in cin):
        fail(failures, f"{point} convective_inhibition below 0 (min {min(cin)})")
    for moment, freezing, snow in zip(times, hourly.get("freezing_level_height", []), hourly.get("snowfall_height", [])):
        if not all(isinstance(value, (int, float)) for value in (freezing, snow)):
            continue
        if freezing > elevation + 50 and snow > freezing:
            fail(failures, f"{point} {moment} snowfall_height {snow} exceeds freezing_level_height {freezing}")
            break


def check_lake(failures, point, body):
    elevation = body.get("elevation")
    series = finite(body.get("hourly", {}).get("model_elevation", []))
    if not isinstance(elevation, (int, float)) or not series:
        fail(failures, f"{point} lake elevation missing")
        return
    if elevation < 50 or min(series) < 50:
        fail(failures, f"{point} lake elevation {elevation} m, model_elevation {min(series)} m, want both above 50 m")
    gap = max(abs(elevation - value) for value in series)
    if gap > 0.5:
        fail(failures, f"{point} elevation {elevation} m != model_elevation (gap {gap} m)")


def check_range(failures, base, model, point):
    status, body, raw, _url = get(base, {
        "latitude": point["latitude"],
        "longitude": point["longitude"],
        "hourly": "temperature_level66",
        "forecast_hours": 1,
        "models": model,
        "windspeed_unit": "ms",
        "elevation": "nan",
        "cell_selection": "nearest",
    })
    text = raw if isinstance(raw, str) else ""
    if "1...65" not in text:
        reason = body.get("reason", text[:240]) if isinstance(body, dict) else text[:240]
        fail(failures, f"temperature_level66 status {status} did not report 1...65: {reason}")


def query(base, model, point, names):
    return get(base, {
        "latitude": point["latitude"],
        "longitude": point["longitude"],
        "hourly": ",".join(names),
        "forecast_hours": 6,
        "models": model,
        "windspeed_unit": "ms",
        "elevation": "nan",
        "cell_selection": "nearest",
    })


def render(path, ok, candidate, oracle, failures, notes, rows, lakes, generated):
    def cell(value):
        return html.escape("" if value is None else str(value))

    status = "pass" if ok else "fail"
    failure_rows = "".join(f"<li>{html.escape(item)}</li>" for item in failures) or "<li>none</li>"
    note_rows = "".join(f"<li>{html.escape(item)}</li>" for item in notes) or "<li>none</li>"
    diff_rows = "".join(
        "<tr><td>{point}</td><td>{name}</td><td>{diff}</td><td>{gate}</td><td>{verdict}</td></tr>".format(
            point=cell(row["point"]),
            name=cell(row["name"]),
            diff=cell(row["diff"]),
            gate=cell(row["gate"]),
            verdict=cell(row["verdict"]),
        )
        for row in rows
    )
    lake_rows = "".join(
        "<tr><td>{name}</td><td>{candidate}</td><td>{model}</td><td>{oracle}</td></tr>".format(
            name=cell(row["name"]),
            candidate=cell(row["candidate"]),
            model=cell(row["model"]),
            oracle=cell(row["oracle"]),
        )
        for row in lakes
    )
    hours = "".join(f"<li>{html.escape(item)}</li>" for item in generated["hours"]) or "<li>none</li>"
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ICON-D2 native regression {status}</title>
<style>
body {{ font: 15px/1.4 sans-serif; margin: 2rem; }}
.fail {{ color: #9b1c1c; }}
.pass {{ color: #146c43; }}
table {{ border-collapse: collapse; margin: 1rem 0; }}
td, th {{ border: 1px solid #ccc; padding: 0.3rem 0.6rem; text-align: left; }}
</style>
</head>
<body>
<h1 class="{status}">ICON-D2 native regression: {status}</h1>
<p>Generated {html.escape(generated["at"])}</p>
<p>Candidate {html.escape(candidate)} model {html.escape(CANDIDATE_MODEL)}<br>
Oracle {html.escape(oracle)} model {html.escape(ORACLE_MODEL)}</p>
<h2>Shared hours</h2>
<ul>{hours}</ul>
<h2>Lakes</h2>
<table>
<tr><th>Place</th><th>Candidate elevation m</th><th>Candidate model_elevation m</th><th>Oracle elevation m</th></tr>
{lake_rows}
</table>
<h2>Failures</h2>
<ul>{failure_rows}</ul>
<h2>Notes</h2>
<ul>{note_rows}</ul>
<h2>Max absolute differences</h2>
<table>
<tr><th>Place</th><th>Variable</th><th>Max abs</th><th>Gate</th><th></th></tr>
{diff_rows}
</table>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(page)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default=CANDIDATE)
    parser.add_argument("--oracle", default=ORACLE)
    parser.add_argument("--report", default=REPORT_PATH)
    args = parser.parse_args()

    failures = []
    notes = []
    rows = []
    lakes = []
    hour_lines = []

    check_range(failures, args.candidate, CANDIDATE_MODEL, POINTS[0])

    for point in POINTS:
        label = point["name"]
        print(label)
        cand_status, cand_body, cand_raw, cand_url = query(args.candidate, CANDIDATE_MODEL, point, SURFACE + profile_names())
        ora_status, ora_body, ora_raw, ora_url = query(args.oracle, ORACLE_MODEL, point, SURFACE + profile_names())
        print(" ", cand_status, cand_url)
        print(" ", ora_status, ora_url)
        if cand_status != 200 or not isinstance(cand_body.get("hourly"), dict):
            fail(failures, f"{label} candidate HTTP {cand_status}: {cand_body.get('reason', '')[:240]}")
            continue
        if ora_status != 200 or not isinstance(ora_body.get("hourly"), dict):
            fail(failures, f"{label} oracle HTTP {ora_status}: {ora_body.get('reason', '')[:240]}")
            continue

        names = SURFACE + profile_names()
        check_series(failures, notes, f"{label} candidate", names, cand_body["hourly"])
        check_series(failures, notes, f"{label} oracle", names, ora_body["hourly"])
        check_units(failures, f"{label} candidate", cand_body.get("hourly_units", {}))
        check_units(failures, f"{label} oracle", ora_body.get("hourly_units", {}))
        for raw, where in ((cand_raw, "candidate"), (ora_raw, "oracle")):
            decimals = qv_decimals(raw, 65)
            if decimals is None:
                fail(failures, f"{label} {where} missing specific_humidity_level65 in the raw JSON")
            elif decimals < 5:
                fail(failures, f"{label} {where} specific humidity decimals {decimals}")
        check_agl(failures, f"{label} candidate", cand_body["hourly"])
        check_agl(failures, f"{label} oracle", ora_body["hourly"])
        check_half_levels(failures, f"{label} candidate", cand_body["hourly"])
        check_half_levels(failures, f"{label} oracle", ora_body["hourly"])
        check_candidate_surface(failures, label, cand_body)
        if point["lake"]:
            check_lake(failures, label, cand_body)
            model_values = finite(cand_body["hourly"].get("model_elevation", []))
            lakes.append({
                "name": label,
                "candidate": cand_body.get("elevation"),
                "model": model_values[0] if model_values else None,
                "oracle": ora_body.get("elevation"),
            })
            print(f"  lake candidate {cand_body.get('elevation')} model {lakes[-1]['model']} oracle {ora_body.get('elevation')}")

        left_times = cand_body["hourly"].get("time", [])
        right_times = ora_body["hourly"].get("time", [])
        common = shared_times(left_times, right_times)
        hour_lines.append(f"{label}: {', '.join(common) if common else 'none'}")
        if not common:
            fail(failures, f"{label} no overlapping hours")
            continue
        for name in names:
            if name not in cand_body["hourly"] or name not in ora_body["hourly"]:
                continue
            diff = max_abs(left_times, cand_body["hourly"][name], right_times, ora_body["hourly"][name])
            limit, unit = gate_for(name)
            if diff is None:
                verdict = "no finite overlap"
                if name not in OPTIONAL_NULLS:
                    fail(failures, f"{label} {name} has no finite overlapping values")
            elif limit is not None and diff > limit:
                verdict = "fail"
                fail(failures, f"{label} {name} max abs {diff:.3f} {unit} exceeds {limit}")
            else:
                verdict = "ok"
            gate = "" if limit is None else f"{limit:g} {unit}"
            shown = "" if diff is None else f"{diff:.3f}"
            rows.append({"point": label, "name": name, "diff": shown, "gate": gate, "verdict": verdict})
            if limit is not None or name.startswith("height") or name == "model_elevation":
                print(f"  {name} {shown or 'n/a'} {verdict}")

    ok = not failures
    try:
        render(args.report, ok, args.candidate, args.oracle, failures, notes, rows, lakes, {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "hours": hour_lines,
        })
    except OSError as error:
        print(f"FAIL could not write {args.report}: {error}", file=sys.stderr)
        return 1
    print(REPORT_URL)
    print("PASS" if ok else f"FAIL {len(failures)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
