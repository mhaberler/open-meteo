#!/bin/bash -eu
#
# Build the openmeteo-api .deb locally, mirroring .github/workflows/release.yml.
#
# Must run on Ubuntu jammy / amd64 with the Swift toolchain + netcdf/eccodes
# headers present. The simplest way is inside the project build container:
#
#   docker run --rm -v "$PWD":/src -w /src \
#     ghcr.io/open-meteo/docker-container-build:latest \
#     build/make-deb.sh [VERSION]
#
# VERSION defaults to `git describe` (or 0.0.0-dev). Output: ./openmeteo-api_<VERSION>_amd64.deb
#
# Install the result (libeccodes0 is not in stock Ubuntu repos):
#   curl -L https://github.com/patrick-zippenfenig/ecCodes-ubuntu/releases/download/2.41.0/libeccodes0_2.41.0_jammy_amd64.deb -o libeccodes0.deb
#   sudo apt install ./libeccodes0.deb ./openmeteo-api_<VERSION>_amd64.deb

cd "$(dirname "$0")/.."          # repo root

VER="${1:-$(git describe --tags --always 2>/dev/null || echo 0.0.0-dev)}"
# Set MARCH_SKYLAKE=TRUE for the open-meteo amd64 release target; unset on other CPUs.
: "${MARCH_SKYLAKE:=TRUE}"
export MARCH_SKYLAKE

echo ">> building openmeteo-api $VER (MARCH_SKYLAKE=$MARCH_SKYLAKE)"

# 1. native release build (static stdlib, with debug symbols for backtraces)
swift build -c release -Xswiftc -g -Xswiftc -static-stdlib

# 2. stage artifacts exactly as the workflow does
cp /usr/libexec/swift/linux/swift-backtrace-static ./swift-backtrace
cp .build/release/openmeteo-api ./openmeteo-api
rm -rf Resources && mkdir -p Resources
cp -r .build/release/*.resources Resources/

# 3. ensure fpm is available
if ! command -v fpm >/dev/null 2>&1; then
    echo ">> installing fpm"
    gem install --no-document fpm
fi

# 4. build the .deb
rm -f "openmeteo-api_${VER}_amd64.deb"
fpm -s dir -t deb -n openmeteo-api -v "$VER" \
    -d tzdata -d libnetcdf19 -d libeccodes0 \
    --deb-systemd-enable --deb-systemd-auto-start \
    --deb-systemd build/openmeteo-sync.service \
    --deb-systemd build/openmeteo-api.service \
    --deb-systemd build/openmeteo-api2.service \
    --deb-systemd build/openmeteo-api3.service \
    --deb-default build/openmeteo-api.env \
    --before-install build/openmeteo-before-install.sh \
    --before-upgrade build/openmeteo-before-install.sh \
    build/openmeteo-notify.sh=/usr/local/bin/ \
    openmeteo-api=/usr/local/bin/ \
    swift-backtrace=/usr/local/bin/ \
    Public=/var/lib/openmeteo-api \
    Resources=/var/lib/openmeteo-api

echo ">> done: openmeteo-api_${VER}_amd64.deb"
