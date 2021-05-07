from django.conf.urls import url
from .views import *

app_name = 'toolbox'
urlpatterns = [
    url(r'^DataClipping/$', data_clipping, name="data_clipping"),
    url(r'^TrackDemonstration/$', track_demonstration, name="track_demonstration"),

    url(r'^example/$', HomeView.as_view(), name="example"),
    url(r'^groundbased/$', ground_based, name="ground_based"),
    url(r'^microplastics/$', microplastics, name="microplastics"),


    url(r'^api/data/$', get_data, name="api-data"),
    url(r'^chart/data/$', ChartData.as_view()),

]