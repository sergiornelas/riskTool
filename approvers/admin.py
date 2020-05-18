from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#from .models import Profile
from .models import patchApproverRelationship

class approvers_patch(admin.ModelAdmin):
    #list_display = ('id', 'patch', 'approver')
    list_display = ('patch', 'approver')
    #list_display = ('id', 'patch')
    list_display_links = ('patch'),

    # list_display = ('approver'),
    # list_display_links = ('approver'),
    
    search_fields = ('patch'),
    list_per_page = 25

admin.site.register(patchApproverRelationship, approvers_patch)