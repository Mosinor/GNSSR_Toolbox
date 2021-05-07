import json
from datetime import datetime as dt
from datetime import timedelta
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


def datetime_array_to_string(array):
    string_array = []
    for datetime_object in array:
        string_array.append(datetime_object.strftime("%Y-%m-%dT%H:%M:%SZ"))

    return string_array


def collect_sea_levels():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sea_level.json")
    sea_level = load_json_data(file)
    ssl_timestamps = []
    levels = []

    for measure in sea_level:
        ssl_timestamps.append(ordinal_to_iso(measure["time"]))
        levels.append(measure["sea_level"])

    ssl_labels = datetime_array_to_string(ssl_timestamps)

    step = int(np.floor(len(levels)/100))

    return ssl_labels[0:len(ssl_labels):step], levels[0:len(ssl_labels):step]


def collect_sea_roughness():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sea_roughness.json")
    sea_roughness = load_json_data(file)
    ssr_timestamps = []
    roughness = []

    for measure in sea_roughness:
        ssr_timestamps.append(ordinal_to_iso(measure["time"]))
        roughness.append(measure["roughness"]*100)

    ssr_labels = datetime_array_to_string(ssr_timestamps)

    step = int(np.floor(len(roughness) / 100))

    return ssr_labels[0:len(ssr_labels):step], roughness[0:len(roughness):step]


def collect_sat_info():
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "satellites_info.json")
    data = load_json_data(file)

    sat_info = []

    for measure in data:
        time = (ordinal_to_iso(measure["time"]))
        sat_info.append([measure["sat_prn"], measure["sat_elevation"], measure["sat_azimuth"], time, measure["sp_lat"], measure["sp_lon"]])

    # Split the data into separate arrays for satellites by when PRN change is detected.
    separate_satellites_prn = np.split(np.array(sat_info), np.where(np.diff(np.array(sat_info)[:, 0]))[0]+1)

    # Also check for big difference in timestamp
    separate_satellites = []
    event = False
    a = 0
    for satellite in separate_satellites_prn:
        split = []
        for t in range(0, len(satellite) - 1):
            if satellite[t + 1][3] - satellite[t][3] > timedelta(minutes=1):
                event = True
                split.append(t+1)
        if event:
            atcho = np.split(satellite, split)

            separate_satellites.append(atcho[0])
            separate_satellites.append(atcho[1])

            event = False
        else:
            separate_satellites.append(satellite)

    table_info = []
    elevation_data = []

    for satellite in separate_satellites:
        prn = int(satellite[0][0])
        elevation_min = str(round(min(satellite[:, 1]), 1)) + "°"
        elevation_max = str(round(max(satellite[:, 1]), 1)) + "°"
        azimuth_min = str(round(min(satellite[:, 2]), 1)) + "°"
        azimuth_max = str(round(max(satellite[:, 2]), 1)) + "°"
        table_info.append([prn, elevation_min, elevation_max, azimuth_min, azimuth_max])
        elevation_data.append([prn, satellite[:, 1].tolist(), satellite[:, 2].tolist()])

    coordinates = []
    for satellite in separate_satellites:
        prn = int(satellite[0][0])
        lat = satellite[:, 4]
        lon = satellite[:, 5]
        time = datetime_array_to_string(satellite[:, 3])
        elevation = satellite[:, 2]
        azimuth = satellite[:, 1]
        coordinates.append([prn, lat.tolist(), lon.tolist(), time, elevation.tolist(), azimuth.tolist()])

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
    raw_data_prn = np.split(np.array(raw_data), np.where(np.diff(np.array(raw_data)[:, 0]))[0]+1)

    # Also check for big difference in timestamp
    separate_satellites = []
    event = False
    a = 0
    for satellite in raw_data_prn:

        split = []
        for t in range(0, len(satellite) - 1):
            if satellite[t + 1][7] - satellite[t][7] > timedelta(minutes=1):
                event = True
                split.append(t+1)
        if event:
            atcho = np.split(satellite, split)

            separate_satellites.append(atcho[0])
            separate_satellites.append(atcho[1])

            event = False
        else:
            separate_satellites.append(satellite)

    raw_chart_data = []

    for satellite in separate_satellites:

        prn = int(satellite[0][0])
        Mst_raw_I = satellite[:, 1]
        Mst_raw_q = satellite[:, 2]
        Cpo_raw_I = satellite[:, 3]
        Cpo_raw_q = satellite[:, 4]
        Xpo_raw_I = satellite[:, 5]
        Xpo_raw_q = satellite[:, 6]
        time = datetime_array_to_string(satellite[:, 7])

        raw_chart_data.append([prn, Mst_raw_I.tolist(), Mst_raw_q.tolist(), Cpo_raw_I.tolist(), Cpo_raw_q.tolist(), Xpo_raw_I.tolist(), Xpo_raw_q.tolist(), time])

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
    intf_data_prn = np.split(np.array(intf_data), np.where(np.diff(np.array(intf_data)[:, 0]))[0]+1)

    # Also check for big difference in timestamp
    separate_satellites = []
    event = False
    a = 0
    for satellite in intf_data_prn:

        split = []
        for t in range(0, len(satellite) - 1):
            if satellite[t + 1][7] - satellite[t][7] > timedelta(minutes=1):
                event = True
                split.append(t+1)
        if event:
            atcho = np.split(satellite, split)

            separate_satellites.append(atcho[0])
            separate_satellites.append(atcho[1])

            event = False
        else:
            separate_satellites.append(satellite)

    intf_chart_data = []

    for satellite in separate_satellites:

        prn = int(satellite[0][0])
        Mst_int_I = satellite[:, 1]
        Mst_int_I[Mst_int_I == None] = 0
        Mst_int_q = satellite[:, 2]
        Mst_int_q[Mst_int_q == None] = 0

        Cpo_int_I = satellite[:, 3]
        Cpo_int_I[Cpo_int_I == None] = 0

        Cpo_int_q = satellite[:, 4]
        Cpo_int_q[Cpo_int_q == None] = 0

        Xpo_int_I = satellite[:, 5]
        Xpo_int_I[Xpo_int_I == None] = 0

        Xpo_int_q = satellite[:, 6]
        Xpo_int_q[Xpo_int_q == None] = 0

        time = datetime_array_to_string(satellite[:, 7])

        intf_chart_data.append([prn, Mst_int_I.tolist(), Mst_int_q.tolist(), Cpo_int_I.tolist(), Cpo_int_q.tolist(), Xpo_int_I.tolist(), Xpo_int_q.tolist(), time])

    return intf_chart_data
