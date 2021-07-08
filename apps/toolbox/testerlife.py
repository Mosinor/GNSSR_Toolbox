import datetime
import numpy as np
import netCDF4 as nc
from global_land_mask import globe
import time
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from geographiclib.geodesic import Geodesic
import pyproj
from scipy import signal, interpolate
from scipy.ndimage.filters import uniform_filter1d
import calendar


# Fixed the axis and interpolated the data
def interpolate_track(track):
    # X-axis should be along track distance
    geod = pyproj.Geod(ellps='WGS84')
    lats = track[1]
    lons = track[0]

    distance = 0
    distances = [0]
    for i in range(len(lats)-1):
        distance += geod.inv(lats[i], lons[i], lats[i+1], lons[i+1])[2]
        distances.append(distance)
    x = distances

    # Y-axis is NBRCS in log10 scale
    y = 10*np.log(track[2])

    t, dt = np.linspace(0, x[-1], len(x), retstep=True)
    t0 = np.arange(0, len(x))

    intp_data = np.interp(t, x, y)

    return t0, intp_data


def smoothen_data(nbrcs_data, kernel_size):
    kernel = np.ones(kernel_size) / kernel_size
    data_convolved = np.convolve(nbrcs_data, kernel, mode='same')  #smoothed data

    return data_convolved


def find_track_peaks(data, prominence, width):
    peak_indices, peak_properties = signal.find_peaks(data, prominence=prominence, width=width)

    return peak_indices, peak_properties


# Removes all rows for a track where NBRCS values are negative.
def remove_null_data(track):

    nbrcs_list = np.array(track[2])
    indexNull = np.where(nbrcs_list < 0)
    track_list = np.delete(track, indexNull, 1)

    return track_list


# Seoarates tracks if distance between two points are large.
def separate_track_length(track):
    subtracks = []

    geod = pyproj.Geod(ellps='WGS84')
    lats = track[1]
    lons = track[0]

    start = 0
    for i in range(len(lats) - 1):
        length = geod.inv(lats[i], lons[i], lats[i + 1], lons[i + 1])[2]

        # If difference between points are bigger than 100 km
        if length > 100000:
            subtrack = []

            for variable in track:
                subtrack.append(variable[start:i])

            subtracks.append(subtrack)

            start = i

    if len(subtracks) > 0:

        if not start == len(track[0]):
            subtrack = []
            for variable in track:
                subtrack.append(variable[start:len(track[0])])
            subtracks.append(subtrack)

    return subtracks


def plot_track_map(track):
    x = track[1]
    y = track[0]
    z = track[2]

    m = Basemap(llcrnrlon=-180.1, llcrnrlat=-40.1, urcrnrlon=180.1, urcrnrlat=40.1)
    m.drawcoastlines(linewidth=0.5)
    m.fillcontinents(color='gray')

    scat = m.scatter(x, y, c=z, s=1)

    m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])
    m.drawparallels([-40, 0, 40], labels=[1, 1, 0, 0])

    plt.show()


# Takes in a track and returns list of peaks with relevant data.
def find_peaks(track):
    peak_list = []

    # X-axis should be along track distance
    geod = pyproj.Geod(ellps='WGS84')
    lats = track[0]
    lons = track[1]

    distance = 0
    distances = [0]
    for i in range(len(lats) - 1):
        distance += geod.inv(lats[i], lons[i], lats[i + 1], lons[i + 1])[2]
        distances.append(distance)
    x = np.array(distances)

    y = np.array(10 * np.log(track[2]))

    # Apply filter to the data in order to get a smooth, continuous curve representation of the data
    smoothened_y = uniform_filter1d(y, size=10)

    peak_index, properties = find_track_peaks(smoothened_y, 1, 5)

    prominences = properties['prominences']
    widths = properties['widths']

    i = 0
    for peak in peak_index:
        peak_list.append([track[0][peak], track[1][peak], y[peak], track[3][peak], prominences[i], widths[i]])
        i = i + 1

    return peak_list


def plot_track_nbrcs(track):
    geod = pyproj.Geod(ellps='WGS84')
    lats = track[1]
    lons = track[0]

    distance = 0
    distances = [0]
    for i in range(len(lats) - 1):
        distance += geod.inv(lats[i], lons[i], lats[i + 1], lons[i + 1])[2]
        distances.append(distance)
    x = np.array(distances)

    y = np.array(10 * np.log(track[2]))

    # Apply filter to the data in order to get a smooth, continuous curve representation of the data
    smoothened_y = uniform_filter1d(y, size=10)

    peak_index, properties = find_track_peaks(smoothened_y, 1, 5)

    plt.title("NBRCS along track")
    plt.xlabel("Track distance [m]")
    plt.ylabel("NBRCS reading [log10 scale]")

    plt.scatter(x, y, alpha=0.5, color='#5e3c99', marker='o', zorder=2, label="Raw NBRCS")

    plt.plot(x, smoothened_y, color='#fdb863', zorder=3, label="Smoothened NBRCS")

    plt.scatter(x[peak_index], smoothened_y[peak_index], color='#e66101', marker='x', zorder=4, label="Peak")

    ax = plt.axes()
    ax.set_facecolor("#b2abd2")



    plt.show()


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


def find_nearest_peak_wind(peak_list, date, ds):
    day = date.day

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

        lat_index = round((peak_lat - 45) / -0.25)
        lon_index = round((peak_lon + 180) / 0.25)


        # Special case, for rounding to 180 error
        if lon_index == 1440:
            lon_index = 1439

        wind_speed = np.hypot(ds['u10'][hour_of_day][lat_index][lon_index], ds['v10'][hour_of_day][lat_index][lon_index])
        peak.append(wind_speed)

    return peak_list


# removes all data points with a designated "bad quality" flag
def remove_bad_quality(track):
    track = np.array(track)

    bad_quality_indices = np.where(np.mod(track[4], 2) != 0)
    good_quality_track = np.delete(track, bad_quality_indices, 1)

    return good_quality_track


def process_track_peak_list(track):
    track = remove_bad_quality(remove_null_data(raw_track))
    peak_list = []

    # We only inspect peaks for tracks of minimum 50 data points.
    if len(track[0]) > 50:
        peak_list = remove_peaks_on_land(find_peaks(track))
        find_nearest_peak_wind(peak_list, date, wind_data)
        peak_list = remove_high_wind_peaks(peak_list, 5)

    return peak_list



# Use this if you want to plot NBRCS tracks to check
date = datetime.date(2020, 4, 1)

file = open('D:/GNSS-R Data/Track_separation/' + str(date.year) + '-' + str('%02d' % date.month) + '/track_list' + str(
    date.year) + '_' + date.strftime("%B").lower() + '_' + str(date.day + 1) + '.txt', 'rb')

nbrcs_tracks = pickle.load(file)
file.close()

for track in nbrcs_tracks[0:100]:
    track_no_null = remove_null_data(track)
    track_good = remove_bad_quality(track_no_null)

    if len(track_good[0]) > 50:
        plot_track_nbrcs(track_no_null)



# Use this to process

year = 2017
# calendar.monthrange(year, month)[1]
for month in [3]:
    for day in range(17, calendar.monthrange(year, month)[1]):
        complete_peak_list = []
        date = datetime.date(year, month, day+1)
        print(date)

        file = open('D:/GNSS-R Data/Track_separation/'+str(date.year)+'-'+str('%02d' % date.month)+'/track_list' + str(date.year) + '_' + date.strftime("%B").lower() + '_' + str(day + 1) + '.txt', 'rb')
        nbrcs_tracks = pickle.load(file)
        file.close()

        wind_data = nc.Dataset("D:/GNSS-R Data/era5_data/era_winds_"+str(date.year)+"_"+str('%02d' % date.month)+".nc")

        for raw_track in nbrcs_tracks:
            subtracks = separate_track_length(raw_track)

            if subtracks == []:
                peaks = process_track_peak_list(raw_track)

                if not peaks == []:
                    for peak in peaks:
                        complete_peak_list.append(peak)
            else:
                for subtrack in subtracks:
                    peaks = process_track_peak_list(subtrack)

                    if not peaks == []:
                        for peak in peaks:
                            complete_peak_list.append(peak)


        file = open('D:/GNSS-R Data/Peak_list/'+str(date.year)+'-'+str('%02d' % date.month)+'/Complete_peak_list_'+str(date.year)+'_'+date.strftime("%B").lower()+'_'+str(day+1)+'.txt', 'wb')
        pickle.dump(complete_peak_list, file)
        file.close()
        print("fin")
