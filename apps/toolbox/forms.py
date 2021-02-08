from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis import forms


class TrackDemoTool(forms.Form):
    grid = forms.PolygonField(widget=LeafletWidget(), required=False)
    coordinate_a = forms.CharField()
    coordinate_b = forms.CharField()
    date = forms.DateField(widget=DatePickerInput().start_of('event days'))
    start_time = forms.TimeField(widget=TimePickerInput().start_of('event days'))
    end_time = forms.TimeField(widget=TimePickerInput().start_of('event days'))
    level = forms.ChoiceField(choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')])
    version = forms.ChoiceField(choices=[('v2.1', 'v2.1'), ('v3.0', 'v3.0')])

    def clean(self):
        cleaned_data = super(TrackDemoTool, self).clean()


class DataClippingTool(forms.Form):
    grid = forms.PolygonField(widget=LeafletWidget(), required=False)
    coordinate_a = forms.CharField()
    coordinate_b = forms.CharField()
    start_date = forms.DateTimeField(widget=DateTimePickerInput().start_of('event days'))
    end_date = forms.DateTimeField(widget=DateTimePickerInput().start_of('event days'))
    level = forms.ChoiceField(choices=[('1', 'L1'), ('2', 'L2'), ('3', 'L3')])
    version = forms.ChoiceField(choices=[('2', 'v2.1'), ('3', 'v3.0')])

    def clean(self):
        cleaned_data = super(DataClippingTool, self).clean()
