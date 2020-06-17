"""
Forms used for entering data to go in a database
"""

from django import forms
from django.forms import FileInput, DateInput
from .models import Place

#Takes in name and visited data for the Place model
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

#Create a custom date input field, otherwise would get a plain text field.
class DateInput(forms.DateInput):
    input_type = 'date'     #Override the default input type, which is 'text'.

#Takes in note, date visited, and photo data for the Place model
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }

