# ICON downloads

Names for one scheduled ICON fetch and the two parts the chart draws for it. "Ingest" was being used for both the whole thing and the download half.

## Language

**Run**:
One cron invocation of one model and one variable group for one DWD run hour.
_Avoid_: ingest, job

**Download**:
The part of a run that fetches the files. The chart stores this phase as `ingest`.
_Avoid_: ingest

**Convert**:
The part of a run that writes the archive after the download. The chart stores this phase as `process`.
_Avoid_: process, ingest

## Surface water

**Precipitation**:
Surface water depth in millimetres over a quarter-hour or an hour.
_Avoid_: rain, rain water

## Hydrometeor content

**Rain water**:
The mass of rain in a parcel of air, per mass of moist air, in g/kg.
_Avoid_: rain

**Snow water**:
The mass of snow in a parcel of air, per mass of moist air, in g/kg.
_Avoid_: snowfall

**Graupel water**:
The mass of graupel in a parcel of air, per mass of moist air, in g/kg.
_Avoid_: graupel
