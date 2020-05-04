from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.logout, name='logout'),
    
    #messages
    path('login', views.login, name='login'),

    #path('<int:user_id>', views.dashboard, name='dashboard'),
    
    path('dashboard', views.dashboard, name='dashboard'),

    path('approvalsList', views.approvalsList, name='approvalsList'),

    path('approvalsList/<int:patch_id>', views.approvalDetail, name='approvalDetail'), #views.listing refers to the listing method.

    #first parameter: empty path means home directory like /
    #second parameter: method we want to connect in the view file
    #third parameter: name to easily access this path
]