from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('ajax', views.ajax, name='ajax'),

    #path('testPath', views.test, name='tewaefast'),
    #path('testJS', views.javascript, name='awef'),

    path('firstOBJECTS', views.firstOBJECTS, name='firstOBJECTS'),
    # path('post', views.post, name='post'),

    #test
    path('test', views.test, name='test'),
]