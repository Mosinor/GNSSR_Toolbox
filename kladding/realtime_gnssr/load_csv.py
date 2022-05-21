import pandas as pd
from random import random
import math
import datetime


def get_cygnss_time_series(start_date, end_date, region) -> list:

    # cygnss_df = pd.read_csv('cygnss_data.csv')
    # Convert the date input attributes to day number
    # cygnss_df = filter_cygnss_date(cygnss_df, start_day, end_day)
    # Maybe sort the dataframe on day_of_year to make sure the coordinates are correct?
    # Do some averaging for each day. Maybe .group_by('date').mean() or something
    # Include the possibility of varying the step size and the interval?
    # return list(cygnss_df['sr'])

    area = {'north': region[0], 'south': region[2], 'west': region[1], 'east': region[3]}

    base_path = 'data/CYGNSS '
    delta = datetime.timedelta(days=1)
    cygnss_ts = []

    while start_date <= end_date:
        if start_date.year in [2019, 2020, 2021]:
            path = base_path + str(start_date.year) + '/' + str(start_date.month) + '-' + str(start_date.day) + '.csv'
            current_df = pd.read_csv(path)[['lat', 'long', 'sr']]
            current_df = filter_location(current_df, area)

            cygnss_ts.append(current_df['sr'].mean())

        start_date += delta

    return cygnss_ts


def get_smap_time_series(start_date, end_date, region) -> list:
    return [i*math.cos(i) for i in range(get_day_interval(start_date, end_date) + 1)]


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
