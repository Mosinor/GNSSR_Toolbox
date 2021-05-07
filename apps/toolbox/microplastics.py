import numpy as np
import datetime
from opendap import generate_url
from pydap.client import open_url


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


def collect_nbrcs_data(date, location):
    opendap_url = generate_url(date, "L1", "v3.0")

    track_list = []

    for satellite in range(8):
        lat_lon_dataset = open_url(opendap_url[satellite] + "?sp_lat,sp_lon", output_grid=False)

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

            main_dataset = open_url(opendap_url[satellite] + "?ddm_nbrcs", output_grid=False)
            nbrcs = np.array(main_dataset['ddm_nbrcs'][:, ddm])

            for track in tracks:
                lat = sp_lat[track.min():track.max()].flatten().tolist()
                lon = sp_lon[track.min():track.max()].flatten().tolist()
                track_nbrcs = nbrcs[track.min():track.max()].flatten().tolist()

                track_list.append([lat, lon, track_nbrcs])

    return track_list


# Variables:
date = datetime.datetime(2021, 4, 1)
location_grid = [35.10193, -27.02637, 30.37288, -19.37988]

nbrcs_track_list = collect_nbrcs_data(date, location_grid) # Scatter this? then find peaks?

print(nbrcs_track_list)
