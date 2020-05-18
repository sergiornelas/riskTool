from django.shortcuts import render, redirect

from django.shortcuts import get_object_or_404

#message alerts
from django.contrib import messages

#user registration, model 
from django.contrib.auth.models import User

#user registration, login after register
from django.contrib import auth

#*
from patches.models import patch
from roles.models import Profile
from exception.models import exclude_patch
from .models import patchApproverRelationship
from django.http import HttpResponse
#*

def approvalsList(request): 
    var = patchApproverRelationship.objects.filter(approver=request.user.id).values_list('patch_id')
                                                                           #.values_list('patch_id', flat=True)
    #var = patchApproverRelationship.objects.filter(patch_id=3)

    #print (var)

    #exceptions = exclude_patch.objects.filter(patch_id=request.user.id)
    #exceptions = exclude_patch.objects.filter(patch_id=1)

    exceptions = exclude_patch.objects.filter(patch_id__in=var)
                              #objects.select_related('patch', 'patch__client')
    
    #hello = exclude_patch.objects.filter(patch_id__in=patchApproverRelationship.objects.all())
    #hello = exclude_patch.objects.filter(pk__in=[1,2,3])
                                     #.filter(patch_id__in=[1,3])
    #It means, give me all objects of model Model that either have {var} as their primary key.

    context = {
        'exceptions': exceptions,
    }

    if request.user.is_authenticated:
        #if request.user.profile.role == 2:
        return render(request, 'approvers/approvalsList.html', context)
        #else:
        #    messages.error(request, 'Not allowed to enter here')
        #    return redirect('index')
        
    else:
        return render(request, 'pages/index.html')







# def approvalDetail(request):
#     approvals = patch.objects.filter(user=request.user.id)
#     exception = exclude_patch.objects.filter(patch=request.user.id)
#     context = {
#         'patches': approvals,
#         'exceptions' : exception
#     }
#     return render(request, 'approvers/approvalDetail.html', context)
#     #aveztrus -> patches

def approvalDetail(request, patch_id):
    #parche = get_object_or_404(patch, pk=patch_id)
    exception = get_object_or_404(exclude_patch, pk=exclude_patch_id)
        #pk=listing_id se refiere al mismo listing_id segundo parámetro de la función.

    context = {
        #'patch': parche, #en el url se remplaza approvalsList por el id del parche
        'excepcion': exception
    } 

    # user = auth.authenticate(username=username, password=password)
    #     if user:
            # if user.is_active:
                # auth.login(request, user)
                # if user.is_superuser==1:

    if request.user.is_authenticated:
        if request.user.profile.role == 2:
            return render(request, 'approvers/approvalDetail.html', context)
            # return redirect(request, 'approvers/approvalDetail.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    #else:
        #return render(request, 'pages/index.html')
    else:
        return redirect('login')

# NOTAS:
# las acciones de cada def le corresponde en su sitio actual, no aplica en todos

def sergio(request):
    return render(request, 'approvers/approvalDetail.html')