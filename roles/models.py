from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.conf import settings

class Profile(models.Model):
    CLIENT = 1
    APPROVER = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (CLIENT, 'Client'),
        (APPROVER, 'Approver'),
        (ADMIN, 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

#Django Signals es una estrategia para permitir que las aplicacionesdesacopladas sean notificadas
# cuando ocurren ciertos eventos.