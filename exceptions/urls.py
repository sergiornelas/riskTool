from django.urls import path

from . import views

#lo cree solo para ver si funcionaba el dashboard <form action="{% url 'exclude' %}" method="POST">
# Y SI ES NECESARIO!!
urlpatterns = [
    path('exclude', views.exclude, name='exclude')
]