from django.contrib import admin

# from .models import exception_status
# from .models import exceptionTable

# admin.site.register(exception_status)
# admin.site.register(exceptionTable)

#--------------------------------------------------

from .models import exclude_patch

class ExcludePatchesAdmin(admin.ModelAdmin):
    #list_display = ('id', 'title', 'justification', 'excludeDate')
    list_display = ('id', 'user', 'title', 'justification', 'excludeDate')

    #list_display_links = ('id', 'title')
    list_display_links = ('id', 'user', 'title')

    search_fields = ('excludeDate',)

    #list_display = ('id', 'title')
    list_display = ('id', 'user', 'title')
    
    search_fields = ('title',)
    list_per_page = 25

admin.site.register(exclude_patch, ExcludePatchesAdmin)