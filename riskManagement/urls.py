from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('pages.urls')), #linking the urls.py of the pages app. #'' = homepage
    path('patchlist/', include('clients.urls')),
    path('approvallist/', include('approvers.urls')),

    path('admin/', admin.site.urls),
]