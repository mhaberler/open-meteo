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

## Open question (revised)

Given current DWD data + current upstream code both produce the bug, the
question flips: **why doesn't production show it?** Candidates, not yet
distinguished:
- Production runs additional/different logic not present in this public
  checkout (e.g. a DEM-based correction, a different/lower `FR_LAND`
  threshold, or lake-specific handling).
- Production's static elevation file is itself an *older* snapshot, from
  before DWD's `FR_LAND` mask degraded for this area — i.e. production
  being correct could be its own staleness accident, predating whatever
  changed DWD's land-fraction data here, rather than evidence of a fix.
- Production ingests from a different DWD product/grid variant (this
  check used the `regular-lat-lon` remap; DWD also publishes an
  `icosahedral` native-grid version — different regridding could shift a
  borderline `FR_LAND` value, though 3 of the 4 measured values are far
  enough below `0.5` that regridding alone seems unlikely to flip them).

Not yet established which. Would need visibility into production's actual
ingest history/pipeline to settle it, which isn't available from this
side.

## Impact

`elevation: 0.0` over a lake is indistinguishable from sea level to API
consumers, which breaks anything computing height-above-ground-level from
`elevation` + model levels (e.g. trajectory/AGL calculations) for
locations over large lakes.

## Scope

If confirmed as a genuine data/code issue (pending the open question
above), it likely isn't ICON-specific: the same `-999`-marks-sea /
`.sea → 0` convention is used by most downloaders in this codebase (GFS,
UKMO, ERA5, GEM, ECMWF, CMA, MeteoSwiss, ItaliaMeteoArpae, MfWave, ...),
so any sufficiently large lake could show the same wrong `0` on any model
whose upstream land-sea mask lumps big lakes in with ocean.
