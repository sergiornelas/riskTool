from django.contrib import admin
from .models import PATCHES

class PatchesAdmin(admin.ModelAdmin):
    #list_display = ('patch_id', 'advisory_id', 'server_id', 'scheduled_date')
    #list_display = ('patch_id', 'is_supported', 'due_date', 'is_overdue', 'advisory_id', 'scheduled_date', 'server_id', 'created_date' ,'last_update_date', 'patched_date', 'status_id', 'exception_id')
    list_display = ('patch_id', 'advisory_id', 'server_id', 'scheduled_date', 'created_date' ,'last_update_date')

    readonly_fields = ('patch_id', 'advisory', 'server', 'is_supported', 'due_date', 'is_overdue', 'scheduled_date', 'created_date' ,'last_update_date', 'patched_date', 'status_id', 'exception_id')
    #readonly_fields = ('patch_id', 'advisory_id', 'server_id', 'scheduled_date', 'created_date' ,'last_update_date')
    
    list_display_links = ('patch_id',)
    search_fields = ('patch_id',)
    list_per_page = 25

admin.site.register(PATCHES, PatchesAdmin)