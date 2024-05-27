from django.forms import ModelForm
from django import forms
from .models import Document


class DocumentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_choices = list(self.fields['doctype'].widget.choices)
        current_choices[0] = ('', 'Escoge documento')
        self.fields['doctype'].widget.choices = current_choices

        current_choices = list(self.fields['origin'].widget.choices)
        current_choices[0] = ('', 'Escoge origen')
        self.fields['origin'].widget.choices = current_choices

        current_choices = list(self.fields['direction'].widget.choices)
        current_choices[0] = ('', 'Escoge dirección')
        self.fields['direction'].widget.choices = current_choices

    class Meta:     
        model = Document
        fields = ['dateregister', 'doctype',
                  'direction', 'origin', 'description', 'folios' , 'fileupload',]

        widgets = {
            'dateregister': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }


