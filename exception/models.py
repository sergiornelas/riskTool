from django.db import models
from datetime import datetime

#se utiliza para utilizar el id foraneo del usuario
from django.conf import settings
from django.contrib.auth.models import User

class exclude_patch(models.Model):

    #ESTE ES EL MERO MERO
    #id = models.AutoField(primary_key=True, auto_created=True)
    #cascade = if you delete the parent it will delete the childs

    patchFrom = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    excludeDate = models.DateTimeField(default=datetime.now, blank=False)
    
    #user_id = models.IntegerField(blank=True)

    def __str__(self):
	    return self.title