from django.shortcuts import render


# Create your views here.
def user_input(request):
    return render(request, "toolbox/user_selection.html")