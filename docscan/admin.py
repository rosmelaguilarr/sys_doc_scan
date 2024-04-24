from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(Document, DocumentAdmin)
