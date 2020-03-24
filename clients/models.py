from django.db import models
#from django.contrib.auth.models.User
#from django.conf import settings
#*
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   department = models.CharField(max_length=100)
#*