from django.urls import path
from . import views

urlpatterns = [
   	path('', views.index, name='approvalzlist'),

    #first parameter: empty path means home directory like /
    #second parameter: method we want to connect in the view file
    #third parameter: name to easily access this path
]