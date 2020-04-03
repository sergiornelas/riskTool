from django.db import models
from datetime import datetime
#*
#from django.conf import settings
#*

#class exception_status(models.Model):
    ##id se genera solo
    #name = models.CharField(max_length=45)

class exclude_patch(models.Model):
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    excludeDate = models.DateTimeField(default=datetime.now, blank=False)
    #foraneas del modelo de arriba:
    #server_package = models.ForeignKey(patch, on_delete=models.DO_NOTHING)
    def __str__(self):
	    return self.title