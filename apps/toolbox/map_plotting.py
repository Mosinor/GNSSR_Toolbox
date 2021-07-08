import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import cmocean
import datetime
import calendar

data_list = []
num_peaks = 0
days = 0

# March 2017 is from 18 to 31, so it need a separate input window

for day in range(17, 31):
    date = datetime.date(2017, 3, day+1)
    path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
    file = open(path, 'rb')

    peak_list = pickle.load(file)
    data_list.append(peak_list)
    num_peaks = num_peaks + len(peak_list)
    days = days + 1


months_2017 = [12, 11, 10, 9, 8, 7, 6, 5, 4]
months_2018 = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
months_2019 = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
months_2020 = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
months_2021 = [1, 2, 3, 4, 5]
title = "Peak Prominence (March 18. 2017 - May 31. 2021)"

year_list = [months_2017, months_2018, months_2019, months_2020, months_2021]


# THIS WILL LOOP THROUGH EVERYTHING ONCE YOU STATE YEAR AND MONTH!
year = 2017
for year_months in year_list:
    print(year)
    print(year_months)
    for month in year_months:
        days_in_month = calendar.monthrange(year, month)[1]

        for day in range(0, days_in_month):
            date = datetime.date(year, month, day + 1)
            path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
            file = open(path, 'rb')

            peak_list = pickle.load(file)
            data_list.append(peak_list)
            num_peaks = num_peaks + len(peak_list)
            days = days + 1
    year = year + 1


'''
for month in months_2020:
    year = 2020

    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(0, days_in_month):
        date = datetime.date(year, month, day + 1)
        path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
        file = open(path, 'rb')

        peak_list = pickle.load(file)
        data_list.append(peak_list)
        num_peaks = num_peaks + len(peak_list)
        days = days + 1


for month in months_2019:
    year = 2019

    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(0, days_in_month):
        date = datetime.date(year, month, day + 1)
        path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
        file = open(path, 'rb')

        peak_list = pickle.load(file)
        data_list.append(peak_list)
        num_peaks = num_peaks + len(peak_list)
        days = days + 1


for month in months_2018:
    year = 2018

    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(0, days_in_month):
        date = datetime.date(year, month, day + 1)
        path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
        file = open(path, 'rb')

        peak_list = pickle.load(file)
        data_list.append(peak_list)
        num_peaks = num_peaks + len(peak_list)
        days = days + 1


for day in range(0, 30):
    date = datetime.date(2021, 5, day+1)
    path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
    file = open(path, 'rb')

    peak_list = pickle.load(file)
    data_list.append(peak_list)
    num_peaks = num_peaks + len(peak_list)
    days = days + 1
'''

'''
for day in range(0, 30):
    date = datetime.date(2021, 4, day+1)
    path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
    file = open(path, 'rb')

    peak_list = pickle.load(file)
    data_list.append(peak_list)
    num_peaks = num_peaks + len(peak_list)
    days = days + 1
'''

peaks = np.array(data_list, dtype=object)

print(num_peaks)
print(days)



x = np.array([])
y = np.array([])
z = np.array([])

for dataset in peaks:
    if dataset == []:
        pass
    else:
        dataset = np.array(dataset)

        x = np.append(x, dataset[:, 1])
        y = np.append(y, dataset[:, 0])
        #z = np.append(z, 10*np.log(dataset[:, 4]))
        z = np.append(z, dataset[:, 6])

bins = (80, 360)

valid = np.where(z > 3)
x = x[valid]
y = y[valid]
z = z[valid]

print("num of points:"+str(len(z)))

zi, yi, xi = np.histogram2d(y, x, bins=bins, weights=z)
counts, _, _ = np.histogram2d(y, x, bins=bins)

zi[zi == 0] = 'nan' # once to not divide by zero
zi = counts

zi[zi == 0] = 'nan' #and again to remove 0's from dataset

print("max: "+str(np.nanmax(zi)))
vmax = np.nanquantile(zi, 0.99)
print("vmax: "+str(vmax))

#vmax = np.nanquantile(zi, 0.98) # Max boundary of colormap is top 5 %

zi = np.ma.masked_invalid(zi) # Masks non values for the plotting


#zi[zi < np.quantile(z, 0.90)] = 'nan'


# COLORMAP - thermal, dense, amp
cmap = cmocean.cm.thermal


#bounds = [0, np.quantile(count_list, 0.75), np.quantile(z, 0.95), np.quantile(z, 0.999)]

#bounds = [0, 20, 40, 80]

#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

m = Basemap(llcrnrlon=-180.1, llcrnrlat=-40.1, urcrnrlon = 180.1, urcrnrlat = 40.1)
m.drawcoastlines(linewidth=0.5)

m.shadedrelief()
#m.fillcontinents(color='gray')

# manually set upper count -> vmax = n
print(vmax)

cs = m.pcolormesh(xi, yi, zi, edgecolors='black', linewidth=0, cmap=cmap, vmin=0, vmax=850)
scat = m.scatter(x, y, c=z, s=0)
cbar = m.colorbar(cs, pad=0.5)
cbar.ax.locator_params(nbins=5) # number of parameters shown on colorbar



m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])
m.drawparallels([-40, 0, 40], labels=[1, 1, 0, 0])


plt.title(title)
plt.savefig('plot_name.png', dpi=300, bbox_inches='tight')


plt.show()
