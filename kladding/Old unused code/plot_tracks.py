import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs


def extract(lst, index):
    return [item[index] for item in lst]


def add_track_to_map(track):
    lat_list = extract(track, 0)
    lon_list = extract(track, 1)
    plt.scatter(lon_list, lat_list, alpha=0.5, transform=ccrs.PlateCarree())


def plot_single_tracks(track, lats, lons):
    fig = plt.figure()
    ax = fig.gca()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_ylim(min(lats), max(lats))
    ax.set_xlim(min(lons), max(lons))

    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")
    ax.set_title("Track over selected area")
    add_track_to_map(track)
    ax.set_extent([min(lons), max(lons), min(lats), max(lats)], crs=ccrs.PlateCarree())
    print(min(lons), max(lons), min(lats), max(lats))
    ax.add_feature(cfeature.LAND, zorder=0)
    ax.add_feature(cfeature.OCEAN, zorder=0)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.RIVERS, zorder=0)
    ax.add_feature(cfeature.BORDERS, linestyle=':', zorder=0)

    plt.show()
