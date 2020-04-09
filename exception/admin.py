from django.contrib import admin
from .models import exclude_patch

class ExcludePatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'patchFrom', 'title', 'justification', 'excludeDate')
    
    list_display_links = ('id', 'title')
    
    search_fields = ('excludeDate',)

    list_display = ('id', 'title')
        
    search_fields = ('title',)
    list_per_page = 25

admin.site.register(exclude_patch, ExcludePatchesAdmin)