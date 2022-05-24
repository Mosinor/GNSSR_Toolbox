import pandas as pd
from random import random
import math
import datetime
import numpy as np


def get_cygnss_time_series(start_date, end_date, region) -> list:

    area = {'north': region[0], 'south': region[2], 'west': region[1], 'east': region[3]}

    base_path = 'data/CYGNSS '
    delta = datetime.timedelta(days=1)
    cygnss_ts = []

    while start_date <= end_date:
        if start_date.year in [2019, 2020, 2021]:
            path = base_path + str(start_date.year) + '/' + str(start_date.month) + '-' + str(start_date.day) + '.csv'
            current_df = pd.read_csv(path)[['lat', 'long', 'sr']]
            current_df = filter_location(current_df, area)

            if len(current_df) > 0:
                cygnss_ts.append(current_df['sr'].mean())

        start_date += delta

    cygnss_ts = fill_missing_values(cygnss_ts)

    return cygnss_ts


def get_smap_time_series(start_date, end_date, region) -> list:

    area = {'north': region[0], 'south': region[2], 'west': region[1], 'east': region[3]}

    base_path = 'data/SMAP '
    delta = datetime.timedelta(days=1)
    smap_ts = []

    while start_date <= end_date:
        if start_date.year in [2019, 2020, 2021]:
            if start_date.day < 10:
                day_string = '0' + str(start_date.day)
            else:
                day_string = str(start_date.day)
            if start_date.month < 10:
                month_string = '0' + str(start_date.month)
            else:
                month_string = str(start_date.month)

            path = base_path + str(start_date.year) + '/' + month_string + '-' + day_string + '.csv'

            try:
                current_df = pd.read_csv(path)[['lat', 'long', 'smap_sm']]
            except FileNotFoundError:
                current_df = pd.DataFrame.from_dict({'lat': [], 'long': [], 'smap_sm': []})

            current_df = filter_location(current_df, area)

            if len(current_df) > 0:
                smap_ts.append(current_df['smap_sm'].mean())
            else:
                smap_ts.append(-999)

        start_date += delta

    smap_ts = fill_missing_values(smap_ts)

    return smap_ts


def fill_missing_values(ts):
    for i in range(len(ts)):
        if ts[i] == -999:
            closest_back_value = find_closest_existing_value(ts, i, False)
            closest_forward_value = find_closest_existing_value(ts, i, True)

            if closest_back_value is None and closest_forward_value is None:
                return None
            if closest_back_value is not None and closest_forward_value is not None:
                ts[i] = np.mean([closest_back_value, closest_forward_value])

            elif closest_back_value is None:
                ts[i] = closest_forward_value
            elif closest_forward_value is None:
                ts[i] = closest_back_value
    return ts


def find_closest_existing_value(ts, index, forward):
    if forward:
        while index < len(ts):
            if ts[index] > 0:
                return ts[index]
            index = index + 1
        return None
    else:
        while index >= 0:
            if ts[index] > 0:
                return ts[index]
            index = index - 1
        return None


def filter_date(df, start_day, end_day, date_column_name='day_of_year') -> pd.DataFrame:
    return df[(df[date_column_name] >= start_day) & (df[date_column_name] <= end_day)]


def get_day_interval(start_day, end_day):
    return (end_day - start_day).days


def filter_location(df, area) -> pd.DataFrame:

    filtered_df = df[(df['lat'] <= area['north']) & (df['lat'] >= area['south'])]
    filtered_df = filtered_df[(filtered_df['long'] <= area['east']) & (filtered_df['long'] >= area['west'])]
    return filtered_df


def convert_list_coordinates_to_dict(coordinates) -> dict:
    return {'north': coordinates[0], 'south': coordinates[2], 'west': coordinates[1], 'east': coordinates[3]}
