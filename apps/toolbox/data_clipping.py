from pydap.client import open_url
from pydap.cas.urs import setup_session
import wget
import numpy as np
import datetime
from .opendap import generate_url


def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)


def collect_level_3_data(start_date, end_date, location, level, keys, version):
    selected_dates = [start_date + datetime.timedelta(days=x) for x in
                      range(0, (end_date.date() - start_date.date()).days)]

    if not selected_dates:
        date = start_date
        opendap_url = generate_url(date, level, version)[0]
        start_time = start_date.hour
        end_time = end_date.hour

        j = 0
        for key in keys:
            if j == 0:
                opendap_url += "?"
            else:
                opendap_url += ","
            geogrid = "geogrid(" + key + "," + str(location[0]) + "," + str(location[1]) + "," + str(
                location[2]) + "," + str(location[3]) + "," + "\"" + str(start_time) + "<=time<=" + str(
                end_time) + "\")"
            opendap_url += geogrid
            j += 1

        # TODO: wget download
        print(opendap_url)

    else:
        selected_dates.append(end_date)
        print(selected_dates)

        i = 0
        for date in selected_dates:
            start_time = 0
            end_time = 23
            if i == 0:
                start_time = date.hour
            elif i == len(selected_dates)-1:
                end_time = date.hour
            else:
                pass

            opendap_url = generate_url(date, "L3", version)[0]
            variables = []

            j = 0
            for key in keys:
                if j == 0:
                    opendap_url += "?"
                else:
                    opendap_url += ","
                geogrid = "geogrid("+key+","+str(location[0])+","+str(location[1])+","+str(location[2])+","+str(location[3])+","+"\""+str(start_time)+"<=time<="+str(end_time)+"\")"
                opendap_url += geogrid
                j += 1
            i += 1

            # TODO: wget download
            print(opendap_url)


def collect_level_2_data(start_date, end_date, location, level, keys, version):


    date = start_date
    opendap_url = generate_url(date, level, version)[0]

    dataset = open_url(opendap_url, output_grid=False)

    print(dataset)


def collect_level_1_data(start_date, end_date, location, level, keys, version):
    selected_dates = [start_date + datetime.timedelta(days=x) for x in
                      range(0, (end_date.date() - start_date.date()).days)]


    if not selected_dates:
        selected_dates.append(start_date)
    else:
        selected_dates.append(end_date)

    for date in selected_dates:
        print(date)
        opendap_url = generate_url(date, level, version)


        for satellite in range(8):
            print("sat: "+str(satellite))
            try:
                lat_lon_dataset = open_url(opendap_url[satellite]+"?sp_lat,sp_lon", output_grid=False)
            except:
                print("anomaly in link")
                break

            shape_dataset = open_url(opendap_url[0])

            for ddm in range(4):
                print("ddm: "+str(ddm))
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



#start_date = datetime.datetime(2021, 4, 1, 12)
#end_date = datetime.datetime(2021, 4, 1, 13)
#keys = ['spacecraft_num', 'ddm_timestamp_utc', 'sp_lat', 'brcs']
#v = "v2.1"
#location = [35, 300, 40, 330]



#collect_level_2_data(start_date, end_date, location, "L2", keys, v)
