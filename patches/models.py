from django.db import models
from datetime import datetime

#se utiliza para utilizar el id foraneo del usuario
from django.conf import settings

class patch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, related_name='users')
    server_package = models.CharField(max_length=30)
    time = models.DateTimeField(default=datetime.now, blank=False)
    criticality = models.CharField(max_length=30)

    

    #approver = models.ForeignKey(settings.AUTH_USER_MODEL,
    #    on_delete=models.CASCADE, null=True, related_name='approvers')

    def __str__(self):
	    #return self.criticality
        #return self.patch_id
        return str(self.id)

# on_delete=models.CASCADE 
# When the referenced object is deleted, also delete the objects that have references to it .

# NO SE TE OLVIDE QUITAR EL NULL CUANDO EN EL CAMPO DEL USER,
# AL MOMENTO QUE HAGAS DEL DEPLOY AL SERVER.