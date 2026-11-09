# ICON-D2 stores precipitating hydrometeors on the lowest three full levels

ICON-D2 on the regular lat/lon grid downloads specific rain, snow, and graupel content (`rain_water`, `snow_water`, `graupel_water`) only for full levels 63–65, inside the existing `hiresTemp` group. The full column would be about twenty times as many files on a download that already hits timeouts. A separate cron and the `heidiVars` surface run were rejected. The native grid stays out until lat/lon visibility is no longer there to check against.
