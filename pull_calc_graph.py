# https://github.com/lkilcher/cdip
# https://github.com/wavebitscientific/ndbc
import cdip
from ndbc import Station

from datetime import datetime
import pandas as pd
import numpy as np

def get_ndbc_df(buoy, start_date, end_date, SWF):
    #save?
    station = Station(buoy, start_date, end_date)
    df = pd.DataFrame(data=station.wvht, index=station.time, columns=["wave_height_(m)"])
    df = remove_data_NAs(df)
    df = create_sea_state_col(df)
    return df

def get_cdip_df(buoy, SWF, realtime):
    # SWFPAC buoy 248 does not have historic data, has to be pulled as "realtime"
    # SWFLANT buoy 132 can be pulled without arguement, but the last couple of months has to be pulled with realtime
    if realtime:
        dat = cdip.get_thredd(buoy, deploy="realtime")
    else:
        dat = cdip.get_thredd(buoy)
    wave_hs = dat.variables["waveHs"][:]
    wave_time = pd.to_datetime(dat.variables["waveTime"][:], unit='s')
    df = pd.DataFrame(data=wave_hs, index=wave_time, columns=["wave_height_(m)"])
    df = remove_data_NAs(df)
    df = create_sea_state_col(df)
    return df

def remove_data_NAs(df):
    #this dataset fills missing values with the value 99 (int)
    df = df[df['wave_height_(m)'] != 99]
    df = df.dropna()
    return df

def date_time_conversions(df):
    df['date_time'] = pd.to_datetime(df['date_time'])
    df = df.set_index("date_time")
    return df

def create_sea_state_col(df):
    """
    sea state 0-1 - 0-.1, mean=0.05
    sea state 2 - 0.1-.5, mean=0.30
    sea state 3 - 0.5 - 1.25, mean = 0.88
    sea state 4 - 1.25 - 2.5, mean = 1.88
    sea state 5 - 2.5 - 4, mean = 3.25
    sea state 6+ - 4<x
    """
    bins = [0, .1, 0.5, 1.25, 2.5, 4]
    names = [1, 2, 3, 4, 5, 6] #maybe '6+'?
    sea_state_dict = dict(enumerate(names, 1))
    df['sea_state'] = np.vectorize(sea_state_dict.get)(np.digitize(df['wave_height_(m)'], bins))
    return df

def create_and_save_dfs(df, max_wave_fn, sea_state_count_fn):
    max_wave_df = create_daily_max_df(df)
    sea_state_count = create_daily_sea_state_count_df(max_wave_df)
    max_wave_df.to_csv(max_wave_fn)
    sea_state_count.to_csv(sea_state_count_fn)

def create_daily_max_df(df):
    daily_max_df = df.groupby(pd.Grouper(freq='D')).max()
    return daily_max_df

def create_daily_sea_state_count_df(df):
    sea_state_count_df = df.groupby(by="sea_state").agg('count')
    return sea_state_count_df


def main():
    run_SWFLANT = True
    run_SWFPAC = False #True
    run_ndbc_pull = True
    run_cdip_pull = False #True
    create_sea_state_count = True

    if run_SWFLANT:
        SWF = "SWFLANT"
        if run_ndbc_pull:
            # buoy = 41112
            buoy = 41008
            website = "NDBC"
            max_wave_fn = "data/{}_open_waters_buoy{}_max_sig_wave_height_{}.csv".format(SWF, buoy, website)
            sea_state_count_fn = "data/{}_open_waters_buoy{}_sea_state_counts_{}".format(SWF, buoy, website)
            # pulled start stop dates from looking at the buoy's historical data
            # https: // www.ndbc.noaa.gov / station_history.php?station = 41112
            start_date = datetime(2006, 1, 1)
            end_date = datetime(2019, 12, 31)
            df = get_ndbc_df(buoy, start_date, end_date, SWF)
            create_and_save_dfs(df, max_wave_fn, sea_state_count_fn)

        if run_cdip_pull:
            buoy = 132
            website = "CDIP"
            max_wave_fn = "data/{}_open_waters_buoy{}_max_sig_wave_height_{}.csv".format(SWF, buoy, website)
            sea_state_count_fn = "data/{}_open_waters_buoy{}_sea_state_counts_{}".format(SWF, buoy, website)
            realtime = False
            df = get_cdip_df(buoy, SWF, realtime)
            create_and_save_dfs(df, max_wave_fn, sea_state_count_fn)

    if run_SWFPAC:
        SWF = "SWFPAC"
        if run_ndbc_pull:
            buoy = 46088
            website = "NDBC"
            max_wave_fn = "data/{}_open_waters_buoy{}_max_sig_wave_height_{}.csv".format(SWF, buoy, website)
            sea_state_count_fn = "data/{}_open_waters_buoy{}_sea_state_counts_{}".format(SWF, buoy, website)
            # pulled start stop dates from looking at the buoy's historical data
            # https://www.ndbc.noaa.gov/station_history.php?station=46088
            start_date = datetime(2004, 1, 1)
            end_date = datetime(2019, 12, 31)
            df = get_ndbc_df(buoy, start_date, end_date, SWF)
            create_and_save_dfs(df, max_wave_fn, sea_state_count_fn)

        if run_cdip_pull:
            buoy = 248
            website = "CDIP"
            max_wave_fn = "data/{}_open_waters_buoy{}_max_sig_wave_height_{}.csv".format(SWF, buoy, website)
            sea_state_count_fn = "data/{}_open_waters_buoy{}_sea_state_counts_{}".format(SWF, buoy, website)
            realtime = True
            df = get_cdip_df(buoy, SWF, realtime)
            create_and_save_dfs(df, max_wave_fn, sea_state_count_fn)

if __name__ == '__main__':
    main()
