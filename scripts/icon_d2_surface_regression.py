#!/usr/bin/env python3
"""Compare ICON-D2 surface fields on the public API, wetterheidi, and the native host.

The public API and wetterheidi are both regular lat-lon icon_d2. A shared
name must agree within one stored step. The native host is gated against
wetterheidi with the looser gates from the column regression. The native
host is not compared with the public API. Pass `--skip-public` to compare
only the oracle and the candidate.

model_elevation and surface_pressure_model are omitted from the public
request: either name makes that host reject the whole hourly list. They
are compared only between wetterheidi and the native host.

Writes /var/www/vpsmon/regression/surface.html and prints
https://vpsmon.meteo.mah.priv.at/regression/surface.html
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

PUBLIC = "https://api.open-meteo.com"
ORACLE = "https://open-meteo.wetterheidi.de"
CANDIDATE = "https://open-meteo-next.mah.priv.at"
PUBLIC_MODEL = "icon_d2"
ORACLE_MODEL = "icon_d2"
CANDIDATE_MODEL = "dwd_icon_d2_native"
REPORT_PATH = "/var/www/vpsmon/regression/surface.html"
REPORT_URL = "https://vpsmon.meteo.mah.priv.at/regression/surface.html"

POINTS = [
    {"name": "Munich", "latitude": 48.14, "longitude": 11.58, "lake": False},
    {"name": "Zugspitze", "latitude": 47.42, "longitude": 10.98, "lake": False},
    {"name": "Starnberger See", "latitude": 47.88, "longitude": 11.31, "lake": True},
    {"name": "Ammersee", "latitude": 47.99, "longitude": 11.12, "lake": True},
    {"name": "Chiemsee", "latitude": 47.88, "longitude": 12.45, "lake": True},
]

# heidiVars surface names. snowfall_convective_water_equivalent is ingest-only.
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

# Either name makes api.open-meteo.com reject the whole hourly list.
PUBLIC_OMIT = {"model_elevation", "surface_pressure_model"}
OPTIONAL_NULLS = {"visibility"}


def public_names():
    return [name for name in SURFACE if name not in PUBLIC_OMIT]


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
    return status, body, url


def finite(values):
    return [value for value in values if isinstance(value, (int, float))]


def fail(failures, message):
    failures.append(message)
    print("FAIL", message)


def note(notes, message):
    notes.append(message)
    print("note", message)


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


def candidate_gate(name):
    """Gates shared with the native column regression. Other names are reported only."""
    if name.startswith("temperature") or name.startswith("soil_temperature"):
        return 3.0, "K"
    if name.startswith("wind_"):
        return 2.0, "m/s"
    if name in {"pressure_msl", "surface_pressure", "surface_pressure_model"}:
        return 2.0, "hPa"
    return None, None


def public_gate(name):
    """One stored step, with a small margin, for the shared lat-lon cell."""
    if name in OPTIONAL_NULLS:
        return None, None
    if name.startswith("temperature") or name.startswith("soil_temperature"):
        return 0.1, "K"
    if name.startswith("wind_"):
        return 0.2, "m/s"
    if name == "pressure_msl":
        return 0.2, "hPa"
    if name in {"precipitation", "rain", "showers", "snowfall_water_equivalent"}:
        return 0.2, "mm"
    if name.startswith("cloud_cover") or name == "relative_humidity_2m":
        return 1.0, ""
    if name == "weather_code":
        return 0.0, ""
    if name in {"cloud_base", "freezing_level_height", "snowfall_height", "convective_cloud_base", "convective_cloud_top"}:
        return 20.0, "m"
    if name in {"cape", "convective_inhibition"}:
        return 10.0, ""
    if name == "lightning_potential":
        return 0.2, ""
    return None, None


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


def check_units(failures, where, units):
    expected = {
        "model_elevation": "m",
        "pressure_msl": "hPa",
        "surface_pressure_model": "hPa",
        "wind_gusts_10m": "m/s",
        "wind_u_component_10m": "m/s",
        "wind_v_component_10m": "m/s",
    }
    for name, want in expected.items():
        if name not in units:
            continue
        if units.get(name) != want:
            fail(failures, f"{where} unit {name}={units.get(name)!r}, want {want!r}")


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


def compare(failures, point, name, left_times, left_values, right_times, right_values, gate):
    diff = max_abs(left_times, left_values, right_times, right_values)
    if name in OPTIONAL_NULLS:
        shown = "" if diff is None else f"{diff:.3f}"
        return shown, "", "note"
    limit, unit = gate(name)
    if diff is None:
        if name not in OPTIONAL_NULLS:
            fail(failures, f"{point} {name} has no finite overlapping values")
        return "", "" if limit is None else f"{limit:g} {unit}".strip(), "no finite overlap"
    if limit is not None and diff > limit:
        fail(failures, f"{point} {name} max abs {diff:.3f} {unit} exceeds {limit:g}")
        verdict = "fail"
    else:
        verdict = "ok"
    gate_text = "" if limit is None else f"{limit:g} {unit}".strip()
    return f"{diff:.3f}", gate_text, verdict


def render(path, ok, failures, notes, rows, lakes, generated, include_public):
    def cell(value):
        return html.escape("" if value is None else str(value))

    status = "pass" if ok else "fail"
    failure_rows = "".join(f"<li>{html.escape(item)}</li>" for item in failures) or "<li>none</li>"
    note_rows = "".join(f"<li>{html.escape(item)}</li>" for item in notes) or "<li>none</li>"
    def diff_row(row):
        public_cells = ""
        if include_public:
            public_cells = "<td>{public}</td><td>{public_gate}</td><td>{public_verdict}</td>".format(
                public=cell(row["public"]),
                public_gate=cell(row["public_gate"]),
                public_verdict=cell(row["public_verdict"]),
            )
        return (
            "<tr><td>{point}</td><td>{name}</td>{public}"
            "<td>{candidate}</td><td>{candidate_gate}</td><td>{candidate_verdict}</td></tr>".format(
                point=cell(row["point"]),
                name=cell(row["name"]),
                public=public_cells,
                candidate=cell(row["candidate"]),
                candidate_gate=cell(row["candidate_gate"]),
                candidate_verdict=cell(row["candidate_verdict"]),
            )
        )

    diff_rows = "".join(diff_row(row) for row in rows)
    public_header = "<th>Public vs oracle</th><th>Gate</th><th></th>" if include_public else ""
    public_line = f"Public {html.escape(PUBLIC)} model {html.escape(PUBLIC_MODEL)}<br>\n" if include_public else ""
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
<title>ICON-D2 surface regression {status}</title>
<style>
body {{ font: 15px/1.4 sans-serif; margin: 2rem; }}
.fail {{ color: #9b1c1c; }}
.pass {{ color: #146c43; }}
table {{ border-collapse: collapse; margin: 1rem 0; }}
td, th {{ border: 1px solid #ccc; padding: 0.3rem 0.6rem; text-align: left; }}
</style>
</head>
<body>
<h1 class="{status}">ICON-D2 surface regression: {status}</h1>
<p>Generated {html.escape(generated["at"])}</p>
<p>{public_line}Oracle {html.escape(ORACLE)} model {html.escape(ORACLE_MODEL)}<br>
Candidate {html.escape(CANDIDATE)} model {html.escape(CANDIDATE_MODEL)}</p>
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
<tr><th>Place</th><th>Variable</th>{public_header}<th>Candidate vs oracle</th><th>Gate</th><th></th></tr>
{diff_rows}
</table>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(page)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", default=PUBLIC)
    parser.add_argument("--oracle", default=ORACLE)
    parser.add_argument("--candidate", default=CANDIDATE)
    parser.add_argument("--report", default=REPORT_PATH)
    parser.add_argument("--skip-public", action="store_true", help="Compare only the oracle and the candidate")
    args = parser.parse_args()
    include_public = not args.skip_public

    failures = []
    notes = []
    rows = []
    lakes = []
    hour_lines = []
    asked_public = public_names()

    for point in POINTS:
        label = point["name"]
        print(label)
        pub_status, pub_body, pub_url = (None, {}, None)
        if include_public:
            pub_status, pub_body, pub_url = query(args.public, PUBLIC_MODEL, point, asked_public)
            print(" ", pub_status, pub_url)
        ora_status, ora_body, ora_url = query(args.oracle, ORACLE_MODEL, point, SURFACE)
        cand_status, cand_body, cand_url = query(args.candidate, CANDIDATE_MODEL, point, SURFACE)
        print(" ", ora_status, ora_url)
        print(" ", cand_status, cand_url)
        hosts = [
            ("oracle", ora_status, ora_body, SURFACE),
            ("candidate", cand_status, cand_body, SURFACE),
        ]
        if include_public:
            hosts.insert(0, ("public", pub_status, pub_body, asked_public))
        skipped = False
        for where, status, body, names in hosts:
            if status != 200 or not isinstance(body.get("hourly"), dict):
                reason = body.get("reason", "") if isinstance(body, dict) else ""
                fail(failures, f"{label} {where} HTTP {status}: {str(reason)[:240]}")
                skipped = True
        if skipped:
            continue

        if include_public:
            check_series(failures, notes, f"{label} public", asked_public, pub_body["hourly"])
            check_units(failures, f"{label} public", pub_body.get("hourly_units", {}))
        check_series(failures, notes, f"{label} oracle", SURFACE, ora_body["hourly"])
        check_series(failures, notes, f"{label} candidate", SURFACE, cand_body["hourly"])
        check_units(failures, f"{label} oracle", ora_body.get("hourly_units", {}))
        check_units(failures, f"{label} candidate", cand_body.get("hourly_units", {}))
        if point["lake"]:
            check_lake(failures, label, cand_body)
            model_values = finite(cand_body["hourly"].get("model_elevation", []))
            lakes.append({
                "name": label,
                "candidate": cand_body.get("elevation"),
                "model": model_values[0] if model_values else None,
                "oracle": ora_body.get("elevation"),
            })

        pub_times = pub_body["hourly"].get("time", []) if include_public else []
        ora_times = ora_body["hourly"].get("time", [])
        cand_times = cand_body["hourly"].get("time", [])
        public_common = shared_times(pub_times, ora_times) if include_public else []
        candidate_common = shared_times(cand_times, ora_times)
        if include_public:
            hour_lines.append(
                f"{label}: public {', '.join(public_common) if public_common else 'none'}; "
                f"candidate {', '.join(candidate_common) if candidate_common else 'none'}"
            )
            if not public_common:
                fail(failures, f"{label} no overlapping public and oracle hours")
        else:
            hour_lines.append(f"{label}: {', '.join(candidate_common) if candidate_common else 'none'}")
        if not candidate_common:
            fail(failures, f"{label} no overlapping candidate and oracle hours")

        for name in SURFACE:
            public_diff, public_gate_text, public_verdict = "", "", ""
            if include_public and name not in PUBLIC_OMIT and public_common and name in pub_body["hourly"] and name in ora_body["hourly"]:
                public_diff, public_gate_text, public_verdict = compare(
                    failures, f"{label} public", name,
                    pub_times, pub_body["hourly"][name],
                    ora_times, ora_body["hourly"][name],
                    public_gate,
                )
            candidate_diff, candidate_gate_text, candidate_verdict = "", "", ""
            if candidate_common and name in cand_body["hourly"] and name in ora_body["hourly"]:
                candidate_diff, candidate_gate_text, candidate_verdict = compare(
                    failures, f"{label} candidate", name,
                    cand_times, cand_body["hourly"][name],
                    ora_times, ora_body["hourly"][name],
                    candidate_gate,
                )
            rows.append({
                "point": label,
                "name": name,
                "public": public_diff,
                "public_gate": public_gate_text,
                "public_verdict": public_verdict,
                "candidate": candidate_diff,
                "candidate_gate": candidate_gate_text,
                "candidate_verdict": candidate_verdict,
            })

    ok = not failures
    try:
        render(args.report, ok, failures, notes, rows, lakes, {
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "hours": hour_lines,
        }, include_public)
    except OSError as error:
        print(f"FAIL could not write {args.report}: {error}", file=sys.stderr)
        return 1
    print(REPORT_URL)
    print("PASS" if ok else f"FAIL {len(failures)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
