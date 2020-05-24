from django.urls import path

from . import views

urlpatterns = [
    path('exclude', views.exclude, name='exclude'),
    #path('approvalDetail2', views.approvalDetail2, name='approvalDetail2')
]