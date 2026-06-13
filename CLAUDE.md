# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

```bash
# macOS: install dependencies
brew install netcdf bzip2

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

Environment variables (set in shell or `.env` file):
- `DATA_DIRECTORY` — path to weather data, must end with `/`, default `./data/`
- `REMOTE_DATA_DIRECTORY` — remote S3 data URL (triggers HTTP-based reads with local block cache)
- `TEMP_DIRECTORY` — scratch space for downloads
- `DATA_RUN_DIRECTORY` — output path for full-run databases

## Architecture

### Three-layer design

1. **HTTP API** (`Sources/App/Controllers/`) — Vapor-based. `ForecastapiController` routes requests, decodes query parameters (`ForecastapiQuery`), calls one or more `GenericReader` instances, and serialises the result (JSON, FlatBuffers via `OpenMeteoSdk`, CSV, etc.).

2. **Domain model** (`Sources/App/<ModelName>/`) — One directory per weather model (Icon, Gfs, Ecmwf, MeteoFrance, …). Each contains:
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
