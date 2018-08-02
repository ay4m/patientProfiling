from django.forms import ModelForm
from django import forms

from .models import TestItem, TestImage


class TestItemForm (ModelForm):
    """ Form for adding lab records """
    class Meta:
        model = TestItem
        fields = [
            'testName',
            'result',
        ]
        labels = {
            'testName' : '',
            'result' : '',
        }

class TestImageForm(ModelForm):
    """ Form for adding Lab Images like Xray """
    class Meta:
        model = TestImage
        fields = [
            'tag',
            'image',
            'description',
        ]
        widgets = {
            'tag' : forms.Select(attrs={'class':'custom-select'}),
            'image' : forms.FileInput(attrs={'class':'form-control-file border'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows' : 5, 'placeholder':'Short Description about Image'})
        }
        labels = {
            'tag': 'Catagory of Image',
            'image':'Image File',
            'description': 'Description',
        }
        help_text = {
            "image" : "Choose Image File of Patient's Report",
        }
