# ICON native model levels

Port of the vertical ICON column onto the native grids in 1.7.0. There is no third domain. Fast surface fields stay on the parent native domain. The delayed column stays on the existing sibling (`icon-d2-native-model-level`, and the EU and global twins).

Cron targets the parent (`icon-d2-native`, `icon-eu-native`, `icon-native`). The sibling CLI name only accepts `--group modelLevel`. Nothing here is copied onto the regular lat-lon `dwd_icon` grid, the EPS domains, or `icon-d2-native-15min`.

## Where files go

| Download | Domain | Spatial index |
|---|---|---|
| `--group modelLevel` | sibling | `latest.json` (no realm) |
| `--group hiresTemp` | sibling | `latest_hires-temp.json` |
| `--group heidiVars` | parent | `latest_heidi.json` |
| surface, pressure levels | parent | parent `latest.json`, `latest_pressure-level.json` |
| `hhl.om` (first `hiresTemp` run only), masked HSURF, unmasked `HSURF_raw` | parent static | shared with the sibling via `domainRegistryStatic` |

`modelLevel` and `hiresTemp` must not share a spatial file, and neither must `heidiVars` and the parent surface job. Map layers have to read both `latest.json` and `latest_hires-temp.json`. Time-series files are per variable. `heidiVars` rewrites the same surface time series as the surface job.

Only `--group hiresTemp` on a domain with a sibling downloads `hhl.om`. EPS feeds publish HHL for the lowest levels only, and a surface job must not wait on HHL. `--group hiresTemp` on any other domain is rejected.

`--update-meta` still advances `static/meta.json`. A hires-only run has no surface marker (`temperature_2m` and the like), so meta would not move without the flag. `--max-forecast-hour` caps the lead time. The download deadline stays hard-coded (2 h for D2, 5 h otherwise).

## Cron (`/etc/cron.d/openmeteo-api`)

These lines are installed. EU and D2 `hiresTemp` and `heidiVars` run on the parent native domains. Minutes stay off the D2 surface and pressure jobs, which already run at minute 44. The regular-grid `icon-d2` and `icon-eu` lines stay commented through the rollback (30 Nov 2026). EU is not capped. A run at 00, 06, 12, or 18 goes to 120 h, and the hours in between go to 30 h. Global runs at 00, 06, 12, and 18, so its jobs are the 02, 08, 14, 20 slot. `--max-forecast-hour 24` keeps a lead hour when it is less than or equal to 24, so hour 24 is included. Without that cap, global 06 and 18 go to 120 h and 00 and 12 go to 180 h.

```cron
# icon-d2 native column -> sibling latest_hires-temp.json
53 0,3,6,9,12,15,18,21 * * * openmeteo-api nice -15 /usr/local/bin/openmeteo-api download icon-d2-native --update-meta --group hiresTemp --concurrent 12 > $DATA_DIRECTORY/log/icon-d2_model-level.log 2>&1 || cat $DATA_DIRECTORY/log/icon-d2_model-level.log

# icon-d2 native heidiVars -> parent
45 0,3,6,9,12,15,18,21 * * * openmeteo-api nice -15 /usr/local/bin/openmeteo-api download icon-d2-native --update-meta --group heidiVars --concurrent 12 > $DATA_DIRECTORY/log/icon-d2_heidivars.log 2>&1 || cat $DATA_DIRECTORY/log/icon-d2_heidivars.log

# icon-eu native column -> sibling latest_hires-temp.json
48 2,5,8,11,14,17,20,23 * * * openmeteo-api nice -17 /usr/local/bin/openmeteo-api download icon-eu-native --update-meta --group hiresTemp --concurrent 12 > $DATA_DIRECTORY/log/icon-eu_model-level.log 2>&1 || cat $DATA_DIRECTORY/log/icon-eu_model-level.log

# icon-eu native heidiVars -> parent
40 2,5,8,11,14,17,20,23 * * * openmeteo-api nice -17 /usr/local/bin/openmeteo-api download icon-eu-native --update-meta --group heidiVars --concurrent 12 > $DATA_DIRECTORY/log/icon-eu_heidivars.log 2>&1 || cat $DATA_DIRECTORY/log/icon-eu_heidivars.log

# icon global native column, first 24h -> sibling latest_hires-temp.json
41 2,8,14,20 * * * openmeteo-api nice -19 /usr/local/bin/openmeteo-api download icon-native --update-meta --group hiresTemp --max-forecast-hour 24 --concurrent 12 > $DATA_DIRECTORY/log/icon_model-level.log 2>&1 || cat $DATA_DIRECTORY/log/icon_model-level.log

# icon global native heidiVars, first 24h -> parent
36 2,8,14,20 * * * openmeteo-api nice -19 /usr/local/bin/openmeteo-api download icon-native --update-meta --group heidiVars --max-forecast-hour 24 --concurrent 12 > $DATA_DIRECTORY/log/icon_heidivars.log 2>&1 || cat $DATA_DIRECTORY/log/icon_heidivars.log
```

An existing elevation file is left in place. Delete the parent and remapped `dwd_icon` HSURF files to regenerate the sea mask. `FR_LAKE` is added to `FR_LAND` before the sea test, so lakes are not stored as −999.

## First D2 run (2026-10-16 21:00 UTC)

Parent `dwd_icon_d2_native` and sibling `dwd_icon_d2_native_model_level` `static/meta.json` share that run and the same data end, 2026-10-18 22:00 UTC. The end is exclusive: hours 0 through 48, then one step. The sibling file was written about two minutes after the parent, which is the `hiresTemp` job with `--update-meta`. That flag writes `meta.json` for each domain present in the handles. `hiresTemp` advances the sibling, `heidiVars` advances the parent. EU and global native directories were not on disk yet.

On this host `DEM_DOWNSCALING=false`, so the API elevation is the model cell, the same value as `model_elevation`. Starnberger See cells stay at HSURF (about 581–614 m) with the lowest full level 10 m above ground. A native nearest cell can sit tens of metres off the lat-lon cell and off DEM90. That is grid selection. A masked lake would report elevation 0 while `model_elevation` stayed near 580 m.

## `--group modelLevel`

Unchanged meaning: the surface variables whose DWD category is `model-level`. That is u, v, and t at 80, 120, and 180 m, which are full levels `N−2`, `N−3`, and `N−4`.

| Domain | Full levels `N` |
|---|---|
| icon (global) | 120 |
| icon-eu | 74 |
| icon-d2 | 65 |

These stay stored under their API names. On the model-level reader, `temperature_80m`, `temperature_120m`, and `temperature_180m` read those files. Other readers still alias them to 100, 150, and 200 m. The level index is not the same physical layer across D2, EU, and global, so the metre names stay for `icon_seamless`.

## `--group hiresTemp`

Stored, one file per level. Level 1 is the model top.

| Name | Levels | DWD | Notes |
|---|---|---|---|
| `wind_u_component`, `wind_v_component`, `temperature` | 1…N | U, V, T | |
| `specific_humidity`, `cloud_water`, `cloud_ice` | 1…N | QV, QC, QI | g/kg, logarithmic int16 |
| `pressure` | 1…N | P | Pa stored as hPa, logarithmic int16 (global top is about 0.02 hPa) |
| `cloud_cover` | 1…N | CLC | global levels 1–38 are not published |
| `wind_w` | 1…N+1 | W | half levels, m/s, ignores `windspeed_unit` |

Derived on read, not stored: `height`, `height_agl`, `height_half`, `height_half_agl`, `relative_humidity`, `wind_speed`, `wind_direction`, `dew_point`.

A full-level height is the mean of the enclosing half levels in `hhl.om`. AGL heights subtract the last half level, which is HSURF, not the sea-masked elevation. That file is one 3D array `[ny, nx, nHalf]` with the level last. Native grids have `ny = 1`. Compression is 32-bit `.pfor_delta2d` because global tops are near 75 km and overflow int16. A missing `hhl.om` fails the height query. A level outside `1…N` (or `1…N+1` for half levels) is rejected with that range in the message.

Specific humidity is printed with five decimals. The SDK default of two remains for other uses of g/kg.

## `--group heidiVars`

Thirty-one surface fields on the parent, the same list on every domain. A field DWD does not publish is skipped when `getVarAndLevel` returns nil (`CEILING` and several others are missing on global; `VIS` is not in the v1 feed; `LPI` is D2 only).

`model_elevation` and `surface_pressure_model` are excluded from `--group all`, `surface`, and `surfaceAndPressure`.

| Name | Meaning |
|---|---|
| `surface_pressure_model` | raw DWD `PS`, hPa, not reduced by `elevation=` |
| `model_elevation` | unmasked HSURF, written every hour from the static raw file |
| `cloud_base` | DWD `CEILING`, metres MSL, EU and D2 only |

`surface_pressure` is still the elevation-reduced field. Dew point, wet bulb, and 10 m wind speed and direction stay derived.

## Elevation correction

`DEM_DOWNSCALING=false` skips DEM90, terrain matching, and the lapse and pressure correction when the query omits `elevation`. An explicit numeric `elevation=` still applies. The default is the upstream behaviour. The switch is process-wide.

Model-level variables are not elevation-correctable.

## API names

`<var>_levelN` is parsed beside the existing fixed-height `<var>_<metres>m` names. FlatBuffers has no model-level slot, so every `_levelN` name maps to `undefined`. A level is never written as `altitude`. `surface_pressure_model` and `model_elevation` are also `undefined`. JSON and CSV keep the real names. Heights are a time series, not response metadata.

## Tests

`Tests/AppTests/IconHhlTests.swift` checks the native-grid HHL layout (`ny = 1`), the heidiVars and hiresTemp variable lists, logarithmic qv, and the out-of-range message. `Tests/AppTests/SiUnitTests.swift` checks the five-decimal specific humidity. `Tests/AppTests/IconLakeElevationTests.swift` checks `maskOpenSea` without GRIB: a lake with low `FR_LAND` keeps HSURF, the same cell becomes −999 when `FR_LAKE` is zero, and the cut is strictly below 0.5. `scripts/icon_model_level_regression.py` checks the live `https://open-meteo.wetterheidi.de` host: lowest full level near 10 m AGL, five-decimal qv, `wind_w` in m/s, and an out-of-range level reporting `1…N`. That host is the older lat-lon deployment, so temperatures at the same lat/lon will not match a native-grid server. Heights should.
