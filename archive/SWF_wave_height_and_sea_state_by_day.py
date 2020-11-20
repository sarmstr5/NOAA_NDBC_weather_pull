#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import numpy as np


# In[ ]:


os.listdir(os.curdir)
os.listdir("../data")


# In[ ]:


pac_data_fn = 'data/SWFPAC_open_waters_buoy46088_sig_wave_height_2004_2019.csv'
pac_df = pd.read_csv(pac_data_fn)
pac_df.columns = ["date_time", "wave_height_(ft)"]
pac_df.tail()


# In[ ]:


def remove_data_NAs(df):
    #this dataset fills missing values with the value 99 (int)
    df = df[df['wave_height_(ft)'] != 99]
    return df

# converting to metric for calculations (and sea state comparisons) and date_time for pandas
# could create new column for meters, so there are feet and meters for comparisons
def col_conversions(df):
    ft_to_meters_ratio = 0.3048
    df['wave_height_(ft)'] = df['wave_height_(ft)'].apply(lambda ft: ft*ft_to_meters_ratio)
    df.columns = ["date_time", "wave_height_(m)"]
    df['date_time'] = pd.to_datetime(df['date_time'])
    df = df.set_index("date_time")
    return df

#sea state 1 - 0-.1, mean=0.05
#sea state 2 - 0.1-.5, mean=0.30
#sea state 3 - 0.5 - 1.25, mean = 0.88
#sea state 4 - 1.25 - 2.5, mean = 1.88
#sea state 5 - 2.5 - 4, mean = 3.25
#sea state 6+ - 4<x
def create_sea_state_col(df):
    bins = [0, .1, 0.5, 1.25, 2.5, 4]
    names = [1, 2, 3, 4, 5, 6] #maybe '6+'?
    sea_state_dict = dict(enumerate(names, 1))
    df['sea_state'] = np.vectorize(sea_state_dict.get)(np.digitize(df['wave_height_(m)'], bins))
    return df


# In[ ]:


pac_df = remove_data_NAs(pac_df)
pac_df = col_conversions(pac_df)
pac_sea_state_df = create_sea_state_col(pac_df)
pac_sea_state_df.head()


# In[ ]:


pac_max_df = pac_sea_state_df.groupby(pd.Grouper(freq='D')).max()
pac_max_df.head()


# In[ ]:


pac_sea_state_count_df = pac_max_df.groupby(by="sea_state").agg('count')
pac_sea_state_count_df
pac_df.loc["2004-07-31"]


# In[ ]:


pac_max_sea_state_fn = 'data/SWFPAC_open_waters_buoy46088_mWH&seastate_2004_2019.csv'
pac_sea_state_count_fn = 'data/SWFPAC_open_waters_buoy46088_sea_state_counts_2004_2019.csv'


# In[ ]:


pac_max_df.to_csv(pac_max_sea_state_fn)
pac_sea_state_count_df.to_csv(pac_sea_state_count_fn)


# In[ ]:


""" doing lant now
-----------------------------------------
"""


# In[ ]:


lant_data_fn = 'data/SWFLANT_open_waters_buoy41112_sig_wave_height_2006_2019.csv'
lant_df = pd.read_csv(lant_data_fn)
lant_df.columns = ["date_time", "wave_height_(ft)"]
lant_df.head()


# In[ ]:


lant_df = remove_data_NAs(lant_df)
lant_df = col_conversions(lant_df)
lant_sea_state_df = create_sea_state_col(lant_df)
lant_sea_state_df.head()


# In[ ]:


lant_max_df = lant_sea_state_df.groupby(pd.Grouper(freq='D')).max()
lant_max_df.head()


# In[ ]:


lant_sea_state_count_df = lant_max_df.groupby(by="sea_state").agg('count')
lant_sea_state_count_df
# lant_df.loc["2004-07-31"]


# In[ ]:


lant_max_sea_state_fn = 'data/SWFLANT_open_waters_buoy41112_mWH&seastate_2006_2019.csv'
lant_sea_state_count_fn = 'data/SWFLANT_open_waters_buoy41112_sea_state_counts_2006_2019.csv'
lant_max_df.to_csv(lant_max_sea_state_fn)
lant_sea_state_count_df.to_csv(lant_sea_state_count_fn)


# In[ ]:





# In[ ]:




