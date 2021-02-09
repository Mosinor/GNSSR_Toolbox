from django.shortcuts import render
from .forms import *
import datetime
from .opendap import generate_url, collect_dataset, clock_to_seconds


# Form website where user defines input.
def track_demonstration(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            coordinate_a = form.cleaned_data['coordinate_a']
            coordinate_b = form.cleaned_data['coordinate_b']
            date = form.cleaned_data['date']
            start_time = clock_to_seconds(form.cleaned_data['start_time'])
            end_time = clock_to_seconds(form.cleaned_data['end_time'])
            level = form.cleaned_data['level']
            version = form.cleaned_data['version']

            lats = [coordinate_a.split(",")[0], coordinate_b.split(",")[0]]
            lons = [coordinate_a.split(",")[1], coordinate_b.split(",")[1]]

            print(start_time)
            print(end_time)

            #url = generate_url(date, level, version)
            #print(url)
            #for link in url:
            #    print(link)
            #    dataset = collect_dataset(link)
            #    print(dataset)


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
