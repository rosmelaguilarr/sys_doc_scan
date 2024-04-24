from django.forms import ModelForm
from django import forms
from .models import Document


class DateInput(forms.DateInput):
    input_type = 'date'


class DocumentForm(ModelForm):

    class Meta:
        model = Document
        fields = ('dateregister', 'doctype', 'description',
                  'folios', 'origin', 'fileupload',)

        widgets = {
            'dateregister': DateInput(),
        }
