from django.contrib import admin
from .models import patch_status
from .models import patch

admin.site.register(patch_status)
admin.site.register(patch)
# Register your models here.
