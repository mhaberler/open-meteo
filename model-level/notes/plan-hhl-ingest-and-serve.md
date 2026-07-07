# Plan: Ingest and Serve HHL (Half-Level Heights) for ICON Models

Ingest the ICON HHL (height of half levels) time-invariant GRIB data from DWD as a single 3D static OM file, provide lazy column access for per-location vertical heights, derive full-level geometric heights, and enable serving (initially for existing fixed-height variables, later for native model levels).

This fulfills the deferred item from the model-level variable plan.

## Context and Goals

From `notes/ALTITUDE.md` and `untracked/plan.md` (item 6: "HHL per-location level heights: deferred to follow-up") and the DWD ICON database reference PDF (Appendix A):

- ICON model levels are terrain-following (SLEVE). Standard height tables (A.1-A.4) are only valid for zero topography.
- Real geometric heights require the time-invariant `HHL` (height of half levels ASL) + `HSURF` (surface elevation ASL).
- Formula (per PDF):
  ```
  half_agl[k] = HHL[k] - HSURF
  full_agl[i] = (half_agl[i] + half_agl[i+1]) / 2
  ```
- Currently (as of 2026-06): open-meteo fully processes HSURF (2D static "HSURF.om", used for SLP corrections, snow/freezing adjustments, lapse-rate temp/pressure corrections, modelElevation in readers). HHL is **never** downloaded/stored/used (confirmed by greps over Sources/, data/*/static/ only contains HSURF.om + meta/cdo weights; only references in untracked/notes we created).
- DWD publishes HHL as time-invariant GRIBs under `/hhl/` (per-half-level files for global: 121 files like `icon_global_icosahedral_time-invariant_YYYYMMDDHH_<N>_HHL.grib2.bz2`; similar but adapted naming for EU/D2).
- Half-level counts (from PDF + code): global/icon/icon-eps = 121, icon-eu = 75, icon-d2 family = 66. Full levels = halfs-1 (already in `IconDomains.numberOfModelFullLevels`).
- Related: model-level variable rollout (u/v/t/p/qv + derived on native DWD full levels 1..N top-down) is in planning (`untracked/plan.md`, `docs/adr/0001-icon-model-level-naming.md`); some download group support exists in `DownloadIconCommand.swift` but full variable typing/reader exposure for `_levelN` may be partial or in-progress in this snapshot (still sees 80m/5500m hacks in `IconVariableDownloadable.swift`).
- Goal of this plan: Ingest HHL (raw ASL half-level heights) for all ICON domains (incl. EPS where grids apply), store as static data, derive/serve full-level geometric heights (ASL preferred), integrate with existing elevation/static machinery and future model-level vars. Enable accurate per-gridpoint altitudes for model levels without users needing external HHL data.

Benefits:
- Users querying model level data (or the fixed 80m/120m/180m/5500m slices) can get real `height_levelN` (or equivalent) at their location.
- Better internal corrections possible for upper-air data (lapse rates etc. referenced to actual level height).
- Fulfills the deferred item; complements ALTITUDE.md.
- Static data, low runtime cost (lazy single-column read on first height request; no preload), compressible.

Non-goals (for v1):
- Storing pre-derived full-level heights on disk (derive on read from halves; halves are native).
- AGL vs ASL choice in storage (store raw HHL=ASL; derive AGL by subtracting model surface; expose both or ASL primary).
- Raw HHL_half queries as first-class (focus on full-level heights matching the data vars).
- Historical reprocessing of old runs (HHL is time-invariant; one-time or on-next-download populate).
- Per-ensemble-member HHL (share with deterministic where grids match).

## Key Data Facts (DWD + PDF)
- HHL GRIBs: time-invariant, one (or few) 2D field per half level. Global splits into 121 individual files (`_1_HHL`, `_2_HHL`, ..., `_121_HHL` after the date). D2/EU similar with domain-specific naming and fewer levels.
- Example global URL pattern (varies by run date): `http://opendata.dwd.de/weather/nwp/icon/grib/00/hhl/icon_global_icosahedral_time-invariant_2026061300_42_HHL.grib2.bz2`
- D2 pattern (from inspection): includes `_000_<N>_hhl` (e.g. `..._2026061300_000_10_hhl.grib2.bz2`); dir `/hhl/`, lowercase in suffix for d2 family.
- EU (non-EPS): uppercase `HHL`, regular-lat-lon (matches the hsurf ternary — uppercase for icon/icon-eu, lowercase for d2/eps variants). See casing note in Ingestion section.
- Levels in GRIB filenames correspond 1:1 to half-level index 1 (top) .. N (surface).
- HHL values: geometric height ASL (incl. over ocean gridpoints where surface half-level ≈ 0). No need for sea masking (unlike the HSURF "elevation" product which sets sea=-999 for user convenience).
- File sizes: small per level (2D field); total per domain modest after OM compression.

DWD URLs follow the hsurf/ pattern but under hhl/ + per-level suffix instead of single file.

## Architecture Decisions

1. **Storage**:
   - **Single 3D static file**: `<domain>/static/hhl.om` with dimensions **`[ny, nx, nHalfLevels]`** — series (level) dimension LAST, matching the existing codebase convention (`[ny, nx, nTime]` / `[ny, nx, nMembers, nTime]` in `OmFileSplitter.swift:637`).
   - **Chunking is the critical decision**: chunk **`[y, x, nlev]`** (small spatial tile, FULL vertical column contiguous in one chunk). Do **not** chunk level-first (`[1, y, x]` would put one level per chunk → a column read touches all nlev chunks → defeats the single-I/O goal).
   - Use the existing `Array<Float>.writeOmFile(file:dimensions:chunks:...)` (supports arbitrary dims; see `OmFileWriterHelper.swift:65`).
   - In convert: collect the per-level remapped 2D arrays into one stacked `[Float]` of size `ny*nx*nlev` in `[ny, nx, nlev]` layout (spatial-major, level innermost), write **once**.
   - Why: om-file-format fully supports N-D; `read3D` (`OmFileSplitter.swift:678`) already indexes `location * nLevels + level`, i.e. level adjacent to location. One RemoteFileManager open + one chunk read for a full vertical column at a point: `read(range: [y..<y+1, x..<x+1, 0..<nlev], ...)`.
   - Add helper (next to existing `readFromStaticFile` / `readElevation` logic, e.g. in `Gridable.swift` or a new extension on OmFileReaderArrayProtocol for static vertical):
     ```swift
     func readColumnFromStaticFile(gridpoint: Int, file: any OmFileReaderArrayProtocol<Float>) async throws -> [Float]
     // For the 3D hhl.om [ny, nx, nlev] (level LAST / fastest varying):
     //   let x = gridpoint % nx, y = gridpoint / nx
     //   Use the low-level `read` (or a thin wrapper around the case-3 logic in read3D, treating the level dim as the innermost) with range [y..y+1, x..x+1, 0..<nlev] → the nlev values in one I/O.
     // Also provide an interpolated variant for fractional grid points (similar to readElevationInterpolated).
     // Note: the existing read3D paths are time-oriented; the column helper may be a small dedicated static 3D path or reuse by faking nTime=1.
     ```
   - Enum change: `case .hhl` (no `halfLevel` param). The single file reader is returned by `getStaticFile(type: .hhl)`.
   - Content: raw ASL (no -999 sea mask).  nlev matches `numberOfModelHalfLevels`.
   - For `domainRegistryStatic`: the hhl.om lives under the static domain (same as HSURF).
   - This kills the 121-file fan-out problem completely. DEM precedent was spatial *tiling of one field*; HHL is one multi-field vertical coordinate → 3D array is the natural shape.

2. **Ingestion** (modeled 1:1 on `convertSurfaceElevation`):
   - New `convertHhlHeights(application: Application, domain: IconDomains, run: Timestamp) async throws`.
   - Early exit if `static/hhl.om` exists locally (idempotent).
   - URL construction: same serverPrefix / domainPrefix / gridType / additionalTimeString as hsurf.
     - Per-domain casing exactly mirrors the existing hsurf logic (confirmed via opendata):
       ```swift
       let hhlVar = (domain == .iconD2 || domain == .iconD2Eps || domain == .iconEuEps || domain == .iconEps) ? "hhl" : "HHL"
       ```
     - For d2-family the per-file names embed `_000_<N>_<hhl>`; non-d2 use `_<N>_<HHL>`. Build accordingly (see verified patterns in the doc header).
   - Download: **loop over the per-level GRIB files** (they are published split), `msgs = try await cdo.downloadAndRemap(url)` (1 msg each).
   - Collect the 2D arrays, stack into one `[Float]` of size ny*nx*nlev in **`[ny, nx, nlev]`** layout (spatial-major, level innermost).
   - Write **once**:
     ```swift
     try stacked.writeOmFile(file: domain.hhlFileOm.getFilePath(), dimensions: [ny, nx, nlev], chunks: [y, x, nlev], ...)
     ```
     (One 3D file; full column contiguous per chunk — see Storage section for why level-last/column-contiguous.)
   - Call site unchanged (after convertSurfaceElevation).
   - Same reuse of CdoHelper, idempotency, EPS handling.
   - **Casing verification**: Confirmed from live opendata listings (2026-06 data):
     - icon / icon-eu: `..._N_HHL.grib2.bz2` (uppercase HHL)
     - icon-d2: `..._000_N_hhl.grib2.bz2` (lowercase hhl + 000 prefix)
     - Use the *exact* same domain condition as the hsurf variableName ternary for future-proofing. EU non-EPS uses uppercase (matches icon, not the EPS variants).

3. **Domain / Config** (in `Sources/App/Icon/Icon.swift` + protocol):
   - Add:
     ```swift
     var numberOfModelHalfLevels: Int {
         switch self { ... 121/75/66 as above }
     }
     // single 3D static file, no per-level chunk
     var hhlFileOm: OmFileType {
         .staticFile(domain: domainRegistryStatic ?? domainRegistry, variable: "hhl", chunk: nil)
     }
     // helper
     var isD2FamilyForFilenames: Bool { ... } // for URL construction only
     ```
   - Update comments: `/// model level standard heights, full levels (now derivable from ingested HHL half levels)`
   - Optionally: `var numberOfModelFullLevels: Int { numberOfModelHalfLevels - 1 }` (but keep explicit for now).
   - Mirror the existing `surfaceElevationFileOm` / `soilTypeFileOm` computed-property pattern in `GenericDomain` (chunk: nil single file); Icon-specific is fine since only ICON has HHL.

4. **Reader / Static Access**:
   - `enum ReaderStaticVariable`: `case .hhl` (no level param; single 3D file).
   - `getStaticFile(type: .hhl)`: returns the *one* `staticFile(..., variable: "hhl", chunk: nil)` reader. (Only this switch needs the new case; most other "getStatic" sites are thin delegators like `GenericReaderMulti.reader.first?.getStatic(...)` — no fan-out.)
   - Add helper next to `readFromStaticFile` / elevation readers:
     ```swift
     func readColumnFromStaticFile(gridpoint: Int, file: any OmFileReaderArrayProtocol<Float>) async throws -> [Float]
     // For 3D [ny, nx, nlev] file (level LAST): read full lev range at the (y,x) point in ONE I/O, e.g. range [y..y+1, x..x+1, 0..<nlev]. Also interpolated variant.
     ```
   - In `GenericReader<...>` init:
     - Do **not** preload by default.
   - Lazy load (default):
     - Add (on IconReader or via a cached column in GenericReader):
       ```swift
       private var _hhlColumn: [Float]?
       func hhlColumnASL() async throws -> [Float] {
           if let c = _hhlColumn { return c }
           guard let file = await domain.getStaticFile(type: .hhl, ...) else { return [] }
           let col = try await readColumnFromStaticFile(gridpoint: position, file: file)
           _hhlColumn = col
           return col
       }
       ```
     - Then `fullLevelHeightASL(fullLevel: Int)` does the avg from the (lazily loaded) column.
   - `getStatic(.hhl)` can be kept for compatibility or removed; the column reader is the primitive.
   - Sea / AGL handling unchanged.
   - Benefit: zero cost until a height is actually requested. Single file open + single column read.

5. **Serving / Variable Integration** (aligns with model-level plan.md):
   - Define (or extend post model-level rollout):
     - `struct IconModelLevelHeightVariable: ModelLevelVariableRespresentable, ... { let level: Int }` (full level 1..N; DWD-native numbering).
     - Or reuse/extend `IconModelLevelVariable` with a `.height` case in its Type enum (but separate struct cleaner to avoid polluting physical vars).
   - Add to `IconVariable` sum type (the SurfacePressureAndHeightVariable<...> pattern from plan): support the height var in the "height" realm.
   - `IconVariableDownloadable` conformance for height var:
     - `getVarAndLevel(...) -> ("", "", nil)` or `nil` (not sourced from model-level GRIB downloads; static).
   - In `IconReader.get(raw:)` / derived path:
     - Special case for height model-level var: compute `let h = try await fullLevelHeightASL(level: theLevel) ?? .nan`
       - Return `DataAndUnit( Array(repeating: h, count: time.count), .metre )`
     - No time interpolation needed (constant); mark scalefactor/unit appropriately.
   - Exposure in API (IconController.swift, ForecastapiController, variable lists):
     - Parse `height_level42` (and `height_level1` etc.) via the representable (add to onlyVariables path, group handling).
     - For `--group levels` (when implemented): do **not** auto-include height_* (keep byte-identical with physical-only; decision from plan.md item 8/33). Users request explicitly: `&hourly=temperature_level42,height_level42,wind_speed_level42`
     - Or: when a physical `_levelN` is requested, optionally auto-attach its height (but explicit is simpler + consistent with geopotential_height on p-levels).
   - In output writers (JsonWriter, Csv, Xlsx, FlatBuffers): height series will appear as constant values (with unit metre). Add meta if possible (e.g. "level": N, "levelType": "model").
   - Current fixed-height hacks (80m etc.): optionally backfill `height_80m` etc. as surface vars (mapping the internal model level index → compute height). Low priority; the general `_levelN` is the future.
   - Non-time-series access: heights also available via the column reader (`readColumnFromStaticFile` on the `.hhl` file) for advanced use (or future /static endpoint extension). For now, the var path is primary for forecast responses.

6. **Other Components**:
   - `OmFileType.swift`, `RemoteFileManager`: no changes (static + chunk works).
   - `Gridable.swift` / elevation readers: reuse read*Elevation* helpers; add the 3D `readColumnFromStaticFile` (single file, full column in one I/O — see Storage section).
   - Download groups / CLI (`DownloadIconCommand.swift`): heights not in physical modelLevel group. `onlyVariables` parser will pick them up if added to representable.
   - Export / copy statics (`ExportCommand.swift`, `VariablePerMemberStorage.swift` etc.): generalize any HSURF hardcodes to also handle the single `static/hhl.om` (extend "known static vars").
   - Full-run / data_run: HHL is static, not per-run (ignore in FullRunsVariables).
   - Tests: parse roundtrips for `height_level42`; reader tests for computed height vs manual avg on a fixture point; match approx standard table for flat point + topo adjustment for mountain point (use known test lat/lon).
   - FlatBuffers / SDK: best-effort (heights are metre; add level info in comments/meta).
   - Docs: 
     - Update `notes/ALTITUDE.md` (ingestion status, example queries with `height_level63`, note on ASL).
     - Update `untracked/plan.md` (mark HHL done, link this doc).
     - Possibly `docs/adr/0002-icon-hhl-heights.md` (or reuse 0001) for naming (height_levelN vs hhl_half_levelN; ASL default; why not auto-attach).
     - README / getting-started if relevant.
   - DomainRegistry / data dirs: new files under existing static/ will be picked up by sync/cron.
   - Performance: negligible (lazy single-column read once per point on first height request; heights constant so cheap fill).

## Implementation Status (as of 2026-06-14)

HHL ingestion, the reader helpers, and `height_levelN` serving over JSON/CSV are **implemented and verified end-to-end**. The sections below this one are the original design; this section is the source of truth for what actually landed and what remains.

### Commits (branch `hhl-ingest`)

| Commit | Summary |
|--------|---------|
| `eddde0e` | feat: ingest HHL as single 3D static `hhl.om` + lazy column / full-level height helpers (initial implementation) |
| `011f3fc1` | fix: d2 HHL uses `regular-lat-lon`, not the forced `icosahedral` (no remap weights for d2 → `Array2D` precondition crash) |
| `df471489` | fix: write `hhl.om` with 32-bit `.pfor_delta2d` — `.pfor_delta2d_int16` capped at 32767 m, so global levels 1–34 (33 k–75 k m) became NaN |
| `c0a5bace` | test: network-free regression for the 3D column read + level averaging (`Tests/AppTests/IconHhlTests.swift`) |
| `b51ade2e` | docs: ALTITUDE.md updated to "HHL ingested" |
| `33ec3f5e` | feat: Icon model-level variable category — `IconModelLevelVariable`, `IconVariable` → 3-arm sum, `IconReader` computes height from HHL |
| `6e5486b1` | feat: generic `ForecastVariable` model-level arm → `height_levelN` queryable over JSON/CSV |

### What works (verified live, run `2026061300`)

- **Ingestion**: `convertHhlHeights` (`DownloadIconCommand.swift`) runs after `convertSurfaceElevation`. Loops per-level GRIBs from `/hhl/`, stacks to one 3D `[ny, nx, nlev]` `hhl.om` (level-last), chunk `[chunkY, chunkX, nlev]` (full column per chunk), compression `.pfor_delta2d`, no sea mask. Idempotent on `hhl.om`.
  - On disk + dimension-verified: `icon-d2` `[746,1215,66]` (12.4 MB), `icon-eu` `[657,1377,75]` (15.2 MB), `icon` global `[1441,2879,121]` (44.8 MB). All NaN-free; tops match the DWD standard table (d2 22000 m, eu 22770 m, global 75000 m).
- **Reader**: `Gridable.readColumnFromStaticFile` (one-I/O column), lazy `IconReader.hhlColumnASL()`, `fullLevelHeightASL/AGL(fullLevel:)` (PDF averaging). Unit-tested.
- **API (JSON/CSV)**: `height_levelN` (ASL) and `height_agl_levelN` (AGL) on `/v1/forecast`, level = DWD-native full-level index (1 = top). Values cross-checked vs standard table:
  - `icon_d2` Munich: `height_level1` = 20701 m, `height_level65` = 541 m, `height_agl_level65` = **10.0 m** (exact std match).
  - `icon_global` Munich: `height_level1` = **74210.5 m** (std 74210.3).
  - Existing height-metre (`wind_speed_180m`) and pressure (`temperature_850hPa`) variables still parse — unaffected.

### Architecture as built (deviations from the original design below)

- **Generic layer was the real gate**, not Icon. `/v1/forecast` parses requests into the shared generic `ForecastVariable` (used by all models + FlatBuffers + aggregation) before any model is consulted; it had no model-level concept. Dispatch is purely by `rawValue` (`reader.get(mixed: rawValue)` → `Reader.variableFromString`), so the fix only needed the generic type to **parse + round-trip** `_levelN`.
- **3-arm height slot is now an enum**: `ForecastVariable`'s height arm changed from `ForecastHeightVariable` (struct) to `ForecastHeightOrModelLevelVariable = { height(ForecastHeightVariable) | modelLevel(ForecastModelLevelVariable) }`. The existing height-metre struct and its parsing are **unchanged** (tried as fallback after the unambiguous `_levelN`). New reusable `ModelLevelVariableRespresentable` protocol parses `<var>_level<N>` (`PressureVariableRespresentable.swift`).
- **Icon `IconVariable`** is now the 3-arm `SurfacePressureAndHeightVariable<Surface, Pressure, IconModelLevelVariable>` (mirrors UKMO/MeteoSwiss). `IconReader.get(raw:)`/`prefetchData(raw:)` intercept the `.height` (model-level) arm: compute constant series from HHL, nothing to download/prefetch.
- **Height vars are not stored or downloaded** — purely computed from the static `hhl.om`. `getVarAndLevel` → nil; `omFileName` is a never-read placeholder.

## What remains to be done

### Serving completeness (deferred by the "JSON/CSV only" decision)

- **FlatBuffers meta** for model levels is a placeholder (`ForecastHeightOrModelLevelVariable.getFlatBuffersMeta` returns `.geopotentialHeight` with no altitude). Needs a real model-level meta (variable + level index) in `FlatBufferVariable.swift` / the SDK enum, or the binary `.fbs` output mislabels `height_levelN`.
- **Daily / weekly / monthly aggregation** of model-level vars is not wired (the `ForecastVariableDaily` path). Low priority — height is constant, so aggregation is trivial but currently absent.

### Correctness / polish

- **Global `height_agl_levelN` precision**: global `height_agl_level120` returned 0.0 (expected ≈10 m). ASL is exact; AGL = full-level-ASL − HSURF, and global `HSURF.om` is remapped/masked independently from `hhl.om`, so the lowest level can round to 0. d2 AGL is exact (10.0) with identical code → global-grid artifact. **Action**: compare global `hhl.om` surface half-level (121) vs `HSURF.om` at several land points; decide whether AGL should subtract the HHL surface half-level instead of `HSURF` for self-consistency.
- **Out-of-range level**: `height_level999` returns NaN (helper returns nil → `.nan`). Acceptable, but consider rejecting at parse with a clear error.
- **Sea points**: `fullLevelHeightAGL` returns ASL when `modelElevation` is sea/no-data. Confirm desired behaviour (0 vs ASL) and test.
- **`Array2D` precondition crash** on a grid/count mismatch is a bare `precondition` in shared `downloadAndRemap`; a friendly `HHL grid mismatch for <domain>` error would aid future domain onboarding. (Mitigated now by correct `gridType`.)

### Coverage / ops

- **EPS + d2-15min domains**: `numberOfModelHalfLevels` is defined for all, and EU/global/d2 are verified, but the EPS variants (`icon-eps`, `icon-eu-eps`, `icon-d2-eps`) are not run-tested — confirm DWD publishes HHL for them and the casing branch is right.
- **Remote (`REMOTE_DATA_DIRECTORY`/S3)**: column read via `RemoteFileManager` block cache is untested for `hhl.om`; verify a pure API server fetches it on demand. Document the static-prep step in `cronjobs.md`.
- **Export / sync**: confirm static-sync picks up the single `hhl.om` (no per-level glob assumptions).
- **ADR**: `docs/adr/0001-icon-model-level-naming.md` is an empty placeholder — record the `height_levelN` / ASL-default / DWD-native-indexing naming decision (optionally a new `0002` for HHL storage).

### Future (out of scope here, enabled by this work)

- Native model-level data variables (`temperature_levelN`, `wind_speed_levelN`, …) now have a home: add cases to `IconModelLevelVariableType` + `ForecastModelLevelVariableType` and download/store the model-level GRIBs (the `modelLevel` download group already exists). `height_levelN` pairs with them directly.

## Implementation Phases (decoupled)

**Critical**: Phase 3 (general `height_levelN` for arbitrary model levels) is gated on the unfinished `_levelN` / ModelLevelVariableRespresentable work from the prior plan (still sees legacy 80m/5500m hacks in current `IconVariableDownloadable.swift`). Phases 1+2 are fully independent and can ship HHL data + queryable heights today.

1. **Domain + Ingestion + 3D write (core, shippable now)**:
   - Add `numberOfModelHalfLevels`, `hhlFileOm` (returns single 3D static "hhl", no per-level chunk).
   - Implement `convertHhlHeights` with verified URL casing (exact hsurf ternary), collect levels, **one** stacked 3D `writeOmFile` using OmFileWriterHelper + arbitrary-dim write (no 121 files).
   - Wire after convertSurfaceElevation.
   - Smoke: download icon-d2 (or small global), confirm single `static/hhl.om` with correct nlev, sensible values (use future readColumn or temporary netcdf dump).
   - Idempotent check on the hhl.om.

2. **Reader plumbing + lazy column (also independent, shippable now)**:
   - `ReaderStaticVariable`: `case .hhl`
   - `getStaticFile(.hhl)` for the single file (minimal change; most getStatic sites are delegators, only the getStaticFile exhaustive switch + core GenericReader I/O path need work).
   - Implement `readColumnFromStaticFile` (and interp version) for 3D hhl.om — full vertical in one I/O.
   - Lazy: `hhlColumnASL()` computed on first access (no preload in every init).
   - Helpers `fullLevelHeightASL(fullLevel:)` etc. (derive avg from column).
   - Test column read + derivation in isolation (no API surface yet).

3. **Serving integration (gated)**:
   - Once model-level `_levelN` infrastructure lands, add the height var support + `height_levelN` path (constant fill from the helper).
   - **Near-term win while gated**: Backfill computed heights for the *existing* fixed surface vars (80m/120m/180m/5500m). The download code already maps specific model-level indices for them (`numberOfModelFullLevels - k`). Use the new fullLevelHeight helper to expose real `height_80m` etc. (or attach in meta). This works today without new variable types.

4. **Polish**:
   - Exhaustive cases (small), sea handling, EPS, tests comparing to standard table + real topo point.
   - Docs updates (this file, ALTITUDE.md), optional small ADR.
   - Remote / missing file behavior.
   - Size: one file is even smaller win than 121.

Order lets the team populate real HHL data and have internal + fixed-height serving without waiting for the broader levelN feature. Update this plan with any deviations after implementation.

## Risks / Considerations / Open Questions
- **Filename variability**: Patterns from opendata listings (global no _000 uppercase `_N_HHL`; d2 `_000_<n>_hhl` lowercase; EU non-EPS uppercase `_N_HHL`). Casing follows the exact hsurf ternary condition. The per-domain branch in the URL builder is isolated. **Assert level count + at least the first/last filename resolve at download time** (fail loud if DWD naming differs). Test with `icon`, `icon-eu`, `icon-d2`.
- **Storage shape**: One 3D `hhl.om` (nlev, ny, nx) — even better than 121 tiny files. Chunking inside the 3D for good I/O. Update any export/glob code if it assumed per-hhl files (now just the one hhl.om + existing HSURF etc.).
- **When to populate**: Tied to `download` runs. For pure API servers with REMOTE_DATA_DIRECTORY, may need separate static prep step (like current elevation). Document in cronjobs.md.
- **Model level rollout dependency**: Phases 1+2 (ingest + lazy 3D column + helpers) are completely independent and deliver HHL data + internal height computation. General `height_levelN` (Phase 3) is gated on the `_levelN` / ModelLevelVariableRespresentable work. Near-term: backfill the legacy 80m/120m/180m/5500m fixed vars using the helpers. Explicitly decoupled in the phases above.
- **Exact HHL grid alignment**: HHL GRIBs are on the native model horizontal grid (icosa or latlon); our remap (for global) produces values on the open-meteo analysis grid. Consistent with how all other ICON data is treated.
- **Vertical indexing guarantee**: Filename _N_ == our half level N (top=1). Verified conceptually against PDF Table A.1 ordering. Add assert + test.
- **Compression / om format**: HHL fields are smooth (esp. upper levels); good compression. No special scalefactor needed (raw floats ok for static).
- **API surface bloat**: Heights only on explicit request. No change to default `&hourly=...` payloads.
- **AGL vs ASL**: ASL primary (matches raw HHL + geopotential_height precedent on p-levels). Provide AGL helper for users who want "above ground".
- **Future**: Once raw model levels (`temperature_level42` etc.) are queryable, `height_level42` pairs perfectly. Could add level metadata in responses.
- **Testing without full DWD data**: Use small --max-forecast-hour + existing fixtures, or synthetic HHL in tests.

## References
- DWD PDF `untracked/icon_database_main.pdf` (Tables A.1–A.6, formulas p.173).
- `notes/ALTITUDE.md` (current summary + Python fragment).
- `untracked/plan.md` (model levels context + explicit HHL deferral).
- `Sources/App/Icon/DownloadIconCommand.swift` (convertSurfaceElevation, CdoHelper, URL patterns).
- `Sources/App/Helper/Reader/GenericDomain.swift`, `GenericReader.swift`, `Gridable.swift` (static + elevation reading).
- `Sources/App/Icon/{Icon.swift,IconVariable*.swift,IconReader.swift,IconController.swift}` (domain + vars).
- Existing static examples: HSURF, soil_type, cdo_weights.nc, DEM chunks.
- Opdata listings (for URL reverse-engineering).

This plan preserves the sound ingestion design from convertSurfaceElevation while using a single 3D static file for efficiency, lazy access, and decoupled phases.

Next steps (implementation order): 
1. Domain props + convertHhlHeights (Phase 1).
2. Reader column helper + lazy + getStaticFile updates (Phase 2).
3. Backfill heights for legacy 80m/120m/etc. fixed vars as near-term win.
Update this doc with deviations during implementation. Update ALTITUDE.md and cross-references when done.