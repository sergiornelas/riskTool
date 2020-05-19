from django.urls import path
from . import views

urlpatterns = [
    path('approvalsList', views.approvalsList, name='approvalsList'),
    path('approvalsList/<int:exclude_patch_ID>', views.approvalDetail, name='approvalDetail'),
]