from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from patches.models import patch
from django.conf import settings

#La relación entre un parche y el aprobador es de muchos a muchos, se necesita crear un nuevo modelo para ello.
class patchApproverRelationship(models.Model):
    patch = models.ForeignKey(patch, on_delete=models.CASCADE, null=True)
    #patch = models.ManyToManyField(patch)

    approver = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, related_name='approverz')

    state = models.BooleanField(default=False)

    # def __str__(self):
	#     return self.approver

    # def __str__(self):
    #     return str(self.ProductName) if self.ProductName else ''