from django.contrib import admin
from .models import PATCHES

class PatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'advisory_id', 'server_id', 'scheduled_date')
    
    list_display_links = ('id', 'advisory_id')
    search_fields = ('id',)
    list_per_page = 25

admin.site.register(PATCHES, PatchesAdmin)