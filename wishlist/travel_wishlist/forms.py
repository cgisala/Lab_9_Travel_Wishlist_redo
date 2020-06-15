"""
Forms used for entering data to go in a database
"""

from django import forms
from .models import Place

#Takes in data for the place model
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')