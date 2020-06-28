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
from urllib import parse

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

    """
    context={
        'serversPoll':serversPoll
    }
    """

    if request.method == "GET":
        return HttpResponse(serializers.serialize("json", serversPoll))
    #return render(request, 'clients/selectServers.html', context)



#TESTING
@csrf_exempt
def filterPatches(request):
    if request.method == 'POST':
        #toma el servidor seleccionado

        #string mode
        selectedServer = request.POST['selectedServer'] #wdcdmzyz22033245,wdcgz22050068

        #object mode
        #selectedServer = request.POST.getlist['selectedServer'] #'method' object is not subscriptable
        #yourdict = json.loads(request.POST.get('selectedServer')) #the JSON object must be str, bytes or bytearray, not NoneType
        #print(yourdict)

        #arr = request.POST.get('selectedServer')
        #dict_ = json.loads(arr)

        #selectedServer = request.POST['selectedServer'] #wdcdmzyz22033245,wdcgz22050068
        #value = parse.parse_qs(self.request.POST.get('selectedServer'))
        
        
        #agrega aqui:
        #---------------------------------------------------------------------------
        #los servidores que posee el cliente logeado.
        client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
        
        servers_ids=[]
        for server in client_has_server:
            servers_ids.append(server.server_id)

        #---------------------------------------------------------------------------


        #---------------------------------------------------------------------------
        #TESTING
        list=["wdcdmzyz22033245","wdcgz22050068"]
        print("testing:")
        print(list) #['wdcdmzyz22033245', 'wdcgz22050068']
        print(list[0]) #wdcdmzyz22033245
        #---------------------------------------------------------------------------


        #toma los objetos de los servidores que contengan los id de los servidores del
        #usuario loggeado y el hostname seleccionado en el dropdown list.
        takeServers=SERVER.objects.filter(pk__in=servers_ids).filter(hostname=selectedServer)

        servers_selected_ids=[]

        #almacenamos los ids de los servidores que contengan takeServers
        for server in takeServers:
            servers_selected_ids.append(server.pk)

        #hacemos comunicación entre un advisory y un server a través del parche.
        #por eso para conocer los advisories necesitamos los objetos patches.
        patch_advisory = PATCHES.objects.filter(server_id__in=servers_selected_ids)

        #tomamos los id de los advisories de los parches que estan involucrados
        #con el servidor seleccionado.
        takeAdvisories = [o.advisory_id for o in patch_advisory]

        #utilizamos los id de los advisories para obtener los objetos completos
        getAdvisoriesObjects = ADVISORY.objects.filter(pk__in=takeAdvisories)
        #print(type(getAdvisoriesObjects))

        #LISTA <NO SE USA>
        #obtenemos solo la descripción de esos objetos, REGRESA UN SOLO STRING
        takeAdvisoriesDescription = [o.description for o in getAdvisoriesObjects]
        #print(takeAdvisoriesDescription)

        context = {
            #'takeServers':takeServers
            #'advisories':advisories,
            'takeAdvisoriesDescription':takeAdvisoriesDescription,
        }

        return HttpResponse(serializers.serialize("json", getAdvisoriesObjects))
        
        #return HttpResponse(data, content_type="application/json")
        #return HttpResponse(json.dumps(context))
        #return JsonResponse(json.loads(takeAdvisoriesDescription))
        #return HttpResponse(takeAdvisoriesDescription)


def serverOrPatch(request):
    return render(request, 'clients/serverOrPatch.html')

def selectServers(request):
    return render(request, 'clients/selectServers.html')

def selectServerPatch(request):
    return render(request, 'clients/selectServerPatch.html')

def selectPatches(request):
    return render(request, 'clients/selectPatches.html')

def inquiryPatches(request):
    return render(request, 'clients/inquiryPatches.html')

def inquiryServers(request):
    return render(request, 'clients/inquiryServers.html')

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