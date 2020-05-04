from django.urls import path
from . import views

urlpatterns = [
    
    path('approvalsList', views.approvalsList, name='approvalsList'),

    path('approvalsList/<int:patch_id>', views.approvalDetail, name='approvalDetail'), #views.listing refers to the listing method.
]