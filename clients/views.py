from django.shortcuts import render
from django.http import HttpResponse

#función que redirige a una pagina, no la renderea
def logout(request):
    return redirect('index')