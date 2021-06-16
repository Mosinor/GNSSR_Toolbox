import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import cmocean
import datetime
import calendar
import csv



header = ['lat', 'lon', 'ddm_nbrcs', 'timestamp_utc', 'prominence', 'width', 'wind_speed', 'date']


for month in [12, 11, 10, 9, 8, 7]:
    year = 2019

    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(0, days_in_month):

        date = datetime.date(year, month, day+1)

        path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(date.day)+".txt"
        file = open(path, 'rb')
        peak_list = pickle.load(file)

        for peak in peak_list:
            peak.append(date)


        with open("D:/GNSS-R Data/Peak CSV/"+str(date.year)+"/"+str('%02d' % date.month)+"/peak_information_"+str(date.year)+"-"+str('%02d' % date.month)+"-"+str(date.day)+'.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(peak_list)