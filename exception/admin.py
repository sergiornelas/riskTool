from django.contrib import admin

from .models import EXCEPTION
from .models import VALIDATE_EXCEPTION

class ExcludePatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'title', 'justification', 'exclude_date')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_per_page = 25

class ExcludeValidationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'comment', 'approver', 'time', 'exception')
    list_display_links = ('id', 'state')
    search_fields = ('state',)
    list_per_page = 25

admin.site.register(EXCEPTION, ExcludePatchesAdmin)
admin.site.register(VALIDATE_EXCEPTION, ExcludeValidationsAdmin)