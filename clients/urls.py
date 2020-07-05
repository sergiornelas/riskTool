from django.urls import path
from . import views

urlpatterns = [
    #path('<int:user_id>', views.dashboard, name='dashboard'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('exceptionsBoard', views.exceptionsBoard, name='exceptionsBoard'),
    
    path('exclude_server', views.exclude_server, name='exclude_server'),
    path('server_user_list', views.server_user_list, name='server_user_list'),
    
    path('filterPatches', views.filterPatches, name='filterPatches'),
    
    #new
    path('serverOrPatch', views.serverOrPatch, name='serverOrPatch'),
    path('selectServers', views.selectServers, name='selectServers'),
    path('selectServerPatch', views.selectServerPatch, name='selectServerPatch'),
    path('selectPatches', views.selectPatches, name='selectPatches'),
    path('inquiryServers', views.inquiryServers, name='inquiryServers'),
    path('inquiryPatches', views.inquiryPatches, name='inquiryPatches'),

    path('getDaysLimit', views.getDaysLimit, name='getDaysLimit'),

    path('transform', views.transform, name='transform'),

    path('getValidationDetails', views.getValidationDetails, name='getValidationDetails'),
    path('getApprovalNames', views.getApprovalNames, name='getApprovalNames'),

    path('getHostnames', views.getHostnames, name='getHostnames'),
    path('getAdvisoriesDesc', views.getAdvisoriesDesc, name='getAdvisoriesDesc'),
    path('getServerIDServer', views.getServerIDServer, name='getServerIDServer'),
    path('getServerIDPatch', views.getServerIDPatch, name='getServerIDPatch'),

    

    path('clean', views.clean, name='clean'),
    #path('getPatchObject', views.getPatchObject, name='getPatchObject'),
    
]