# heidiVars ICON download group

A curated, lightweight `--group` selector for the ICON downloader
(`Sources/App/Icon/DownloadIconCommand.swift`), added alongside the existing
`hiresTemp` (full model-level profile) group. Where `hiresTemp` downloads the
full 3D wind/temperature/humidity/cloud profile stack across every model
level, `heidiVars` downloads a fixed set of everyday 2D surface/near-surface
fields — a lighter-weight alternative to `--group surface` (which pulls all
~35 `IconSurfaceVariable` cases).

## Variables

The group downloads 27 raw variables:

```swift
case .heidiVars:
    let vars: [IconSurfaceVariable] = [
        .wind_gusts_10m, .wind_u_component_10m, .wind_v_component_10m,
        .visibility, .pressure_msl, .surface_pressure_model, .model_elevation,
        .weather_code,
        .precipitation, .rain, .showers,
        .snowfall_water_equivalent, .snowfall_convective_water_equivalent,
        .snowfall_height,
        .temperature_2m, .relative_humidity_2m,
        .cloud_cover, .cloud_cover_low, .cloud_cover_mid, .cloud_cover_high,
        .cloud_base, .freezing_level_height,
        .cape, .convective_inhibition, .lightning_potential,
        .convective_cloud_base, .convective_cloud_top
    ]
    return vars
```

Only `cloud_base` (DWD `CEILING`) had to be added to `IconSurfaceVariable` for
the first batch; everything else already existed as a downloadable case with
a DWD GRIB mapping. The DWD → open-meteo names for the second batch are:

| DWD GRIB | open-meteo name | domains |
|---|---|---|
| `HZEROCL` | `freezing_level_height` | icon, icon-eu, icon-d2 |
| `CLCT` / `CLCL` / `CLCM` / `CLCH` | `cloud_cover` / `_low` / `_mid` / `_high` | all |
| `U_10M` / `V_10M` | `wind_u_component_10m` / `wind_v_component_10m` | all |
| `CIN_ML` | `convective_inhibition` | icon-eu, icon-d2 |
| `CEILING` | `cloud_base` | icon-eu, icon-d2 |
| `SNOWLMT` | `snowfall_height` | icon-eu, icon-d2 |

A third batch adds raw model surface pressure and orography, both new
`IconSurfaceVariable` cases:

| DWD GRIB | open-meteo name | domains | how it's fetched |
|---|---|---|---|
| `PS` | `surface_pressure_model` | icon, icon-eu, icon-d2 | generic per-hour path, same as `pressure_msl` |
| `HSURF` | `model_elevation` | icon, icon-eu, icon-d2 | once per run, see below |

Nuances baked into that list:

- **`dewpoint_2m`, `wet_bulb_temperature_2m` are omitted on purpose.**
  They're derived on read in `IconReader.swift` from `temperature_2m` +
  `relative_humidity_2m`, both already in the list, so they become
  queryable automatically with no extra download. The same holds for
  `wind_speed_10m` / `wind_direction_10m`, derived from the u/v components.
- **`surface_pressure_model` sits alongside the existing derived
  `surface_pressure`, it does not replace it.** `surface_pressure` (see
  `IconReader.swift`) is a barometric reduction of `pressure_msl` using
  `temperature_2m` and the *requested* `elevation=` parameter — it follows
  the caller anywhere on the grid cell's vertical column. `surface_pressure_model`
  is DWD's raw `PS`, valid only at the model's own orography, and
  `isElevationCorrectable == false`, so `elevation=` has no effect on it.
  Over steep terrain (e.g. the Alps) the two diverge measurably; see
  `examples/heidivars.py` for a live comparison. Which one should be the
  API's default `surface_pressure` is an open question — not resolved by
  this change.
- **`model_elevation` is the *unmasked* counterpart to the static `elevation`
  API field, not a duplicate of it.** `convertSurfaceElevation` already runs
  before every group and writes a static, sea-masked (-999) HSURF file that
  backs the response's `elevation` scalar. `model_elevation` is a genuine
  per-forecast-hour time series built from a **second**, independent HSURF
  download (`DownloadIconCommand.downloadHsurfRaw`, shared by both call
  sites) that is *not* sea-masked — open sea reads as the model's true
  orography (~0 m), not -999. The two fields intentionally disagree over
  water. HSURF itself doesn't vary by forecast hour, so the fetch happens
  once per run and the same array is written into every timestep.
- **`snowfall_height` is included even though it is rarely queried directly.**
  The ingest uses it to correct DWD weather codes and to split rain from snow
  (the `weather_code` / `rain` / `snowfall_water_equivalent` post-processing
  blocks in `DownloadIconCommand.swift`). Without it those corrections
  silently fall back to a temperature-only rule, and the group's
  `weather_code`, `rain` and `snowfall` would disagree with a full
  `--group surface` run.
- **The list is domain-independent.** `cloud_base`, `convective_inhibition`,
  `snowfall_height`, `visibility` and `lightning_potential` are not published
  for every domain; `getVarAndLevel` returns nil there and the download is
  skipped silently, so nothing 404-loops. `surface_pressure_model` (`ps`) and
  `model_elevation` (`hsurf`), by contrast, are published for all three
  deterministic domains.
- **`surface_pressure_model` and `model_elevation` are excluded from
  `--group all` / `surface` / `surfaceAndPressure`** via
  `VariableGroup.heidiVarsOnly` — reachable only through `--group heidiVars`.
  `model_elevation` is a constant field, odd to write into a routine
  `--group surface` run; `surface_pressure_model` stays opt-in until its
  accuracy is measured (see above).
- **Neither is fetched on the EPS domains** (`icon-eps`, `icon-eu-eps`,
  `icon-d2-eps`). `pressure_msl` already downloads the identical `ps` GRIB
  under its own name there (`getVarAndLevel`'s EPS branch), so a separate
  `surface_pressure_model` fetch would duplicate that download under two
  variable names; `model_elevation` was simply never extended to those
  domains.
- **`snowfall_convective_water_equivalent` is included even though it's
  never persisted to disk.** `DownloadIconCommand.swift` merges it into
  `snowfall_water_equivalent` at ingest time and explicitly skips writing it
  separately. It still has to be downloaded, or the derived `snowfall`
  value would silently miss the convective contribution.
- No `--update-meta` flag is needed for this group: `temperature_2m`,
  `precipitation`, and `pressure_msl` are already in the marker-variable
  list (`GenericVariableHandle.swift:56`) that triggers `meta.json` writes
  automatically.
- **`format=flatbuffers` cannot represent `surface_pressure_model` or
  `model_elevation`.** The external `sdk` package's `openmeteo_sdk_Variable`
  enum has no member for either (`surfacePressure` is already taken by the
  derived variable), so both map to `.undefined` in
  `FlatBuffers+WeatherApi.swift`. JSON and CSV are unaffected. Fixing this
  needs an upstream SDK change, out of scope here.

### `cloud_base` semantics

Two consumer-visible properties, both verified against live DWD GRIB rather
than assumed:

- **Metres above MSL, not above ground.** Compared point-by-point against
  `HSURF` over all 525,072 valid icosahedral cells, `CEILING − HSURF` is never
  negative (min +9.8 m, 1st percentile +562 m) across terrain reaching 4080 m.
  It is published raw and uncorrected, consistent with MeteoSwiss's
  `cloud_base` (also `CEILING`) and with ICON's own `convective_cloud_base`
  (`HBAS_CON`/`HBAS_SC`, also MSL). Note that UKMO's `cloud_base` is AGL —
  that cross-model inconsistency pre-dates this group.
- **Clear sky is a large value, not null.** DWD does *not* mark "no ceiling"
  as missing: where `CLCT == 0` the field is filled with the top of the scan
  range (5th percentile 16,000 m, median 16,164 m over 358k clear points on
  the icon-d2 grid) and is never bitmap-missing there. So a
  `cloud_base < threshold` test behaves correctly with no special casing.
  The GRIB2 bitmap (16.7% of the regular-lat-lon grid) only masks
  out-of-domain points — `CLCT` carries the identical mask — and is left as
  NaN like every other field.

## Storage, relative to `hiresTemp`

Both groups share the same chunking/compression/retention machinery, so
file count is the reliable comparison. Of the 27 raw variables,
`snowfall_convective_water_equivalent` is merged rather than written on every
domain (−1); `model_elevation`, despite bypassing the generic per-hour GRIB
path, is written like any other field and persists everywhere (HSURF is
published on all three deterministic domains):

| Domain | grid points | `hiresTemp` files (8×full + half) | `heidiVars` files | ratio |
|---|---|---|---|---|
| icon-d2 | 906,390 | 586 | 26 | **4.4%** |
| icon-eu | 904,689 | 667 | 25 | **3.7%** |
| icon (global) | 4,148,639 | 1,081 | 21 | **1.9%** |

i.e. `heidiVars` adds roughly 2–4% of the disk footprint the
model-level (`hiresTemp`) work already added, per domain.

## Proposed crontab entries

Not yet applied to `/etc/cron.d/openmeteo-api`. Mirrors the existing
`hiresTemp` entries' domains/hours, offset a few minutes earlier (surface
fields tend to publish on DWD's server before the full model-level stack):

```cron
# icon-d2 heidiVars - lightweight surface set (~2.5% of model-level size)
45 0,3,6,9,12,15,18,21 * * * openmeteo-api  /usr/local/bin/openmeteo-api download icon-d2  --group heidiVars --concurrent 12 > $DATA_DIRECTORY/log/icon-d2_heidivars.log 2>&1 || cat $DATA_DIRECTORY/log/icon-d2_heidivars.log

# icon-eu heidiVars - lightweight surface set
40 2,5,8,11,14,17,20,23  * * *  openmeteo-api  /usr/local/bin/openmeteo-api download icon-eu  --group heidiVars --concurrent 12  > $DATA_DIRECTORY/log/icon-eu_heidivars.log 2>&1

# icon global heidiVars - lightweight surface set (disabled, matches icon global hiresTemp being disabled)
#50  2,8,14,20  * * * openmeteo-api /usr/local/bin/openmeteo-api download icon --group heidiVars --concurrent 12 >> ${DATA_DIRECTORY}log/icon_heidivars.log 2>&1
```

No `--max-forecast-hour` cap proposed (cheap enough to take each domain's
natural forecast range); the existing 6-day `find -mtime +6 -delete`
cleanup already covers these new chunk files.

## Manual ingest (icon-d2)

```bash
sudo -u openmeteo-api bash -c 'DATA_DIRECTORY=/open-meteo/ /usr/local/bin/openmeteo-api download icon-d2 --group heidiVars --concurrent 12 > /open-meteo/log/icon-d2_heidivars.log 2>&1'
```

- `DATA_DIRECTORY=/open-meteo/` is required — the app defaults to `./data/`
  (`configure.swift:14`) when unset. Cron sets it implicitly at the file
  level; an ad-hoc `sudo` shell does not inherit that, so it must be passed
  explicitly. Files land under `/open-meteo/dwd_icon_d2/` (`dwd_icon_d2`
  is the fixed on-disk name for the `icon-d2` domain, `DomainRegistry.swift:87`).
  - `bash -c '...'` wrapper makes the env assignment apply reliably
  regardless of sudoers' env-passthrough policy.
- `sudo -u openmeteo-api` matches the cron job's user, so file ownership on
  the new chunks matches everything else already on disk.

## Deployment

Originally implemented in commit `21ba9716` (`feat(icon): add heidiVars curated
surface variable download group`) on branch `heidivars`, with 15 variables.
Deployed via `build/deploy-release.sh` — confirmed the running
`/usr/local/bin/openmeteo-api` binary matches the current release build and
HEAD commit (md5 `ff82bc4d`).

The second batch (`HZEROCL`, `CEILING`, `CLCT`/`CLCL`/`CLCM`/`CLCH`,
`U_10M`/`V_10M`, `CIN_ML`, plus `SNOWLMT`) brought the group to 25 variables.

The third batch (`PS` → `surface_pressure_model`, `HSURF` → `model_elevation`)
brings the group to 27 variables and is **not deployed yet** — the release
binary still has to be rebuilt and rolled out before the crontab entries
above start picking these up. Unlike the first two batches, this one is
explicitly not meant to change what `--group surface` or `--group all`
write (see `VariableGroup.heidiVarsOnly`), and `surface_pressure_model` is
deliberately additive rather than a replacement for the existing derived
`surface_pressure` — see the "Variables" section above before wiring either
into anything that assumes `surface_pressure` is the only pressure field.
