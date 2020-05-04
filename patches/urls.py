from django.urls import path
from . import views

urlpatterns = [
   	#first parameter: empty path means home directory like /
    #second parameter: method we want to connect in the view file
    #third parameter: name to easily access this path
       
    path('json', views.list, name='list'),
]