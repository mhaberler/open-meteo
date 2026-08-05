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

## Open question

Production returning the correct, non-zero value at the same coordinates
means this needs to be resolved before it's clear where the bug actually
is:
- Does production's ICON-D2 `HSURF`/elevation static file differ from
  what this repo's current downloader produces (e.g. a data source change,
  a masking-threshold fix, or a DEM-based correction applied to
  production's static file that isn't present in this repo's code)?
- Or is the self-hosted instance simply running stale/corrupted static
  data (an old `HSURF.om`) unrelated to any code defect?

Not yet established which. Worth diffing this repo's `HSURF` ingest logic
against whatever produced production's current static file, and/or
re-generating the self-hosted instance's `HSURF.om` from a fresh DWD
download to see if the discrepancy persists.

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
