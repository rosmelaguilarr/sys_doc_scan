from django.forms import ModelForm
from django import forms
from .models import Document
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class DocumentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'card card-body mb-5'
        self.helper.layout = Layout(
            Row(
                Column('dateregister', css_class='form-group col-md-6 mb-0'),
                Column('doctype', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-6 mb-0'),
                Column('direction', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('origin', css_class='form-group col-md-6 mb-0'),
                Column('folios', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'fileupload',
            Submit('submit', 'Enviar', css_class='btn btn-primary')
        )

        self.fields['doctype'].empty_label = 'Escoge documento ...'
        self.fields['direction'].empty_label = 'Escoge dirección ...'
        self.fields['origin'].empty_label = 'Escoge origen ...'
    
    class Meta:     
        model = Document
        fields = ['dateregister', 'doctype','direction', 'origin', 'description', 'folios' , 'fileupload',]

        widgets = {
            'dateregister': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }


