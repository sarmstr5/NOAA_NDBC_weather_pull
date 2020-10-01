
# https://github.com/wavebitscientific/ndbc
from ndbc import Station
import pandas as pd
import datetime

# instance variables:
# wspd = wind speed (knots)
# wvht = wave height (ft)
# gst = wind gust (knots)
# atmp = air temperature (F)

#Station 46267 - Angeles Point, WA (248)
#48.173 N 123.607 W (48°10'21" N 123°36'26" W)

#has: time, wvht, DPD, APD, MWD, WTMP

#Station 46088 (LLNR 16337) - NEW DUNGENESS - 17 NM NE of Port Angeles, WA
# NOAA Environmental Lighted Buoy 46088
# 48.332 N 123.179 W (48°19'56" N 123°10'44" W)
# pulled start stop dates from looking at the buoy's historical data
# https://www.ndbc.noaa.gov/station_history.php?station=46088

start_date = datetime(2004,1,1)
end_date = datetime(2019,12,31)
swfpac_buoy = 46088
station = Station(swfpac_buoy, start_date, end_date)
station_46088_df = pd.DataFrame(data=station.wvht, index=station.time, columns=["wave_height_(ft)"])
file_path = "data/SWFPAC_open_waters_buoy46088_sig_wave_height_2004_2019.csv"
station_46088_df.to_csv(file_path)


# Station 41112 - Offshore Fernandina Beach, FL (132)
# 30.709 N 81.292 W (30°42'33" N 81°17'32" W)
# NOAA Environmental Lighted Buoy 46088
start_date = datetime(2006,1,1)
end_date = datetime(2019,12,31)
swflant_buoy = 41112
station = Station(swflant_buoy, start_date, end_date)
station_46088_df = pd.DataFrame(data=station.wvht, index=station.time, columns=["wave_height_(ft)"])
file_path = "data/SWFLANT_open_waters_buoy41112_sig_wave_height_2006_2019.csv"
station_46088_df.to_csv(file_path)

#Station PTAW1 - 9444090 - Port Angeles, WA
#48.125 N 123.441 W (48°7'29" N 123°26'28" W)



