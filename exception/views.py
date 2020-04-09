from django.shortcuts import render, redirect
from django.contrib import messages

#from django.core.mail import send_mail

from .models import exclude_patch
from patches.models import patch

from django.contrib.auth.models import User

def exclude(request):
    
    if request.method == 'POST':
        # patch_id = request.POST['patch_id']
        patchFrom = request.user
        
        #patch = request.POST['patch'] #patch name?
    
        title = request.POST['title']
        justification = request.POST['justification']
        excludeDate = request.POST['excludeDate']

        #user_id = request.POST['user_id']
        
        #Check if user has made exclusion already
        # if request.user.is_authenticated:
        # ...
        #     has_contacted = exclude_patch.objects.all().filter(patch_id=patch_id)
        #     if has_contacted:
        #         messages.error(request, 'You have already made an inquiry for this listing')
                # return redirect('/approvallist')               
        
       
        exclude = exclude_patch(patchFrom=patchFrom, title=title, justification=justification, excludeDate=excludeDate)
        # exclude = exclude_patch(title=title, justification=justification, excludeDate=excludeDate)

        #funcion de base de datos
        exclude.save()

        #PENDIENTE SI AGREGARLO O NO (7 DE ABRIL)
        
        client_patches = patch.objects.filter(user=request.user.id)
        context = {
            'patches': client_patches
        }

        messages.success(request, "Your request has been submitted, an approver will get back to you soon")

        return render(request, 'clients/dashboard.html', context)

        #The render function Combines a given template with a given context
        #dictionary and returns an HttpResponse object with that rendered text.