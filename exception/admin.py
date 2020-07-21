from django.contrib import admin

from .models import EXCEPTION
from .models import VALIDATE_EXCEPTION

class ExcludePatchesAdmin(admin.ModelAdmin):
    #list_display = ('risk_id', 'client', 'title', 'patch_id', 'exclude_date', 'state')
    list_display = ('risk_id', 'client', 'title', 'patch_id', 'exclude_date', 'state')

    readonly_fields = ('risk_id', 'server_id', 'client', 'content', 'exclude_date', 'action_plan', 'justification', 'title', 'patch_id', 'exception_type')

    list_display_links = ('risk_id', 'title')
    search_fields = ('state',)
    list_per_page = 25

class ExcludeValidationsAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'risk_id', 'state', 'approver', 'approver_pending')
    #readonly_fields = ('exception', 'comment', 'time', 'risk_id', 'approver')
    readonly_fields = ('exception', 'comment', 'time', 'approver', 'approver_pending', 'risk_id')


    list_display_links = ('id', 'state')
    search_fields = ('state', 'risk_id') #no funciona poner approver
    list_per_page = 25
   
admin.site.register(EXCEPTION, ExcludePatchesAdmin)
admin.site.register(VALIDATE_EXCEPTION, ExcludeValidationsAdmin)