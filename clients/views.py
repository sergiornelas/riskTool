from django.shortcuts import render
from django.http import HttpResponse

#message alerts
from django.contrib import messages

#messages
def login(request):
	if request.method == 'POST':
		return
	else:
		return render(request, 'pages/index.html')

#función que redirige a una pagina, no la renderea
def logout(request):
    return redirect('index')

#test
def test(request):
    return render(request, 'pages/test.html')