from django.conf.urls import url
from .views import *

app_name = 'toolbox'
urlpatterns = [
    url(r'^input/$', user_input, name="user_input"),
]