from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#from .models import Profile
#from .models import patchApproverRelationship
#from .models import authorize_Exception

# class approvers_patch(admin.ModelAdmin):
#     #list_display = ('id', 'patch', 'approver')
#     list_display = ('patch', 'approver_id')
#     #list_display = ('id', 'patch')
#     list_display_links = ('patch'),

#     # list_display = ('approver'),
#     # list_display_links = ('approver'),
    
#     search_fields = ('patch'),
#     list_per_page = 25

# class authorizeExc(admin.ModelAdmin):
#     list_display = ('id', 'exception_id', 'approver_id', 'state', 'comment')
#     list_display_links = ('state'),

#     search_fields = ('exception_id'),
#     list_per_page = 25

# admin.site.register(patchApproverRelationship, approvers_patch)
# admin.site.register(authorize_Exception, authorizeExc)