from django.db import models
from datetime import datetime
from servers.models import SERVER
from advisory.models import ADVISORY

from django.conf import settings

class patch(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, related_name='users')
    server_package = models.CharField(max_length=30)
    time = models.DateTimeField(default=datetime.now, blank=False)
    criticality = models.CharField(max_length=30, null=True)

    def __str__(self):
	    return str(self.id)

class PATCHES(models.Model):
    is_supported=models.PositiveSmallIntegerField(default=1)
    due_date=models.DateTimeField(default=datetime.now, blank=False)
    is_overdue=models.PositiveSmallIntegerField(default=0)

    server=models.ForeignKey(SERVER, on_delete=models.CASCADE, null=True)
    advisory=models.ForeignKey(ADVISORY, on_delete=models.CASCADE, null=True)
    #FALTA AGREGAR LA EXCEPCION


# NO SE TE OLVIDE QUITAR EL NULL CUANDO EN EL CAMPO DEL USER,
# AL MOMENTO QUE HAGAS DEL DEPLOY AL SERVER.