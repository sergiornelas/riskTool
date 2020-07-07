from django.db import models
from datetime import datetime
from servers.models import SERVER
from advisory.models import ADVISORY

from django.conf import settings

class PATCHES(models.Model):
    is_supported=models.PositiveSmallIntegerField(default=1)
    due_date=models.DateField(default=datetime.now, blank=False)
    scheduled_date=models.DateTimeField(default=datetime.now, blank=False)
    is_overdue=models.PositiveSmallIntegerField(default=0)

    server=models.ForeignKey(SERVER, on_delete=models.CASCADE, null=True)
    advisory=models.ForeignKey(ADVISORY, on_delete=models.CASCADE, null=True)

    #estos solo funcionan en python (server side):
    #def __str__(self):
    #    return (self.server.hostname + " : " + self.advisory.description)

    def __str__(self):
        return (self.server.hostname + " : " + "'" + self.advisory.description + "'" +" , ")



# NO SE TE OLVIDE QUITAR EL NULL CUANDO EN EL CAMPO DEL USER, AL MOMENTO QUE HAGAS DEL DEPLOY AL SERVER.