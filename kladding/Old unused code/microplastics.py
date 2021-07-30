import numpy as np
import datetime
from opendap import generate_url
from pydap.client import open_url
from scipy import signal
import matplotlib.pyplot as plt
import pyproj


# Collect wind speeds:
def collect_wind_data(date, location):
    level_2_data_url = generate_url(date, "L2", "v3.0")[0]
    wind_dataset = open_url(level_2_data_url+"?lat,lon,wind_speed")

    lat = np.array(wind_dataset.lat[:])
    lon = np.array(wind_dataset.lon[:])
    wind_speed = np.array(wind_dataset.wind_speed[:])

    a = (np.where(lon > 180))
    lon[a] -= 360

    indices = np.where(
        (lat[:] < location[0])
        & (lon[:] > location[1])
        & (lat[:] > location[2]) &
        (lon[:] < location[3])
    )

    lat = lat[indices].tolist()
    lon = lon[indices].tolist()
    wind_speed = wind_speed[indices].tolist()

    # lat, lng, intensity
    wind_speed_heat = []
    for index in range(len(lat)):
        wind_speed_heat.append([lat[index], lon[index], wind_speed[index]])

    return wind_speed_heat


def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)


# Collects the CYGNSS L1 nbrcs data
def collect_nbrcs_data(date, location):
    opendap_url = generate_url(date, "L1", "v3.0")

    track_list = []

    for satellite in range(8):
        # TODO: remove print
        print("gathering info from sat: "+str(satellite))
        try:
            lat_lon_dataset = open_url(opendap_url[satellite] + "?sp_lat,sp_lon", output_grid=False)
        except:
            lat_lon_dataset = None
        if lat_lon_dataset is None:
            pass
        else:
            for ddm in range(4):
                sp_lat = np.array(lat_lon_dataset.sp_lat[:, ddm])
                sp_lon = np.array(lat_lon_dataset.sp_lon[:, ddm])
                a, b = (np.where(sp_lon > 180))
                sp_lon[a] -= 360

                indices, zero_array = np.where(
                    (sp_lat[:] < location[0])
                    & (sp_lon[:] > location[1])
                    & (sp_lat[:] > location[2]) &
                    (sp_lon[:] < location[3])
                )


                tracks = consecutive(indices)

                main_dataset = open_url(opendap_url[satellite] + "?ddm_nbrcs,ddm_timestamp_utc", output_grid=False)

                nbrcs = np.array(main_dataset['ddm_nbrcs'][:, ddm])
                ddm_timestamp_utc = np.array(main_dataset['ddm_timestamp_utc'][:])

                for track in tracks:
                    lat = sp_lat[track.min():track.max()].flatten().tolist()
                    lon = sp_lon[track.min():track.max()].flatten().tolist()
                    track_nbrcs = nbrcs[track.min():track.max()].flatten().tolist()
                    timestamp = ddm_timestamp_utc[track.min():track.max()].flatten().tolist()

                    track_list.append([lat, lon, track_nbrcs, timestamp])

    return track_list


def plot_raw_nbrcs(track):
    index = []
    y_axis = []

    for i in range(len(track[2])):
        if track[2][i] < 0:
            # skips point if no nbrcs reading.
            pass
        else:
            y_axis.append(track[2][i])
            index.append(i)
    peak_index = signal.find_peaks(y_axis, prominence=1, width=2, height=5)[0]

    return index, y_axis


# Removes null data from dataset and generates axies [x = distance, y = data]
def generate_track_axis(track):
    start_point = [track[0][0], track[1][0]]
    geod = pyproj.Geod(ellps='WGS84')
    x_axis = []
    y_axis = []

    for i in range(len(track[0])):
        this_point = [track[0][i], track[1][i]]
        distance = geod.inv(start_point[1], start_point[0], this_point[1], this_point[0])
        if track[2][i] < 0:
            y_axis.append(float('nan'))
            x_axis.append(distance[2] / 1000)
        else:
            y_axis.append(track[2][i])
            x_axis.append(distance[2] / 1000)
    x = np.array(x_axis)
    y = np.array(y_axis)

    return x, y


# Interpolate the track giving us values for all the points.
def interpolate_track(track):
    x, y = generate_track_axis(track)
    t, dt = np.linspace(0, x[-1], len(x), retstep=True)
    t0 = np.arange(0, len(x))
    np.all(np.diff(y) > 0)
    intp_data = np.interp(t, x[~np.isnan(y)], y[~np.isnan(y)])
    return t0, intp_data


def smoothen_data(nbrcs_data, kernel_size):
    kernel = np.ones(kernel_size) / kernel_size
    data_convolved = np.convolve(nbrcs_data, kernel, mode='same')  #smoothed data
    return data_convolved


def find_track_peaks(data, prominence, width):
    peak_indices, peak_properties = signal.find_peaks(data, prominence=prominence, width=width)

    return peak_indices, peak_properties


def generate_peak_list(track_list):
    peak_list = []
    for track in track_list:
        if len(track[0]) > 15 and np.average(track[2]) != -9999: # ignore "short" dataset
            t0, intp = interpolate_track(track)

            intp = 10*(np.log(intp)) # Convert nbrcs data to Db scale

            data_convolved = smoothen_data(intp, 5)

            peak_index, properties = find_track_peaks(data_convolved, 1, 3)

            prominences = properties['prominences']
            widths = properties['widths']




            i = 0
            for peak in peak_index:
                peak_list.append([track[0][peak], track[1][peak], intp[peak], track[3][peak], prominences[i], widths[i]])
                i = i+1
        else:
            pass

    return peak_list

