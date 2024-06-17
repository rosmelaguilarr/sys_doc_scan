from django.db import models
from django.contrib.auth.models import User
import os
from django.core.validators import MinValueValidator

class DocType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Direction(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

def get_upload_path(instance, filename):
    return os.path.join('uploads', filename)

class Document(models.Model):
    dateregister = models.DateField(verbose_name='Fecha documento:', auto_now=False)
    doctype = models.ForeignKey(DocType, on_delete=models.CASCADE, verbose_name='Tipo documento:')
    description = models.TextField(verbose_name='Descripción:',null=False, blank=False)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Dirección:', null=False, blank=False)
    origin = models.CharField(max_length=50, verbose_name='Origen documento:', default='Ninguno', null=False, blank=False)
    folios = models.PositiveIntegerField(verbose_name='Folios:',default=0, null=False, blank=False, validators=[MinValueValidator(1),])
    fileupload = models.FileField(verbose_name='Documento PDF - 30MB max. :', upload_to=get_upload_path)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # db_table = "Document"
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return f'{self.fileupload}'
