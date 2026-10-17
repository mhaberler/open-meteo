#!/usr/bin/env python3
"""Check model-level API contracts against a server.

Default host is https://open-meteo.wetterheidi.de (regular lat-lon). To test a native
server, pass --host and --model, e.g.
    icon_model_level_regression.py --host http://127.0.0.1:8080 --model icon_d2=dwd_icon_d2_native

Heights are a property of the grid and should match within 1 m. Thermodynamic
profiles are only compared when the runs look like the same one. The domain
string in the response is not part of the contract.
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_HOST = "https://open-meteo.wetterheidi.de"
HOST = DEFAULT_HOST + "/v1/forecast"
POINTS = [
    # icon_d2, Munich. Host elevation 531 m. Lowest full level is 10 m AGL.
    {"domain": "icon_d2", "latitude": 48.14, "longitude": 11.58, "elevation": 531, "full": 65, "top_height": None},
    # icon_eu. Top and lowest full level are checked; elevation comes back from the host.
    {"domain": "icon_eu", "latitude": 48.14, "longitude": 11.58, "elevation": None, "full": 74, "top_height": 22433.50},
]


def get(params):
    url = HOST + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            payload = response.read().decode()
            status = response.status
    except urllib.error.HTTPError as error:
        payload = error.read().decode()
        status = error.code
    try:
        body = json.loads(payload)
    except json.JSONDecodeError:
        body = {"reason": payload}
    return status, body, payload, url


def fail(message):
    print("FAIL", message)
    return 1


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default=DEFAULT_HOST, help="Base URL without /v1/forecast")
    parser.add_argument(
        "--model", action="append", default=[], metavar="POINT=MODEL",
        help="Replace the models= value for a point, e.g. icon_d2=dwd_icon_d2_native. Repeatable.",
    )
    parser.add_argument("--only", action="append", default=[], help="Run only these points (icon_d2, icon_eu)")
    return parser.parse_args()


def main():
    global HOST
    args = parse_args()
    HOST = args.host.rstrip("/") + "/v1/forecast"
    models = dict(item.split("=", 1) for item in args.model)
    errors = 0
    for point in POINTS:
        if args.only and point["domain"] not in args.only:
            continue
        model = models.get(point["domain"], point["domain"])
        hourly = ",".join([
            f"height_agl_level{point['full']}",
            "height_level1",
            f"temperature_level{point['full']}",
            f"specific_humidity_level{point['full']}",
            f"wind_w_level{point['full'] + 1}",
        ])
        params = {
            "latitude": point["latitude"],
            "longitude": point["longitude"],
            "hourly": hourly,
            "models": model,
            "windspeed_unit": "ms",
            "forecast_days": 1,
        }
        if point["elevation"] is not None:
            params["elevation"] = point["elevation"]
        status, body, payload, url = get(params)
        print(point["domain"], status, url)
        if status != 200:
            errors += fail(f"{point['domain']} profile request {status}: {body.get('reason')}")
            continue
        hourly_body = body.get("hourly", {})
        units = body.get("hourly_units", {})
        agl = hourly_body.get(f"height_agl_level{point['full']}", [None])[0]
        if agl is None or abs(agl - 10.0) > 1.0:
            errors += fail(f"{point['domain']} height_agl_level{point['full']}={agl}, expected 10 m")
        if point["top_height"] is not None:
            top = hourly_body.get("height_level1", [None])[0]
            if top is None or abs(top - point["top_height"]) > 1.0:
                errors += fail(f"{point['domain']} height_level1={top}, expected {point['top_height']}")
        wind = f"wind_w_level{point['full'] + 1}"
        if units.get(wind) != "m/s":
            errors += fail(f"{point['domain']} {wind} unit {units.get(wind)}")
        qv_name = f'"specific_humidity_level{point["full"]}":['
        if qv_name not in payload:
            errors += fail(f"{point['domain']} missing specific humidity")
        else:
            snippet = payload.split(qv_name, 1)[1].split("]", 1)[0]
            first = snippet.split(",")[0]
            decimals = first.split(".")[-1] if "." in first else ""
            if len(decimals) < 5:
                errors += fail(f"{point['domain']} qv decimals {first}")
        bad = dict(params)
        bad["hourly"] = f"temperature_level{point['full'] + 1}"
        bad_status, bad_body, _, _ = get(bad)
        reason = bad_body.get("reason", "")
        if f"1...{point['full']}" not in reason:
            errors += fail(f"{point['domain']} level {point['full'] + 1} status {bad_status} did not report 1...{point['full']}: {reason}")
    return errors


if __name__ == "__main__":
    sys.exit(main())
