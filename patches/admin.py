from django.contrib import admin
from .models import patch
from .models import exclude_patch

class PatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'server_package', 'time', 'criticality')
    list_display_links = ('id', 'server_package')
    search_fields = ('server_package',)
    list_per_page = 25

class ExcludePatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'justification', 'excludeDate')
    list_display_links = ('id', 'title')
    search_fields = ('excludeDate',)
    list_per_page = 25

admin.site.register(patch, PatchesAdmin)
admin.site.register(exclude_patch, ExcludePatchesAdmin)