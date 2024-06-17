from django.contrib import admin
from .models import Document

admin.site.site_header = "Sistema Digital de Archivo Central | ARDIG"
admin.site.site_title = "ARDIG"

class DocumentAdmin(admin.ModelAdmin):
    list_display = ["fileupload","doctype","direction","folios","dateregister","user"]
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(Document, DocumentAdmin)
