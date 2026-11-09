# ICON precipitation storage

ICON precipitation, rain, showers, and snowfall water equivalent are stored at 0.01 mm. The scalefactor is 100. int16 saturates at 327.67 mm in one stored step. A 15-minute D2 step stays under that. A 3-hour global step can reach it.

`IconSurfaceVariable` is shared by deterministic global, EU, and D2, so those three domains use one factor. The same names on `DwdIconD2EpsGlobalVariable` use 100. EU ensemble stores `precipitation` and `snowfall_water_equivalent` at 100. Global ensemble stores `precipitation` at 100.

Convective snowfall stays at scalefactor 10. It is added into `snowfall_water_equivalent` and is not written. AICON precipitation stays at 10; that case is shared with pressure and wind. Ensemble precipitation probability stays a 0.1 mm/h test on the raw member values, before compression.

The factor is written into each OM file header, and the reader decodes from that header. Files from before this change stay at 0.1 mm until the run is downloaded again. Previous-day copies of these names pick up 100 on the next run that writes them. Temporal interpolation re-rounds with the current factor. A stored 0.1 mm value is exact at 0.01 mm.

`precipitation` is the deaccumulated DWD total. Rain and snowfall are then rewritten: convective snow is added, and snow is moved into rain when hourly 2 m temperature is above 1.5 °C or the snowfall height is more than 50 m above the grid cell. A comparison with raw GRIB can match `precipitation`. It will still differ for rain and snowfall.

Quarter-hour D2 values are the stored series on `dwd_icon_d2_native_15min` (`dtSeconds` 900), through 47 h 45 min. Reading the hourly domain at a 15-minute interval uses `backwards_sum` and spreads the hourly total. The comparison has to use the native cell. The regular 0.02° cell is a different point.
