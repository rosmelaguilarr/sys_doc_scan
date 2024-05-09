from django.core.management.base import BaseCommand
from docscan.models import DocType, Origin

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Crear instancias de DocType
        doctype1 = DocType.objects.create(name='Informe')
        doctype2 = DocType.objects.create(name='Memorandum')

        # Crear instancias de Origin
        origin1 = Origin.objects.create(name='Administración')
        origin2 = Origin.objects.create(name='Logística')

        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente'))