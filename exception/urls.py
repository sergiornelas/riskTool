from django.urls import path

from . import views

urlpatterns = [
    path('exclude', views.exclude, name='exclude'),
]