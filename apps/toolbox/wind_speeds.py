import datetime
import numpy as np
import netCDF4 as nc
from microplastics import *
from global_land_mask import globe
import time
import pickle


def extract_wind_data():
    ds = nc.Dataset("../staticpages/era5_data/era5_winds_2021_04_01.nc")
    # (time, latitude, longitude)
    lat = np.array(ds['latitude'][:])
    lon = np.array(ds['longitude'][:])

    u10 = np.array(ds['u10'][:])  # (24, 19, 31) Eastward component
    v10 = np.array(ds['v10'][:])  # (24, 19, 31) Northward component

    # Hour 0:
    map_data = []
    for time in range(24):
        map_data_hour = []
        for lat_i in range(len(lat)):
            for lon_i in range(len(lon)):
                wind_speed = np.hypot(u10[time][lat_i][lon_i], v10[time][lat_i][lon_i])
                map_data_hour.append([lat[lat_i], lon[lon_i], wind_speed])
        map_data.append(map_data_hour)

    return map_data


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def find_nearest_peak_wind(peak_list, date):
    ds = nc.Dataset("../staticpages/era5_data/era_winds_2020_12.nc")

    u10 = np.array(ds['u10'][:])  # (720, 361, 1440) Eastward component
    v10 = np.array(ds['v10'][:])  # (720, 361, 1440) Northward component

    day = date.day

    wind_peak_list = []
    for peak in peak_list:
        # Find the closest hour of data capture
        if peak[3] > 84000:
            hour_of_day = 23 + 24*(day-1)
        else:
            time = datetime.datetime.utcfromtimestamp(peak[3])
            roundtime = time.replace(second=0, microsecond=0, minute=0, hour=time.hour) + datetime.timedelta(
                hours=time.minute // 30)
            hour_of_day = roundtime.hour + 24*(day-1)

        peak_lat = peak[0]
        peak_lon = peak[1]
        lat_index = round((peak_lat-45)/-0.25)
        lon_index = round((peak_lon + 180) / 0.25)

        # Special case, for rounding to 180 error
        if lon_index == 1440:
            lon_index = 1439

        wind_speed = np.hypot(u10[hour_of_day][lat_index][lon_index], v10[hour_of_day][lat_index][lon_index])
        peak.append(wind_speed)

    return peak_list


def remove_high_wind_peaks(peak_list, threshold):
    new_peak_list = []
    for peak in peak_list:
        if peak[6] > threshold:
            pass
        else:
            new_peak_list.append(peak)
    return new_peak_list


def remove_peaks_on_land(peak_list):
    ocean_peak_list = []
    for peak in peak_list:
        if peak[1] < -180:
            if globe.is_ocean(peak[0], peak[1] + 360):
                ocean_peak_list.append(peak)
        elif peak[1] > 180:
            if globe.is_ocean(peak[0], peak[1] - 360):
                ocean_peak_list.append(peak)
        elif globe.is_ocean(peak[0], peak[1]):
            ocean_peak_list.append(peak)

    return ocean_peak_list


# Variables:
for day in range(5, 31):
    data_list = []

    start = time.time()
    date = datetime.datetime(2020, 12, day+1)
    print(date)

    location_grid = [45, -180, -45, 180]

    print("downloading CYGNSS data")
    nbrcs_track_list = collect_nbrcs_data(date, location_grid)
    print("CYGNSS data collected")
    time1 = time.time()
    print("Elapsed time is  {}".format(time1-start))

    file = open('nbrcs_raw_'+str(date.year)+'_'+date.strftime("%B").lower()+'_'+str(day+1)+'.txt', 'wb')
    pickle.dump(nbrcs_track_list, file)
    file.close()

    print("Finding Peaks")
    raw_peak_list = generate_peak_list(nbrcs_track_list)
    print("Peaks found")
    time2 = time.time()
    print("Elapsed time is  {}".format(time2-time1))

    print("Collecting Wind data")
    peak_list = remove_high_wind_peaks(find_nearest_peak_wind(remove_peaks_on_land(raw_peak_list), date), 5)
    print("Wind data appended")
    time3 = time.time()
    print("Elapsed time is  {}".format(time3-time2))

    data_list.append(peak_list)

    file = open('data_list_'+str(date.year)+'_'+date.strftime("%B").lower()+'_'+str(day+1)+'.txt', 'wb')
    pickle.dump(data_list, file)
    file.close()
    end = time.time()
