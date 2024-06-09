from django.core.management.base import BaseCommand
from docscan.models import DocType, Direction

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Crear instancias de DocType
        doctype1 = DocType.objects.create(name='Carta')
        doctype2 = DocType.objects.create(name='Memorandum')
        doctype3 = DocType.objects.create(name='Oficio')
        doctype4 = DocType.objects.create(name='Informe')
        doctype5 = DocType.objects.create(name='Contrato')
        doctype6 = DocType.objects.create(name='Convenio')
        doctype7 = DocType.objects.create(name='Adenda')
        doctype8 = DocType.objects.create(name='Comprobante de Pago')
        doctype9 = DocType.objects.create(name='Orden de Servicio')
        doctype10 = DocType.objects.create(name='Expediente Técnico')
        doctype11 = DocType.objects.create(name='Valorización')

        # Crear una instancia de Direction
        direction1 = Direction.objects.create(name='Dirección General')
        direction2 = Direction.objects.create(name='Administración')
        direction3 = Direction.objects.create(name='Planificación y Presupuesto')
        direction4 = Direction.objects.create(name='Asesoría Jurídica')
        direction5 = Direction.objects.create(name='Caminos')
        direction6 = Direction.objects.create(name='Telecomunicaciones')
        direction7 = Direction.objects.create(name='Circulación Terrestre')

        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente'))