from django.db import models
from datetime import datetime
from django.conf import settings

APP = "Approved"
REJ = "Rejected"
PEND = "Pending"

state_choices = (
    (APP, "Approved"),
    (REJ, "Rejected"),
    (PEND, "Pending"),
)

class EXCEPTION(models.Model):
    patch_id = models.IntegerField(null=True)
    title = models.CharField(max_length=30)
    justification = models.TextField(blank=False)
    action_plan=models.TextField(blank=False)
    exclude_date = models.DateTimeField(default=datetime.now, blank=False)
    state = models.CharField(max_length=8, choices = state_choices, default = PEND)

class AUTHORIZE_EXCEPTION(models.Model):
    exception_id = models.IntegerField(null=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    comment = models.TextField(blank=True, default="Pending")
    state = models.CharField(max_length=8, choices = state_choices, default = PEND)

    




#---------------------OLD RISK MANAGEMENT-----------------------------------------------------

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

class approve_Exception(models.Model):
    #exception = models.ForeignKey(exclude_patch, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=8, choices = state_choices, default = PEND)
    comment = models.TextField(blank=True, default="Pending")
    exception_id = models.IntegerField(null=True, default=0)
    patch_id = models.IntegerField(null=True, default=0)
    approver_id = models.IntegerField(null=True, default=0)