import json
from datetime import datetime as dt
import numpy as np
import os
import matplotlib.pyplot as plt


def load_json_data(filepath):
    file_object = open(filepath, "r")
    json_content = file_object.read()
    json_array = json.loads(json_content)
    return json_array


# Converts time object from ordinal time to ISO standard 8601
def ordinal_to_iso(time):
    time = time-365
    date = dt.fromordinal(int(time)).date()
    second_of_day = (time-int(time))*24*60*60
    hour = int(np.floor(second_of_day/3600))
    minute = int(np.floor((second_of_day/60/60-hour)*60))
    second = int(np.floor(second_of_day-hour*3600-minute*60))
    time_string = "%sT%02d:%02d:%02dZ" %(date, hour, minute, second)
    return dt.strptime(time_string, "%Y-%m-%dT%H:%M:%S%z")


def collect_sea_levels():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sea_level.json")
    sea_level = load_json_data(file)
    ssl_labels = []
    levels = []

    for measure in sea_level:
        ssl_labels.append(ordinal_to_iso(measure["time"]))
        levels.append(measure["sea_level"])

    step = int(np.floor(len(levels)/100))

    return ssl_labels[0:len(ssl_labels):step], levels[0:len(ssl_labels):step]


def collect_sea_roughness():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sea_roughness.json")
    sea_roughness = load_json_data(file)
    ssr_labels = []
    roughness = []

    for measure in sea_roughness:
        ssr_labels.append(ordinal_to_iso(measure["time"]))
        roughness.append(measure["roughness"]*100)

    step = int(np.floor(len(roughness) / 100))

    return ssr_labels[0:len(ssr_labels):step], roughness[0:len(roughness):step]


def collect_sat_info():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "satellites_info.json")
    data = load_json_data(file)

    sat_info = []
    satellite_coordinates = []

    for measure in data:
        time = (ordinal_to_iso(measure["time"]))
        sat_info.append([measure["sat_prn"], measure["sat_elevation"], measure["sat_azimuth"], time])
        satellite_coordinates.append([measure["sat_prn"], measure["sp_lat"], measure["sp_lon"]])

    # Split the data into separate arrays for satellites by PRN number

    separate_satellites = np.split(np.array(sat_info), np.where(np.diff(np.array(sat_info)[:, 0]))[0]+1)

    table_info = []
    elevation_data = []

    for satellite in separate_satellites:
        prn = int(satellite[0][0])
        elevation_min = str(round(min(satellite[:, 1]), 1)) + "°"
        elevation_max = str(round(max(satellite[:, 1]), 1)) + "°"
        azimuth_min = str(round(min(satellite[:, 2]), 1)) + "°"
        azimuth_max = str(round(max(satellite[:, 2]), 1)) + "°"
        table_info.append([prn, elevation_min, elevation_max, azimuth_min, azimuth_max])
        elevation_data.append([prn, satellite[:, 1], satellite[:, 2]])

    satellite_coordinates = np.split(np.array(satellite_coordinates), np.where(np.diff(np.array(satellite_coordinates)[:, 0]))[0] + 1)
    coordinates = []
    for satellite in satellite_coordinates:
        prn = int(satellite[0][0])
        lat = satellite[:, 1]
        lon = satellite[:, 2]
        coordinates.append([prn, lat, lon])


    return table_info, coordinates, elevation_data


def raw_measure_info():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "raw_observations.json")
    data = load_json_data(file)

    raw_data = []

    for measure in data:
        time = (ordinal_to_iso(measure["time"]))
        raw_data.append([measure["sat_prn"], measure["Mst_raw_I"], measure["Mst_raw_q"], measure["Cpo_raw_I"],
                         measure["Cpo_raw_q"], measure["Xpo_raw_I"], measure["Xpo_raw_q"], time])

    # Split the data into separate arrays for satellites by PRN number
    raw_data = np.split(np.array(raw_data), np.where(np.diff(np.array(raw_data)[:, 0]))[0]+1)

    raw_chart_data = []

    for satellite in raw_data:
        prn = int(satellite[0][0])
        Mst_raw_I = satellite[:, 1]
        Mst_raw_q = satellite[:, 2]
        Cpo_raw_I = satellite[:, 3]
        Cpo_raw_q = satellite[:, 4]
        Xpo_raw_I = satellite[:, 5]
        Xpo_raw_q = satellite[:, 6]
        time = satellite[:, 7]

        raw_chart_data.append([prn, Mst_raw_I, Mst_raw_q, Cpo_raw_I, Cpo_raw_q, Xpo_raw_I, Xpo_raw_q, time])

    return raw_chart_data


def interferometric_fringe_info():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "interferometric_fringe.json")
    data = load_json_data(file)

    intf_data = []

    for measure in data:
        time = (ordinal_to_iso(measure["time"]))
        intf_data.append([measure["sat_prn"], measure["Mst_int_I"], measure["Mst_int_q"], measure["Cpo_int_I"],
                         measure["Cpo_int_q"], measure["Xpo_int_I"], measure["Xpo_int_q"], time])

    # Split the data into separate arrays for satellites by PRN number
    intf_data = np.split(np.array(intf_data), np.where(np.diff(np.array(intf_data)[:, 0]))[0]+1)

    intf_chart_data = []

    for satellite in intf_data:
        prn = int(satellite[0][0])
        Mst_int_I = satellite[:, 1]
        Mst_int_q = satellite[:, 2]
        Cpo_int_I = satellite[:, 3]
        Cpo_int_q = satellite[:, 4]
        Xpo_int_I = satellite[:, 5]
        Xpo_int_q = satellite[:, 6]
        time = satellite[:, 7]

        intf_chart_data.append([prn, Mst_int_I, Mst_int_q, Cpo_int_I, Cpo_int_q, Xpo_int_I, Xpo_int_q, time])

    return intf_chart_data



# TODO: - Separate the data into unique satellites
# TODO: - Plot the trajectory for each satellite with given cutoff angle
def skyplot():
    # Polar coordinates -> polar(azi, ele)
    return None