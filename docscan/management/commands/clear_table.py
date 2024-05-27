from django.core.management.base import BaseCommand
from docscan.models import Direction, Origin  

class Command(BaseCommand):
    help = 'Vacía la tabla MyModel'

    def handle(self, *args, **kwargs):
        table = Direction
        table.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Tabla {table} vaciada exitosamente'))