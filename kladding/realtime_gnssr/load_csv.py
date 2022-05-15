import pandas as pd
from random import random
import math

def get_cygnss_time_series(start_date, end_date, region) -> list:

    # cygnss_df = pd.read_csv('cygnss_data.csv')
    # Convert the date input attributes to day number
    # cygnss_df = filter_cygnss_date(cygnss_df, start_day, end_day)
    # Maybe sort the dataframe on day_of_year to make sure the coordinates are correct?
    # Do some averaging for each day. Maybe .group_by('date').mean() or something
    # Include the possibility of varying the step size and the interval?
    # return list(cygnss_df['sr'])

    return [i*math.sin(i) for i in range(get_day_interval(start_date, end_date) + 1)]


def get_smap_time_series(start_date, end_date, region) -> list:
    return [i*math.cos(i) for i in range(get_day_interval(start_date, end_date) + 1)]


def filter_date(df, start_day, end_day, date_column_name='day_of_year') -> pd.DataFrame:
    return df[(df[date_column_name] >= start_day) & (df[date_column_name] <= end_day)]


def get_day_interval(start_day, end_day):
    return (end_day - start_day).days


def filter_location(df, area) -> pd.DataFrame:

    filtered_df = df[(df['lat'] <= area['south']) & (df['lat'] >= area['north'])]
    filtered_df = filtered_df[(filtered_df['long'] <= area['west']) & (filtered_df['long'] >= area['east'])]
    return filtered_df


def convert_list_coordinates_to_dict(coordinates) -> dict:
    return {'north': coordinates[0], 'south': coordinates[2], 'west': coordinates[1], 'east': coordinates[3]}
