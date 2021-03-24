from track_list import track_list
from apps.toolbox.plot_tracks import plot_single_tracks, extract
import datetime

lats = [-21.943046, 0.0]
lons = [-180, -170]
print(lons)



#date = datetime.date(2021, 2, 1)

plot_single_tracks(track_list[9], lats, lons)

