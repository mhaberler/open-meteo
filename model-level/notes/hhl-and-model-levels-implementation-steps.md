# HHL Ingest + Model-Level Variables Implementation Log

This document chronicles the steps, decisions, and changes from the initial HHL (half-level heights) 3D static ingest through the addition of physical model-level variables (u/v, temperature, pressure, humidity) and related CLI/API support. It builds on the original plan in `notes/plan-hhl-ingest-and-serve.md` and `notes/ALTITUDE.md`.

All work is on the `hhl-ingest` branch (and follow-on Grok-assisted refinements).

## Phase 0: Context & Planning (pre-HHL code)
- DWD ICON uses terrain-following SLEVE hybrid levels (Lorenz staggering: half-levels for HHL/w, full-levels for t/u/v/q).
- Standard zero-topo heights in `icon_database_main.pdf` (Appendix A). Actual heights require HHL(x) - HSURF(x) (half) or averages (full).
- Prior state: only HSURF (elevation) ingested as 2D static. No HHL. Legacy "model level" hacks in surface vars for 80m/120m/180m/5500m winds/temps (mapped to specific full levels via `getVarAndLevel` + "model-level" GRIB cat).
- Model-level variable rollout planned (ADR placeholder, `untracked/plan.md` item 6 deferred HHL).
- Proposal for high-res short-term vertical profiles (hires-wind-proposal.md): focus surface-to-FL180 (~30 levels on D2), U/V + ideally T/RH/P/geopot. Limited lookahead to keep data volume manageable.
- `getDownloadForecastSteps` already existed (hardcoded per-domain/run); no `--max-forecast-hour` on ICON download (unlike GFS/ECMWF/etc.).

## Phase 1: HHL 3D Static Ingest (core feat: eddde0eb + follow-ups)
**Goal**: One `static/hhl.om` per domain, shape `[ny, nx, nHalfLevels]` (level last for column contiguity), chunks `[y, x, nlev]`.

- Added to `IconDomains` (Icon.swift):
  - `numberOfModelHalfLevels` (full+1).
  - `hhlFileOm: .staticFile(..., "hhl", nil)`.
  - `hiresTempBelowFL180StartLevel` (later).
- `GenericDomain.swift`, `GenericReader.swift`: `case .hhl` in `getStaticFile` / `ReaderStaticVariable`.
- New `convertHhlHeights(application, domain, run)` (DownloadIconCommand.swift, modeled on `convertSurfaceElevation`):
  - Idempotent early-exit if `hhl.om` exists.
  - Per-half-level GRIB download (loop 1...nHalf).
  - Domain-specific naming: `hhlVar = (d2/eu-eps/eps) ? "hhl" : "HHL"`.
  - Level part: d2 `_000_N`, else `_N`.
  - URL: `.../hhl/..._time-invariant_..._N_... .grib2.bz2` (cdo remap).
  - Stack 2D arrays into `[Float]` of size ny*nx*nlev in [ny,nx,nlev] layout (spatial-major, level innermost).
  - Single `writeOmFile(..., dimensions: [ny,nx,nlev], chunks: [chunkY,chunkX,nlev], compression: .pfor_delta2d, scalefactor:1, createNetCdf:false)`.
  - 32-bit pfor (int16 would overflow global ~75km levels) — later fix commit.
  - Log "Converting HHL for X (will download N files)", "HHL downloaded K/N".
- Called unconditionally after `convertSurfaceElevation` in download run (for any group).
- Gridable.swift: `readColumnFromStaticFile(gridpoint: Int, file: OmFileReaderArrayProtocol<Float>) -> [Float]` (infers nlev from dim[2]; reads [y..y+1, x..x+1, 0..nlev]; fallback for 2D).
- IconReader.swift:
  - `hhlColumnASL() async -> [Float]`: reads via `domain.grid.readColumnFromStaticFile` from `domain.getStaticFile(.hhl)`, pad/truncate to nlev.
  - `fullLevelHeightASL(fullLevel: Int) -> Float?`: avg of hhl[full-1] + hhl[full].
  - `fullLevelHeightAGL(fullLevel)`: ASL - max(0, surface elev).
  - `IconMixer` forwards for ensembles.
- Tests: `Tests/AppTests/IconHhlTests.swift` (network-free regression for column + averaging).
- Fixes:
  - d2 HHL: use regular-lat-lon (not forced icosahedral) — matches hsurf weights.
  - Write as 32-bit pfor.
  - Docs updates (ALTITUDE.md mark ingested; plan-hhl status).
- HHL download triggered on any `download icon*` (even minimal groups); produces ~12-45MB files (D2/EU/global).

## Phase 2: Model-Level Heights API (height_levelN)
**Goal**: Expose computed `height_levelN` / `height_agl_levelN` (ASL/AGL) using HHL, without storing per-level files.

- `IconModelLevelVariableType`: enum `height`, `height_agl`.
- `IconModelLevelVariable` (implements `ModelLevelVariableRespresentable`, `IconVariableDownloadable`):
  - `rawValue` → `height_levelN` (via protocol extension in PressureVariableRespresentable.swift).
  - `getVarAndLevel` → nil (never from GRIB; static-derived).
  - `omFileName` placeholder.
  - No multiplyAdd, etc.
- Typealias `IconVariable = SurfacePressureAndHeightVariable<Surface, Pressure, IconModelLevelVariable>` (3rd arm).
- `ForecastModelLevelVariableType` + `ForecastHeightOrModelLevelVariable` (in VariableHourly.swift) for generic query parsing (`_levelN` unambiguous, tried before `_Nm` heights).
- IconReader:
  - In `get(raw:)`: special-case `if case let .height(modelLevel) = raw` → switch on `.height` / `.height_agl` → constant series from fullLevelHeight* (no prefetch).
  - Prefetch: skip for `.height` (computed).
- API: `Reader.variableFromString` + deriver paths now resolve via rawValue.
- FBs: placeholder `.geopotentialHeight` (model levels not fully modelled in SDK yet; JSON/CSV work).
- Docs + tests updated.
- Backfill note: legacy 80m/120m/etc. heights can now use the helpers (near-term).

## Phase 3: Physical Model-Level Vars (u/v/t/p/qv/rh on native levels)
**Motivation**: User request to download raw model-level winds (lower 10 on d2) instead of fixed-height mapped (80m/120m/180m etc.). "Forget about" the mapped; focus native full levels. Enables full vertical profiles + pairs with `height_levelN`.

- Extended `IconModelLevelVariableType`: added `wind_u_component`, `wind_v_component`, `temperature`, `specific_humidity`, `pressure`, `relative_humidity`.
- In `IconModelLevelVariable`:
  - `getVarAndLevel`: 
    - winds: ("u"/"v", "model-level", level)
    - temp: ("t", ...)
    - specific: ("qv", ...)
    - pressure: ("p", ...)  [fixed from "pres"; d2 uses lowercase p, global uppercases filename via existing logic]
    - relative: nil (derived)
  - `multiplyAdd`: temp (K→C), specific (×1000 → g/kg), pressure (/100 → hPa).
  - scalefactor/unit/interp: appropriate (e.g. rh .percentage, hermite 0-100; specific 1000; winds like surface 10/hermite).
- Download:
  - `onlyVariables` parser: try `IconModelLevelVariable(rawValue)` first (skip heights), then pressure/surface.
  - `--group modelLevel`: now builds `IconModelLevelVariable` list for u/v + t + specific + p across levels (reversed, or limited for below-FL180 variants). (Originally only pulled mapped surface vars.)
  - `hiresTemp*` groups added (see below).
- Reader (IconReader.get/prefetch):
  - Only skip prefetch / special-case constant for computed `.height`/`.height_agl`.
  - Physical fall through to `reader.get(variable: .height(IconModelLevel...))` (resolves to "xxx_levelN" .om files).
  - New: `relative_humidity` case → fetch specific_humidity_level + temperature_level + pressure_level at same level/time → `Meteorology.specificToRelativeHumidity(...)` → return as .percentage. (Also prefetch the three deps.)
- FBs meta: extended `ForecastHeightOrModelLevelVariable` + `IconModelLevelVariable` conformance (winds→U/VComponent, temp→temperature, specific/rh→relativeHumidity, pressure→surfacePressure as placeholder; full model-level FBs not modelled yet).
- VariableHourly.swift: extended `ForecastModelLevelVariableType` with the physical cases (rawValue parsing works).
- IconVariableDownloadable.swift: no changes needed (physical now use the model-level struct).
- GRIB availability: d2 provides qv/t/u/v/p (model-level cat); relhum not direct (hence derivation). Pres name is "p" (confirmed via curl patterns + successful downloads).
- `specific_humidity_levelN` stores raw qv (g/kg); `relative_humidity_levelN` derived on read (no extra storage).

## Phase 4: Named Groups for Hires Profiles (hires-temp etc.)
- `VariableGroup` enum: added `hiresTemp = "hires-temp"`, `hiresTempBelowFL180 = "hires-temp-below-fl180"`, `hiresTempAllLevels = "hires-temp-all-levels"`.
- `realm` updated to return "model-level" for them (and modelLevel).
- Logic:
  - `hiresTemp` / `hiresTempBelowFL180` / (modelLevel alias): levels from `domain.hiresTempBelowFL180StartLevel ... n` (D2=28 (~5.4km), EU=47, global=93; ~30-40 levels on D2 matching proposal).
  - `hiresTempAllLevels`: 1...n full.
- Added `hiresTempBelowFL180StartLevel` to `IconDomains` (Icon.swift).
- Comment updated in group switch.
- `modelLevel` kept as legacy alias (now points to below-FL180 practical set).
- Matches proposal: focused surface-to-FL180 profile (u/v + T + P + RH) for short-term vertical use (balloon/flight). All-levels for full.

## Phase 5: --max-forecast-hour N (limit future steps)
- Added to `DownloadIconCommand.Signature` (and passed to `downloadIcon`).
- In `downloadIcon`: 
  ```swift
  var forecastSteps = domain.getDownloadForecastSteps(run: run.hour)
  if let maxForecastHour { forecastSteps = forecastSteps.filter { $0 <= maxForecastHour } }
  let timestamps = forecastSteps.map { ... }
  ```
- Affects all groups/vars (including hires model levels + 15min d2 path). Consistent with other downloaders (GFS etc.).
- Enables practical short-term hires ingest (e.g. `--group hires-temp --max-forecast-hour 12`) without editing `getDownloadForecastSteps`.
- No change to HHL/static (run-invariant).

## Other / Supporting Changes & Fixes
- `Icon.swift`: `numberOfModelFullLevels` + half; start levels for hires; region/grid updates incidental.
- `IconVariable.swift` / Downloadable: legacy mapped 80m etc. kept (for compat); their getVarAndLevel still point to model-level GRIBs.
- PressureVariableRespresentable: `ModelLevelVariableRespresentable` protocol + rawValue parsing (handles `foo_levelN`).
- Generic reader/controller paths: now support the new arm for model-level physicals + heights.
- Tests/docs: HHL regression, ALTITUDE.md, plan-hhl updated with status/risks (e.g. no native relhum on model-level for D2; p vs pres naming; FBs limitations).
- Build/CI incidental (Docker, etc. from earlier thread, but core is Swift changes).
- Availability notes: Model-level GRIBs have delay (hence separate group historically); some vars (p) less consistent across domains/runs.
- Future-proof: RH derivation + height helpers ready for more model-level vars (e.g. clouds, w).

## Current State (post --max-forecast-hour)
- `download icon-d2 --group hires-temp --max-forecast-hour 12` (or `modelLevel`) pulls exactly the requested profile vars (u/v/t/qv/p) for relevant lower levels + derives RH.
- HHL always populated on first download for domain.
- Full vertical + heights queryable.
- Limited lookahead prevents data bloat for short-term use cases.
- Backwards: old groups, mapped surface vars, pressure levels unchanged.

## Open / Next (from plan + new)
- Full FBs modelling for model-level (variable + level index, not just geo placeholder).
- Daily/agg for model-level vars.
- Expose more model-level physicals if needed (e.g. vertical vel, clouds).
- Per-domain availability guards for p/relhum if 404s common.
- CLI/docs examples for hires + max-forecast (cronjobs.md, downloading-datasets.md).
- Possibly deprecate/rename modelLevel in favor of hires-temp* (or keep both).
- Network-free tests for physical model levels (similar to HHL tests).
- Update `getDownloadForecastSteps` callers/docs if max becomes primary.

References: `notes/plan-hhl-ingest-and-serve.md`, `notes/ALTITUDE.md`, `untracked/icon_database_main.pdf`, `untracked/hires-wind-proposal.md`, relevant .swift files (Icon*, DownloadIconCommand, VariableHourly, FlatBuffers+..., Gridable, etc.).

This log was prepared from git history (eddde0eb HHL start onward), code inspection, and session changes.
