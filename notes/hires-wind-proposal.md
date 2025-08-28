# proposal: Short term wind forecasts with high vertical resolution


## use case: 

- last check before a flight/jump
- nowcasting and short term  trajectory forecasting during flight
- project contexts: trajectory forecasting for ballooning (https://github.com/open-meteo/open-meteo/discussions/1298), skydive planning (https://github.com/wetterheidi/upper_winds_open_meteo)

## observations:

- pressure levels are coarse 
- the Icon family of models provides very dense vertical forecasts through model levels (about 3-4 times higher vertical resolution over pressure levels). 
- we are not aware of any projects or API services providing vertical wind data based on Icon model levels. 
- we believe a model-level short-term vertical forecast could be an interesting USP for open meteo.
- vertical profiles using all available model levels is computationally expensive and probably not feasible for extended forecast periods. 
- using a subset of vertical levels and a reduced forecast period might make the effort feasible even within the DWD data playout structure. 
- we believe the most relevant vertical range is surface to flight level 180 which translates into something like 30 model levels in the Icon family. 
- as the use case is very short term focused, there is not much value in extended forecasting beyond several hours. 
- just providing wind U and V values covers many usage scenarios 

## ballpark calculation of download size:

- assume 30 model levels from ICOND2/ICON-EU or ICON Global define a relevant vertical range
- each level needs the wind U and V variables
- assume a forecast loookahead of eight hours. 
- this translates into 30x2x8 = 480 files per forecast run (every three hours assuming Icon-D2) which looks like a managable amount of data
- Looking at the ICOND2 pressure level download, this looks like 55 variables per hour; for 48 hours this would be 2640 files to dowload
- same filecount assumed for a hires u/v download would yield some 44 hours (2640/60) so comparable effort

## scope:

- we would restrict to just addressing the ICON family of models (which might include variants thereof, like the Swiss icon model. )
- We will start with ICON D2 and possibly expand to ICON EU and ICON Global if there is demand. 
- Any additions resulting from this effort should not impact existing installations in any shape or form.

## preliminary work:

- I did a throwaway branch to implement extracting a single model level layer, namely wind speed and wind direction at 5500 meters: https://github.com/open-meteo/open-meteo/compare/main...mhaberler:open-meteo:mah
- I added the 5500 meter level to the Icon surface variable set and added derived variables for wind speed and wind direction at 5500 meters. 
- the results  - comparing the 500hPa pressure level and 5500 meter model level - look reasonable (see query below)
- this is my first-ever exposure to Swift, so bear with me. Most changes are cargo-cult coding.

## Implementation and prerequisites:

- I would take on this task if there is a chance of the result being merged back.
- some of the work could be scripted to reduce manual editing, once the naming questions below are resolved. 
- I would take on the development of this feature. However, I need guidance and a bit of help in a few following areas:
    - Variable naming: I'm unsure if encoding the altitude in the level name (eg windspeed_5500m) is the right way to go or if we should retain the level number (windspeed_level27) and provide a model-specific lookup mechanism to translate level into an altitude. Since the level height of ICON Global and EU versus ICON D2 are not identical, using the height in the name would be cause a major increase  of layer names whose heights do not match across models. 
    - To avoid impact on existing installations, this variable set should be a separate download option, similar to the model levels or surface groups. 
    - I'd be looking for advice how to best structure this variable set, and how to control the download via a command line group argument. . For instance, adding an IconLevelVariableType, or a new 'realm'?
    - Currently the number of forecast hours is fixed per model. To limit the look-ahead time span, this must be made a command line argument, or at least configurable in some way.
    - advice on possible side effects, which I am unaware of.  I might be trampling on many assumptions. 
    - For instance, It is unclear to me if this limited forecast hours would impact for instance on the omFileLength  variable 


## output of test branch
purpose: sanity-check wind_speed_500hPa vs wind_speed_5500m, and wind_direction_500hPa vs wind_direction_5500m

https://api.openmeteo.mah.priv.at//v1/forecast?latitude=47&longitude=15&hourly=wind_speed_5500m,wind_speed_500hPa,wind_direction_5500m,wind_direction_500hPa&models=icon_d2&start_date=2025-08-28&end_date=2025-08-29
````json
{
  "latitude": 47.02,
  "longitude": 15.019999,
  "generationtime_ms": 0.447630882263184,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 871,
  "hourly_units": {
    "time": "iso8601",
    "wind_speed_5500m": "km/h",
    "wind_speed_500hPa": "km/h",
    "wind_direction_5500m": "°",
    "wind_direction_500hPa": "°"
  },
  "hourly": {
    "time": [
      "2025-08-28T00:00",
      "2025-08-28T01:00",
      "2025-08-28T02:00",
      "2025-08-28T03:00",
      "2025-08-28T04:00",
      "2025-08-28T05:00",
      "2025-08-28T06:00",
      "2025-08-28T07:00",
      "2025-08-28T08:00",
      "2025-08-28T09:00",
      "2025-08-28T10:00",
      "2025-08-28T11:00",
      "2025-08-28T12:00",
      "2025-08-28T13:00",
      "2025-08-28T14:00",
      "2025-08-28T15:00",
      "2025-08-28T16:00",
      "2025-08-28T17:00",
      "2025-08-28T18:00",
      "2025-08-28T19:00",
      "2025-08-28T20:00",
      "2025-08-28T21:00",
      "2025-08-28T22:00",
      "2025-08-28T23:00",
      "2025-08-29T00:00",
      "2025-08-29T01:00",
      "2025-08-29T02:00",
      "2025-08-29T03:00",
      "2025-08-29T04:00",
      "2025-08-29T05:00",
      "2025-08-29T06:00",
      "2025-08-29T07:00",
      "2025-08-29T08:00",
      "2025-08-29T09:00",
      "2025-08-29T10:00",
      "2025-08-29T11:00",
      "2025-08-29T12:00",
      "2025-08-29T13:00",
      "2025-08-29T14:00",
      "2025-08-29T15:00",
      "2025-08-29T16:00",
      "2025-08-29T17:00",
      "2025-08-29T18:00",
      "2025-08-29T19:00",
      "2025-08-29T20:00",
      "2025-08-29T21:00",
      "2025-08-29T22:00",
      "2025-08-29T23:00"
    ],
    "wind_speed_5500m": [26.8, 34.9, 45.4, 50.2, 42.3, 42.7, 39.3, 38, 42.8, 37.7, 45.3, 49.1, 43.5, 53.7, 52.5, 45.4, 52.2, 43.5, 48.6, 56.8, 62, 66.2, 56.5, 58.4, 72.6, 71.5, 79.1, 84, 76.6, 80.4, 83.9, 71.2, 69.6, 72.5, 64.9, 76.3, 77.9, 69.4, 85.6, 78.7, 81.1, 89.1, 82.5, 76, 76.5, 72.4, 61.3, 58.1],
    "wind_speed_500hPa": [23.1, 32.2, 36.6, 45.4, 44.9, 40.1, 42.6, 39.9, 44.2, 38.3, 46.9, 53.7, 41.4, 49, 42.4, 54.7, 48.3, 49.6, 54.4, 50, 55.4, 66, 63.2, 64, 71.6, 84, 79.6, 81.9, 82.2, 85.2, 66.9, 72.9, 76.9, 82.8, 88.5, 89.1, 95, 83.2, 65.3, 82.9, 87.1, 80.5, 80.6, 72.2, 70.4, 60.2, 67.6, 69.4],
    "wind_direction_5500m": [213, 222, 222, 227, 218, 210, 221, 217, 226, 237, 237, 233, 240, 246, 242, 239, 243, 233, 226, 215, 213, 218, 207, 201, 207, 207, 207, 210, 210, 212, 212, 209, 208, 202, 208, 218, 213, 207, 213, 206, 197, 198, 198, 191, 192, 202, 201, 198],
    "wind_direction_500hPa": [219, 225, 229, 217, 214, 219, 212, 224, 223, 212, 220, 246, 248, 234, 245, 244, 235, 238, 229, 210, 210, 207, 213, 210, 215, 211, 211, 212, 209, 212, 213, 213, 214, 210, 207, 206, 205, 213, 212, 202, 203, 197, 195, 191, 189, 203, 205, 210]
  }
}
````

## download commmands used:

/usr/local/bin/openmeteo-api download icon-d2 --group surface
/usr/local/bin/openmeteo-api download icon-d2 --group pressureLevel

