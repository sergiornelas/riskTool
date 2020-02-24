from django.db import models
from datetime import datetime

class patch(models.Model):
    server_package = models.CharField(max_length=30)
    time = models.DateTimeField(default=datetime.now, blank=False)
    criticality = models.CharField(max_length=30)
    def __str__(self):
	    return self.server_package

class exclude_patch(models.Model):
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    excludeDate = models.DateTimeField(default=datetime.now, blank=False)
    #foraneas del modelo de arriba:
    #server_package = models.ForeignKey(patch, on_delete=models.DO_NOTHING)
    def __str__(self):
	    return self.title