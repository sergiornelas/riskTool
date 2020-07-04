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
from exception.models import VALIDATE_EXCEPTION
from urllib import parse
from django.contrib.auth.models import User

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
    validations=VALIDATE_EXCEPTION.objects.all()

    context ={
        'client_exceptions':client_exceptions,
        'validations':validations
    }
    return render(request, 'clients/exceptionsBoard.html', context)

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
        #print(selectedServer)
        selectedServer = selectedServer.replace(",", " ")
        selectedServer = selectedServer.split()

        #print(type(x))

        """
        #object mode
            selectedServer = request.POST.getlist['selectedServer'] #'method' object is not subscriptable
            yourdict = json.loads(request.POST.get('selectedServer')) #the JSON object must be str, bytes or bytearray, not NoneType
            print(yourdict)

            arr = request.POST.get('selectedServer')
            dict_ = json.loads(arr)
        """
        
        #los servidores que posee el cliente logeado.
        client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)

        #almacenamos en una lista los id de los servidores del cliente loggeado.        
        servers_ids=[]
        for server in client_has_server:
            servers_ids.append(server.server_id)

        #toma los objetos de los servidores que contengan los id de los servidores del
        #usuario loggeado y el hostname seleccionado en el dropdown list.
        takeServers=SERVER.objects.filter(pk__in=servers_ids).filter(hostname__in=selectedServer)
        
        servers_selected_ids=[]

        #almacenamos los ids de los servidores que contengan takeServers
        for server in takeServers:
            servers_selected_ids.append(server.pk)

        #hacemos comunicación entre un advisory y un server a través del parche.
        #por eso para conocer los advisories necesitamos los objetos patches.
        
        patch_advisory = PATCHES.objects.filter(server_id__in=servers_selected_ids)

        #return HttpResponse(serializers.serialize("json", patch_advisory))

        #----------------------------------------------------------------

        #sample_instance = SERVER.objects.get(id=2)
            #sample_instance = SERVER.objects.filter(pk=request.user.id)
        #value_of_name = sample_instance.hostname
            #print(value_of_name)
        
        #list=["manzana", "banana", "pera"]

        thisdict = {
            "brand": "Ford",
            "model": "Mustang",
            "year": 1964
        }
        
        

        #result = json.dumps(thisdict)
        
        print(patch_advisory)

        print(type(patch_advisory)) #'django.db.models.query.QuerySet'
        print(type(serializers.serialize("json", patch_advisory))) #'str'


        # takeAdvisoriesid = [o.advisory_id for o in patch_advisory]
        # print("takeadvisories: ",takeAdvisoriesid)

        # takeduedate = [o.due_date for o in patch_advisory]
        # print("takeadvisories: ",takeduedate)

        # thisdict = {
        #     "takeAdvisoriesid": takeAdvisoriesid,
        #     "takeduedate": takeduedate,
        # }

        #print("thisdict: ", thisdict)
                
        return HttpResponse(serializers.serialize("json", patch_advisory))
        #return HttpResponse(patch_advisory)
        
        
        
        
        
        
        
        
        
        #----------------------------------------------------------------

        #tomamos los id de los advisories de los parches que estan involucrados
        #con el servidor seleccionado.
        takeAdvisories = [o.advisory_id for o in patch_advisory]
        print("takeadvisories: ",takeAdvisories)

        #utilizamos los id de los advisories para obtener los objetos completos
        #getAdvisoriesObjects = ADVISORY.objects.filter(pk__in=takeAdvisories)
        #print(type(getAdvisoriesObjects))

        #get() returns a single object. 
                
        getAdvisoriesObjects = ADVISORY.objects.filter(pk__in=takeAdvisories)
        #print("getAdvisoriesObjects: ",getAdvisoriesObjects)

        """
        #UNION: When they querysets are from different models, the FIELDS and their datatypes should MATCH.
        #Junta dos query sets, evitando las repeticiones (+<User: rishab>)
            total = ADVISORY.objects.filter(pk__in=takeAdvisories).union(ADVISORY.objects.filter(pk__in=[1, 2]), all=True)
            print("total: ",total)
        """
        
        """
        #obtenemos solo la descripción de esos objetos, REGRESA UN SOLO STRING
            takeAdvisoriesDescription = [o.description for o in getAdvisoriesObjects]
            print(takeAdvisoriesDescription)
        """

        #return HttpResponse(serializers.serialize("json", getAdvisoriesObjects))
        #return HttpResponse(data, content_type="application/json")
        #return HttpResponse(json.dumps(context))
        #return JsonResponse(json.loads(takeAdvisoriesDescription))
        #return HttpResponse(takeAdvisoriesDescription)

@csrf_exempt
def getDaysLimit(request):
    if request.method == 'POST':
        limitDay = request.POST['limitDay']
        #print(limitDay)

        #print(selectedServer)
        limitDay = limitDay.replace(",", " ")
        limitDay = limitDay.split()
        
        #los servidores que posee el cliente logeado.
        client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)

        #almacenamos en una lista los id de los servidores del cliente loggeado.        
        servers_ids=[]
        for server in client_has_server:
            servers_ids.append(server.server_id)

        #toma los objetos de los servidores que contengan los id de los servidores del
        #usuario loggeado y el hostname seleccionado en el dropdown list.
        takeServers=SERVER.objects.filter(pk__in=servers_ids).filter(hostname__in=limitDay)
        
        servers_selected_ids=[]

        #almacenamos los ids de los servidores que contengan takeServers
        for server in takeServers:
            servers_selected_ids.append(server.pk)

        #hacemos comunicación entre un advisory y un server a través del parche.
        #por eso para conocer los advisories necesitamos los objetos patches.
        patch_advisory = PATCHES.objects.filter(server_id__in=servers_selected_ids)

        #print(patch_advisory)

        takeAdvisories = [o.advisory_id for o in patch_advisory]
        #print("takeadvisories: ",takeAdvisories)

        getAdvisoriesObjects = ADVISORY.objects.filter(pk__in=takeAdvisories)
        getCriticality = [o.criticality for o in getAdvisoriesObjects]

        print("Criticalities: ",getCriticality)

        #names = ['Alice','Bob','Cassie','Diane','Ellen']
        #for name in names:
        #    if name[0] in "AEIOU":
        #        print(name + " starts with a vowel")
		
        days=0

        for critical in getCriticality:
            if critical == "High":
                #print(critical," es alto")
                days = 30
                break
            elif critical == "Medium":
                #print(critical," es medio")
                days = 90
                break
            elif critical == "Low":
                #print(critical," es bajo")
                days = 180

        print(days)
        
        return HttpResponse(days)



#POST REQUEST CREAR EXCEPCIÓN
def exclude_server(request):
    if request.method == 'POST':
        patch_id = request.POST['patch_id']
        action_plan = request.POST['action_plan']
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
               
        exclude_this_server = EXCEPTION(patch_id=patch_id, action_plan=action_plan, client=client, title=title, justification=justification, exclude_date=exclude_date, content=content, exception_type=exception_type)
        #exclude_this_server = EXCEPTION(client=client, title=title, justification=justification, exclude_date=exclude_date, content=content, exception_type=exception_type)
        
        
        for x in exclude_this_server:
            x.save()
        
        #exclude_this_server.save()
        

        

        messages.success(request, "Your request has been submitted, an approver will get back to you soon")

        return redirect('exceptionsBoard')


@csrf_exempt
def transform(request): # << 1:1, 1:3, 2:3
    if request.method == 'POST':

        serverPatch = request.POST['serverPatch']

        serverPatch = serverPatch.replace(" ", "")
        serverPatch = serverPatch.replace(":", "")
        serverPatch = serverPatch.replace(",", "")

        #print(serverPatch)

        array=[]

        arrayAdvisories=[]
        arrayServers=[]

        for x in serverPatch:
            #print(x)
            array.append(x)

        arrayServers = array[::2]
        arrayAdvisories = array[1::2]
        
        #print(arrayServers)
        #print(arrayAdvisories)

        patches = PATCHES.objects.filter(server_id__in=arrayServers).filter(advisory_id__in=arrayAdvisories)
        
        #1: 2,1: 1,2: 4,1: 4:

            #serverArrays:    patchArrays:
            #[1, 1, 1]   ->  [2, 1, 4]
            #[2]         ->  [4]       

        #context = {
            #'patches':patches,
            #'servers':servers,
        #} 

        return HttpResponse(serializers.serialize("json", patches))

@csrf_exempt
def getValidationDetails(request):
    #validations=VALIDATE_EXCEPTION.objects.all()
    
    if request.method == "POST":

        query = request.POST.get('query')
        #print(query)
        
        validations=VALIDATE_EXCEPTION.objects.filter(exception_id=query)
        #print(validations)
        return HttpResponse(serializers.serialize("json", validations))
        #return HttpResponse(query)

@csrf_exempt
def getApprovalNames(request):
    if request.method == "POST":
        data = request.POST.get("data")
        #print(data)

        approverNames = User.objects.filter(pk__in=data)
        #print(approverNames)

        return HttpResponse(serializers.serialize("json", approverNames))





@csrf_exempt
def getHostnames(request):
    if request.method == "POST":
        serverID = request.POST.get("serverID")
        #print(serverID)

        serverhostnames = SERVER.objects.filter(pk__in=serverID)
        #print("--------------------------------------------")
        return HttpResponse(serializers.serialize("json", serverhostnames))

@csrf_exempt
def getAdvisoriesDesc(request):
    if request.method == "POST":
        advisoryDescription = request.POST.get("advisoryDescription")
        #print(serverID)

        #advDesc = SERVER.objects.filter(pk__in=serverID)
        advDesc = ADVISORY.objects.filter(pk__in=advisoryDescription)

        #print("--------------------------------------------")
        return HttpResponse(serializers.serialize("json", advDesc))
