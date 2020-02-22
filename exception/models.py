from django.db import models

class exception_status(models.Model):
    #id se genera solo
    name = models.CharField(max_length=45)

class exceptionTable(models.Model):
    #id se genera solo
    approval_name = models.CharField(max_length=45)
    expiration = models.CharField(max_length=45)
    # id = models.ForeignKey(exception_status, on_delete=models.DO_NOTHING)