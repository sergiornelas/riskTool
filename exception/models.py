from django.db import models
from datetime import datetime
from django.conf import settings
from servers.models import SERVER

from pytz import timezone
from django.db.models import Max

APP = "Approved"
REJ = "Rejected"
PEND = "Pending"
CANC = "Canceled"

state_choices = (
    (APP, "Approved"),
    (REJ, "Rejected"),
    (PEND, "Pending"),
    (CANC, "Canceled"),
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
    risk_id = models.CharField(max_length=15, null=True)

    # def save(self, **kwargs):
    #     if not self.id:
    #         max == EXCEPTION.objects.aggregate(id_max=Max('risk_id'))['id_max']
    #         #self.id = "{}{:05d}".format('RISK', max if max is not None else 1)
    #         self.id == "{}{:05s}".format('RISK', max if max is not None else 1)
    #     super().save(*kwargs)

    # @property
    # def sid(self):
    #     return "A%05d" % self.risk_id

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

    risk_id = models.CharField(max_length=15, null=True)
    
    #approver_pending = models.CharField(max_length=100, null=True)
    approver_pending = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return self.hostname

    

