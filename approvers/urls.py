from django.urls import path
from . import views

urlpatterns = [
    path('approvalsList', views.approvalsList, name='approvalsList'),
    path('approvalsList/<int:exclude_patch_ID>', views.approvalDetail, name='approvalDetail'),
    
    path('authorize', views.authorize, name='authorize'),
    #path('authorize/<int:exclude_patch_ID>', views.authorize, name='authorize'),
    #path('authorize/<int:user_id>', views.authorize, name='authorize'),
]