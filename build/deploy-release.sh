#!/bin/bash -e
#
# Build (if needed) and deploy the release openmeteo-api binary to
# /usr/local/bin, restarting the systemd service. Keeps one timestamped
# backup of the previously deployed binary and rolls back automatically
# if the service fails to come up.
#
# Usage: build/deploy-release.sh [--skip-build]

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RELEASE_BIN="$REPO_DIR/.build/release/openmeteo-api"
DEST_BIN="/usr/local/bin/openmeteo-api"
SERVICE="openmeteo-api"
SKIP_BUILD=0

for arg in "$@"; do
    case "$arg" in
        --skip-build) SKIP_BUILD=1 ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

if [ "$SKIP_BUILD" -eq 0 ]; then
    echo "==> Building release binary"
    (cd "$REPO_DIR" && swift build -c release)
fi

if [ ! -x "$RELEASE_BIN" ]; then
    echo "error: $RELEASE_BIN not found or not executable" >&2
    exit 1
fi

NEW_MD5="$(md5sum "$RELEASE_BIN" | cut -d' ' -f1)"
CUR_MD5="$( [ -f "$DEST_BIN" ] && md5sum "$DEST_BIN" | cut -d' ' -f1 || echo "" )"

if [ "$NEW_MD5" = "$CUR_MD5" ]; then
    echo "==> $DEST_BIN is already up to date (md5 $NEW_MD5), nothing to do"
    exit 0
fi

BACKUP_BIN="${DEST_BIN}.bak-$(date +%Y%m%d%H%M%S)"

echo "==> Deploying $RELEASE_BIN ($NEW_MD5) -> $DEST_BIN"
echo "    previous binary: ${CUR_MD5:-none} -> backed up to $BACKUP_BIN"

sudo systemctl stop "$SERVICE"

if [ -f "$DEST_BIN" ]; then
    sudo cp "$DEST_BIN" "$BACKUP_BIN"
fi
sudo cp "$RELEASE_BIN" "$DEST_BIN"

sudo systemctl start "$SERVICE"

echo "==> Waiting for $SERVICE to become active"
for i in $(seq 1 10); do
    if systemctl is-active --quiet "$SERVICE"; then
        echo "==> $SERVICE is active, deployed md5 $(md5sum "$DEST_BIN" | cut -d' ' -f1)"
        exit 0
    fi
    sleep 1
done

echo "error: $SERVICE did not become active, rolling back to $BACKUP_BIN" >&2
sudo systemctl stop "$SERVICE" || true
if [ -f "$BACKUP_BIN" ]; then
    sudo cp "$BACKUP_BIN" "$DEST_BIN"
fi
sudo systemctl start "$SERVICE"
echo "error: deploy failed, rolled back. Check: journalctl -u $SERVICE -n 100" >&2
exit 1
