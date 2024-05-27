from django.core.management.base import BaseCommand
from docscan.models import DocType, Origin, Direction

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Crear instancias de DocType
        # doctype1 = DocType.objects.create(name='Carta')
        # doctype2 = DocType.objects.create(name='Memorandum')
        # doctype3 = DocType.objects.create(name='Oficio')
        # doctype4 = DocType.objects.create(name='Informe')
        # doctype5 = DocType.objects.create(name='Contrato')
        # doctype6 = DocType.objects.create(name='Convenio')
        # doctype7 = DocType.objects.create(name='Adenda')
        # doctype8 = DocType.objects.create(name='Comprobante de Pago')
        # doctype9 = DocType.objects.create(name='Orden de Servicio')
        # doctype10 = DocType.objects.create(name='Expediente Técnico')
        # doctype11 = DocType.objects.create(name='Valorización')

        # Crear una instancia de Direction
        direction1 = Direction.objects.create(name='Dirección General')
        direction2 = Direction.objects.create(name='Administración')
        direction3 = Direction.objects.create(name='Planificación y Presupuesto')
        direction4 = Direction.objects.create(name='Asesoría Jurídica')
        direction5 = Direction.objects.create(name='Caminos')
        direction6 = Direction.objects.create(name='Telecomunicaciones')
        direction7 = Direction.objects.create(name='Circulación Terrestre')

        # Crear instancias de Origin relacionadas con Direction
        origin1 = Origin.objects.create(name='Recursos Humanos', direction=direction2)
        origin2 = Origin.objects.create(name='Contabilidad y Tesorería', direction=direction2)
        origin3 = Origin.objects.create(name='Abastecimiento y SS.AA', direction=direction2)
        origin4 = Origin.objects.create(name='Archivo Central', direction=direction2)

        origin5 = Origin.objects.create(name='Planificación', direction=direction3)
        origin6 = Origin.objects.create(name='Racionalización y Modernización', direction=direction3)

        origin7 = Origin.objects.create(name='Estudios y Obras', direction=direction5)
        origin8 = Origin.objects.create(name='Equipo Mecánico', direction=direction5)
        origin9 = Origin.objects.create(name='Resid. Grau - Cotabambas', direction=direction5)
        origin10 = Origin.objects.create(name='Resid. Aymaraes - Antabamba', direction=direction5)

        origin11 = Origin.objects.create(name='Control y Supervisión', direction=direction6)
        origin12 = Origin.objects.create(name='Proyectos, Concesiones y Autorizaciones', direction=direction6)
        origin13 = Origin.objects.create(name='Mantenimiento y Operación', direction=direction6)

        origin14 = Origin.objects.create(name='Pasajeros y Mercancías', direction=direction7)
        origin15 = Origin.objects.create(name='Licencia de Conducir y Educación Vial', direction=direction7)
        origin16 = Origin.objects.create(name='Supervisión, Fiscalización y Sanciones', direction=direction7)


        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente'))