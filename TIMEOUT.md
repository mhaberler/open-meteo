# Download timeouts

`hiresTemp` runs die with `CurlError.timeoutReached`. The last error is `HTTPClientError.getConnectionFromPoolTimeout`. `heidiVars` uses the same client and finishes.

The jobs fetch `http://opendata.dwd.de`, so each file is one HTTP/1 connection. async-http-client 1.34.0 allows 8 connections per host. Cron starts every download with `--concurrent 32` (`/etc/cron.d/openmeteo-api`). The extra requests wait in the pool and fail when the 30-second connect timeout fires. `TimeoutTracker` retries every 5 seconds until `deadLineHours`: 2 hours for icon-d2, 5 hours for icon-eu and icon. `Process.alarm` kills the process one hour after that.

icon-eu (`:48`), icon-d2 (`:53`), and icon (`:57`) overlap, so three processes each hold 8 connections to the same host. A full icon-d2 column is about 29 000 files (586 fields, hours 0–48). Those runs use the whole 2 hours and stop between hour 12 and 32.

DWD has no outage that matches the 9–10 October logs. The 6 October 2026 grid change does not apply to deterministic ICON (grid #26), ICON-EU on the regular lat/lon path, or ICON-D2. After 30 November 2026 the old URL scheme for those three models is switched off, and ICON-EU and ICON-D2 stop arriving on a regular lat/lon grid.

## Changes

1. In `makeNewHttpClient` and `http1Client` (`Sources/App/configure.swift`), set `concurrentHTTP1ConnectionsPerHostSoftLimit` to the job’s `--concurrent` value (32). The pool is currently created with only `idleTimeout`.

2. Run one `hiresTemp` job at a time. A limit of 32 per process is 96 connections to DWD while the three domains overlap, which stretches the 5-minute read timeout. Leave the `heidiVars` minutes as they are.

3. Give icon-d2 `hiresTemp` more than 2 hours. `deadLineHours` in `DownloadIconCommand` is domain-wide. Raise it for `hiresTemp`, or pass `--max-forecast-hour` until a full run fits in 2 hours.

`--concurrent 8` matches the current pool and stops the timeout storm without a code change. A full icon-d2 run can still miss the 2-hour deadline at that rate. `build/manual-ingest.sh` uses 12, which still queues behind the limit of 8.
