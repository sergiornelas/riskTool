from django.contrib import admin
from .models import exception_status
from .models import exceptionTable

admin.site.register(exception_status)
admin.site.register(exceptionTable)

# Register your models here.
