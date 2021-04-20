from pydap.client import open_url
import numpy as np


def generate_url(date, level, version):

    if version == "2":
        version = "v2.1"
    elif version == "3":
        version = "v3.0"

    opendap_url = []
    base_url = "https://podaac-opendap.jpl.nasa.gov/opendap/hyrax/allData/cygnss/"+level+"/"+version+"/"
    date_string = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
    if version == "v2.1":
        v = "a21.d21"
    elif version == "v3.0":
        v = "a30.d31"

    if level == "L1":
        for satellite_number in range(8):
            specific_url = "/cyg0" + str(satellite_number+1) + ".ddmi.s" + date_string + "-000000-e" + date_string + "-235959.l1.power-brcs."+v+".nc"
            opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    elif level == "L2":
        specific_url = "/cyg.ddmi.s" + date_string + "-000000-e" + date_string + "-235959.l2.wind-mss."+v+".nc"
        opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    elif level == "L3":
        if version == "v2.1":
            v = "a10.d21"
        specific_url = "/cyg.ddmi.s" + date_string + "-003000-e" + date_string + "-233000.l3.grid-wind."+v+".nc"
        opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    return opendap_url


def collect_dataset(url):
    try:
        dataset = open_url(url, output_grid=False, timeout=30)
    except:
        dataset = None
    return dataset


def clock_to_seconds(time):
    return sum(x * int(t) for x, t in zip([3600, 60, 1], str(time).split(":")))


# Filters the coordinate data based on user input and separates them into tracks.
def filter_valid_points_time_specific_level1(dataset, lats, lons, start_time, end_time):
    sat_num = np.array(dataset.spacecraft_num)
    track_list = []
    current_track = []
    previous_timestamp = -9
    previous_ddm = -9

    for ddm in range(4):
        sp_lat = np.array(dataset.sp_lat[start_time:end_time, ddm])
        sp_lon = np.array(dataset.sp_lon[start_time:end_time, ddm])
        for ddm_timestamp, latitude in enumerate(sp_lat):
            if min(lats) <= latitude <= max(lats):
                longitude = sp_lon[ddm_timestamp][0]
                if min(lons) <= longitude <= max(lons):
                    measure = [latitude[0], longitude, ddm_timestamp+start_time, ddm, int(sat_num)]
                    if not previous_timestamp + 1 == measure[2] or not measure[3] == previous_ddm:
                        track_list.append(current_track)
                        current_track = [measure]
                    else:
                        current_track.append(measure)

                    previous_ddm = measure[3]
                    previous_timestamp = measure[2]

    if track_list:
        del track_list[0]
        track_list.append(current_track)

    return track_list


# Filters the coordinate data based on user input and separates them into tracks.
#def filter_valid_points_time_specific_level2(dataset, lats, lons, start_time, end_time):
    #sat_num = np.array(dataset.spacecraft_num)
    #track_list = []
    #current_track = []
    #previous_timestamp = -9
    #previous_ddm = -9

    #for ddm in range(4):
    #    lat = np.array(dataset.lat.lat)
    #    lon = np.array(dataset.lon.lon)

        #for ddm_timestamp, latitude in enumerate(sp_lat):
        #    if min(lats) <= latitude <= max(lats):
        #        longitude = sp_lon[ddm_timestamp][0]
        #        if min(lons) <= longitude <= max(lons):
        #            measure = [latitude[0], longitude, ddm_timestamp+start_time, ddm, int(sat_num)]
        #            if not previous_timestamp + 1 == measure[2] or not measure[3] == previous_ddm:
        #                track_list.append(current_track)
        #                current_track = [measure]
        #            else:
        #                current_track.append(measure)
        #
        #            previous_ddm = measure[3]
        #           previous_timestamp = measure[2]

    #if track_list:
    #    del track_list[0]
    #    track_list.append(current_track)

    #return track_list
