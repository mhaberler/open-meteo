# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

```bash
# macOS: install dependencies
brew install netcdf bzip2

# Linux (Ubuntu): install dependencies
sudo apt install libnetcdf-dev libeccodes-dev libbz2-dev libz-dev build-essential

# Run API server (debug)
swift run

# Run API server (release)
swift run -c release openmeteo-api serve --hostname 0.0.0.0 --port 8080

# Run all tests
swift test

# Run single test
swift test --filter AppTests.HelperTests

# Lint
swiftlint

# Docker dev build
docker build -f Dockerfile.development -t open-meteo-development .
docker run -it --security-opt seccomp=unconfined -p 8080:8080 -v ${PWD}:/app -v open-meteo-data:/app/data open-meteo-development /bin/bash
```

Downloading weather data for local development:
```bash
# Sync specific variables from AWS open data (no API key needed)
swift run openmeteo-api sync ncep_gfs013 temperature_2m --past-days 3

# Sync from a local/custom server with an API key
swift run openmeteo-api sync dwd_icon,dwd_icon_eu temperature_2m --server http://127.0.0.1:8080/ --apikey 123 --past-days 7
```

Environment variables (set in shell or `.env` file):
- `DATA_DIRECTORY` — path to weather data, must end with `/`, default `./data/`
- `REMOTE_DATA_DIRECTORY` — remote S3 data URL (triggers HTTP-based reads with local block cache)
- `TEMP_DIRECTORY` — scratch space for downloads
- `DATA_RUN_DIRECTORY` — output path for full-run databases

## Architecture

### Three-layer design

1. **HTTP API** (`Sources/App/Controllers/`) — Vapor-based. `ForecastapiController` registers all `/v1/*` routes, each backed by a `WeatherApiController` instance with a default model. It decodes query parameters (`ForecastapiQuery`), calls one or more `GenericReader` instances, and serialises the result (JSON, FlatBuffers via `OpenMeteoSdk`, CSV, XLSX, etc.).

2. **Domain model** (`Sources/App/<ModelName>/`) — One directory per weather model (Icon, Gfs, Ecmwf, MeteoFrance, Gem, Bom, Kma, …; 25+ models total). Each contains:
   - `<Model>.swift` — `enum` conforming to `GenericDomain` (grid definition, file layout, time resolution, ensemble count)
   - `<Model>Variable.swift` — raw and derived variables for that domain
   - `<Model>Reader.swift` — `GenericReaderDerived` subclass that computes derived variables from raw ones
   - `Download<Model>Command.swift` — download pipeline (fetch GRIB/NetCDF → convert → write `.om` files)

3. **Storage** (`Sources/App/Helper/`) — Custom binary time-series format via [`om-file-format`](https://github.com/open-meteo/om-file-format). Files live under `./data/<domain_registry>/`. `OmFileSplitter` splits data into fixed-length chunks. `RemoteFileManager` optionally fetches chunks from S3 with block-level caching.

### Key protocols

| Protocol | Purpose |
|----------|---------|
| `GenericDomain` | Grid, time-step, file layout for a weather model |
| `Gridable` | Spatial projection + point lookup (regular lat/lon, Lambert, rotated, Gaussian, …) |
| `GenericReaderProtocol` | `get(variable:time:)` + `prefetchData` — implemented by `GenericReader` |
| `GenericReaderDerived` | Layered reader: satisfies derived variables, delegates raw reads to `GenericReader` |
| `GenericVariableMixable` | Allows multi-model mixing via `GenericReaderMixerRaw` |

### Helper subdirectories

- `Helper/Reader/` — core reader protocols and implementations: `GenericReader`, `GenericReaderDerived`, `GenericReaderMixerRaw` (blends multiple domains), `GenericReaderMulti` (multi-location), `GenericReaderCached`, `VariableHourlyDeriverHighLevel`
- `Helper/Download/` — HTTP/FTP download utilities: `Curl.swift`, `CurlIndexed.swift` (indexed GRIB), specialisations for CDS/ECMWF/NetCDF; `GribStream`, `GribAttributes`; S3 uploader/lister; bzip2 decompressor
- `Helper/OmReader/` — block-cache layer for HTTP-range reads (`OmHttpReaderBackend`, `OmReaderBlockCache`, `AtomicBlockCache`)
- `Helper/Vapor/` — API key management, rate limiting, CIDR filtering, Stripe metering
- `Helper/Solar/` — solar position algorithm, sun rise/set, DNI/GTI radiation helpers
- `Helper/Writer/` — output serialisers: `JsonWriter`, `CsvWriter`, `XlsxWriter`, `ForecastApiResult`, `GenericVariableHandle`
- `Helper/File/` — run-metadata JSON (`FullRunMetaJson`, `ModelMetaJson`), remote file management
- `Helper/FlatBufferWriter/` — per-API-type FlatBuffers serialisers (weather, air-quality, marine, ensemble, climate, flood)
- `Helper/Time/` — `Timestamp`, `TimerangeDt`, `IsoDate`, `IsoDateTime`
- `Domains/` — grid projection implementations: `RegularGrid`, `ProjectionGrid`, `LambertConformalConic`, `LambertAzimuthalEqualArea`, `RotatedLatLon`, `GaussianGrid`, `Stereographic`

### Data pipeline

Download commands fetch raw GRIB or NetCDF data, convert it to `.om` files, and write metadata JSON. `CronjobCommand` schedules these commands automatically (see `docs/cronjobs.md`). `SyncCommand` pulls pre-built `.om` files from S3 (AWS open data or a private server) — the easiest way to get data for local development.

### Adding a new weather model

1. Create `Sources/App/<Name>/` directory mirroring an existing model (e.g. `Gfs/` or `MeteoFrance/`).
2. Define domain enum conforming to `GenericDomain`; add cases to `DomainRegistry` (`Helper/DomainRegistry.swift`).
3. Define variable enums; implement `GenericReaderDerived` for derived variables.
4. Implement download command (fetch raw data, convert to `.om`); register in `Commands/`.
5. Register routes in `ForecastapiController`.

### Data files

`.om` files use the custom OM format (see `om-file-format` package). Files are named by domain + variable + time chunk. Static files (elevation, soil type) share a separate `domainRegistryStatic` domain. Spatial JSON metadata (`FullRunMetaJson`, `ModelMetaJson`) tracks available runs.

### Release build notes

- `Package.swift` enables `-cross-module-optimization -Ounchecked` and aggressive C flags (`-O3 -fno-math-errno …`) in release only.
- `MARCH_SKYLAKE=TRUE` sets `-march=skylake` for Docker/Ubuntu release builds.
- `ENABLE_PARQUET=TRUE` adds optional Apache Arrow Parquet output support.
