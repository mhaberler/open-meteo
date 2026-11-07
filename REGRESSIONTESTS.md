# ICON-D2 native regression

Compare ingested ICON-D2 on the native host with the lat-lon host. EU and global stay out until they are ingested. The script is `scripts/icon_d2_native_regression.py`.

`scripts/icon_model_level_regression.py` is a separate contract check on `/v1/forecast`. It does not do this comparison.

## Hosts and query

| | Candidate | Oracle |
|---|---|---|
| Host | `https://open-meteo-next.mah.priv.at` | `https://open-meteo.wetterheidi.de` |
| Model | `dwd_icon_d2_native` | `icon_d2` |

Both requests go to `/v1/dwd-icon` with `forecast_hours=6`, `elevation=nan`, `windspeed_unit=ms`, and `cell_selection=nearest`. One request per point carries the surface names and the profile sample together. One unknown hourly name makes the whole list HTTP 400, so `snowfall_convective_water_equivalent` is omitted: it is ingest-only and not a `VariableHourly` case.

The candidate runs with `DEM_DOWNSCALING=false`, so the returned elevation is the model cell.

## What is allowed to differ

The native nearest cell and the lat-lon nearest cell are different points. Elevations are recorded and are not required to match. The lake points are places where both nearest cells share the lake HSURF, so a shoreline cell does not trip the pressure gates. Starnberger See at 47.86N, 11.29E is that shoreline case (native 614 m, wetterheidi 584 m, about 3.5 hPa) and is not a test point.

Heights above ground are a property of the column. The lowest full level stays near 10 m AGL on both hosts.

## Points

Munich 48.14, 11.58 and Zugspitze 47.42, 10.98 are ordinary land points. Starnberger See 47.88, 11.31, Ammersee 47.99, 11.12, and Chiemsee 47.88, 12.45 are the lake mask. On the candidate only, `elevation` must equal `model_elevation` within 0.5 m and both must be above 50 m. The oracle elevation is recorded.

## Names

The default surface list is the heidi surface set without `snowfall_convective_water_equivalent`: gusts and 10 m wind components, `visibility`, `pressure_msl`, `surface_pressure_model`, `model_elevation`, `weather_code`, precipitation, rain, showers, snowfall water equivalent and height, 2 m temperature and humidity, soil temperature at 0, 6, 18, and 54 cm, cloud cover and its three layers, `cloud_base`, `freezing_level_height`, CAPE, CIN, lightning potential, and convective cloud base and top.

`--surface` also requests the names a full `--group surface` download stores and the wetterheidi archive does not: five soil-moisture layers, `snow_depth`, both heat fluxes, `direct_radiation`, `diffuse_radiation`, and `updraft`. Those series must be present and finite on both hosts, with no numeric gate. On the current oracle they are all null, so that run fails. `snowfall_convective_water_equivalent` stays out of both lists. The 80/120/180 m fields stay out; they are `--group modelLevel`.

The profile sample is full levels 1, 30, and 65 for temperature, u, v, specific humidity, pressure, and cloud cover; half levels 64, 65, and 66 for `wind_w` and `height_half_agl`; plus `height_agl_level65`. D2 has 65 full levels and 66 half levels.

`visibility` may be all null. It is not in the DWD v1 feed. That is a note, not a failure. Every other requested series must be present and finite on both hosts.

## Checks on each host

- Units: metres for elevation, hPa for the pressure names, m/s for the wind components and `wind_w`.
- `specific_humidity_level65` in the raw JSON has at least five digits after the decimal. Parsed floats drop a trailing zero, so the check reads the text.
- `height_agl_level65` is within 1 m of 10.
- Half-level AGL decreases toward the surface: level 64 above 65 above 66.
- On the candidate, `cloud_base` is not more than 50 m below the cell elevation, CIN is not negative, and `snowfall_height` does not exceed `freezing_level_height` when the freezing level is more than 50 m above the grid.
- On the candidate, `temperature_level66` at Munich must answer with the range text `1...65`.

## Comparison

Shared hours are the overlap of the two time axes. For each name, the report prints the maximum absolute difference on those hours. A name with no finite overlap fails, except `visibility`.

| Names | Gate |
|---|---|
| `temperature*` and `soil_temperature*` | 3 K |
| `wind_*` | 2 m/s |
| `specific_humidity*` | 2 g/kg |
| `pressure_msl`, `surface_pressure`, `surface_pressure_model`, `pressure_level*` | 2 hPa |

Other names are printed and are not gated. `model_elevation` is one of those.

## Report

Each run overwrites `/var/www/vpsmon/regression/index.html` and prints `https://vpsmon.meteo.mah.priv.at/regression/`. The page is behind the same basic auth as `/ui`. The process exits non-zero when any check fails, and it still writes the page.

```bash
python3 scripts/icon_d2_native_regression.py
python3 scripts/icon_d2_native_regression.py --surface
```

`--candidate`, `--oracle`, `--report`, and `--surface` override the defaults.

## Surface three-way

`scripts/icon_d2_surface_regression.py` compares the heidi surface names only. It does not request the column. The public host is `https://api.open-meteo.com` model `icon_d2`. The oracle and the candidate are the same hosts as above.

The public request omits `model_elevation` and `surface_pressure_model`. Either name makes that host reject the whole hourly list. Those two names are compared only between the oracle and the candidate.

Public against the oracle must agree within one stored step: temperature and soil temperature 0.1 K, wind 0.2 m/s, `pressure_msl` 0.2 hPa, precipitation, rain, showers, and snowfall water equivalent 0.2 mm, cloud cover and relative humidity 1, `weather_code` 0, `cloud_base`, `freezing_level_height`, `snowfall_height`, and the convective cloud heights 20 m, CAPE and CIN 10, `lightning_potential` 0.2. `visibility` is a note when a host is all null, and it is not a numeric failure.

The candidate against the oracle uses the gates in the comparison table above. Names without a gate, including `model_elevation`, are printed and do not fail. The candidate lake check is the same: `elevation` equals `model_elevation` within 0.5 m and both are above 50 m. The candidate is not compared with the public API.

Each run overwrites `/var/www/vpsmon/regression/surface.html` and prints `https://vpsmon.meteo.mah.priv.at/regression/surface.html`.

```bash
python3 scripts/icon_d2_surface_regression.py
python3 scripts/icon_d2_surface_regression.py --skip-public
```

`--skip-public` compares only the oracle and the candidate. `--public`, `--oracle`, `--candidate`, and `--report` override the defaults.
