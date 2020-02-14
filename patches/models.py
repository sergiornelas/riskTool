from django.db import models
from servers.models import server
from packages.models import package
from exception.models import exceptionTable

class patch_status(models.Model):
    #id se genera solo
    name = models.CharField(max_length=45)
    
class patch(models.Model):
    #id se genera solo
    dou_supported = models.CharField(max_length=30)
    # id = models.ForeignKey(server, on_delete=models.DO_NOTHING)
    # id = models.ForeignKey(package, on_delete=models.DO_NOTHING)
    # id = models.ForeignKey(patch_status, on_delete=models.DO_NOTHING)
    # id = models.ForeignKey(exceptionTable, on_delete=models.DO_NOTHING)
    is_supported = models.IntegerField()