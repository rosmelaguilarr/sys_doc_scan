from django.forms import ModelForm
from django import forms
from .models import Document

class DocumentForm(ModelForm):

    class Meta:
        model = Document
        fields = ['dateregister', 'doctype', 'description',
                  'folios', 'origin', 'fileupload',]

        widgets = {
            'dateregister': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }

