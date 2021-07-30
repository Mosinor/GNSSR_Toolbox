# This file collects the tracks from the CYGNSS opendap database, and stores lats, lon, nbrcs, timestamp and quality flags for each date.


import datetime
import numpy as np
import time
import pickle
from pydap.client import open_url
from opendap import generate_url
import calendar


def collect_tracks(date):
    url = generate_url(date, "L1", "v2.1")
    track_list = []

    for satellite in range(8):
        print("satellite: "+str(satellite))
        try:
            dataset = open_url(url[satellite], output_grid=False)
        except:
            dataset = None
        if dataset is None:
            print("Something went wrong with dataset collection")
            pass
        else:
            for ddm in range(4):
                track_id = np.array(dataset.track_id[:, ddm]).flatten()
                track_indices = np.append(np.append(-1, np.where(np.diff(track_id) > 0)), len(track_id))

                sp_lat = np.array(dataset.sp_lat[:, ddm]).flatten().tolist()
                sp_lon = np.array(dataset.sp_lon[:, ddm])

                # We need to convert longitude to [-180, 180] (ERA5 Winds)
                a, b = (np.where(sp_lon > 180))
                sp_lon[a] -= 360

                nbrcs = np.array(dataset.ddm_nbrcs[:, ddm]).flatten().tolist()
                ddm_timestamp_utc = np.array(dataset['ddm_timestamp_utc'][:]).tolist()
                quality_flags = np.array(dataset['quality_flags'][:, ddm]).flatten().tolist()

                for track in range(len(track_indices)-1):
                    start = track_indices[track]+1
                    end = track_indices[track+1]

                    lats = sp_lat[start: end]
                    lons = sp_lon[start: end].flatten().tolist()
                    track_nbrcs = nbrcs[start: end]
                    track_ddm_timestamp_utc = ddm_timestamp_utc[start: end]
                    track_quality_flags = quality_flags[start: end]

                    track_list.append([lats, lons, track_nbrcs, track_ddm_timestamp_utc, track_quality_flags])

    return track_list


year = 2017

for month in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:

    for day in range(0, calendar.monthrange(year, month)[1]):
        date = datetime.date(year, month, day+1)
        print(date)

        nbrcs_track = collect_tracks(date)

        file = open('D:/GNSS-R Data/Track_separation/' + str(date.year) + '-' + str('%02d' % date.month) + '/track_list' + str(
            date.year) + '_' + date.strftime("%B").lower() + '_' + str(day + 1) + '.txt', 'wb')

        pickle.dump(nbrcs_track, file)
        file.close()
