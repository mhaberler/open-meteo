# ICON-D2 `elevation` returns 0 over large lakes (Starnberger See)

## Summary

`/v1/forecast` with `models=icon_d2` returns `elevation: 0.0` for grid
cells over Starnberger See (a lake at ~584 m ASL near Munich), instead of
the lake's actual elevation. A land point ~5 km away on the same query
returns a correct, sane elevation.

**Note:** this reproduces on a self-hosted instance built from this repo,
but **not** on the production `api.open-meteo.com` — the same coordinates
against production return the correct `585.0`. So either production's
ICON-D2 static/elevation data differs from what a fresh build+ingest
produces from this repo today, or something about the self-hosted
instance's data pipeline/state is stale or diverged. This needs to be
narrowed down before treating it as a confirmed upstream code bug — see
"Open question" below.

## Steps to reproduce

```bash
curl -sS -G 'https://<host>/v1/forecast' \
  --data-urlencode 'latitude=47.90' \
  --data-urlencode 'longitude=11.31' \
  --data-urlencode 'hourly=temperature_2m' \
  --data-urlencode 'models=icon_d2' \
  --data-urlencode 'forecast_days=1' \
  --data-urlencode 'cell_selection=nearest'
```

| host | probe | resolved cell | elevation |
|---|---|---|---|
| self-hosted | 47.90, 11.31 | 47.9, 11.32 (lake) | **0.0** |
| self-hosted | 47.88, 11.31 | 47.88, 11.32 (lake) | **0.0** |
| self-hosted | 47.92, 11.33 | 47.92, 11.34 (lake) | **0.0** |
| self-hosted | 47.86, 11.29 | 47.86, 11.30 (lake) | **0.0** |
| self-hosted | 47.90, 11.25 | 47.9, 11.26 (land) | 671.0 (sane) |
| `api.open-meteo.com` | 47.90, 11.31 | 47.9, 11.32 (lake) | **585.0** (correct) |
| `api.open-meteo.com` | 47.86, 11.29 | 47.86, 11.30 (lake) | **637.0** (correct) |

Cross-check with the DEM-based elevation endpoint confirms the true
elevation: `https://api.open-meteo.com/v1/elevation?latitude=47.90&longitude=11.31`
→ `585.0` — matching production's `icon_d2` forecast output, and matching
Starnberger See's known real elevation (~584 m ASL).

## Root cause (in the self-hosted case)

Traced through this repo's code:

1. `Sources/App/Icon/DownloadIconCommand.swift` — when ingesting ICON's
   `HSURF` orography field, every grid cell DWD's land-sea mask flags as
   water is forced to `-999`:
   ```swift
   // Set all sea grid points to -999
   hsurf[i] = -999
   ```
2. `Sources/App/Domains/Gridable.swift` (`readElevation`) — any elevation
   `<= -999` is classified `.sea`. This is the path `cell_selection=nearest`
   takes.
3. `Sources/App/Domains/Gridable.swift` (`ElevationOrSea.numeric`) — `.sea`
   is converted to `0` for API output.

If DWD's own land-sea mask for ICON-D2 stamps `-999` on Starnberger See the
same way it does open ocean, `0` is the guaranteed (wrong) result on any
instance ingesting that raw upstream data — this collapse is a `.sea → 0`
design choice that's only correct for actual sea level, not large inland
lakes sitting well above it.

## Investigation update: staleness ruled out, code+current-DWD-data reproduces it

Two things were checked directly:

1. **Code parity**: `git diff upstream/main -- Sources/App/Icon/DownloadIconCommand.swift Sources/App/Domains/Gridable.swift` shows zero divergence — this repo's masking logic is byte-identical to upstream `main`.
2. **Fresh DWD data, decoded directly** (via `cfgrib`/`eccodes`, bypassing any locally cached `.om` file entirely) for the latest published ICON-D2 time-invariant fields (`.../icon-d2/grib/00/hsurf/..._2026080400_..._hsurf.grib2.bz2` and the matching `fr_land` file):

   | probe | current DWD `HSURF` | current DWD `FR_LAND` | this repo's code would mask to -999? |
   |---|---|---|---|
   | 47.90, 11.31 | 584.3 m | 0.129 | **yes** |
   | 47.88, 11.31 | 582.4 m | 0.056 | **yes** |
   | 47.92, 11.33 | 592.8 m | 0.324 | **yes** |
   | 47.86, 11.29 | 584.2 m | 0.145 | **yes** |
   | 47.90, 11.25 (land) | 670.8 m | 1.000 | no |

   DWD's raw `HSURF` orography is actually correct at every lake cell (~584 m, matching reality). It's `FR_LAND` that's the problem: DWD's **current** land-fraction mask still classifies these cells as majority-water (well under this codebase's `< 0.5` threshold in `DownloadIconCommand.swift`), so **a brand-new ingest today, with unmodified upstream code, reproduces `elevation: 0.0`** — this is not stale local data.

A local reproduction of the fix-by-regeneration attempt was also started and aborted before completion (DWD doesn't republish the time-invariant `HSURF`/`FR_LAND` files under every run timestamp, only occasionally — the naive `--run latest` picked a run with no published file at all, hit 404s, and was stopped; the original `HSURF.om` was restored from backup with no lasting effect). The direct grib decode above supersedes that attempt and is conclusive on its own.

## Root cause, confirmed

DWD publishes a **separate `fr_lake` field** for icon, icon-eu and icon-d2
(external parameters used to initialize ICON's own FLake lake scheme —
`fr_lake`, `depth_lk`, `t_bot_lk`, `c_t_lk` are all published alongside
`fr_land`/`hsurf`). Decoded directly from the current DWD grib at each
probe:

| probe | `FR_LAND` | `FR_LAKE` | `FR_LAND + FR_LAKE` |
|---|---|---|---|
| 47.90, 11.31 | 0.1286 | 0.8714 | 1.0000 |
| 47.88, 11.31 | 0.0563 | 0.9437 | 1.0000 |
| 47.92, 11.33 | 0.3239 | 0.6761 | 1.0000 |
| 47.86, 11.29 | 0.1449 | 0.8551 | 1.0000 |
| 47.90, 11.25 (land) | 1.0000 | 0.0000 | 1.0000 |

At every lake cell, the fraction "missing" from `FR_LAND` is accounted for
entirely by `FR_LAKE` — these cells are 0% actual open ocean, 68–94% lake.
DWD's own model distinguishes "lake" from "sea" as separate categories;
this repo's downloader only ever fetches/checks `FR_LAND`
(`DownloadIconCommand.swift`, `convertSurfaceElevation`) and treats
"not-land" as synonymous with "sea," discarding the exact information
(`fr_lake`) that would tell it otherwise. `HSURF` itself was never wrong —
DWD's raw orography is ~584 m at every one of these cells, correctly.

**This is the confirmed, complete root cause** — no longer just a
staleness or data-snapshot question. Whether or not production separately
avoids it (still unknown — see below), the defect is real and
reproducible with current upstream code and current DWD data.

## Suggested fix

In `convertSurfaceElevation` (`Sources/App/Icon/DownloadIconCommand.swift`),
also download `fr_lake` (same URL/remap pattern as the existing `fr_land`
fetch) and change the masking condition from:
```swift
if landFraction[i] < 0.5 {
    hsurf[i] = -999
}
```
to something that only masks cells with negligible land **and** negligible
lake fraction, e.g.:
```swift
if landFraction[i] + lakeFraction[i] < 0.5 {
    hsurf[i] = -999
}
```
`HSURF`'s raw value needs no correction — it's already correct for lake
cells; only the masking condition that discards it is wrong.

## Open question (secondary) — resolved as "not a code difference"

Initially assumed production's non-reproduction meant upstream had a newer
fix this repo (checked out from an older base) was missing. Checked that
directly, live, rather than relying on the locally cached `upstream/main`
ref (which was a month stale):

- Fetched the **current** `Sources/App/Icon/DownloadIconCommand.swift` and
  `Sources/App/Domains/Gridable.swift` straight from
  `raw.githubusercontent.com/open-meteo/open-meteo/main` — byte-identical
  masking logic, no `fr_lake` anywhere, no lake-aware handling at all.
- Pulled the **full commit history** for `DownloadIconCommand.swift` via
  the GitHub API, back to the project's first commit (`253981d07`,
  2022-07-27). The `FR_LAND`-based sea-masking approach has existed
  essentially unchanged since day one; nothing in the history touches
  lake-fraction handling.

**Conclusion: this is not a fork-is-older problem.** A byte-for-byte
current upstream checkout has the identical defect. Whatever explains
production's correct value at these coordinates, it is not a code
difference visible in the public repository — most likely production's
static elevation file predates a DWD-side change to `FR_LAND` for this
area (the same "generate once, cache forever" mechanism this repo has,
just cutting the other way: production being stale-but-lucky rather than
fixed), or production applies an out-of-band correction outside this
codebase. Not resolvable from this side, and doesn't block fixing the
confirmed root cause above.

## Impact

`elevation: 0.0` over a lake is indistinguishable from sea level to API
consumers, which breaks anything computing height-above-ground-level from
`elevation` + model levels (e.g. trajectory/AGL calculations) for
locations over large lakes.

## Scope

Confirmed `fr_lake` is published by DWD for all three deterministic ICON
domains (`icon`, `icon-eu`, `icon-d2`), so this affects every large lake
covered by any of them, not just Starnberger See/icon-d2 — e.g. Lake
Constance, Lake Geneva, and others within the icon-eu/icon-d2 domains.

More broadly, the same `-999`-marks-sea / `.sea → 0` convention (with no
lake-fraction check) is used by most other downloaders in this codebase
(GFS, UKMO, ERA5, GEM, ECMWF, CMA, MeteoSwiss, ItaliaMeteoArpae, MfWave,
...). Each would need checking individually for whether its own upstream
source publishes an equivalent lake-fraction field that's similarly being
ignored.
