# heidiVars ICON download group

A curated, lightweight `--group` selector for the ICON downloader
(`Sources/App/Icon/DownloadIconCommand.swift`), added alongside the existing
`hiresTemp` (full model-level profile) group. Where `hiresTemp` downloads the
full 3D wind/temperature/humidity/cloud profile stack across every model
level, `heidiVars` downloads a fixed set of everyday 2D surface/near-surface
fields — a lighter-weight alternative to `--group surface` (which pulls all
~35 `IconSurfaceVariable` cases).

## Variables

Requested: `wind_gusts_10m, visibility, pressure_msl, weather_code,
precipitation, rain, showers, snowfall, temperature_2m,
relative_humidity_2m, dewpoint_2m, surface_pressure,
wet_bulb_temperature_2m, cape, lightning_potential,
convective_cloud_base, convective_cloud_top`.

All of these already existed as downloadable `IconSurfaceVariable` cases
with DWD GRIB mappings — no new variables were invented. The group downloads
15 raw variables:

```swift
case .heidiVars:
    let vars: [IconSurfaceVariable] = [
        .wind_gusts_10m, .visibility, .pressure_msl, .weather_code,
        .precipitation, .rain, .showers,
        .snowfall_water_equivalent, .snowfall_convective_water_equivalent,
        .temperature_2m, .relative_humidity_2m,
        .cape, .lightning_potential,
        .convective_cloud_base, .convective_cloud_top
    ]
    return vars
```

Two nuances baked into that list:

- **`dewpoint_2m`, `surface_pressure`, `wet_bulb_temperature_2m` are omitted
  on purpose.** They're derived on read in `IconReader.swift` from
  `temperature_2m` + `relative_humidity_2m` (+ `pressure_msl` for
  `surface_pressure`), all of which are already in the list — so they
  become queryable automatically with no extra download.
- **`snowfall_convective_water_equivalent` is included even though it's
  never persisted to disk.** `DownloadIconCommand.swift` merges it into
  `snowfall_water_equivalent` at ingest time and explicitly skips writing it
  separately. It still has to be downloaded, or the derived `snowfall`
  value would silently miss the convective contribution.
- No `--update-meta` flag is needed for this group: `temperature_2m`,
  `precipitation`, and `pressure_msl` are already in the marker-variable
  list (`GenericVariableHandle.swift:56`) that triggers `meta.json` writes
  automatically.

## Storage, relative to `hiresTemp`

Both groups share the same chunking/compression/retention machinery, so
file count is the reliable comparison:

| Domain | grid points | `hiresTemp` files (8×full + half) | `heidiVars` files | ratio |
|---|---|---|---|---|
| icon-d2 | 906,390 | 586 | 15 | **2.6%** |
| icon-eu | 904,689 | 667 | 15 | **2.3%** |
| icon (global) | 4,148,639 | 1,081 | 15 | **1.4%** |

i.e. `heidiVars` adds roughly 1.5–2.5% of the disk footprint the
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

Implemented in commit `21ba9716` (`feat(icon): add heidiVars curated
surface variable download group`) on branch `heidivars`. Deployed via
`build/deploy-release.sh` — confirmed the running `/usr/local/bin/openmeteo-api`
binary matches the current release build and HEAD commit (md5 `ff82bc4d`).
