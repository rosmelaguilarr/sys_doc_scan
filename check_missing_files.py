import os
import django
from django.conf import settings

# Inicializar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sysdocscan.settings')
django.setup()

from docscan.models import Document

missing_files = []
for document in Document.objects.all():
    if not os.path.exists(document.fileupload.path):
        missing_files.append(document.fileupload.path)

if missing_files:
    print("Archivos faltantes:")
    for file in missing_files:
        print(file)
else:
    print("Todos los archivos están presentes.")


# Ejecutar dentro de Docker/contenedor Django
# python check_missing_files.py