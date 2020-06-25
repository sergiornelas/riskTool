from django.urls import path
from . import views

urlpatterns = [
    #path('<int:user_id>', views.dashboard, name='dashboard'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('exceptionsBoard', views.exceptionsBoard, name='exceptionsBoard'),
    
    path('exclude_server', views.exclude_server, name='exclude_server'),
    path('server_user_list', views.server_user_list, name='server_user_list'),
    
    path('filterPatches', views.filterPatches, name='filterPatches'),
    #path('testing/<int:number>', views.testing, name='testing'),
    
]