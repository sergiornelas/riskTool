from django.shortcuts import render, redirect
from django.contrib import messages
from patches.models import patch

def dashboard(request):
    client_patches = patch.objects.filter(client=request.user.id)

    context = {
		'patches': client_patches
    }

    if request.user.is_authenticated:
        if request.user.profile.role == 1:
            return render(request, 'clients/dashboard.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return render(request, 'pages/index.html')