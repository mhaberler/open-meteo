#  Cronjobs

The  cronjobs for hiresTemp ingestion of ICON models

## Weather forecast models

```bash
# DWD ICON
DATA_DIRECTORY=/open-meteo/

# icon-d2 model levels - all
53 0,3,6,9,12,15,18,21 * * * openmeteo-api  /usr/local/bin/openmeteo-api download icon-d2  --update-meta --group hiresTemp --concurrent 12 > $DATA_DIRECTORY/log/icon-d2_model-level.log 2>&1 || cat $DATA_DIRECTORY/log/icon-d2_model-level.log


# icon-eu model levels - 48h
48 2,5,8,11,14,17,20,23  * * *  openmeteo-api  /usr/local/bin/openmeteo-api download icon-eu  --update-meta --group hiresTemp --max-forecast-hour 48 --concurrent 12  > $DATA_DIRECTORY/log/icon-eu_model-level.log 2>&1 

# icon global - 24h
57  2,8,14,20  * * * openmeteo-api /usr/local/bin/openmeteo-api download icon --update-meta --group hiresTemp --max-forecast-hour 12  --concurrent 12 >> ${DATA_DIRECTORY}log/icon_model-level.log 2>&1

# cleanup
# Delete forecasts older than 2 days
5 * * * * openmeteo-api  find ${DATA_DIRECTORY} -type f -name "chunk_*" -mtime +2 -delete


```
