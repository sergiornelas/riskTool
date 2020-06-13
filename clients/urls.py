from django.urls import path
from . import views

urlpatterns = [
    #path('<int:user_id>', views.dashboard, name='dashboard'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('exclude_server', views.exclude_server, name='exclude_server'),
    path('patch_server_list', views.patch_server_list, name='patch_server_list'),
    
]