from pydap.client import open_url
from pydap.cas.urs import setup_session
import wget
import numpy as np
import datetime
from .opendap import generate_url


def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)


def collect_level_1_demo_data(date, location, start_time, end_time, level, version, graph_variables):
    opendap_url = generate_url(date, level, version)
    print(location)

    track_list = []

    for satellite_number in range(1):
        print("Starting scan for satellite: " + str(satellite_number))
        try:
            lat_lon_dataset = open_url(opendap_url[satellite_number] + "?sp_lat,sp_lon", output_grid=False)
        except:
            print("anomaly in link")
            break

        for ddm in range(4):
            print("ddm: " + str(ddm))
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

            if any(tracks[0]):
                y_axis_2 = []
                if graph_variables[2] != 'none':
                    rest_dataset = open_url(
                        opendap_url[satellite_number] + "?ddm_timestamp_utc,prn_code," + graph_variables[1] + "," + graph_variables[2],
                        output_grid=False)
                    y_axis_2 = np.array(rest_dataset[graph_variables[2]][:, ddm])
                else:
                    rest_dataset = open_url(opendap_url[satellite_number] + "?ddm_timestamp_utc,prn_code," + graph_variables[1], output_grid=False)
                ddm_timestamp_utc = np.array(rest_dataset.ddm_timestamp_utc[:, ddm])
                prn_code = np.array(rest_dataset.prn_code[:, ddm])
                y_axis = np.array(rest_dataset[graph_variables[1]][:, ddm])

                i = 1
                for track in tracks:
                    lat = sp_lat[track.min():track.max()].flatten().tolist()
                    lon = sp_lon[track.min():track.max()].flatten().tolist()
                    ddm_timestamp_utc_list = ddm_timestamp_utc[track.min():track.max()].tolist()
                    prn_code_list = prn_code[track.min():track.max()].tolist()
                    y_axis_list = y_axis[track.min():track.max()].tolist()
                    y_axis_2_list = []

                    if any(y_axis_2):
                        y_axis_2_list = y_axis_2[track.min():track.max()].tolist()

                    track_id = (satellite_number)*10+ddm+0.1*i
                    i += i

                    x_axis = []
                    if graph_variables[0] == 'time':
                        x_axis = ddm_timestamp_utc_list
                    elif graph_variables[0] == 'length':
                        # TODO: Create code for measuring length of track
                        x_axis = np.arange(len(lat)).tolist()
                    elif graph_variables[0] == 'step':
                        x_axis = np.arange(len(lat)).tolist()

                    track_list.append([lat, lon, ddm_timestamp_utc_list, prn_code_list, (np.ones(len(lat))*satellite_number).flatten().tolist(), (np.ones(len(lat))*ddm).flatten().tolist(), x_axis, y_axis_list, y_axis_2_list, track_id])
            else:
                pass

        print(track_list)

    return track_list, opendap_url


def collect_level_2_demo_data(date, location, start_time, end_time, level, version, graph_variables):
    opendap_url = generate_url(date, level, version)

    try:
        lat_lon_dataset = open_url(opendap_url[0] + "?lat,lon,sample_time,prn_code,num_ddms_utilized,spacecraft_num", output_grid=False)
    except:
        lat_lon_dataset = []
        print("anomaly in link")

    lat = np.array(lat_lon_dataset.lat[:])
    lon = np.array(lat_lon_dataset.lon[:])
    sample_time = np.array(lat_lon_dataset.sample_time[:])
    prn_code = np.array(lat_lon_dataset.prn_code[:])
    ddm_num = np.array(lat_lon_dataset.num_ddms_utilized[:])
    cygnss_sc_num = np.array(lat_lon_dataset.spacecraft_num[:])

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
    time = sample_time[indices].tolist()
    prn = prn_code[indices].tolist()
    ddm = ddm_num[indices].tolist()
    cygnss_num = cygnss_sc_num[indices].tolist()

    x_axis = []
    if graph_variables[0] == 'time':
        x_axis = time
    elif graph_variables[0] == 'length':
        # TODO: Create code for measuring length of track
        x_axis = np.arange(len(time)).tolist()
    elif graph_variables[0] == 'step':
        x_axis = np.arange(len(time)).tolist()


    y_axis_2 = []
    if graph_variables[2] != 'none':
        rest_dataset = open_url(opendap_url[0] + "?" + graph_variables[1] + "," + graph_variables[2], output_grid=False)
        y_axis_2 = np.array(rest_dataset[graph_variables[2]][:])
    else:
        rest_dataset = open_url(opendap_url[0] + "?" + graph_variables[1], output_grid=False)

    y_axis = np.array(rest_dataset[graph_variables[1]][:, ddm])
    y_axis_list = y_axis[indices].tolist()

    y_axis_2_list = []
    if any(y_axis_2):
        y_axis_2_list = y_axis_2[indices].tolist()

    track_list = []
    cygnss_num_indeces = (np.where(np.diff(cygnss_num)))[0] + 1
    prn_indeces = (np.where(np.diff(prn)))[0] + 1
    time_indices = (np.where(np.diff(time) > 60))[0] + 1


    # returns tracks based on time, CYGNSS sattellite and prn changes
    track_indices = np.unique(np.sort(np.concatenate((cygnss_num_indeces, time_indices, prn_indeces), axis=None)))

    np.append(track_indices, len(time))

    prev = 0
    track_id = 0
    for index in track_indices:
        track = [lat[prev:index], lon[prev:index], time[prev:index], prn[prev:index], cygnss_num[prev:index], ddm[prev:index], x_axis[prev:index], y_axis_list[prev:index], y_axis_2_list[prev:index], track_id]
        track_list.append(track)
        prev = index
        track_id += 1

# [lat, lon, ddm_timestamp_utc_list, prn_code_list, satellite_number, ddm, x_axis, y_axis_list, y_axis_2_list, track_id]
    return track_list, opendap_url
