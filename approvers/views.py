from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'approvers/approvalsList.html')

def details(request):
	return render(request, 'approvers/approvalDetail.html')

def tracking(request):
	return render(request, 'approvers/approvalTracking.html')