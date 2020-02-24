from django.contrib import admin
from .models import patch
from .models import exclude_patch

admin.site.register(patch)
admin.site.register(exclude_patch)