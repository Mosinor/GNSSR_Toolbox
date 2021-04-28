from pydap.client import open_url
import numpy as np
import datetime
from opendap import generate_url


date = datetime.datetime(2021, 4, 1)
level = "L3"
version = "v2.1"
location = [33.41845161768445, -17.59520088483109, 32.05076496221775, -15.870358842881421]
start_time = datetime.time(0, 00)
end_time = datetime.time(23, 59, 59)

opendap_url = generate_url(date, level, version)[0]

dataset = open_url(opendap_url)

key = "wind_speed_uncertainty"
data = dataset[key]

lat = np.array(data.lat[:])
lat_indices = np.where((lat[:] < location[0]) & (lat[:] > location[2]))

lon = np.array(data.lon[:])-180
lon_indices = np.where((lon[:] < location[3]) & (lon[:] > location[1]))

print("gathering data")
data = np.array(data[key][start_time.hour:end_time.hour][min(lat_indices):max(lat_indices)][min(lon_indices):max(lon_indices)])
print(data)
print(len(data))

print("done")