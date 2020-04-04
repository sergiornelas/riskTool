from django.db import models
from datetime import datetime

#se utiliza para utilizar el id foraneo del usuario
from django.conf import settings

class exclude_patch(models.Model):

    #patch = models.CharField(max_length=200)
    #patch_id = models.IntegerField()

    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    excludeDate = models.DateTimeField(default=datetime.now, blank=False)
    def __str__(self):
	    return self.title