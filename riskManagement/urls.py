from django.contrib import admin
from django.urls import path
from django.urls import include

#new added (estilo al admin)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #root paths
    path('', include('pages.urls')), #linking the urls.py of the pages app. #'' = homepage
    path('patchlist/', include('patches.urls')),
    path('approvallist/', include('approvers.urls')),

    path('admin/', admin.site.urls),
    
    #testing
    path('test/', include('clients.urls')),
    
    #new added (estilo al admin)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#dentro de views.py de cualquier aplicación, si quieres hacer una función
#para crear un url, y el archivo html se encuentra dentro de la carpeta
#templates pero fuera de una carpeta dentro de templates, entonces la puedes
#referir de esta manera:
#def test(request):
#    return render(request, './base.html')