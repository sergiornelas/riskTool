from django.contrib import admin

from .models import SERVER
#from .models import SERVER_APPROVER_RELATION, SERVER_CLIENT_RELATION
from .models import SERVER_USER_RELATION

class serverAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostname', 'os', 'reboot_required', 'domain', 'ansible_id', 'carbon_black', 'crowd_strike', 'big_fix')

    list_display_links = ('id', 'hostname', 'os')
    search_fields = ('hostname',)
    list_per_page = 25

    readonly_fields = ('id', 'hostname', 'os', 'reboot_required', 'domain', 'ansible_id', 'carbon_black', 'crowd_strike', 'big_fix')

class serverApprover(admin.ModelAdmin):
    list_display = ('id', 'server' , 'user_id')

    list_display_links = ('id', 'server')
    search_fields = ('server',)
    list_per_page = 25

admin.site.register(SERVER, serverAdmin)
#admin.site.register(SERVER_USER_RELATION, serverApprover)