from django.contrib import admin

from .models import EXCEPTION
from .models import VALIDATE_EXCEPTION

class ExcludePatchesAdmin(admin.ModelAdmin):
    list_display = ('risk_id', 'client', 'title', 'patch_id', 'exclude_date', 'state')
    list_display_links = ('risk_id', 'title')
    search_fields = ('risk_id',)
    list_per_page = 25

class ExcludeValidationsAdmin(admin.ModelAdmin):

    list_display = ('id', 'state', 'approver', 'time')
    list_display_links = ('id', 'state')
    search_fields = ('state',)
    list_per_page = 25

admin.site.register(EXCEPTION, ExcludePatchesAdmin)
admin.site.register(VALIDATE_EXCEPTION, ExcludeValidationsAdmin)