import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import cmocean
import datetime
import calendar

file = open('April_1_2021_Wind_Speed_example_data', 'rb')
wind_point = np.array(pickle.load(file))
file.close()

y = wind_point[:, 0]
x = wind_point[:, 1]
z = wind_point[:, 2]

bins = (80, 360)

zi, yi, xi = np.histogram2d(y, x, bins=bins, weights=z)
counts, _, _ = np.histogram2d(y, x, bins=bins)

zi = zi / counts


m = Basemap(llcrnrlon=-180.1, llcrnrlat= -45.1, urcrnrlon = 180.1, urcrnrlat = 45.1)
m.drawcoastlines(linewidth=0.5)

cmap = cmocean.cm.thermal

cs = m.pcolormesh(xi, yi, zi, edgecolors='black', linewidth=0, cmap=cmap)
scat = m.scatter(x, y, c=z, s=0)
m.colorbar(cs, pad=0.5)


m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])
m.drawparallels([-40, 0, 40], labels=[1, 1, 0, 0])

plt.title("ERA5 Wind speeds [m/s] (April 1. 2021 at 00:00)")
plt.savefig('wind_speed.png', dpi = 300)


plt.show()