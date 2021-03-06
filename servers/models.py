from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class SERVER(models.Model):
    hostname = models.CharField(max_length=30)
    os = models.CharField(max_length=30)
    reboot_required = models.CharField(max_length=5, default = "False")
    domain = models.CharField(max_length=30, default="ibmcloud.dst.ibm.com")
    ansible_id = models.CharField(max_length=50)
    carbon_black = models.CharField(max_length=5, default = "N/A")
    crowd_strike = models.CharField(max_length=5, default = "N/A")
    big_fix = models.CharField(max_length=5, default = "True")

    def __str__(self):
        return self.hostname

class SERVER_USER_RELATION(models.Model):
    server = models.ForeignKey(SERVER, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)