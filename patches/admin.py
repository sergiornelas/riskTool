from django.contrib import admin
from .models import patch
#]
#from .models import patchApproverRelationship

class PatchesAdmin(admin.ModelAdmin):
    #list_display = ('id', 'server_package', 'time', 'criticality', 'user', 'approver')
    list_display = ('id', 'server_package', 'time', 'criticality')
    list_display_links = ('id', 'server_package')
    search_fields = ('server_package',)
    list_per_page = 25

admin.site.register(patch, PatchesAdmin)