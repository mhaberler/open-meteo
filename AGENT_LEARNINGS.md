# Agent learnings

Human-facing layout is in `MODELLEVELS.md`. This file is the decisions and traps that are easy to undo.

## 2026-10-16 — native ICON model levels on `redo-modellevels`

Branch is a port onto `upstream-1.7.0` native grids (`65c6a804`). Do not rebase `modellevel-cand`. The live oracle is HTTP `https://open-meteo.wetterheidi.de`, which is ahead of local `modellevel-cand` tip `cbb1d375`. That host is regular lat-lon, so temperatures at the same lat/lon will not match a native server. Heights should, within 1 m.

### Placement the user settled

- No third domain. Parent native domain holds surface, pressure levels, `heidiVars`, `hhl.om`, masked HSURF, and `HSURF_raw`. The existing `_native_model_level` sibling holds both the 80/120/180 m fields and the full column.
- `--group modelLevel` keeps its 1.7.0 meaning: surface variables whose DWD category is `model-level` (u/v/t at 80, 120, 180 m). Store them. The user cancelled the idea of serving those names as a read of levels `N−2`/`N−3`/`N−4` and dropping the second store.
- `heidiVars` has realm `"heidi"` on the parent. With realm nil it overwrote the surface job's `<time>.om` and `latest.json` for the same run (D2 surface :44, heidiVars :45).
- Sibling realm for `modelLevel` stays nil, so the file is `latest.json`. `VariableGroup.realm` returns `"model-level"` for that group and is passed only to the parent writer. Pass `siblingRealm` (`"hires-temp"` for `hiresTemp`, otherwise nil) to the sibling writer. Two writers with realm nil overwrite `latest.json` and the spatial file.
- Cron targets the parent (`icon-d2-native`, `icon-eu-native`, `icon-native`). The sibling CLI name rejects anything but `--group modelLevel` (`DownloadIconCommand`, the `modelLevelParent` guard).
- `--max-forecast-hour` is an optional `Int` and keeps a step when `leadHours <=` the value, so 24 includes hour 24. Only the global cron lines pass it (`24`). Do not put `144` on EU. Uncapped lengths come from `getDownloadForecastSteps`: EU 120 h on 00/06/12/18 and 30 h on the side runs, global 120 h on 06/18 and 180 h on 00/12.
- Diverted variables (`IconModelLevelVariable(rawValue:)` matches both the 80/120/180 names and `<var>_levelN`) go to the sibling and must return before the remapper. Copying them into regular `dwd_icon` was rejected. No column on EPS or `icon-d2-native-15min`.
- `finalise()` writes nothing when a writer has zero handles, so an empty parent writer during a sibling-only group is safe.
- `--update-meta` is gone. Upstream `#2241` writes `static/meta.json` for every time-series convert with `writeUpdateJson`, so a `hiresTemp` run no longer needs a flag to pass the old surface-variable allow-list. `static/meta.json` is still separate from `data_spatial/latest_*.json`. Realm does not replace it.
- `convert` ignores its domain argument and groups handles by `handle.domain`. `hiresTemp` handles are the sibling, so that job advances the sibling meta. `heidiVars` advances the parent. A pressure-only ensemble download sets `writeUpdateJson` false so it does not replace the surface run's meta. `data_end_time` is exclusive: start of the last timestep plus `dtSeconds`. Deployed crons must drop `--update-meta`; ArgumentParser rejects the unknown flag.
- Download deadline stays hard-coded: 2 h for D2, 5 h otherwise. The user dropped `--connections-per-host`, `--deadline-hours`, and putting the Curl URL on retry logs.

### Reader

- There is no `IconReader.swift` on 1.7.0. Reads go through `GenericReader` and `VariableHourlyDeriver`.
- `DerivedMapping` closures are synchronous. The HHL read is async, so height cannot be a deriver closure. Derivation is in `IconModelLevelReader.get()`.
- An overload of `makeDerivedHourly` on `IconNativeDomain` is not called through `any GenericDomain`. The intercept is in `DomainReaderMapping.Source.makeReader`, comparing the metatype to `IconModelLevelVariable.self`.
- `GenericReaderCached` wraps `GenericReader` only. `VariableHourlyDeriver` accepts any `GenericReaderProtocol`, so the model-level reader is passed in directly.
- A missing time-series file reads back as NaN, it does not throw. `GenericReaderMulti` walks readers from last to first and stops when the series has no NaN. The sibling is listed after the parent, so a finite sibling series wins.
- `getDeriverMap` for `temperature_80m` / `120m` / `180m` aliases to 100/150/200 m for every reader. The stored files are used only when `Reader.MixingVar.self == IconModelLevelVariable.self`. Wind 80/120/180 m already prefers `wind_u_component_80m` when that raw name exists. The parent `IconSurfaceVariable` has those names, so the parent attempts the read, gets NaN, and the sibling fills it.
- `HeightVariableRespresentable` formats raw values as `<name>_<metres>m`. `<var>_levelN` needs `ForecastHeightVariable.modelLevel` and `init?(rawValue:)` / `rawValue` on the struct itself. A protocol-extension default stays the witness if the type only adds the method in an extension.
- Full-level height ASL is the mean of half levels `N` and `N+1` (`hs[fullLevel - 1]` and `hs[fullLevel]`). Half-level count is `N+1`.
- `hhl.om` is `[ny, nx, nHalf]`, level last. Native grids have `ny = 1` and `nx = pointCount`. Compression is `.pfor_delta2d` (32-bit). Global tops near 75 km overflow int16. Download HHL with v1 `getGribUrl` (`("HHL", "model-level", level)`), not the old v0 CDO path from `fix-timeouts`.
- Only `--group hiresTemp` with a sibling downloads HHL. DWD v1 EPS feeds have HHL only on the lowest levels (icon-eps 99–121, icon-eu-eps 72–75, icon-d2-eps 56–66), and Curl retries a 404 until the deadline. `writeOmFile(file:)` traps on an existing file, so `hhl.om` and `HSURF_raw` are checked again just before writing.
- AGL heights subtract the last HHL half level (HSURF), not `reader.modelElevation`, which is −999 masked and NaN off-grid.
- Out-of-range levels throw `IconModelLevelError` with `1...N` in the description. The wetterheidi host returns that sentence as plain text with HTTP 200, and its domain string is `icon-d2-15min`. Lock the range. Leave the domain string as whatever `IconNativeDomain` raw value the server actually is.
- `wind_w` uses `.metrePerSecondNotUnitConverted`, so `windspeed_unit` does not touch it. Default wind speed for the other wind fields is km/h.
- Specific humidity, cloud water, and cloud ice set `omFileCompression` to `.pfor_delta2d_int16_logarithmic`. `compression(or:)` keeps a caller-supplied compression when the variable is still the default int16, because GloFas passes logarithmic for a whole `convert()` call.
- JSON/CSV/XLSX use `SiUnit.apiSignificantDigits` (5 for `.gramPerKilogram`). `json.loads` drops a trailing zero, so a regression against the host has to look at the raw JSON (`7.50550`), not the parsed float.
- FlatBuffers has `undefined = 0` and no model-level field. Every `_levelN` name maps to `.undefined`, including `temperature_level65`; `altitude: level` made it read as 65 m. `surface_pressure_model` and `model_elevation` are also `.undefined`. JSON and CSV are the API.
- `pressure_levelN` uses logarithmic int16 with scalefactor 10000. Linear 0.1 hPa stored global upper levels as 0.

### Surface and static files

- `heidiVars` is the 31-name `heidiSurface` set, the same list on every domain. `getVarAndLevel` returning nil is what skips unpublished fields. `heidiVarsOnly` is only `model_elevation` and `surface_pressure_model`, and those two are filtered out of `all`, `surface`, and `surfaceAndPressure`.
- `VIS` is not in the DWD v1 feed, so `visibility.getVarAndLevel` is nil on every domain. Downloadable heidi counts are 25 global, 28 EU, 29 D2. The fork's 29/30 assumed VIS was published.
- `cloud_base` is DWD `CEILING`, EU and D2 only. Global `clc` levels below `cloudCoverMinimumModelLevel` (39 global, 1 otherwise) are skipped for every hour inside `skipHour`.
- `model_elevation` returns nil from `getVarAndLevel` and is written each hour from `HSURF_raw`. `surface_pressure_model` is `PS` in hPa. On EPS domains the early switch hits `default: return nil` before the main mapping, which keeps it from downloading `PS` a second time under `pressure_msl`.
- `convertSurfaceElevation` returns when the masked file and `HSURF_raw` already exist. It does not delete them. The `FR_LAKE` mask applies only after those files are removed, on the parent and the remapped `dwd_icon` copy.
- The mask is `DownloadIconCommand.maskOpenSea`. Open sea is −999 when `FR_LAND + FR_LAKE < 0.5`. Exactly 0.5 keeps HSURF. `IconLakeElevationTests` covers that without GRIB. On a live lake, `elevation` equals `model_elevation` and `height_agl` of the lowest full level is about 10 m. Elevation 0 with a raw HSURF near 580 m would be the mask. A native nearest cell tens of metres off the lat-lon cell or off DEM90 is a different grid point, not a failed mask (Starnberger See 47.86N 11.29E: native 614 m, wetterheidi 584 m, DEM90 637 m).
- `DEM_DOWNSCALING` defaults to on. `false` makes an omitted `elevation` store `.nan` and skip DEM90, terrain matching, and the lapse in `GenericReader.scale`. The query call site passes `nil` when the parameter is omitted. A default argument of `.nan` is `Optional.some`, so it does not take that path. An explicit numeric `elevation=` still corrects. The switch is process-wide.

### Build and tests

- `swift build` inside the sandbox fails reading `.git/hooks` in `.build/checkouts` (EROFS, code 30). Rebuild with permissions that disable the sandbox.
- `swift test --filter 'IconHhlTests|SiUnitTests|IconLakeElevationTests'` is the local check. `scripts/icon_model_level_regression.py` is the host check. `--host` and `--model icon_d2=dwd_icon_d2_native` point it at a native server. HHL fixtures in tests are `ny = 1`.
- `#expect(optionalFloat == (22000 + 19402) / 2)` fails although the arithmetic is exact: against `Float?` the literal expression is not typed as `Float`. Write the expected value as `Float(20701)`.
- Compare a native server to wetterheidi with `cell_selection=nearest`, `start_date`/`end_date` (those reject `forecast_days`), and `windspeed_unit=ms`. Local model name is `dwd_icon_d2_native`; the oracle is `icon_d2`. Pin `elevation=` for a tight temperature check. wetterheidi parses `model_elevation` and `_levelN` on `/v1/dwd-icon`. `snowfall_convective_water_equivalent` is not a `VariableHourly` case; one unknown name makes the whole hourly list HTTP 400. This host sets `DEM_DOWNSCALING=false`, so the returned elevation is the model cell.
- The ingest chart tails a log from the end when the file already exists at startup, because backfill has read it. A log created after startup, such as `/open-meteo-next/log/icon-d2_heidivars.log`, has to be read from the first byte or that finished run never becomes a bar.
- A missing native domain currently answers HTTP 500 `Something went wrong.`, not a clean missing-domain error. The 2026-10-16 note that EU and D2 had both finished was early: only `dwd_icon_d2_native` and its sibling were on disk, both meta files on the 21:00 UTC run. Do not treat one finished log as both domains.
