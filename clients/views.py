from django.shortcuts import render
from django.http import HttpResponse

#show data frontend
#BOOOM!!, agarré el modelo de la aplicación de patches.
from patches.models import patch

# Create your views here.
def index(request):

	patches = patch.objects.all() #agarramos todos los objetos (elementos de bases de datos)
				     #los almacenamos en la variable listings
	context = {
    	'patches': patches #almacenamos los valores de la bd a un diccionario.
    }

	return render(request, 'patches/patchList.html', context)

def exclude(request):
	return render(request, 'patches/excludePatch.html')