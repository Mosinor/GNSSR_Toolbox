from django.shortcuts import render
from .forms import *


# Form website where user defines input.
def user_input(request):
    if request.method == 'POST':
        form = TrackDemoTool(request.POST)
        if form.is_valid():
            print("Form submitted with data:")

    else:
        form = TrackDemoTool()

    return render(request, "toolbox/user_selection.html", {'form': form})


def tool_selection(request):
    return render(request, "toolbox/tool_selection.html",)


def example(request):
    return render(request, "toolbox/example.html",)
