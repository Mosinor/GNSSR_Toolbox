from django.shortcuts import render
from .forms import *


# Form website where user defines input.
def track_demonstration(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            print("Form submitted with data:")

    else:
        form = TrackDemoTool()

    return render(request, "toolbox/track_demonstration.html", {'form': form})


def data_clipping(request):
    return render(request, "toolbox/data_clipping.html", )


def example(request):
    return render(request, "toolbox/example.html",)
