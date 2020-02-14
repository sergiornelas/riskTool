from django.contrib import admin

# Register your models here.
from .models import package_criticality
from .models import package

admin.site.register(package_criticality)
admin.site.register(package)