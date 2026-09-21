# Swift toolchain setup (this host)

## Why this doc exists

The `openmeteo-api` systemd service runs as the `openmeteo-api` system user,
which cannot read anything under a personal `$HOME` (mode `700`). A Swift
toolchain installed under `~/.local/share/swiftly/...` (swiftly's default
location) gets baked into the built binary's `RUNPATH`. When that binary is
deployed to `/usr/local/bin` and the service starts, it fails with:

```
error while loading shared libraries: libswiftCore.so: cannot open shared object file: No such file or directory
```

This happened in production on 2026-09-21. The fix is architectural, not a
one-off: **all Swift toolchains on this host live under `/opt/swiftly`,
world-readable, never under any user's `$HOME`.**

## Layout

- `/opt/swiftly` — swiftly itself (`bin/`, `config.json`) and every
  installed toolchain (`toolchains/<version>/`), owned `mah:mah`, world
  readable+traversable (`a+rX`).
- `.zprofile` sources `/opt/swiftly/env.sh`, which puts `/opt/swiftly/bin`
  on `PATH`. No Swift-related state lives under `$HOME` on this host.
- **6.3.3 is this project's required version** — matches what
  `Package.swift` (`swift-tools-version:6.2` floor) and the deployed
  production binary are built with. `swiftly use` should be left set to
  6.3.3 as the global default.

## Fresh-machine install

```bash
# 1. Create the shared, world-readable install location
sudo mkdir -p /opt/swiftly
sudo chown "$USER":"$USER" /opt/swiftly

# 2. Download swiftly and init it pointed at /opt/swiftly
curl -O https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz
tar zxf swiftly-$(uname -m).tar.gz
SWIFTLY_HOME_DIR=/opt/swiftly \
SWIFTLY_BIN_DIR=/opt/swiftly/bin \
SWIFTLY_TOOLCHAINS_DIR=/opt/swiftly/toolchains \
./swiftly init --platform debian12 --quiet-shell-followup --assume-yes --skip-install
# --platform debian12: this host reports as Debian 13 (trixie) in
# /etc/os-release, but Swift's official Linux builds only ship as far as
# debian12 currently; debian12 builds run fine on this host. Drop
# --platform if a future swiftly release adds native debian13 support.

# 3. Install and select the project's toolchain
export SWIFTLY_HOME_DIR=/opt/swiftly SWIFTLY_BIN_DIR=/opt/swiftly/bin \
       SWIFTLY_TOOLCHAINS_DIR=/opt/swiftly/toolchains PATH=/opt/swiftly/bin:$PATH
swiftly install 6.3.3 --assume-yes   # also sets it as the global default

# 4. Make sure everything under /opt/swiftly stays world-readable
sudo chmod -R a+rX /opt/swiftly

# 5. Point the shell at it permanently
cat >> ~/.zprofile <<'EOF'

# Added by swiftly
. "/opt/swiftly/env.sh"
EOF
```

Verify:

```bash
swiftly list        # Swift 6.3.3 (in use) (default)
which swift          # /opt/swiftly/bin/swift
swift --version       # Swift version 6.3.3 (swift-6.3.3-RELEASE)
```

## VSCode Swift extension

Machine-scoped setting (applies to every workspace on this host), in
`~/.vscode-server/data/Machine/settings.json`:

```json
{
    "swift.path": "/opt/swiftly/toolchains/6.3.3/usr/bin"
}
```

Reload the VSCode window after changing this — `swift.path` is not
hot-reloaded.

## Installing and selecting other toolchain versions

The machine may legitimately need more than one toolchain around (e.g. to
test a newer Swift release before adopting it project-wide).

- **List what's available upstream:** `swiftly list-available`
- **Install another version alongside 6.3.3:**
  ```bash
  swiftly install 6.4.0
  sudo chmod -R a+rX /opt/swiftly   # MANDATORY — see gotcha below
  ```
- **List what's installed / which is active:** `swiftly list`
- **Switch the global default** (affects every shell/build that doesn't
  pin a version, including `build/deploy-release.sh`):
  ```bash
  swiftly use 6.4.0 --global-default   # switch
  swiftly use 6.3.3 --global-default   # switch back
  swiftly use                          # confirm current default
  ```
  Always confirm `swiftly use` reports **6.3.3** before deploying to
  production.
- **Pin a version for one project without touching the global default:**
  run `swiftly use <version>` (no `-g`) from inside that project's
  directory — this writes a `.swift-version` file there, and swiftly
  auto-selects that toolchain whenever `swift`/`swiftly run` runs inside
  that directory tree, regardless of the global default.
- **One-off override, no pin file:**
  ```bash
  swiftly run swift build +6.4.0
  ```
- **Remove a version no longer needed:** `swiftly uninstall <version>`
- **Point VSCode at a specific version explicitly:** set `swift.path` to
  `/opt/swiftly/toolchains/<version>/usr/bin`.

**Gotcha:** a freshly installed toolchain under `/opt/swiftly/toolchains/`
is not guaranteed to be world-readable — re-run
`sudo chmod -R a+rX /opt/swiftly` after every `swiftly install`. Skipping
this silently reintroduces the exact outage this doc exists to prevent.

## Build & deploy

`build/deploy-release.sh` runs a bare `swift build -c release`, so it
always builds against whatever toolchain `swiftly use` currently reports as
active. With the layout above, that toolchain always lives under
`/opt/swiftly`, so a normal deploy is safe — but always sanity-check first:

```bash
swiftly use                     # confirm: Swift 6.3.3 (default)
```

**Always clean `.build/` after switching the active toolchain version, or
after any toolchain relocation** — stale incremental build artifacts can
otherwise link against a path that no longer matches the active toolchain:

```bash
rm -rf .build
build/deploy-release.sh
```

Pre/post-deploy sanity checks:

```bash
# Confirm the built/deployed binary's runtime linker path
readelf -d /usr/local/bin/openmeteo-api 2>/dev/null | grep -i runpath
#   should show /opt/swiftly/toolchains/<version>/usr/lib/swift/linux

# Confirm the service user can actually read the runtime libs
sudo -u openmeteo-api test -r \
  /opt/swiftly/toolchains/6.3.3/usr/lib/swift/linux/libswiftCore.so \
  && echo READABLE || echo "NOT READABLE — fix perms before deploying"
```

**Note on `deploy-release.sh`'s `cp` step:** if another long-running
`openmeteo-api` invocation is active on this host (e.g. a manual/cron data
download job started via `/usr/local/bin/openmeteo-api download ...`), a
plain `cp` over `/usr/local/bin/openmeteo-api` can fail with `Text file
busy` even while the systemd service itself is stopped, because the other
process still holds the binary open. `deploy-release.sh` does not currently
detect this failure (the `cp` error doesn't stop the script, and it may
report a stale binary as "deployed"). If this happens: build the new binary
under a temp name and `mv` it into place instead of `cp` — a rename doesn't
require the target to be unbusy, and any process still holding the old
inode open keeps running against it unaffected:

```bash
sudo cp .build/release/openmeteo-api /usr/local/bin/openmeteo-api.new
sudo chmod 755 /usr/local/bin/openmeteo-api.new
sudo mv /usr/local/bin/openmeteo-api.new /usr/local/bin/openmeteo-api
sudo systemctl restart openmeteo-api
```

## Troubleshooting

**Symptom:**
```
openmeteo-api[NNNNN]: /usr/local/bin/openmeteo-api: error while loading shared libraries: libswiftCore.so: cannot open shared object file: No such file or directory
```

**Cause:** the deployed binary's `RUNPATH` points at a toolchain location
the `openmeteo-api` service user cannot read (almost always something under
a personal `$HOME`).

**Fix:**
1. `readelf -d /usr/local/bin/openmeteo-api | grep -i runpath` — see what
   path it's actually looking for.
2. `sudo -u openmeteo-api test -r <that path>/libswiftCore.so` — confirm
   it's actually unreadable.
3. If the path is `/opt/swiftly/...` but still fails: `sudo chmod -R a+rX
   /opt/swiftly` (permissions likely reset by a `swiftly install`/`update`).
4. If the path is anything under `/home/...`: the binary was built with a
   misconfigured `PATH`/toolchain. Fix the shell/environment per this doc,
   `rm -rf .build`, rebuild, redeploy.

## Rollback

`build/deploy-release.sh` automatically backs up the previously deployed
binary to `/usr/local/bin/openmeteo-api.bak-<timestamp>` before overwriting
it, and rolls back automatically if the service fails to become active
within 10 seconds of a deploy. To roll back manually:

```bash
sudo systemctl stop openmeteo-api
sudo cp /usr/local/bin/openmeteo-api.bak-<timestamp> /usr/local/bin/openmeteo-api
sudo systemctl start openmeteo-api
```

These backups are not cleaned up automatically — prune old ones
periodically if disk space matters.
