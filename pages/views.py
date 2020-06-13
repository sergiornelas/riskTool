from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from patches.models import PATCHES
from servers.models import SERVER
from django.core import serializers
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def ajax(request):
    return render(request, 'ajax.html')

def test(request):
    return render(request, 'test.txt')

def javascript(request):
    return render(request, 'testClock.html')



def firstOBJECTS(request):
    if request.method == "GET":
        #return HttpResponse(PATCHES.objects.all())
        return HttpResponse(serializers.serialize("json", PATCHES.objects.all()))
        #return HttpResponse(serializers.serialize("json", SERVER.objects.all()))





# def post(request):
#     somevalue = "whatever"
#     if request.method == "POST":
#         title = request.POST['title']
#         justification = request.POST['justification']
        
#         array = {
#             "title" :title,
#             "justification":justification,
#             "response":somevalue
#         }

#         #return HttpResponse(serializers.serialize("json", array))
#         return render(request, 'ajax.html')

#     else:
#         title = "No title given"
#         justification = "No justification given"

#         array = {
#             "title" :title,
#             "justification":justification,
#             "response":somevalue
#         }

#         #return HttpResponse(serializers.serialize("json", array))
#         print("errrorr")
#         return render(request, 'ajax.html')