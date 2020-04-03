from django.shortcuts import render, redirect
from django.contrib import messages
#from exceptions.models import exclude_patch
#from django.core.mail import send_mail
#from django.conf import settings

from .models import exclude_patch
from patches.models import patch

def exclude(request):
    if request.method == 'POST':
        #listing_id = request.POST['listing_id']
        #listing = request.POST['listing']
        title = request.POST['title']
        justification = request.POST['justification']
        excludeDate = request.POST['excludeDate']
        #user_id = request.POST['user_id']

        exclude = exclude_patch(title=title, justification=justification, excludeDate=excludeDate)

        exclude.save()
        messages.success(request, "Your request has been submitted, a realtor will get back to you soon")
        #return redirect('/listings/'+listing_id)

        client_patches = patch.objects.filter(user=request.user.id)
        context = {
            'patches': client_patches
        }

        return render(request, 'clients/dashboard.html', context)

#def exclude(request):
#	return render(request, 'patches/excludePatch.html')