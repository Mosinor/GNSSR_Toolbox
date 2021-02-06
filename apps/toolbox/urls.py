from django.conf.urls import url
from .views import *

app_name = 'toolbox'
urlpatterns = [
    url(r'^DataClipping/$', data_clipping, name="data_clipping"),
    url(r'^TrackDemonstration/$', track_demonstration, name="track_demonstration"),
    url(r'^example/$', example, name="example"),

]