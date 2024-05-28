from django.forms import ModelForm
from django import forms
from .models import Document, Origin


class DocumentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctype'].empty_label = 'Escoge documento ...'
        self.fields['direction'].empty_label = 'Escoge dirección ...'

        self.fields['origin'].empty_label = 'Escoge origen ...'
    


    class Meta:     
        model = Document
        fields = ['dateregister', 'doctype','direction', 'origin', 'description', 'folios' , 'fileupload',]

        widgets = {
            'dateregister': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }


