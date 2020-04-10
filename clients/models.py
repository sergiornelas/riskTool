from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
   id = models.AutoField(primary_key=True, auto_created=True)
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   department = models.CharField(max_length=100)