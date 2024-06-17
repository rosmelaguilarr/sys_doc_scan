import shutil
import os

# Ruta de la base de datos
db_path = '/app/db.sqlite3'
# Restaurar desde el archivo de respaldo más reciente
backup_dir = '/app/backups'
backup_files = sorted(os.listdir(backup_dir), reverse=True)
latest_backup = os.path.join(backup_dir, backup_files[0])

# Restauración de respaldo
shutil.copyfile(latest_backup, db_path)
print(f'Base de datos restaurada desde: {latest_backup}')


# Ejecutar dentro de Docker/contenedor Django
# python restore.py