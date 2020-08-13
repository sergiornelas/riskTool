from django.urls import path
from . import views

urlpatterns = [
    path('approvalsList', views.approvalsList, name='approvalsList'),
    path('authorize', views.authorize, name='authorize'),
    path('approvalsList/<int:exclude_patch_ID>', views.approvalDet, name='approvalDet'),
    path('search', views.search, name='search'),
]