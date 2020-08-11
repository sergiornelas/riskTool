from django.urls import path
from . import views

urlpatterns = [
    #path('<int:user_id>', views.dashboard, name='dashboard'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('exceptionsBoard', views.exceptionsBoard, name='exceptionsBoard'),
    
    path('exclude_server', views.exclude_server, name='exclude_server'),
    #path('exclude_server/<slug:serverString>', views.exclude_server, name='exclude_server'),

    path('searchClient', views.searchClient, name='searchClient'),
    

    path('server_user_list', views.server_user_list, name='server_user_list'),
    path('server_user_list2', views.server_user_list2, name='server_user_list2'),
    
    path('filterPatches', views.filterPatches, name='filterPatches'),
    
    #new
    path('serverOrPatch', views.serverOrPatch, name='serverOrPatch'),
    path('selectServers', views.selectServers, name='selectServers'),
    path('selectServerPatch', views.selectServerPatch, name='selectServerPatch'),
    path('selectPatches', views.selectPatches, name='selectPatches'),
    path('inquiryServers', views.inquiryServers, name='inquiryServers'),
    path('inquiryPatches', views.inquiryPatches, name='inquiryPatches'),
    
    path('inquiryEdit/<int:exclude_patch_ID>', views.inquiryEdit, name='inquiryEdit'),
    path('updateException/<int:exclude_patch_ID>', views.updateException, name='updateException'),
    path('deleteException/<int:deleteRow>', views.deleteException, name='deleteException'),
    
        

    path('getDaysLimit', views.getDaysLimit, name='getDaysLimit'),

    path('transform', views.transform, name='transform'),

    path('getValidationDetails', views.getValidationDetails, name='getValidationDetails'),
    path('getApprovalNames', views.getApprovalNames, name='getApprovalNames'),
    path('getValidationsRemaining', views.getValidationsRemaining, name='getValidationsRemaining'),

    path('getHostnames', views.getHostnames, name='getHostnames'),
    path('getAdvisoriesDesc', views.getAdvisoriesDesc, name='getAdvisoriesDesc'),
    #path('getCriticality', views.getCriticality, name='getCriticality'),
    path('getServerIDServer', views.getServerIDServer, name='getServerIDServer'),
    path('getServerIDPatch', views.getServerIDPatch, name='getServerIDPatch'),

    

    path('clean', views.clean, name='clean'),
    path('cleanEdit', views.cleanEdit, name='cleanEdit'),
    
    path('getPatchesInquiryServer', views.getPatchesInquiryServer, name='getPatchesInquiryServer'),

    path('contentSeparated', views.contentSeparated, name='contentSeparated'),

    #path('exceptionDet/<int:exclude_patch_ID>', views.exceptionDet, name='exceptionDet'),
    path('exceptionDetail/<int:exclude_patch_ID>', views.exceptionDetail, name='exceptionDetail'),   
        
    #path('getPatchObject', views.getPatchObject, name='getPatchObject'),   
]