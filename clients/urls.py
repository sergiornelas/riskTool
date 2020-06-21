from django.urls import path
from . import views

urlpatterns = [
    #path('<int:user_id>', views.dashboard, name='dashboard'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('exclude_server', views.exclude_server, name='exclude_server'),
    path('server_user_list', views.server_user_list, name='server_user_list'),
    path('patch_user_list', views.patch_user_list, name='patch_user_list'),    
]