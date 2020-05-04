from django.db import models
from datetime import datetime

#se utiliza para utilizar el id foraneo del usuario
from django.conf import settings
from django.contrib.auth.models import User

#*
from patches.models import patch
from approvers.models import patchApproverRelationship
#*

class exclude_patch(models.Model):
    #patch_from = models.ForeignKey(patch, to_field="id", db_column="patch_from", on_delete=models.CASCADE, null=True)
    
    #patch_from = models.ForeignKey(patch, on_delete=models.DO_NOTHING, null=True)

    patch_id = models.IntegerField(null=True)
    
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    exclude_date = models.DateTimeField(default=datetime.now, blank=False)
    
    def __str__(self):
	    return self.title