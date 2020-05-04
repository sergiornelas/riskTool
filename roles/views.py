from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages

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

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')