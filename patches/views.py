from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
    
#from patches.models import patch
from .models import patch

def list(request):
    queryset = patch.objects.all()
    queryset = serializers.serialize('json', queryset)

    # context = {
    #     'queryset' : queryset
    # }

    return HttpResponse(queryset, content_type="application/json")