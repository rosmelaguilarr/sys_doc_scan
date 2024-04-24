from django.db import models

""" class VideoQuery(models.QuerySet):
    def visible(self):
        return self.filter(visible=True) """
    


class DocumentManager(models.Manager):

    """ def get_queryset(self):
        return VideoQuery(self.model, using=self._db)   """

    """ def get_by_duration(self, duration=0):
        return self.get_queryset().visible().filter(duration__gte=duration)

    def get_by_title(self, title):
        return self.get_queryset().visible().filter(title__icontains=title) """
    
    def get_by_description(self, description):
        return self.filter(description__icontains=description) 
    
    def get_by_doctype(self, doctype):
        return self.filter(doctype__icontains=doctype) 
    
    def get_by_date(self, date):
        return self.filter(dateregister__icontains=date) 
    
    def get_by_origin(self, origin):
        return self.filter(origin__icontains=origin) 