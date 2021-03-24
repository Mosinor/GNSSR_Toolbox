from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .forms import *
import datetime
from .opendap import generate_url, collect_dataset, clock_to_seconds, filter_valid_points_time_specific_level1
from rest_framework.views import APIView
from rest_framework.response import Response
from kladding.realtime_gnssr.loadJSON import collect_sea_levels, collect_sea_roughness, collect_sat_info,\
     raw_measure_info, interferometric_fringe_info


# Form website where user defines input.
def track_demonstration(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            # variables

            coordinate_a = form.cleaned_data['coordinate_a']
            coordinate_b = form.cleaned_data['coordinate_b']
            lats = [float(coordinate_a.split(",")[0]), float(coordinate_b.split(",")[0])]
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


class HomeView(View):
    def get(self, request, *args, **kwargs):
        table_data, coordinates, elevation_data = collect_sat_info()

        return render(request, 'toolbox/example.html', {'table_data': table_data, })

# API / JSON test call
def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        ssl_lables, levels = collect_sea_levels()
        ssr_lables, roughness = collect_sea_roughness()
        raw_data = raw_measure_info()
        intf_data = interferometric_fringe_info()
        table_data, coordinates, skyplot_data = collect_sat_info()


        data = {
            "ssl_lables": ssl_lables,
            "levels": levels,
            "ssr_lables": ssr_lables,
            "roughness": roughness,
            "raw_data": raw_data,
            "intf_data": intf_data,
            "map_coordinates": coordinates,
            "skyplot_data": skyplot_data
             }
        return Response(data)
