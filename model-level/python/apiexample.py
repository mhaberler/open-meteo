import openmeteo_requests

import json
import pandas as pd
import requests_cache
from retry_requests import retry
import urllib, time

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"
url = "https://open-meteo.mah.priv.at/v1/forecast"
META = "https://open-meteo.mah.priv.at/data/dwd_icon_d2/static/meta.json"


# Last ICON-D2 model run + forecast end (read from the domain meta.json).
def _utc(ts):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(ts))


with urllib.request.urlopen(META, timeout=30) as f:
    _m = json.load(f)
RUN_INIT = _utc(_m["last_run_initialisation_time"])  # e.g. 2026-06-15T09:00Z
FCST_END = _utc(_m["data_end_time"])  # e.g. 2026-06-17T10:00Z
LEVELS = range(1, 66)
LAT, LON = 48.717, 8.750
TARGET = "2026-06-17T06:00"


# Dew(C), Dir(deg), Spd(m/s) now come straight from the server-side derived
# model-level vars dew_point/wind_direction/wind_speed (no client-side math).
vars = []
for n in LEVELS:
    vars += [
        f"height_level{n}",
        f"pressure_level{n}",
        f"temperature_level{n}",
        f"relative_humidity_level{n}",
        f"dew_point_level{n}",
        f"wind_speed_level{n}",
        f"wind_direction_level{n}",
    ]


params = {
    "models": "icon_d2",
    "forecast_days": 1,
    "latitude": LAT,
    "longitude": LON,
    "hourly": ",".join(vars),
    "models": "icon_d2",
    "wind_speed_unit": "ms",
    "timezone": "GMT",
}
responses = openmeteo.weather_api(url, params=params)

json_response = retry_session.get(url, params=params).json()
print(json.dumps(json_response, indent=2))
# Process first location. Add a for-loop for multiple locations or weather models


# response = responses[0]
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# # Process hourly data. The order of variables needs to be the same as requested.
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()

# hourly_data = {
#     "date": pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#         freq=pd.Timedelta(seconds=hourly.Interval()),
#         inclusive="left",
#     )
# }

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

# hourly_dataframe = pd.DataFrame(data=hourly_data)
# print("\nHourly data\n", hourly_dataframe)

print(f"# run {RUN_INIT} (init), forecast to {FCST_END}")
