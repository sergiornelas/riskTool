from django.contrib import admin

# from .models import exception_status
# from .models import exceptionTable

# admin.site.register(exception_status)
# admin.site.register(exceptionTable)

#-----
from django.conf import settings
from patches.models import patch
from django.contrib.auth.models import User
#-----

#--------------------------------------------------

from .models import exclude_patch

class ExcludePatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'patchFrom', 'title', 'justification', 'excludeDate')
    #este:
    #list_display = ('id', 'user', 'title', 'justification', 'excludeDate')

    list_display_links = ('id', 'title')
    #este:
    #list_display_links = ('id', 'user', 'title')

    search_fields = ('excludeDate',)

    list_display = ('id', 'title')
    #este:
    #list_display = ('id', 'user', 'title')
    
    search_fields = ('title',)
    list_per_page = 25

admin.site.register(exclude_patch, ExcludePatchesAdmin)