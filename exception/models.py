from django.db import models
from datetime import datetime
from django.conf import settings
from servers.models import SERVER

from pytz import timezone

APP = "Approved"
REJ = "Rejected"
PEND = "Pending"

state_choices = (
    (APP, "Approved"),
    (REJ, "Rejected"),
    (PEND, "Pending"),
)

Patch = "Patch"
Server = "Server"

exception_choices = (
    (Patch, "Patch"),
    (Server, "Server"),
)

class EXCEPTION_TYPE(models.Model):
    #type = models.CharField(max_length=10)
    kind = models.CharField(max_length=8, choices = exception_choices)

class AUTHORIZE_TYPE(models.Model):
    #type = models.CharField(max_length=10)
    kind = models.CharField(max_length=8, choices = state_choices)



class EXCEPTION(models.Model):
    #kind = models.ForeignKey(EXCEPTION_TYPE, null=True, on_delete=models.CASCADE) #patch, server
    #state = models.ForeignKey(AUTHORIZE_TYPE, null=True, on_delete=models.CASCADE) #approved, rejected, pending
    state = models.CharField(max_length=8, choices = state_choices, default = PEND)
    exception_type = models.IntegerField(null=True)

    #patch_id = models.IntegerField(null=True) #!
    patch_id = models.TextField(null=True) #!
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    action_plan=models.TextField(blank=False)
    exclude_date = models.DateTimeField(default=datetime.now, blank=False)
    content=models.TextField(blank=False, null=True)
    
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)

    #server = models.ForeignKey(SERVER, on_delete=models.CASCADE, null=True)
    #TEMPORAL!!!!!
    server_id = models.TextField(null=True) #!

#now = datetime.utcnow().replace(tzinfo=timezone('America/Mexico_City'))

class VALIDATE_EXCEPTION(models.Model):
    #exception = models.IntegerField(null=True)
    
    exception = models.ForeignKey(EXCEPTION, on_delete=models.CASCADE, null=True)
    
    approver = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, related_name='approverValidate')

    state = models.CharField(max_length=8, choices = state_choices, default = PEND)
    comment = models.TextField(blank=True, default="Pending")
    #time = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=timezone('America/Mexico_City')), blank=False)
    time = models.DateTimeField(default=datetime.now, blank=False)