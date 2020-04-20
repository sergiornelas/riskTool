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
from approvers.models import Profile
from exception.models import exclude_patch
from django.http import HttpResponse
#*

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                if request.user.profile.role == 3:
                    messages.error(request, 'You are not allowed to enter.')
                    return redirect('index')
                elif request.user.profile.role == 2:
                    messages.success(request, 'You are now logged in')
                    return redirect('approvalsList')
                elif request.user.profile.role == 1:
                    messages.success(request, 'You are now logged in')
                    return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('index')
    else:
        return render(request, 'pages/index.html')

#log out & navbar auth links
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    client_patches = patch.objects.filter(user=request.user.id)
    context = {
		'patches': client_patches
    }
    if request.user.is_authenticated:
        if request.user.profile.role == 1:
            return render(request, 'clients/dashboard.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')

def approvalsList(request):
    approvals = patch.objects.filter(user=request.user.id)
    context = {
        'patches': approvals
    }
    if request.user.is_authenticated:
        if request.user.profile.role == 2:
            return render(request, 'approvers/approvalsList.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')

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
    parche = get_object_or_404(patch, pk=patch_id)
    #exception = get_object_or_404(exclude_patch, pk=exclude_patch_id)
        #pk=listing_id se refiere al mismo listing_id segundo parámetro de la función.

    context = {
        'patch': parche, #en el url se remplaza approvalsList por el id del parche
        #'excepcion': exception
    } 
   
    # user = auth.authenticate(username=username, password=password)
    #     if user:
            # if user.is_active:
                # auth.login(request, user)
                # if user.is_superuser==1:
    if request.user.is_authenticated:
        return render(request, 'approvers/approvalDetail.html', context)
        # return redirect(request, 'approvers/approvalDetail.html', context)
    else:
        return redirect('login')

# NOTAS:
# las acciones de cada def le corresponde en su sitio actual, no aplica en todos
# dentro del context puede tener los mismos nombres (patches), porque cada diccionario
#    context tiene su propio scope, no interfiere con el de los demás.