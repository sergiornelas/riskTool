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
from .models import authorize_Exception
from django.http import HttpResponse
from django import forms
from django.forms import ModelForm
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

    patches = patch.objects.all()

    context = {
        'exceptions': exceptions,
        'patches':patches
    }

    if request.user.is_authenticated:
        if request.user.profile.role == 2:
            return render(request, 'approvers/approvalsList.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
        
    else:
        return render(request, 'pages/index.html')








def approvalDetail(request, exclude_patch_ID):
    exception = get_object_or_404(exclude_patch, pk=exclude_patch_ID)
    patch_exc = get_object_or_404(patch, pk=exception.patch_id)
    patch_approver = patchApproverRelationship.objects.filter(patch=exception.patch_id)
    approver_detail = User.objects.filter(pk__in=patch_approver.values_list('approver_id'))
    
    #toma los valores de la tabla, por lo que tiene que tener campos.
    #los campos no salen en orden
    authExc = authorize_Exception.objects.filter(approver_id__in=patch_approver.values_list('approver_id')) #patch_approver es el mero mero
    print("authExc", authExc)

    print("excepcion id" , exclude_patch_ID)
    #print("excepcion" , exception)
    #print("patch_exc" , patch_exc)
    #print("patch_approver" , patch_approver)
    #print("approver_detail" , approver_detail)
    #print("authExc", authExc)

    flag = True
    #if authorize_Exception.objects.exists(): #model has content
    if authExc.exists():
        authObjects = zip(patch_approver, approver_detail, authExc)
        
    else: #model is empty
        authObjects = zip(patch_approver, approver_detail)
        flag = False

    context = {
        'exception': exception,
        'patch_exc':patch_exc,
        'authObjects':authObjects,
        'flag':flag
    }

    path = patchApproverRelationship.objects.filter(approver_id=request.user.id).filter(patch_id=patch_exc.id).values_list('approver_id', flat=True)
    #path = to user_authenticated_id

    if request.user.is_authenticated:
        try:
            if request.user.id == path[0]:
                return render(request, 'approvers/approvalDetail.html', context)
        except:    
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return redirect('login')







def authorize(request):
    if request.method == 'POST':
        exception_id = request.POST['exception_id']
        approver = request.user
        state = request.POST['state']
        comment = request.POST['comment']
        
    validate = authorize_Exception(exception_id=exception_id, approver=approver, state=state, comment=comment)
    validate.save()
    return redirect('approvalsList')