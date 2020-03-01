from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'approvers/approvalsList.html')

def tracking(request):
	return render(request, 'approvers/approvalTracking.html')

def details(request):
	return render(request, 'approvers/approvalDetail.html')

#función que redirige a una pagina, no la renderea
def logout(request):
    return redirect('index')

#def details(request, approvalDetail_id):
    #return render(request, 'approvers/approvalDetail.html')

	#Esto se pone en approvalsList.htlm
	#<!-- <td><a href="{% url 'listing' listing.id %}" class="btn btn-primary btn-block">View details</a></td> -->