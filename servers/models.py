from django.db import models

# Create your models here.
class server(models.Model):
    #id se genera solo
    hostname = models.CharField(max_length=45)
    os = models.CharField(max_length=45)
    reboot_required = models.CharField(max_length=45)

class contact(models.Model):
    #id se genera solo
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)

#class server_contact(models.Model):
    #id se genera solo
    # id = models.ForeignKey(server, on_delete=models.DO_NOTHING)
    # id = models.ForeignKey(contact, on_delete=models.DO_NOTHING)