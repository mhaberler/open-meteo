# Download timeouts

`hiresTemp` runs die with `CurlError.timeoutReached`. The last error is `HTTPClientError.getConnectionFromPoolTimeout`. `heidiVars` uses the same client and finishes.

The jobs fetch `http://opendata.dwd.de`, so each file is one HTTP/1 connection. async-http-client 1.34.0 allows 8 connections per host. Cron starts every download with `--concurrent 32` (`/etc/cron.d/openmeteo-api`). The extra requests wait in the pool and fail when the 30-second connect timeout fires. `TimeoutTracker` retries every 5 seconds until `deadLineHours`: 2 hours for icon-d2, 5 hours for icon-eu and icon. `Process.alarm` kills the process one hour after that.

icon-eu (`:48`), icon-d2 (`:53`), and icon (`:57`) overlap, so three processes each hold 8 connections to the same host. A full icon-d2 column is about 29 000 files (586 fields, hours 0–48). Those runs use the whole 2 hours and stop between hour 12 and 32.

DWD has no outage that matches the 9–10 October logs. The 6 October 2026 grid change does not apply to deterministic ICON (grid #26), ICON-EU on the regular lat/lon path, or ICON-D2. After 30 November 2026 the old URL scheme for those three models is switched off, and ICON-EU and ICON-D2 stop arriving on a regular lat/lon grid.

## Changes

1. `download` accepts `--connections-per-host`. It sets `concurrentHTTP1ConnectionsPerHostSoftLimit` on `dedicatedHttpClient` for that process. Omitted, the limit stays 8. `http1Client` is unchanged.

2. Run one `hiresTemp` job at a time. A limit of 32 per process is 96 connections to DWD while the three domains overlap, which stretches the 5-minute read timeout. Leave the `heidiVars` minutes as they are.

3. `download` accepts `--deadline-hours` (whole hours). It overrides the Curl deadline for surface elevation, HHL, and the GRIB download. `Process.alarm` stays one hour past that value. Omitted, icon-d2 and icon-d2-eps stay at 2 hours and the other ICON domains stay at 5.

`--concurrent 8` still matches the default pool when `--connections-per-host` is omitted. A full icon-d2 run can still miss the 2-hour deadline at that rate. `build/manual-ingest.sh` uses 12, which still queues behind the default limit of 8.
