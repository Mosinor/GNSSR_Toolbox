from django.shortcuts import render
from .forms import UserInputForm


# Form website where user defines input.
def user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']

    else:
        form = UserInputForm()

    return render(request, "toolbox/user_selection.html", {'form': form})