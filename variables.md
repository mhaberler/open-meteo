# ICON variables: `heidiVars` vs upstream `main`

Comparison of the local `--group heidiVars` download set with the ICON variables stored by [open-meteo/open-meteo](https://github.com/open-meteo/open-meteo) branch `main`.

| side | commit | date |
|---|---|---|
| this checkout (`install-note`) | `892cc80b` | 2026-09-30 |
| upstream `main` | `290493ff` (`#2181`) | 2026-10-06 |

Upstream `main` has no `heidiVars` group. Its ICON downloader (`Sources/App/Icon/DownloadIconCommand.swift`) stores three groups:

- `--group surface` — every `IconSurfaceVariable` whose DWD category is single-level or soil-level (48 enum cases, 9 of them model-level and therefore excluded here).
- `--group modelLevel` — the 9 height-specific winds and temperatures (80 m / 120 m / 180 m), read from model levels.
- `--group pressureLevel` — five fields on every published pressure level.
- `--group all` — surface plus pressure levels. Model-level heights are included because they are `IconSurfaceVariable` cases.

`heidiVars` is a fixed list of 31 `IconSurfaceVariable` cases (`DownloadIconCommand.VariableGroup.heidiVars`). The same list is used for `icon`, `icon-eu`, and `icon-d2`. A variable DWD does not publish for a domain is skipped when `getVarAndLevel` returns nil.

## Surface variables in `heidiVars` and absent from upstream

Three `heidiVars` surface variables are absent from upstream `main`'s `IconSurfaceVariable`:

| open-meteo name | DWD GRIB | domains |
|---|---|---|
| `cloud_base` | `ceiling` | icon-eu, icon-d2 |
| `surface_pressure_model` | `ps` | icon, icon-eu, icon-d2 |
| `model_elevation` | `hsurf` | icon, icon-eu, icon-d2 |

The other 28 names in the `heidiVars` list are already cases on upstream `main`. `surface_pressure_model` and `model_elevation` are also excluded from this tree's `--group surface` and `--group all` via `heidiVarsOnly`. How each one is stored is in [Only in `heidiVars`](#only-in-heidivars).

## Counts

“Persisted” excludes `snowfall_convective_water_equivalent`, which both trees download and then merge into `snowfall_water_equivalent` without writing its own file. `model_elevation` is counted as persisted: it is written once per run from `HSURF`, outside the per-hour GRIB path.

| domain | heidiVars downloaded | heidiVars persisted | main `--group surface` persisted | main `--group modelLevel` | main pressure-level fields | main `--group all` persisted |
|---|---:|---:|---:|---:|---:|---:|
| icon | 26 | 25 | 33 | 9 | 90 (18 levels × 5) | 132 |
| icon-eu | 30 | 29 | 36 | 9 | 85 (17 × 5) | 130 |
| icon-d2 | 31 | 30 | 38 | 9 | 55 (11 × 5) | 102 |

Pressure levels on both trees (`Icon.swift`):

- icon: 30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000 hPa
- icon-eu: same set without 30 hPa
- icon-d2: 200, 250, 300, 400, 500, 600, 700, 850, 950, 975, 1000 hPa

Pressure variable types, identical on both trees: `temperature`, `wind_u_component`, `wind_v_component`, `geopotential_height`, `relative_humidity`.

Both trees also write a static, sea-masked `HSURF` elevation file before the run (`convertSurfaceElevation`). That file backs the API `elevation` field. It is separate from the `model_elevation` time series below.

## Shared surface variables

These 28 names are in `heidiVars` and in upstream `IconSurfaceVariable`. DWD short names are from `IconSurfaceVariable.getVarAndLevel`. A blank cell means DWD does not publish that field for the domain, on either tree.

| open-meteo | DWD | icon | icon-eu | icon-d2 |
|---|---|---|---|---|
| `temperature_2m` | `t_2m` | yes | yes | yes |
| `relative_humidity_2m` | `relhum_2m` | yes | yes | yes |
| `pressure_msl` | `pmsl` | yes | yes | yes |
| `wind_u_component_10m` | `u_10m` | yes | yes | yes |
| `wind_v_component_10m` | `v_10m` | yes | yes | yes |
| `wind_gusts_10m` | `vmax_10m` | yes | yes | yes |
| `precipitation` | `tot_prec` | yes | yes | yes |
| `rain` | `rain_gsp` | yes | yes | yes |
| `showers` | `rain_con` | yes | yes | yes |
| `snowfall_water_equivalent` | `snow_gsp` | yes | yes | yes |
| `snowfall_convective_water_equivalent` | `snow_con` | downloaded, merged | downloaded, merged | downloaded, merged |
| `weather_code` | `ww` | yes | yes | yes |
| `cloud_cover` | `clct` | yes | yes | yes |
| `cloud_cover_low` | `clcl` | yes | yes | yes |
| `cloud_cover_mid` | `clcm` | yes | yes | yes |
| `cloud_cover_high` | `clch` | yes | yes | yes |
| `convective_cloud_base` | `hbas_con` (`hbas_sc` on icon-d2) | yes | yes | yes |
| `convective_cloud_top` | `htop_con` (`htop_sc` on icon-d2) | yes | yes | yes |
| `freezing_level_height` | `hzerocl` | yes | yes | yes |
| `cape` | `cape_ml` | yes | yes | yes |
| `soil_temperature_0cm` | `t_so` level 0 | yes | yes | yes |
| `soil_temperature_6cm` | `t_so` level 6 | yes | yes | yes |
| `soil_temperature_18cm` | `t_so` level 18 | yes | yes | yes |
| `soil_temperature_54cm` | `t_so` level 54 | yes | yes | yes |
| `visibility` | `vis` | | yes | yes |
| `snowfall_height` | `snowlmt` | | yes | yes |
| `convective_inhibition` | `cin_ml` | | yes | yes |
| `lightning_potential` | `lpi` | | | yes |

`snowfall_height` is in the list because ingest uses it to correct `weather_code` and to split rain from snow. Without it those fields would follow the temperature-only fallback and diverge from a full surface run.

## Only in `heidiVars`

These three cases exist on this checkout and are absent from upstream `IconSurfaceVariable` (`main` has 48 surface cases; this tree has 51). `surface_pressure_model` and `model_elevation` are in `VariableGroup.heidiVarsOnly`, so `--group surface`, `--group all`, and `--group surfaceAndPressure` skip them here as well.

| open-meteo | DWD | icon | icon-eu | icon-d2 | how it is stored |
|---|---|---|---|---|---|
| `cloud_base` | `ceiling` | | yes | yes | per-hour GRIB, metres above MSL |
| `surface_pressure_model` | `ps` | yes | yes | yes | per-hour GRIB, hPa, valid at model orography |
| `model_elevation` | `hsurf` | yes | yes | yes | one `HSURF` fetch per run, copied to every timestep, sea points left at ~0 m |

`surface_pressure_model` is DWD surface pressure. The API name `surface_pressure` remains the derived reduction of `pressure_msl` with `temperature_2m` and the requested `elevation`. `model_elevation` is the unmasked orography. The static `elevation` field stays the sea-masked `HSURF` (-999 over open water).

`getVarAndLevel` returns nil for `surface_pressure_model` on `icon-eps`, `icon-eu-eps`, and `icon-d2-eps`, because those domains already fetch `ps` under the `pressure_msl` name.

## On main, absent from `heidiVars`

### Surface group (11)

Upstream `--group surface` stores these. `heidiVars` does not download them, so the derived API names that read them are empty on a heidiVars-only archive.

| open-meteo | DWD | icon | icon-eu | icon-d2 |
|---|---|---|---|---|
| `soil_moisture_0_to_1cm` | `w_so` level 0 | yes | yes | yes |
| `soil_moisture_1_to_3cm` | `w_so` level 1 | yes | yes | yes |
| `soil_moisture_3_to_9cm` | `w_so` level 3 | yes | yes | yes |
| `soil_moisture_9_to_27cm` | `w_so` level 9 | yes | yes | yes |
| `soil_moisture_27_to_81cm` | `w_so` level 27 | yes | yes | yes |
| `snow_depth` | `h_snow` | yes | yes | yes |
| `sensible_heat_flux` | `ashfl_s` | yes | yes | yes |
| `latent_heat_flux` | `alhfl_s` | yes | yes | yes |
| `direct_radiation` | `aswdir_s` | yes | yes | yes |
| `diffuse_radiation` | `aswdifd_s` | yes | yes | yes |
| `updraft` | `w_ctmax` | | | yes |

### Model-level heights (9)

Upstream `--group modelLevel` (and `--group all`) stores these from model levels. They are single fields at fixed heights, separate from the full-column `hiresTemp` group on this checkout, which upstream `main` does not have.

| open-meteo | DWD | level index |
|---|---|---|
| `wind_u_component_80m` / `wind_v_component_80m` / `temperature_80m` | `u` / `v` / `t` | `nFull - 2` |
| `wind_u_component_120m` / `wind_v_component_120m` / `temperature_120m` | `u` / `v` / `t` | `nFull - 3` |
| `wind_u_component_180m` / `wind_v_component_180m` / `temperature_180m` | `u` / `v` / `t` | `nFull - 4` |

`nFull` is 120 (icon), 74 (icon-eu), 65 (icon-d2).

### Pressure levels

Every pressure level listed above, for all five pressure variable types. `heidiVars` downloads none of them.

## Derived names a heidiVars archive can still serve

`IconReader` computes these from variables `heidiVars` already stores. No extra GRIB is required. Legacy aliases (`dewpoint_2m`, `windspeed_10m`, `weathercode`, `cloudcover`, …) follow the same inputs.

| API name | reads |
|---|---|
| `dew_point_2m` | `temperature_2m`, `relative_humidity_2m` |
| `wet_bulb_temperature_2m` | `temperature_2m`, `relative_humidity_2m` |
| `vapour_pressure_deficit` | `temperature_2m`, `relative_humidity_2m` |
| `wind_speed_10m`, `wind_direction_10m` | `wind_u_component_10m`, `wind_v_component_10m` |
| `snowfall` | `snowfall_water_equivalent` (convective part already merged at ingest) |
| `surface_pressure` | `pressure_msl`, `temperature_2m`, requested elevation |
| `surface_temperature` | `soil_temperature_0cm` |
| `is_day` | sun position only |

These derived names stay unavailable on a heidiVars-only archive, because their inputs are in the main-only table above:

- radiation family: `shortwave_radiation`, instants, `direct_normal_irradiance`, `global_tilted_irradiance`, `sunshine_duration`, and `apparent_temperature` (it needs shortwave radiation)
- `evapotranspiration` (`latent_heat_flux`), `et0_fao_evapotranspiration` (also needs shortwave radiation)
- `snow_height` (`snow_depth`)
- soil-moisture aliases `soil_moisture_0_1cm` … `soil_moisture_27_81cm`
- winds at 80 / 100 / 120 / 180 / 200 m
- pressure-level wind, dew point, and cloud cover

## `static/hhl.om`

`static/hhl.om` is a static half-level height file, not an `IconSurfaceVariable` and not part of the `heidiVars` list. Upstream `main` has no `hhl` code and no such file. This checkout writes it from `DownloadIconCommand.convertHhlHeights`, which `run` calls on every ICON download, including `--group heidiVars`, immediately after the sea-masked elevation file. If the file already exists, that call returns without downloading again.

DWD publishes `HHL` as one time-invariant GRIB per half level. The converter stacks those into one 3D file per domain, `[ny, nx, nHalf]` with the level axis last, stored as 32-bit `pfor_delta2d` at 1 m resolution:

| domain | file | half levels |
|---|---|---:|
| icon | `dwd_icon/static/hhl.om` | 121 |
| icon-eu | `dwd_icon_eu/static/hhl.om` | 75 |
| icon-d2 | `dwd_icon_d2/static/hhl.om` | 66 |

The forecast API reads that column for four hourly names, `hourly=<name>_level<N>`, with level 1 at the model top. The value is constant across the requested time range (the same static height repeated once per timestep), in metres. A missing file throws for these four names.

| hourly name | value | levels |
|---|---|---|
| `height_levelN` | full-level height above sea level, the average of the two enclosing half levels | 1…120 icon, 1…74 icon-eu, 1…65 icon-d2 |
| `height_agl_levelN` | that height minus the model surface elevation | same |
| `height_half_levelN` | half-level height above sea level, the stored `HHL` value | one extra level (the surface) |
| `height_half_agl_levelN` | that half-level height above the model surface | same |

Temperature, wind, humidity, and pressure on `_levelN` come from their own forecast files. No `heidiVars` surface variable reads `hhl.om`. Upstream `main` has neither the file nor these four API names.

## Model-level variables ingested by `hiresTemp`

`--group hiresTemp` downloads the native model-level column. Upstream `main` has no such group: its `--group modelLevel` is the nine fixed-height surface fields in the table above (80 m / 120 m / 180 m). Level numbers are DWD-native, 1 at the model top and the highest index nearest the surface. The hourly API name is `<variable>_level<N>`.

Eight fields are stored on every full level. Vertical wind is stored on half levels (one more than the full-level count, the extra level being the surface).

| API name | DWD | levels | unit stored |
|---|---|---|---|
| `wind_u_component_levelN` | `u` | full | m/s |
| `wind_v_component_levelN` | `v` | full | m/s |
| `temperature_levelN` | `t` | full | °C |
| `specific_humidity_levelN` | `qv` | full | g/kg |
| `pressure_levelN` | `p` | full | hPa |
| `cloud_water_levelN` | `qc` | full | g/kg |
| `cloud_ice_levelN` | `qi` | full | g/kg |
| `cloud_cover_levelN` | `clc` | full | % |
| `wind_w_levelN` | `w` | half | m/s |

`cloud_cover` on global ICON is published only for levels 39…120 (82 of 120). Levels 1…38 are skipped before download. icon-eu and icon-d2 publish `clc` on every full level.

| domain | full levels | half levels (`wind_w`) | fields written |
|---|---:|---:|---:|
| icon | 120 | 121 | 1043 |
| icon-eu | 74 | 75 | 667 |
| icon-d2 | 65 | 66 | 586 |

The icon count is `7 × 120 + 82 + 121`. icon-eu is `8 × 74 + 75`. icon-d2 is `8 × 65 + 66`.

These names are computed on read from the ingested fields and from `static/hhl.om`. They have no GRIB of their own:

| API name | reads |
|---|---|
| `relative_humidity_levelN` | `specific_humidity_levelN`, `temperature_levelN`, `pressure_levelN` |
| `dew_point_levelN` | `temperature_levelN`, `relative_humidity_levelN` |
| `wind_speed_levelN`, `wind_direction_levelN` | `wind_u_component_levelN`, `wind_v_component_levelN` |
| `height_levelN`, `height_agl_levelN` | `static/hhl.om` |
| `height_half_levelN`, `height_half_agl_levelN` | `static/hhl.om` |

## Elevation correction and native model levels

`GenericReader.scale` adjusts any Celsius variable whose `isElevationCorrectable` flag is true by 0.65 °C per 100 m between the model-grid elevation and the requested elevation. Upstream `main` turns that flag on for the fixed-height fields it reads off model levels: `temperature_80m`, `temperature_120m`, and `temperature_180m`. Those three flags are unchanged on this checkout, so those names are still corrected.

Native `temperature_levelN` does not get that adjustment. A model level already sits at a geometric height from `static/hhl.om`; shifting it again by the surface-elevation difference would move the level off the surface the model computed. `IconModelLevelVariable.isElevationCorrectable` has been `false` since the type was added. No later commit removed an enabled correction.

| commit | date | what it did |
|---|---|---|
| `4aa5b17f` | 2026-07-07 | `feat(icon): model-level height variable (height_levelN / height_agl_levelN)`. Creates `IconModelLevelVariable` with `isElevationCorrectable == false`. |
| `f9b5ca72` | 2026-07-07 | `feat(icon): download + serve native model-level u/v/t/qv/p with derived relative humidity`. Adds `temperature_levelN` and leaves the flag false, so the lapse correction does not run. |

The same `false` line was copied onto rebases that are not in this branch: `2179f698`, `61ff84eb`, `d1920db8`, and `33ec3f5e`.

`50a343bb` (`feat(api): add DEM_DOWNSCALING=false`, 2026-08-18) is a separate switch. It stops the server from filling in a DEM90 elevation and then applying terrain-based cell selection and the same lapse correction. An explicit numeric `elevation=` parameter is still honored. That flag is instance-wide. It does not change `isElevationCorrectable` on the model-level variables.

## icon-d2 15-minute files

The icon-d2 downloader also writes `icon-d2-15min` for the short allow-list in `getVarAndLevel`. Of the `heidiVars` set, that allow-list keeps `precipitation`, `rain`, `cape`, `lightning_potential`, `snowfall_height`, `snowfall_water_equivalent`, and `freezing_level_height`. Soil temperature, 2 m temperature, humidity, wind, clouds, and pressure stay on the hourly icon-d2 grid. Upstream `main` uses the same 15-minute allow-list; its extra surface fields `direct_radiation` and `diffuse_radiation` are on that grid as well.
