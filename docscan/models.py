from django.db import models
from django.contrib.auth.models import User
import os
from django.core.validators import MinValueValidator
import datetime

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
    # 
    id = models.CharField(primary_key=True, max_length=10, editable=False, unique=True)

    dateregister = models.DateField(verbose_name='Fecha documento:', auto_now=False)
    doctype = models.ForeignKey(DocType, on_delete=models.CASCADE, verbose_name='Tipo documento:')
    description = models.TextField(verbose_name='Descripción:',null=False, blank=False)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Dirección:', null=False, blank=False)
    origin = models.CharField(max_length=50, verbose_name='Origen documento:', default='Ninguno', null=False, blank=False)
    folios = models.PositiveIntegerField(verbose_name='Folios:',default=0, null=False, blank=False, validators=[MinValueValidator(1),])
    fileupload = models.FileField(verbose_name='Documento PDF - 30MB max. :', upload_to=get_upload_path)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 
    def save(self, *args, **kwargs):
        if not self.id:  # Check if the ID is not yet set (new instance)
            current_year = datetime.date.today().year % 100
            sequential_number = Document.objects.count() + 1
            id_format = f"{current_year:02d}D{sequential_number:06d}"
            self.id = id_format

        super().save(*args, **kwargs)
    # 

    class Meta:
        # db_table = "Document"
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return f'{self.fileupload}'
