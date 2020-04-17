from django.db import models
from django.contrib.auth.models import User
# Create your models here.
Roles = (
    ('sales', 'SALES'),
    ('operations', 'OPERATIONS'),
    ('cashier', 'CASHIER'),
    ('frontdesk', 'FRONTDESK'),
    ('client', 'CLIENT'),
)

class UserProfile2(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,    default=None, null=True)
    role = models.CharField(max_length=50, choices=Roles, default='client')

    def __str__(self):
        return self.user.username