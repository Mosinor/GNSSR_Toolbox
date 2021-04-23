from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from .forms import *
from datetime import timedelta
from .opendap import generate_url, define_dataset_keys, collect_dataset, clock_to_seconds, filter_valid_points_time_specific_level1
from rest_framework.views import APIView
from rest_framework.response import Response
from kladding.realtime_gnssr.loadJSON import collect_sea_levels, collect_sea_roughness, collect_sat_info,\
     raw_measure_info, interferometric_fringe_info
from .data_clipping import collect_level_3_data, collect_level_1_data
from .track_demonstration import collect_level_1_demo_data


def track_demonstration(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            coordinate_a = form.cleaned_data['coordinate_a']
            coordinate_b = form.cleaned_data['coordinate_b']
            lats = [float(coordinate_a.split(",")[0]), float(coordinate_b.split(",")[0])]
            lons = [float(coordinate_a.split(",")[1]), float(coordinate_b.split(",")[1])]

            location = [max(lats), min(lons), min(lats), max(lons)]

            date = form.cleaned_data['date']
            start_time = clock_to_seconds(form.cleaned_data['start_time'])
            end_time = clock_to_seconds(form.cleaned_data['end_time'])

            level = form.cleaned_data['level']
            version = form.cleaned_data['version']

            print(level)

            v = ""
            if version == "2":
                v = "v2.1"
            elif version == "3":
                v = "v3.0"

            track_list = []
            if level == "L1":
                print(level)
                key_variable = form.cleaned_data['keys_level1']
                track_list = collect_level_1_demo_data(date, location, start_time, end_time, level, version)

            elif level == "L2":
                pass

            elif level == "L3":
                pass


            return render(request, "toolbox/track_demonstration_presentation.html", {'track_list': track_list, 'boundary': location})



    else:
        form = TrackDemoTool()

    return render(request, "toolbox/track_demonstration.html", {'form': form})


def data_clipping(request):
    if request.method == 'POST':
        form = DataClippingTool(request.POST)
        if form.is_valid():
            coordinate_a = form.cleaned_data['coordinate_a']
            coordinate_b = form.cleaned_data['coordinate_b']
            lats = [float(coordinate_a.split(",")[0]), float(coordinate_b.split(",")[0])]
            lons = [float(coordinate_a.split(",")[1]), float(coordinate_b.split(",")[1])]

            location = [max(lats), min(lons), min(lats), max(lons)]

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            selected_dates = [start_date + timedelta(days=x) for x in range(0, (end_date.date() - start_date.date()).days)]
            selected_dates.append(end_date)

            level = form.cleaned_data['level']
            version = form.cleaned_data['version']

            v = ""
            if version == "2":
                v = "v2.1"
            elif version == "3":
                v = "v3.0"

            keys = []
            if level == "1":
                keys = form.cleaned_data['keys_level1']
                collect_level_1_data(start_date, end_date, location, "L1", keys, v)

            elif level == "2":
                keys = form.cleaned_data['keys_level2']
                print(start_date)
                print(end_date)
                print(keys)
                print(v)
                print(location)

            elif level == "3":
                keys = form.cleaned_data['keys_level3']
                collect_level_3_data(start_date, end_date, location, "L3", keys, v)







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
