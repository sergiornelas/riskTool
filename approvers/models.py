from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from patches.models import patch
from exception.models import exclude_patch
from django.conf import settings
from django import forms
from django.forms import ModelForm

APP = "Approved"
REJ = "Rejected"
PEND = "Pending"

state_choices = (
    (APP, "Approved"),
    (REJ, "Rejected"),
    (PEND, "Pending"),
)

#La relación entre un parche y el aprobador es de muchos a muchos, se necesita crear un nuevo modelo para ello.
class patchApproverRelationship(models.Model):
    patch = models.ForeignKey(patch, on_delete=models.CASCADE, null=True)
    #patch = models.ManyToManyField(patch)

    approver = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, related_name='approverz')

    # def __str__(self):
	#     return self.approver

    # def __str__(self):
    #     return str(self.ProductName) if self.ProductName else ''

class authorize_Exception(models.Model):
    #exception = models.ForeignKey(exclude_patch, on_delete=models.CASCADE, null=True)
    exception_id = models.IntegerField(null=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, related_name='approverAuthorize')
    state = models.CharField(max_length=8, choices = state_choices, default = PEND)
    comment = models.TextField(blank=True, default="Pending")

# class authorizeException(forms.ModelForm):
#     class Meta:
#         model = patchApproverRelationship
#         #fields = ['patch', 'approver', 'state', 'comment']
#         fields = '__all__'