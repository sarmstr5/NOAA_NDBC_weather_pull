#https://github.com/lkilcher/cdip
import cdip
import pandas

#SWFPAC open waters
PAC_dat = cdip.get_thredd(248, deploy="realtime")
PAC_wave_hs = PAC_dat.variables["waveHs"][:]
PAC_wave_time = PAC_dat.variables["waveTime"]
PAC_wave_info_df = pandas.DataFrame(data=PAC_wave_hs, index=PAC_wave_time, columns=["significant_wave_height (m)"])
PAC_wave_info_df.to_csv("data/SWFPAC_open_waters_buoy248_sig_wave_height.csv")

#SWFLANT open waters
LANT_dat = cdip.get_thredd(132)
LANT_wave_hs = LANT_dat.variables["waveHs"][:]
LANT_wave_time = LANT_dat.variables["waveTime"]
LANT_wave_info_df = pandas.DataFrame(data=LANT_wave_hs, index=LANT_wave_time, columns=["significant_wave_height (m)"])
LANT_wave_info_df.to_csv("data/SWFLANT_open_waters_buoy132_sig_wave_height.csv")

