from django.db import models
from datetime import datetime
#*
from django.conf import settings
#*

class patch(models.Model):
    #* Estamos tomando el nombre del dueño del patch.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    #*
    server_package = models.CharField(max_length=30)
    time = models.DateTimeField(default=datetime.now, blank=False)
    criticality = models.CharField(max_length=30)

    def __str__(self):
	    return self.server_package

#*NUEVAS NOTAS:

#on_delete=models.CASCADE 
# When the referenced object is deleted, also delete the objects 
# that have references to it .

# NO SE TE OLVIDE QUITAR EL NULL CUANDO EN EL CAMPO DEL USER,
# AL MOMENTO QUE HAGAS DEL DEPLOY AL SERVER.