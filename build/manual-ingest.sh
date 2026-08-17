#!/bin/bash
#
# Manually run the ICON model-level / heidiVars download jobs that are
# normally triggered by cron, as the openmeteo-api user with its proper
# login environment. Logs to stdout instead of the cron log files.
#
# Mirrors these crontab entries (DATA_DIRECTORY=/open-meteo/):
#   53 0,3,6,9,12,15,18,21 * * *  openmeteo-api  openmeteo-api download icon-d2 --update-meta --group hiresTemp  --concurrent 12
#   48 2,5,8,11,14,17,20,23 * * * openmeteo-api  openmeteo-api download icon-eu --update-meta --group hiresTemp  --concurrent 12
#   45 0,3,6,9,12,15,18,21 * * *  openmeteo-api  openmeteo-api download icon-d2 --group heidiVars --concurrent 12
#   40 2,5,8,11,14,17,20,23 * * * openmeteo-api  openmeteo-api download icon-eu --group heidiVars --concurrent 12
#
# Usage: build/manual-ingest.sh [job ...]
#   job is one of: icon-d2-model-level icon-eu-model-level icon-d2-heidivars icon-eu-heidivars
#   With no arguments, all four jobs run in sequence.

set -u

DATA_DIRECTORY="${DATA_DIRECTORY:-/open-meteo/}"
RUN_USER="openmeteo-api"
BIN="/usr/local/bin/openmeteo-api"

ALL_JOBS=(icon-d2-model-level icon-eu-model-level icon-d2-heidivars icon-eu-heidivars)

if [ "$(id -u)" -eq 0 ] || [ "$(id -un)" = "$RUN_USER" ]; then
    SUDO=()
else
    SUDO=(sudo)
fi

# Runs one job as $RUN_USER, in its login environment, with DATA_DIRECTORY
# exported. Output goes to stdout/stderr.
run_job() {
    local name="$1"
    shift
    echo "==> Running $name"
    if "${SUDO[@]}" -iu "$RUN_USER" env DATA_DIRECTORY="$DATA_DIRECTORY" "$BIN" "$@"; then
        echo "==> $name completed"
        return 0
    else
        local status=$?
        echo "==> $name failed (exit $status)" >&2
        return "$status"
    fi
}

if [ "$#" -gt 0 ]; then
    jobs=("$@")
else
    jobs=("${ALL_JOBS[@]}")
fi

overall_status=0

for job in "${jobs[@]}"; do
    case "$job" in
        icon-d2-model-level)
            run_job "icon-d2 model-level" \
                download icon-d2 --update-meta --group hiresTemp --concurrent 12 \
                || overall_status=1
            ;;
        icon-eu-model-level)
            run_job "icon-eu model-level" \
                download icon-eu --update-meta --group hiresTemp --concurrent 12 \
                || overall_status=1
            ;;
        icon-d2-heidivars)
            run_job "icon-d2 heidiVars" \
                download icon-d2 --group heidiVars --concurrent 12 \
                || overall_status=1
            ;;
        icon-eu-heidivars)
            run_job "icon-eu heidiVars" \
                download icon-eu --group heidiVars --concurrent 12 \
                || overall_status=1
            ;;
        *)
            echo "Unknown job: $job" >&2
            echo "Valid jobs: ${ALL_JOBS[*]}" >&2
            exit 1
            ;;
    esac
done

exit "$overall_status"
