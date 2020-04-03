from django.shortcuts import render, redirect

#from django.shortcuts import get_object_or_404

#message alerts
from django.contrib import messages

#user registration, model 
from django.contrib.auth.models import User

#user registration, login after register
from django.contrib import auth

#*
from patches.models import patch
#*

def login(request):
	
	# patches = patch.objects.all() #agarramos todos los objetos (elementos de bases de datos)
	# 			     #los almacenamos en la variable listings
	# context = {
    # 	'patches': patches #almacenamos los valores de la bd a un diccionario.
    # }

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
        #new method
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			messages.success(request, 'You are now logged in')
			return redirect('dashboard')
		else:
			messages.error(request, 'Invalid credentials')
			print ("Credenciales erroneas")
			#return redirect('login')
			return redirect('index')
	else:
		return render(request, 'pages/index.html')

#log out & navbar auth links
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
	#*
	#client_patches = patch.objects.order_by('-contact_date').filter(user_id=request.user.id)
	#client_patches = patch.objects.filter(user_id=request.user.id)
	client_patches = patch.objects.filter(user=request.user.id)
	context = {
		'patches': client_patches
	}
	#*
	return render(request, 'clients/dashboard.html', context)