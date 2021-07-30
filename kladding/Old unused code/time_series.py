import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from global_land_mask import globe
import cmocean
import datetime
import calendar

months_2017 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
months_2018 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
months_2019 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
months_2020 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
months_2021 = [1, 2, 3, 4, 5]

year_list = [months_2017, months_2018, months_2019, months_2020, months_2021]




# THIS WILL LOOP THROUGH EVERYTHING ONCE YOU STATE YEAR AND MONTH!
average_density = []

year = 2017
for month_list in year_list:
    for month in month_list:
        data_list = []
        num_peaks = 0
        days = 0

        month_name = calendar.month_name[month]
        days_in_month = calendar.monthrange(year, month)[1]

        title = "Peak Density ("+str(month_name)+"-"+str(year)+")"

        for day in range(0, days_in_month):
            date = datetime.date(year, month, day + 1)
            path = "D:/GNSS-R Data/Peak_list/"+str(date.year)+"-"+str('%02d' % date.month)+"/Complete_peak_list_"+str(date.year)+"_"+date.strftime("%B").lower()+"_"+str(day+1)+".txt"
            file = open(path, 'rb')

            peak_list = pickle.load(file)
            data_list.append(peak_list)
            num_peaks = num_peaks + len(peak_list)
            days = days + 1


        peaks = np.array(data_list, dtype=object)

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

        zi, yi, xi = np.histogram2d(y, x, bins=bins, weights=z)
        counts, _, _ = np.histogram2d(y, x, bins=bins)

        zi[zi == 0] = 0 # once to not divide by zero

        zi = counts

        masked_data = np.ma.masked_array(zi, np.isnan(zi))
        average = np.ma.average(masked_data)

        average_density.append([average, month_name+"-"+str(year)])

        a, b = (np.where(zi < np.quantile(z, 0.05)))

        for i in range(len(a)):
            b[i] = b[i] - 180

            lat_array = np.arange(a[i] - 40, a[i] - 40 +1, 0.1)
            lon_array = np.arange(b[i], b[i]+1, 0.1)


            lon_grid, lat_grid = np.meshgrid(lon_array, lat_array)

            if globe.is_land(lat_grid, lon_grid).sum() > 40:
                zi[a[i]][b[i]+180] = 'nan'


        #zi[zi == 0] = 'nan' #and again to remove 0's from dataset

        vmax = np.nanquantile(zi, 0.5)

        #vmax = np.nanquantile(zi, 0.98) # Max boundary of colormap is top 5 %

        zi = np.ma.masked_invalid(zi) # Masks non values for the plotting


        #zi[zi < np.quantile(z, 0.90)] = 'nan'


        # COLORMAP - thermal, dense, amp
        cmap = cmocean.cm.thermal


        #bounds = [0, np.quantile(count_list, 0.75), np.quantile(z, 0.95), np.quantile(z, 0.999)]

        #bounds = [0, 20, 40, 80]

        #norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        m = Basemap(llcrnrlon=-180, llcrnrlat=-40.1, urcrnrlon = 180, urcrnrlat = 40.1)

        #m.fillcontinents(color='gray')

        # manually set upper count -> vmax = n

        cs = m.pcolormesh(xi, yi, zi, edgecolors='black', linewidth=0, cmap=cmap, vmin=0, vmax=65)
        scat = m.scatter(x, y, c=z, s=0)
        cbar = m.colorbar(cs, pad=0.5)
        cbar.ax.locator_params(nbins=5) # number of parameters shown on colorbar

        m.drawcoastlines(linewidth=0.5)

        m.shadedrelief()



        m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])
        m.drawparallels([-40, 0, 40], labels=[1, 1, 0, 0])


        plt.title(title)
        plt.savefig(str(year)+"-"+str(month)+'.png', dpi=300, bbox_inches='tight')


        plt.show()

    year = year+1


print(average_density)