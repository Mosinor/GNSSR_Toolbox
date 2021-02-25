from django.shortcuts import render
from .forms import *
import datetime
from .opendap import generate_url, collect_dataset, clock_to_seconds, filter_valid_points_time_specific_level1


# Form website where user defines input.
def track_demonstration(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            # variables
            coordinate_a = form.cleaned_data['coordinate_a']
            coordinate_b = form.cleaned_data['coordinate_b']
            lats = [float(coordinate_a.split(",")[0]), float(coordinate_b.split(",")[0])]
            lons = [float(coordinate_a.split(",")[1]), float(coordinate_b.split(",")[1])]

            date = form.cleaned_data['date']
            start_time = clock_to_seconds(form.cleaned_data['start_time'])
            end_time = clock_to_seconds(form.cleaned_data['end_time'])

            level = form.cleaned_data['level']
            version = form.cleaned_data['version']

            # gather dataset
            url = generate_url(date, level, version)
            track_list = []

            # collect tracks
            for link in url:
                dataset = collect_dataset(link)
                tracks = filter_valid_points_time_specific_level1(dataset, lats, lons, start_time, end_time)
                for track in tracks:
                    track_list.append(track)

            print(track_list)
            print(lats)
            print(lons)
            print(date)

    else:
        form = TrackDemoTool()

    return render(request, "toolbox/track_demonstration.html", {'form': form})


def data_clipping(request):
    if request.method == 'POST':
        form = DataClippingTool(request.POST)
        if form.is_valid():
            print("Form submitted with data:")

    else:
        form = DataClippingTool()
    return render(request, "toolbox/data_clipping.html", {'form': form})


def example(request):
    return render(request, "toolbox/example.html",)
