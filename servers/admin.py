from django.contrib import admin

from .models import server
from .models import contact

admin.site.register(server)
admin.site.register(contact)
# Register your models here.