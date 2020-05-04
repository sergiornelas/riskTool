from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import patch

def list(request):
    queryset = patch.objects.all()
    queryset = serializers.serialize('json', queryset)

    return HttpResponse(queryset, content_type="application/json")