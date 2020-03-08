from django.shortcuts import render, redirect

#message alerts
from django.contrib import messages

#user registration, model 
from django.contrib.auth.models import User

#user registration, login after register
from django.contrib import auth

#messages
# def login(request):
# 	if request.method == 'POST':
# 		# Login User
# 		return
# 	else:
# 		return render(request, 'pages/index.html')

#user login
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
			return redirect('index')
		else:
			messages.error(request, 'Invalid credentials')
			print ("no se conecto compa")
			#return redirect('login')
			return redirect('index')
	else:
		#return render(request, 'accounts/login.html')
		return render(request, 'pages/index.html')

#función que redirige a una pagina, no la renderea
def logout(request):
    return redirect('index')

#test
def test(request):
    return render(request, 'pages/test.html')