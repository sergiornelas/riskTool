from django.contrib import admin
from django.urls import path
from django.urls import include

#new added (estilo al admin)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')), #linking the urls.py of the pages app. #'' = homepage
    #path('patchlist/', include('clients.urls')),
    path('patchlist/', include('patches.urls')),
    path('approvallist/', include('approvers.urls')),

    path('admin/', admin.site.urls),
    
    #new added (estilo al admin)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)