from docscan.models import Document

# Obtén todos los registros de la tabla Document
documents = Document.objects.all()

# Elimina todos los registros de la tabla Document
documents.delete()