from django.contrib import admin

from .models import SERVER
#from .models import SERVER_APPROVER_RELATION, SERVER_CLIENT_RELATION

class serverAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostname', 'os', 'reboot_required', 'domain', 'ansible_id', 'carbon_black', 'crowd_strike', 'big_fix')

    list_display_links = ('id', 'hostname', 'os')
    search_fields = ('hostname',)
    list_per_page = 25

# class serverApprover(admin.ModelAdmin):
#     list_display = ('id', 'server', 'approver')

#     list_display_links = ('id', 'server', 'approver')
#     search_fields = ('server',)
#     list_per_page = 25

# class serverClient(admin.ModelAdmin):
#     list_display = ('id', 'server', 'client')

#     list_display_links = ('id', 'server', 'client')
#     search_fields = ('server',)
#     list_per_page = 25



# admin.site.unregister(User)

admin.site.register(SERVER, serverAdmin)
# admin.site.register(SERVER, serverApprover)
# admin.site.register(SERVER, serverClient)