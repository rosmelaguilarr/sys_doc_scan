import shutil
from datetime import datetime
import pytz

# Definir la zona horaria de Lima
lima_tz = pytz.timezone('America/Lima')

# Obtener la hora actual en UTC y convertirla a la zona horaria de Lima
now_utc = datetime.now(pytz.utc)
now_lima = now_utc.astimezone(lima_tz)

# Ruta de la base de datos
db_path = '/app/db.sqlite3'
# Generar nombre de archivo de respaldo con la fecha y hora actuales en la zona horaria de Lima
backup_path = f'/app/backups/db_backup_{now_lima.strftime("%Y%m%d_%H%M%S")}.sqlite3'

# Copia de seguridad
shutil.copyfile(db_path, backup_path)
print(f'Respaldo creado en: {backup_path}')


# Ejecutar dentro de Docker/contenedor Django
# python backup.py