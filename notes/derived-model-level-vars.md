# Derived model-level variables: dew_point, wind_speed, wind_direction (ICON)

## What
Three new server-side **derived** native model-level variables for ICON, queryable as
`dew_point_levelN`, `wind_speed_levelN`, `wind_direction_levelN`. They join the existing
read-derived `relative_humidity_levelN` and the native `wind_u/v_component`, `temperature`,
`pressure`, `specific_humidity` levels.

Computed on read from existing model-level fields — **not** stored as `.om`, **not** downloaded.

## Why
Building a radiosonde-style sounding required the client to fetch `wind_u/v_component` and
compute wind speed/direction + dewpoint itself (old `notes/sounding.py`). Now the API returns
these directly, so the sounding query is self-contained.

## How
Mirrors the `relative_humidity` model-level pattern exactly.

- `Sources/App/Icon/IconModelLevelVariable.swift` — 3 cases added to
  `IconModelLevelVariableType` + exhaustive switch arms (scalefactor, interpolation, unit,
  multiplyAdd, `getVarAndLevel`→nil so download skips them).
- `Sources/App/Icon/IconReader.swift` — intercept in `get(raw:)` + `prefetchData`:
  - `wind_speed` ← `Meteorology.windspeed(u:v:)` from u/v
  - `wind_direction` ← `Meteorology.windirectionFast(u:v:)` from u/v (met convention, FROM)
  - `dew_point` ← `Meteorology.dewpoint(temperature:relativeHumidity:)` from t + derived rh
- `Sources/App/Controllers/VariableHourly.swift` — same 3 cases in generic
  `ForecastModelLevelVariableType` (parsing).
- `Sources/App/Helper/FlatBufferWriter/FlatBuffers+WeatherApi.swift` — FlatBuffers mapping
  (`.windSpeed`/`.windDirection`/`.dewPoint`) for both enums (exhaustive-switch requirement).

## Verification
- `swift build` clean.
- Smoke test `notes/sounding.py` (now queries the derived vars directly) at Stiwoll,
  ICON-D2 2026-06-16T00:00Z. Output matches the earlier client-side derivation: wind
  speed/dir exact, dewpoint within ±0.1 °C. Data tops out ~4862 m (FL160) per current
  `below-fl180` ingest.

## Notes / limits
- Derivation lives in `IconReader`; other models expose the parsed names via the generic
  enum but won't produce values until they implement the same interception.
- Units returned SI (m/s, °C, °); honors `wind_speed_unit=ms` etc. at the output layer.
