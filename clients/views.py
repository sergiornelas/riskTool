from django.shortcuts import render, redirect

#message alerts
from django.contrib import messages

#user registration, model 
from django.contrib.auth.models import User

#user registration, login after register
from django.contrib import auth

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
        #new method
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			messages.success(request, 'You are now logged in')
            #return redirect('dashboard')
			return redirect('dashboard')
		else:
			messages.error(request, 'Invalid credentials')
			print ("no se conecto compa")
			#return redirect('login')
			return redirect('index')
	else:
		return render(request, 'pages/index.html')

#función que redirige a una pagina, no la renderea
#def logout(request):
#    return redirect('index')

#log out & navbar auth links
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
	return render(request, 'clients/dashboard.html')