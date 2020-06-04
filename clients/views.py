from django.shortcuts import render, redirect
from django.contrib import messages
from patches.models import PATCHES
from servers.models import SERVER_USER_RELATION

def dashboard(request):
    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    #los servidores que posee el cliente logeado.

    servers_ids=[]
    for server in client_has_server:
        servers_ids.append(server.server_id)

    patches = PATCHES.objects.filter(server_id__in=servers_ids) #faltaría filtrar aqui con el status_id=2
    
    context = {
		'client_has_server':client_has_server,
        'patches':patches
    }

    if request.user.is_authenticated:
        if request.user.profile.role == 1:
            return render(request, 'clients/dashboard.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return render(request, 'pages/index.html')










# def dashboard(request):
#     client_patches = patch.objects.filter(client=request.user.id)

#     context = {
# 		'patches': client_patches
#     }

#     if request.user.is_authenticated:
#         if request.user.profile.role == 1:
#             return render(request, 'clients/dashboard.html', context)
#         else:
#             messages.error(request, 'Not allowed to enter here')
#             return redirect('index')
#     else:
#         return render(request, 'pages/index.html')