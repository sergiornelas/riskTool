from django.shortcuts import render, redirect
from django.contrib import messages
from patches.models import PATCHES
from servers.models import SERVER_USER_RELATION, SERVER
from exception.models import EXCEPTION, EXCEPTION_TYPE
from advisory.models import ADVISORY
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

#DASHBOARD
def dashboard(request):
    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    #los servidores que posee el cliente logeado.

    servers_ids=[]
    for server in client_has_server:
        servers_ids.append(server.server_id)

    patches = PATCHES.objects.filter(server_id__in=servers_ids) #faltaría filtrar aqui con el status_id=2


    serversPoll = SERVER.objects.filter(pk__in=client_has_server)

    #cuando quieras utilizar ahora si la tabla exception_type
    #exception_type_patch = EXCEPTION_TYPE.objects.get(pk=1)
    
    context = {
		'client_has_server':client_has_server,
        'patches':patches,
        'serversPoll':serversPoll,
        #'exception_type_patch':exception_type_patch,
        #'exception_type_server':exception_type_server
    } 

    if request.user.is_authenticated:
        if request.user.profile.role == 1:
            return render(request, 'clients/dashboard.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return render(request, 'pages/index.html')

    #if request.method == "GET":
        #return HttpResponse(serializers.serialize("json", patches))

def exceptionsBoard(request):
    client_exceptions = EXCEPTION.objects.filter(client_id=request.user.id)
    context ={
        'client_exceptions':client_exceptions
    }
    return render(request, 'clients/exceptionsBoard.html', context)


#AJAX LISTA DE SERVIDORES DEL CLIENTE INGRESADO
def server_user_list(request):
    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    serversPoll = SERVER.objects.filter(pk__in=client_has_server)

    if request.method == "GET":
        return HttpResponse(serializers.serialize("json", serversPoll))


#AJAX LISTA DE PARCHES DEL CLIENTE INGRESADO
def patch_user_list(request):
    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    servers_ids=[]
    for server in client_has_server:
        servers_ids.append(server.server_id)
    patches = PATCHES.objects.filter(server_id__in=servers_ids) #faltaría filtrar aqui con el status_id=2
    
    if request.method == "GET":
        return HttpResponse(serializers.serialize("json", patches))




#POST REQUEST CREAR EXCEPCIÓN
def exclude_server(request):
    if request.method == 'POST':
        #patch_id = request.POST['patch_id']
        client = request.user
        title = request.POST['title']
        justification = request.POST['justification']
        exclude_date = request.POST['exclude_date']
        content = request.POST['content']
        exception_type = request.POST['exception_type']

        #Check if user has made inquiry already
        # if request.user.is_authenticated:
        #     has_contacted = exclude_patch.objects.all().filter(patch_id=patch_id, client=client)
        #     if has_contacted:
        #         messages.error(request, 'You have already made an exception for this patch')
        #         return redirect('dashboard')
               
        exclude_this_server = EXCEPTION(client=client, title=title, justification=justification, exclude_date=exclude_date, content=content, exception_type=exception_type)
        exclude_this_server.save()

        messages.success(request, "Your request has been submitted, an approver will get back to you soon")

        return redirect('exceptionsBoard')

#TESTING
@csrf_exempt
def testing(request):
    if request.method == 'POST':
        print("SE LLAMÓ AL SERVER");

        
        xtest = request.POST['xtest']

        takeServers = SERVER.objects.filter(hostname=xtest)

        #print(takeServers)

        servers_ids=[]
        for server in takeServers:
            servers_ids.append(server.pk)

        advisories = PATCHES.objects.filter(server_id__in=servers_ids) #faltaría filtrar aqui con el status_id=2

        #tomamos los id de los advisories
        takeAdvisories = [o.advisory_id for o in advisories]

        #utilizamos los id de los advisories para obtener los objetos completos
        getAdvisoriesObjects = ADVISORY.objects.filter(pk__in=takeAdvisories)
        print(type(getAdvisoriesObjects))

        #LISTA
        #obtenemos solo la descripción de esos objetos, REGRESA UN SOLO STRING
        takeAdvisoriesDescription = [o.description for o in getAdvisoriesObjects]

        #print(type(takeAdvisoriesDescription))
        print(takeAdvisoriesDescription)

    
        context = {
		    #'xtest':xtest,
            #'takeServers':takeServers
            #'advisories':advisories,
            'takeAdvisoriesDescription':takeAdvisoriesDescription,
        }

        
        #data = serializers.serialize('json', context)
        #return HttpResponse(data, content_type="application/json")


        #return HttpResponse(json.dumps(context))
        return HttpResponse(serializers.serialize("json", getAdvisoriesObjects))

        #return JsonResponse(json.loads(takeAdvisoriesDescription))

        #this works:
        #return HttpResponse(takeAdvisoriesDescription)