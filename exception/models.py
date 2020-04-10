from django.db import models
from datetime import datetime

#se utiliza para utilizar el id foraneo del usuario
from django.conf import settings
from django.contrib.auth.models import User

#*
from patches.models import patch
#*

class exclude_patch(models.Model):

    #ESTE ES EL MERO MERO
    #id = models.AutoField(primary_key=True, auto_created=True)
    #cascade = if you delete the parent it will delete the childs

    #con esto hereda el id
    patch = models.ForeignKey(patch, on_delete=models.CASCADE, null=True)
    # patch = models.IntegerField(null=True)

    client = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    exclude_date = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
	    return self.title