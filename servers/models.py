from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class SERVER(models.Model):
    hostname = models.CharField(max_length=30)
    os = models.CharField(max_length=30)
    reboot_required = models.CharField(max_length=5, default = "False")
    domain = models.CharField(max_length=30, default="ibmcloud.dst.ibm.com")
    ansible_id = models.PositiveSmallIntegerField(default=1)
    carbon_black = models.CharField(max_length=5, default = "N/A")
    crowd_strike = models.CharField(max_length=5, default = "N/A")
    big_fix = models.CharField(max_length=5, default = "True")

    # client = models.ForeignKey(settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE, null=True, related_name='client')

    # approver = models.ForeignKey(settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE, null=True, related_name='approver')

class SERVER_CLIENT_RELATION(models.Model):
    server = models.ForeignKey(SERVER, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)

class SERVER_APPROVER_RELATION(models.Model):
    server = models.ForeignKey(SERVER, on_delete=models.CASCADE, null=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)