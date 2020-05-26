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
    exceptions = exclude_patch.objects.filter(patch_id__in=var)
                              #objects.select_related('patch', 'patch__client')
    
    #hello = exclude_patch.objects.filter(pk__in=[1,2,3])
                                 #.filter(patch_id__in=[1,3])
    
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
    #get_object_or_404 will only return one object, get_list_or_404 multiple objects. Levanta la excepción Http404 si no existe el objeto.
    #get_object_or_404 uses get(), get_list_or_404 uses filter()
    #__in se utiliza cuando quieres usar de referencia objetos con otros objetos.

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #FRONTEND SIMPLE QUERIES

        # exclude_patch_ID = 8
    exception = get_object_or_404(exclude_patch, pk=exclude_patch_ID)
        #Selecciona el objeto que contiene el {id 8 en exclude_patch model}:
            #<id=8, title=elID2, just=awef, patch_id=2>
    patch_exc = get_object_or_404(patch, pk=exception.patch_id)
        #Selecciona el objeto que contiene en el id, dentro del patch model, el {valor de patch_id en el objeto exception}:
            #<id=2, server=Linux, crit=Medium, client_id=3>

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #APPROVERS TABLE

    #patch_approver = patchApproverRelationship.objects.filter(patch=exception.patch_id)
        #Selecciona los objetos que contienen en el campo patch_id (patch) dentro del patchApproverRelationship model, el valor {patch_id en el objeto exception}:
            #<id=1, approver_id=4, patch_id=2>,
            #<id=4, approver_id=6, patch_id=2>,
            #<id=8, approver_id=5, patch_id=2>,
    #approver_detail = User.objects.filter(pk__in=patch_approver.values_list('approver_id'))
    
    approver_detail = User.objects.filter(pk__in=patchApproverRelationship.objects.filter(patch=exception.patch_id).values_list('approver_id'))
            #<id=4, username=approver, is_active=1 ...>,
            #<id=5, username=approver2, is_active=1 ...>
            #<id=6, username=approver3, is_active=1 ...>
    
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #TESTING

    #print("exclude_patch_ID = ", exclude_patch_ID, "\n")
    #print("excepcion = " , exception, "\n")
    #print("patch_exc = " , patch_exc, "\n")
    
    print("")

    approverResponsable = []
    
    for x in range(len(approver_detail)):
        approverResponsable.append(approver_detail[x])
        print("aprobadores responsables a esta excepcion: [",x,"] = " , approverResponsable[x])


    # existen autorizaciones ya realizadas en el modelo authorize_Exception
    authorize = authorize_Exception.objects.filter(exception_id=exception.id).filter(approver_id__in=approver_detail)

    print("")
    exceptionReply = []
    
    for x in range(len(authorize)):
        exceptionReply.append(authorize[x])
        print("excepcion ya respondida: [",x,"] = " , exceptionReply[x])
        #if exceptionReply[x]:
    
    
    # for x in range(len(approver_detail)):
    #     #if approverResponsable[x].objects.filter(pk__in=
    #     if approverResponsable[x].objects.filter(id=1):
    #         print("es 1")

    
    if authorize:
        print ("\nExisten campos en la tabla\n")
    else:
        print ("\nNO Existen campos en la tabla\n")

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #CONTEXT

    context = {
        'exception': exception,
        'patch_exc':patch_exc,
        'approver_detail':approver_detail,

        #es resultado es el mismo:
        'authorize':authorize,
        'exceptionReply':exceptionReply
    }

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #URLS

    path = patchApproverRelationship.objects.filter(approver_id=request.user.id).filter(patch_id=patch_exc.id).values_list('approver_id', flat=True)
        #var path = to user_authenticated_id
    
    if request.user.is_authenticated:
        #try:
        if request.user.profile.role == 2:
            #if request.user.id == path[0]:
            return render(request, 'approvers/approvalDetail.html', context)
        else:
        #except:    
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