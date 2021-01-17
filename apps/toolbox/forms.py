from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis import forms


class UserInputForm(forms.Form):
    grid = forms.PolygonField(widget=LeafletWidget(), required=False)
    coordinate_a = forms.CharField()
    coordinate_b = forms.CharField()
    start_time = forms.DateField(widget=DatePickerInput().start_of('event days'))
    end_time = forms.DateField(widget=DatePickerInput().end_of('event days'))

    def clean(self):
        cleaned_data = super(UserInputForm, self).clean()
