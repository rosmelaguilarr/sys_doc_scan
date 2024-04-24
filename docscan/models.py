from django.db import models
from django.contrib.auth.models import User
from .filters import DocumentManager

# Create your models here.

DOCUMENT_TYPE=[
    ('INF', 'Informe'),
    ('MEM', 'Memoradum'),
    ('CAR', 'Carta'),
]

ORIGIN=[
    ('LOG', 'Logística'),
    ('ADM', 'Administración'),
    ('TEL', 'Telecomunincaciones'),
]


class Document(models.Model):
    dateregister = models.DateField(verbose_name='Fecha:', auto_now=False)
    doctype = models.CharField(verbose_name='Tipo de documento:',null=False, max_length=50, choices=DOCUMENT_TYPE)
    description = models.TextField(verbose_name='Descripción:',null=False, blank=False)
    folios = models.PositiveIntegerField(verbose_name='Folios:',default=0, null=False, blank=False)
    origin = models.CharField(verbose_name='Origen de documento:',null=False,max_length=50, choices=ORIGIN)
    fileupload = models.FileField(verbose_name='Cargar PDF - 30MB max. :',upload_to="uploads/")
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = DocumentManager()

    def __str__(self):
        return f'{self.doctype} by {self.user.username} - {self.fileupload}' 
