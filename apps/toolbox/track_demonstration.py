from pydap.client import open_url
from pydap.cas.urs import setup_session
import wget
import numpy as np
import datetime
from .opendap import generate_url


def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)


def collect_level_1_demo_data(date, location, start_time, end_time, level, version):
    opendap_url = generate_url(date, level, version)

    track_list = []

    for satellite_number in range(1):
        print("Starting scan for satellite: " + str(satellite_number))

        try:
            lat_lon_dataset = open_url(opendap_url[satellite_number] + "?sp_lat,sp_lon", output_grid=False)
        except:
            print("anomaly in link")
            break

        for ddm in range(1):
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

            for track in tracks:
                lat = sp_lat[track.min():track.max()].tolist()
                lon = sp_lon[track.min():track.max()].tolist()
                track_list.append([lat, lon])

    return track_list




"""
if len(tracks[0]) == 0:
    print("No valid tracks")
else:
    for track in tracks:
        sample = "[" + str(track.min()) + ":" + str(track.max()) + "]"

        link = opendap_url[satellite]+"?"

        for variable in keys:
            if len(shape_dataset[str(variable)].shape) == 0:
                link += str(variable) + ","
            elif len(shape_dataset[str(variable)].shape) == 1:
                link += str(variable) + sample + ","
            elif len(shape_dataset[str(variable)].shape) == 2:
                link += str(variable) + sample + "[" + str(ddm) + "],"
            elif len(shape_dataset[str(variable)].shape) == 4:
                link += str(variable) + sample + "[" + str(ddm) + "][0:1:16][0:1:10],"

        link = link[:len(link)-1]

        # TODO: wget download
        print(link)

date = datetime.datetime(2021, 4, 1)
keys = ['brcs']
v = "v2.1"
level = "L1"
version = "v2.1"
location = [30.751278, -45.351562, 24.527135, -34.453125]


tracks = collect_level_1_demo_data(date, location, "start_time", "end_time", level, version)
"""