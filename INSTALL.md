# Host install: cron and Caddy

This host runs the ICON download jobs from cron and fronts the API, the trajectory service, MQTT, and the vpsmon dashboard with Caddy. The clock is UTC. See `SWIFTINSTALL.md` for the toolchain and `trajectories-api/TIMEZONE.md` for why the schedules are in UTC.

Debian cron does not honor `CRON_TZ`. The line is in the crontab anyway. The jobs stay on UTC because `/etc/localtime` is UTC.

## Cron

Live file: `/etc/cron.d/openmeteo-api`.

```
CRON_TZ=UTC
DATA_DIRECTORY=/open-meteo/
```

The six download jobs run as `openmeteo-api` through `/usr/local/bin/ingest-wrap`. Minutes are local to the hour list. Hours are UTC, the old Berlin (CEST, UTC+2) hours minus two.

| Job | Minute | UTC hours | nice |
|---|---|---|---|
| icon-d2 heidiVars | 45 | 1,4,7,10,13,16,19,22 | -15 |
| icon-d2 model-level (`hiresTemp`, `--update-meta`) | 53 | 1,4,7,10,13,16,19,22 | -15 |
| icon-eu heidiVars | 40 | 0,3,6,9,12,15,18,21 | -17 |
| icon-eu model-level (`hiresTemp`, `--update-meta`) | 48 | 0,3,6,9,12,15,18,21 | -17 |
| icon global heidiVars | 50 | 0,6,12,18 | |
| icon global model-level (`hiresTemp`, `--update-meta`) | 57 | 0,6,12,18 | |

A line looks like:

```cron
45 1,4,7,10,13,16,19,22 * * * openmeteo-api /usr/local/bin/ingest-wrap icon-d2_heidivars.log nice -15 /usr/local/bin/openmeteo-api download icon-d2 --group heidiVars --concurrent 32
```

`ingest-wrap LOGNAME COMMAND...` truncates `$DATA_DIRECTORY/log/LOGNAME` in place, then runs `COMMAND` with stdout and stderr appended. The dashboard watcher tails those six names and treats a shrink as a new run, so the live path must stay stable. A non-zero exit copies the full log to `/open-meteo/log/failed/<name>.YYYYMMDDTHHMMSSZ.log`, prints the last 200 lines (cron mails that), and exits with the same status. A zero exit prints nothing. Copies older than 14 days are deleted. The wrapper lives at `/usr/local/bin/ingest-wrap`. `build/ingest-wrap` in this repo is a copy.

Two other lines stay in the same file:

- `5 * * * *` deletes `chunk_*` files under `${DATA_DIRECTORY}/dwd*` that are older than 15 days.
- `20 2 * * *` runs `dashboard/cleanup.py` as `mah`. That drops finished ingest-phase rows and disk samples older than 14 days (`RETENTION_DAYS` in `dashboard/phases.py`). The comment in the crontab that says 7 days is stale.

The previous `> log 2>&1 || cat log` lines are commented out in the crontab. Do not bring them back: a failed log was overwritten by the next run, and a `%` in a `date` format inside the crontab is turned into a newline.

## Caddy

Live file: `/etc/caddy/Caddyfile`. Caddy is 2.11. After an edit:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo caddy reload --config /etc/caddy/Caddyfile
```

`build/Caddyfile` in this repo is a copy for reference. Its `Origin` allowlist uses placeholder domains (`example.com`, `example.invalid`). The process reads `/etc/caddy/Caddyfile`, which has the real pattern.

| Site | What it serves |
|---|---|
| `vpsmon.meteo.mah.priv.at` | `/ui` and `/phases.json` go to the ingest chart on `127.0.0.1:8091`, behind HTTP basic auth. A browser request for `/` redirects to `/ui`. An iframe load of `/` is proxied to vpsmon on `localhost:8088`. |
| `meteo.mah.priv.at` | Static files from `/var/www/meteo`. `/trajectories*` is behind a separate basic-auth user. |
| `mqtt.wetterheidi.de` | WebSocket paths `/ws` and `/mqtt` proxy to `127.0.0.1:1884`. Port 8883 in the global `layer4` block proxies TLS to MQTT on `127.0.0.1:1883`. |
| `open-meteo.wetterheidi.de` | `/v1/*` and `/data/*` proxy to the API on `127.0.0.1:8086`. A request that sends an `Origin` outside the allowlist gets 403. A request with no `Origin` is allowed. |
| `trajectory.wetterheidi.de` | Proxies to `127.0.0.1:8010`. |

Basic-auth passwords are bcrypt hashes, not the password. Generate one and paste it after the username:

```bash
caddy hash-password
```

The default algorithm is bcrypt at cost 14, which prints a `$2a$14$…` hash. Each run uses a new salt. Do not commit a live hash if you can avoid it; the one in the Caddyfile on this host is the installed secret.

Access logs are `/var/log/caddy/mqtt.log`, `openmeteo.log`, and `trajectory.log`. Each rolls at 20 MB, keeps 5 rolled files, and deletes a rolled file after 30 days (`roll_keep_for 720h`). Caddy compresses the rolled files. Do not add these paths to logrotate: Caddy holds the file open, and a rename leaves it writing to the old inode.
