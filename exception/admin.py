from django.contrib import admin
from .models import exclude_patch

class ExcludePatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'title', 'justification', 'exclude_date')
    list_display_links = ('id', 'title')
    search_fields = ('exclude_date',)
    list_per_page = 25

admin.site.register(exclude_patch, ExcludePatchesAdmin)