from django.shortcuts import render
from .forms import *
from .opendap import generate_url


# Form website where user defines input.
def track_demonstration(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            coordinate_a = form.cleaned_data['coordinate_a']
            coordinate_b = form.cleaned_data['coordinate_b']
            lats = [coordinate_a.split(",")[0], coordinate_b.split(",")[0]]
            lons = [coordinate_a.split(",")[1], coordinate_b.split(",")[1]]
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            level = form.cleaned_data['level']
            version = form.cleaned_data['version']

            url = generate_url(date, level, version)
            print(url)




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
