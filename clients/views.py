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
import re
import random
import string
from roles.models import Profile
from django.shortcuts import get_object_or_404
from exception.choices import state_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import operator
from django.db.models import Q
from functools import reduce

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ DASHBOARD ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

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

def serverOrPatch(request):
    #client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id).values_list('server_id', flat=True) #<QuerySet [1, 2]>

    #quitarServidorSeleccionado=EXCEPTION.objects.filter(client_id=request.user.id).filter(state="Pending").filter(status_id=1).filter(server_id__in=client_has_server)

    #print(quitarServidorSeleccionado)

    #1) Seleccionar excepciones del usuario loggeado.
    #2)
    return render(request, 'clients/serverOrPatch.html')

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ EXCEPTION BOARD ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def exceptionsBoard(request):
    
    #client_exceptions = EXCEPTION.objects.filter(client_id=request.user.id)
    
    client_exceptions = EXCEPTION.objects.filter(client_id=request.user.id).exclude(state="Canceled")

    # print("AMOR")
    # print(client_exceptions)
    #print("CLIENT_EXCEPCIONS",client_exceptions)

    excepciones= EXCEPTION.objects.filter(client_id=request.user.id).values_list('pk', flat=True)
    #print("EXCEPCIONES",excepciones)
    validaciones=VALIDATE_EXCEPTION.objects.filter(exception_id__in=excepciones).values_list('exception_id', flat=True)
    #validaciones=VALIDATE_EXCEPTION.objects.filter(exception_id__in=excepciones).values_list('exception_id', flat=True)
    #print("VALIDACIONES", validaciones)

    arreglo=[]
    
    for x in excepciones:
        for y in validaciones:
            if x == y:
                arreglo.append(x)
                break
                
    remaining = EXCEPTION.objects.filter(client_id=request.user.id).exclude(pk__in=arreglo)
    #print("REMAINING",remaining)

    paginator = Paginator(client_exceptions, 8)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    # print("paged_listings")
    # print(paged_listings)

    #--------#--------#-------intento de poner el contenido de la excepcion con enters.
    # ------------- a lo mejor se resuelve con AJAX

    zarreglo = []

    for i in paged_listings:
        zarreglo.append(i.pk)
        #arreglo.append(x)
        print("hola")

    print("zarreglo")
    print(zarreglo)

    # zarreglo =  ', '.join(zarreglo)
    # zarreglo = zarreglo.split(",")

    print("zarreglo")
    print(zarreglo)
    print(type(zarreglo))

    #zarreglo = list(map(str, zarreglo))

    # print("zarreglo0")
    # print(zarreglo[0])
    # print("zarreglo1")
    # print(zarreglo[1])
    # print("zarreglo2")
    # print(zarreglo[2])
    # print("zarreglo3")
    # print(zarreglo[3])

    validaciones=EXCEPTION.objects.all().values_list('content', flat=True)
    print("validaciones")
    print(validaciones)

    #listPatches = [o.content for o in client_exceptions]

    context ={
        #'client_exceptions':client_exceptions,
        'client_exceptions':paged_listings,
        'remaining':remaining,

        'state_choices':state_choices,

        #'data': [1, 2, 3, 4, 5],
        #'datazz': validaciones,
        'datazz': zarreglo,
    }

    return render(request, 'clients/exceptionsBoard.html', context)

def searchClient(request):
    client_exceptions = EXCEPTION.objects.filter(client_id=request.user.id)
    excepciones= EXCEPTION.objects.filter(client_id=request.user.id).values_list('pk', flat=True)
    validaciones=VALIDATE_EXCEPTION.objects.filter(exception_id__in=excepciones).values_list('exception_id', flat=True)
    arreglo=[]
    for x in excepciones:
        for y in validaciones:
            if x == y:
                arreglo.append(x)
                break
    remaining = EXCEPTION.objects.filter(client_id=request.user.id).exclude(pk__in=arreglo)

    #queryset_list=EXCEPTION.objects.filter(pk__in=arreglin)

    if 'keywords' in request.GET:
        keywords = request.GET['keywords'] #"KEYWORDS" ES EL NAME EN HTML
        if keywords:
            #queryset_list = queryset_list.filter(risk_id__icontains=keywords) #contiene
            #SI ES POSIBLE FILTRAR NUEVAMENTE UN QUERYSET!!!
            client_exceptions = client_exceptions.filter(risk_id__iexact=keywords)
            #remaining = remaining.filter(risk_id__iexact=keywords)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            client_exceptions = client_exceptions.filter(state__iexact=state)
            #remaining = remaining.filter(state__iexact=state)

    context ={
        'state_choices':state_choices,
        'client_exceptions':client_exceptions,
        'remaining':remaining,
        'values': request.GET
    }

    return render(request, 'clients/searchClient.html', context)

#pendiente
@csrf_exempt
def contentSeparated(request):
    if request.method == 'POST':
        query = request.POST['query']
        print("QUERYYY")
        print(query)

        query = EXCEPTION.objects.filter(pk=query)
        
        print("QUERYYY2")
        print(query)

        return HttpResponse(serializers.serialize("json", query))

def deleteException(request, deleteRow):
    #if request.method == 'POST':
        print (deleteRow)
        getException = EXCEPTION.objects.get(pk=deleteRow)
        getException.state = 'Canceled'
        getException.save()

        return redirect('dashboard')

@csrf_exempt
def getValidationDetails(request):    
    if request.method == "POST":
        query = request.POST.get('query')
        validations=VALIDATE_EXCEPTION.objects.filter(exception=query)
        return HttpResponse(serializers.serialize("json", validations))

@csrf_exempt
def getApprovalNames(request):
    if request.method == "POST":
        data = request.POST.get("data")
        approverNames = User.objects.filter(pk__in=data)
        return HttpResponse(serializers.serialize("json", approverNames))
    
@csrf_exempt
def getValidationsRemaining(request):    
    if request.method == "POST":
        #id de la excepcion seleccionada:
        query = request.POST.get('query')
        
        justException = get_object_or_404(EXCEPTION, pk=query)

        exceptionQuery = EXCEPTION.objects.filter(pk=query)

        takeExceptionServerID= [o.server_id for o in exceptionQuery]
        takeExceptionServerID=', '.join(takeExceptionServerID)
        takeExceptionServerID = takeExceptionServerID.split(",")
        takeExceptionServerID = list(map(int, takeExceptionServerID))

        usersApprover = Profile.objects.filter(role=2).values_list("user_id")

        getServerID = SERVER.objects.filter(pk__in=takeExceptionServerID).values_list("id")

        serverApprover = SERVER_USER_RELATION.objects.filter(user_id__in=usersApprover).filter(server_id__in=getServerID).values_list('user_id')

        approver_detail = User.objects.filter(pk__in=serverApprover)

        authorize = VALIDATE_EXCEPTION.objects.filter(exception=justException.id).filter(approver_id__in =approver_detail)
        print(authorize)
    
        approver_detail_pending = approver_detail.exclude(pk__in=authorize.values_list('approver_id'))

        print("estos:")
        print(approver_detail_pending)

        return HttpResponse(serializers.serialize("json", approver_detail_pending))

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ EDIT EXCEPTION ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def inquiryEdit(request, exclude_patch_ID):
    getException = EXCEPTION.objects.get(pk=exclude_patch_ID)

    getContent = EXCEPTION.objects.filter(pk=exclude_patch_ID)
    getContent = [o.content for o in getContent]
    getContent =  ', '.join(getContent)
    getContent = getContent.split(",")
    #getContent = list(map(int, getContent))
    getContent = list(map(str, getContent))
    
    print("getContent")
    print(getContent)
    
    """
        patch_id: "10,11,12,13" (simple string) -> [10, 11, 12, 13] (list of integers)
    """

    getPatches = EXCEPTION.objects.filter(pk=exclude_patch_ID)
    getPatches = [o.patch_id for o in getPatches]
    getPatches =  ', '.join(getPatches)
    getPatches = getPatches.split(",")
    #getPatches = list(map(int, getPatches))
    getPatches = list(map(str, getPatches))
    
    getPatches = PATCHES.objects.filter(pk__in=getPatches).values_list('advisory_id', flat=True)
    getPatches = ADVISORY.objects.filter(pk__in=getPatches).values_list('criticality', flat=True)
    
    days=0

    for critical in getPatches:
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

    #print(days)
    context = {
        'getException':getException,
        'days':days,
        'getContent':getContent
    }
    return render(request, 'clients/inquiryEdit.html', context)

def updateException(request, exclude_patch_ID):
    print (exclude_patch_ID)
    getException = EXCEPTION.objects.get(pk=exclude_patch_ID)
    if request.method == 'POST':   
        getException.title = request.POST['title']
        getException.save(update_fields=['title'])

        getException.justification = request.POST['justification']
        getException.save(update_fields=['justification'])

        getException.action_plan = request.POST['action_plan']
        getException.save(update_fields=['action_plan'])

        getException.exclude_date = request.POST['exclude_date']
        getException.save(update_fields=['exclude_date'])

    messages.success(request, "Your request has been submitted, an approver will get back to you soon")

    return redirect('exceptionsBoard')

def cleanEdit(request):
    if request.method == 'POST':
        fullObject2 = request.POST['fullObject2']
        
        print("fullObject2")
        #print(type(fullObject2)) #str
        print(fullObject2)

        """
        eliminar contenido dentro de parentesis (2), (8)
        """

        clean = re.sub(r'\([^)]*\)', '', fullObject2)

        print("clean")
        print(clean)

        return HttpResponse(clean)

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ CREATE EXCEPTION TYPE SERVER ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def selectServers(request):
    return render(request, 'clients/selectServers.html')

def inquiryServers(request):
    return render(request, 'clients/inquiryServers.html')

#AJAX LISTA DE SERVIDORES DEL CLIENTE INGRESADO
def server_user_list(request):

        # client_has_exception=EXCEPTION.objects.filter(client_id=request.user.id)
        # listServer_ID = [o.server_id for o in client_has_exception]
        # newList = []

        # for x in listServer_ID:
        #     newList.append(x.split(","))

        # newArray = []
        
        # for x in newList:
        #     for y in x:
        #         newArray.append(y)

        # newArray = set(newArray)
        # newArray = list(newArray) #quitar los repetidos #["1", "1", "2", "2"] -> ["1", "2"]

        # #print(type(newArray[0])) #<class 'str'>

        #     # prueba=EXCEPTION.objects.filter(server_id__contains=newArray) #filtra los que contenga el valor [2] con "1,2" funciona (icontains = insensitive (mayus minus por igual))
            
        #     # print("prueba")
        #     # print(prueba)

        #     # obj_list = [obj for obj in EXCEPTION.objects.all() if any(server_id in obj.server_id for server_id in newArray)]

        #     # print("obj_list")
        #     # print(obj_list)
        #     # print(type(obj_list)) #<class 'list'>

        # ob_list = EXCEPTION.objects.filter(reduce(lambda x, y: x | y, [Q(server_id__contains=word) for word in newArray]))
        # # print("ob_list")
        # # print(ob_list) #<QuerySet [<EXCEPTION: EXCEPTION object (226)>, <EXCEPTION: EXCEPTION object (227)>, <EXCEPTION: EXCEPTION object (228)>]>
        # #                 #aqui tenemos la lista de las excepciones que contienen los servidores de la matriz del paso 2) y 3)
        # # print(type(ob_list)) #<class 'list'>

        # listServer_Exception = [o.pk for o in ob_list]

    #-------------------------------------------------------
   
    quitarServidorPendiente= EXCEPTION.objects.filter(client_id=request.user.id).filter(state="Pending")
    quitarServidorStatusUno= EXCEPTION.objects.filter(client_id=request.user.id).filter(status_id=1)

    #quitamos los servidores que ya tengan realizada una excepción y este "Pendiente" o esten aprobados "status_id=1":
    arregloPendientes = []
    for x in quitarServidorPendiente:
        arregloPendientes.append(x.server_id.split(","))
        #newList.append(x.split(","))
    print("arregloPendientes")
    print(arregloPendientes) #[['1', '2'], ['1', '2']]

    ordenedArray = []
    
    for x in arregloPendientes:
        for y in x:
            ordenedArray.append(y)
    
    print("arregloPendientes nuevamente")
    print(ordenedArray) #[['1', '2'], ['1', '2']]

    #-------------------------------------------------------
    
    #quitamos los servidores que ya tengan realizada una excepción y este "Pendiente" o esten aprobados "status_id=1":
    arregloStatus = []

    for x in quitarServidorStatusUno:
        arregloStatus.append(x.server_id.split(","))

    print("arregloStatus")
    print(arregloStatus)

    ordenedArray2 = []
    
    for x in arregloStatus:
        for y in x:
            ordenedArray2.append(y)
    
    print("arregloStatus nuevamente")
    print(ordenedArray2) #[['1', '2'], ['1', '2']]

    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id).values_list('server_id', flat=True) #<QuerySet [1, 2]>

    serversPoll = SERVER.objects.filter(pk__in=client_has_server).exclude(pk__in=ordenedArray).exclude(pk__in=ordenedArray2)
    
    if request.method == "GET":
        return HttpResponse(serializers.serialize("json", serversPoll))

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

@csrf_exempt
def getPatchesInquiryServer(request):
    if request.method == 'POST':
        
        #string mode
        selectedServer = request.POST['selectedServer'] #wdcdmzyz22033245,wdcgz22050068
        selectedServer = selectedServer.replace(",", " ")
        selectedServer = selectedServer.split()

        client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)

        servers_ids=[]
        for server in client_has_server:
            servers_ids.append(server.server_id)

        takeServers=SERVER.objects.filter(pk__in=servers_ids).filter(hostname__in=selectedServer)
        
        servers_selected_ids=[]

        for server in takeServers:
            servers_selected_ids.append(server.pk)
        
        patch_advisory = PATCHES.objects.filter(server_id__in=servers_selected_ids)       
        
        print(patch_advisory)

        print("patch_advisory")

        #print(type(patch_advisory)) #'django.db.models.query.QuerySet'
        #print(type(serializers.serialize("json", patch_advisory))) #'str'

        return HttpResponse(serializers.serialize("json", patch_advisory))

@csrf_exempt
def getServerIDServer(request):
    if request.method == 'POST':
        #toma el servidor seleccionado

        print("SERVEEEEEEER")
        #string mode
        selectedServer = request.POST['selectedServer'] #wdcdmzyz22033245,wdcgz22050068

        selectedServer = selectedServer.replace(",", " ")
        selectedServer = selectedServer.split()
        print(selectedServer)

        pickServerID = SERVER.objects.filter(hostname__in=selectedServer)
        print(pickServerID)
        return HttpResponse(serializers.serialize("json", pickServerID))

#POST REQUEST CREAR EXCEPCIÓN
def exclude_server(request):
#def exclude_server(request, serverString):
    #print(serverString)
    if request.method == 'POST':
        patch_id = request.POST['patch_id']
        action_plan = request.POST['action_plan']
        client = request.user
        title = request.POST['title']
        justification = request.POST['justification']
        exclude_date = request.POST['exclude_date']
        content = request.POST['content']
        exception_type = request.POST['exception_type']
        server_id = request.POST['server_id']

        # def randomString(stringLength=8):
        #     letters = string.ascii_lowercase
        #     return ''.join(random.choice(letters) for i in range(stringLength))

        #risk_id = ('RISK'+randomString(8))

        #Check if user has made inquiry already
        # if request.user.is_authenticated:
        #     has_contacted = exclude_patch.objects.all().filter(patch_id=patch_id, client=client)
        #     if has_contacted:
        #         messages.error(request, 'You have already made an exception for this patch')
        #         return redirect('dashboard')

        #print(EXCEPTION.objects.latest('risk_id'))

        if(EXCEPTION.objects.exists()):
            var = EXCEPTION.objects.latest('risk_id')

            var = re.sub('RISK', '', var.risk_id)
            var=int(var)
            var+=1
            print(var)#8
            print(type(var))#int
            if (var < 10):
                var=str(var)
                var="RISK0000"+var
            elif (var > 9):
                var=str(var)
                var="RISK000"+var
            elif (var > 99):
                var=str(var)
                var="RISK00"+var
            elif (var > 999):
                var=str(var)
                var="RISK0"+var
            elif (var > 9999):
                var=str(var)
                var="RISK"+var

        else:
            var = "RISK00001"

        print(var)
        print(type(var))

        risk_id=var
              
        #exclude_this_server = EXCEPTION(patch_id=patch_id, action_plan=action_plan, client=client, title=title, justification=justification, exclude_date=exclude_date, content=content, exception_type=exception_type, server_id=server_id)
        exclude_this_server = EXCEPTION(patch_id=patch_id, action_plan=action_plan, client=client, title=title, justification=justification, exclude_date=exclude_date, content=content, exception_type=exception_type, server_id=server_id,risk_id=risk_id)
        
        exclude_this_server.save()
        
        messages.success(request, "Your request has been submitted, an approver will get back to you soon")

        return redirect('exceptionsBoard')

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ CREATE EXCEPTION TYPE PATCH ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def selectServerPatch(request):
    return render(request, 'clients/selectServerPatch.html')

def selectPatches(request):
    return render(request, 'clients/selectPatches.html')

def server_user_list2(request): #cuando seleccionas un Server Patch
    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id).values_list('server_id', flat=True) #<QuerySet [1, 2]>

    #-- robado del de arriba

    # quitarServidorPendiente= EXCEPTION.objects.filter(server_id__in=client_has_server).filter(client_id=request.user.id).filter(state="Pending")
    # quitarServidorStatusUno= EXCEPTION.objects.filter(server_id__in=client_has_server).filter(client_id=request.user.id).filter(status_id=1)
    # print("quitarServidorPendiente")
    # print(quitarServidorPendiente)
    # print("quitarServidorStatusUno")
    # print(quitarServidorStatusUno)

    #-- robado del de arriba

    #print(client_has_server)

    #quitarServidorSeleccionado=EXCEPTION.objects.filter(client_id=request.user.id).filter(exception_type=2)

    #quitarServidorSeleccionado=EXCEPTION.objects.filter(client_id=request.user.id).exclude(state="Canceled").filter(server_id__in=client_has_server)
    quitarServidorSeleccionado=EXCEPTION.objects.filter(client_id=request.user.id).filter(server_id__in=client_has_server)

    print("quitarServidorSeleccionado")
    print(quitarServidorSeleccionado)

    arregloServidor = []
    for x in quitarServidorSeleccionado:
        arregloServidor.append(x.server_id)

    # print("arreglo")
    # print(arregloServidor)

    #serversPoll = SERVER.objects.filter(pk__in=client_has_server).exclude(pk__in=arregloServidor)
    serversPoll = SERVER.objects.filter(pk__in=client_has_server)
    
    print("HERMOSSOOOOSOOS")
    #print(serversPoll)
    """
    context={
        'serversPoll':serversPoll
    }
    """
    if request.method == "GET":
        return HttpResponse(serializers.serialize("json", serversPoll))

def inquiryPatches(request):
    return render(request, 'clients/inquiryPatches.html')

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


        #+++++++++++ eliminar parches ya seleccionados por el usuario +++++++++++++++++++++++++++++++++

        quitarParchesPendientes= EXCEPTION.objects.filter(client_id=request.user.id).filter(state="Pending")

        listPatches = [o.patch_id for o in quitarParchesPendientes]
        
        newList = []
        for x in listPatches:
            newList.append(x.split(","))

        otherList = []
        for x in newList:
            for y in x:
                otherList.append(str(y))
    
        quitarParchesStatusUno=EXCEPTION.objects.filter(client_id=request.user.id).filter(status_id=1)

        listPatches2 = [o.patch_id for o in quitarParchesStatusUno]
        
        newList2 = []
        for x in listPatches2:
            newList2.append(x.split(","))

        otherList2 = []
        for x in newList2:
            for y in x:
                otherList2.append(str(y))

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        patch_advisory = PATCHES.objects.filter(server_id__in=servers_selected_ids).exclude(pk__in=otherList).exclude(pk__in=otherList2)
        
        print(patch_advisory)
        print("patch_advisory")
        print(type(patch_advisory)) #'django.db.models.query.QuerySet'
        print(type(serializers.serialize("json", patch_advisory))) #'str'

        return HttpResponse(serializers.serialize("json", patch_advisory))






@csrf_exempt
def getHostnames(request):
    if request.method == "POST":
        serverID = request.POST.get("serverID")
        serverhostnames = SERVER.objects.filter(pk__in=serverID)
        return HttpResponse(serializers.serialize("json", serverhostnames))

@csrf_exempt
def getAdvisoriesDesc(request):
    if request.method == "POST":
        advisoryDescription = request.POST.get("advisoryDescription")
        advDesc = ADVISORY.objects.filter(pk__in=advisoryDescription)
        return HttpResponse(serializers.serialize("json", advDesc))

@csrf_exempt
def transform(request):
    if request.method == 'POST':

        """
        arrayServers = array[::2] #par impar
        arrayAdvisories = array[1::2]
        """

        fullObject = request.POST['fullObject']

        """
        #DONE SERVERS (quitar el contenido dentro de corchetes)
        # servers = re.sub("[\(\[].*?[\)\]]", "", fullObject)
        # servers = servers.replace(":", "")
        # servers = servers.replace(",", " ")
        # servers = servers.split()
        # serverID = SERVER.objects.filter(hostname__in=servers).values_list('id', flat=True)
        # print(serverID)
        
        #DONE ADVISORIES (seleccionar contenido dentro de corchetes)
        # justAdvisories = re.findall(r'\[(.*?)\]',fullObject)
        # advisoryID = ADVISORY.objects.filter(description__in=justAdvisories).values_list('id', flat=True)
        # print(advisoryID)
        """


        # print("fullObject")
        # print(fullObject)
        takeID = re.findall(r'\((.*?)\)',fullObject)
        #print(takeID)
        patches = PATCHES.objects.filter(pk__in=takeID)
        return HttpResponse(serializers.serialize("json", patches))

@csrf_exempt
def clean(request):
    if request.method == 'POST':
        fullObject2 = request.POST['fullObject2']
        
        print("fullObject2")
        #print(type(fullObject2)) #str
        print(fullObject2)

        """
        eliminar contenido dentro de parentesis (2), (8)
        """

        clean = re.sub(r'\([^)]*\)', '', fullObject2)
        #print("clean")
        #print(clean) #wdcdmzyz22033245:[SUSE-SU-2019:3091-1: important: Securityupdate for ucode-intel] criticality: Low

        
        # clean2 = re.findall('\(([^)]+)', fullObject2)
        # #print("clean2")
        # #print(clean2) #['MSS-0AR-E01-2011:0487.1_atlbz151024', 'MSS-0AR-E01-2011:0487.1_atlbz151037']

        # array=[]
        
        # for i in range(0, len(clean2)):
        #     #clean2[i] = int(clean2[i])
        #     clean2[i] = str(clean2[i])
        #     array.append(clean2[i])
        
        # patches = PATCHES.objects.filter(pk__in=array).values_list('advisory_id', flat=True) #faltaría filtrar aqui con el status_id=2
        # advisories = ADVISORY.objects.filter(pk__in=patches).values_list('criticality', flat=True)
        # print(advisories) #['Low', 'High', 'Low']

        # context = {
        #     'clean':clean,
        #     'advisories':advisories,
        # }

        print("clean")
        print(clean)

        return HttpResponse(clean)

@csrf_exempt
def getServerIDPatch(request):
    if request.method == 'POST':
        print("SERVEEEEEEER")
        #string mode
        fullObject = request.POST['fullObject'] #wdcdmzyz22033245:[RHSA-2019:3538-01: yun security. bug fix.

        #selectedServer = selectedServer.replace(",", " ")
        #selectedServer = selectedServer.split()
        
        #DONE SERVERS (quitar el contenido dentro de corchetes)
        fullObject = re.sub("[\(\[].*?[\)\]]", "", fullObject)
        fullObject = fullObject.replace(":", "")
        fullObject = fullObject.replace(",", " ")
        fullObject = fullObject.split()
        
        serverID = SERVER.objects.filter(hostname__in=fullObject)
        return HttpResponse(serializers.serialize("json", serverID))

"""
@csrf_exempt
def getCriticality(request):
    if request.method == "POST":
        criticality = request.POST.get("criticality")

        criticalidad = ADVISORY.objects.filter(pk__in=criticality)
        return HttpResponse(serializers.serialize("json", criticalidad))
"""

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ EXCEPTION DETAIL ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def exceptionDetail(request, exclude_patch_ID):
    justException = get_object_or_404(EXCEPTION, pk=exclude_patch_ID) #FRONTEND

    exceptionQuery = EXCEPTION.objects.filter(pk=exclude_patch_ID)
    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    servers_ids=[]
    for server in client_has_server:
        servers_ids.append(server.server_id)
    takeServers=SERVER.objects.filter(pk__in=servers_ids)
    takeExceptionPatchIDS=[]
    for x in exceptionQuery:
        takeExceptionPatchIDS.append(x.patch_id)
    takeExceptionPatchIDS =  ', '.join(takeExceptionPatchIDS)
    takeExceptionPatchIDS = takeExceptionPatchIDS.replace(",", " ")
    takeExceptionPatchIDS = takeExceptionPatchIDS.split()
    for i in range(0, len(takeExceptionPatchIDS)): 
        takeExceptionPatchIDS[i] = str(takeExceptionPatchIDS[i])
    patchObjects = PATCHES.objects.filter(pk__in=takeExceptionPatchIDS).filter(server_id__in=takeServers) #FRONTEND

    validations=VALIDATE_EXCEPTION.objects.filter(exception=exclude_patch_ID)

    #approver remaining:
    takeExceptionServerID= [o.server_id for o in exceptionQuery]
    takeExceptionServerID=', '.join(takeExceptionServerID)
    takeExceptionServerID = takeExceptionServerID.split(",")
    takeExceptionServerID = list(map(int, takeExceptionServerID))
    usersApprover = Profile.objects.filter(role=2).values_list("user_id")
    getServerID = SERVER.objects.filter(pk__in=takeExceptionServerID).values_list("id")
    serverApprover = SERVER_USER_RELATION.objects.filter(user_id__in=usersApprover).filter(server_id__in=getServerID).values_list('user_id')
    approver_detail = User.objects.filter(pk__in=serverApprover)
    authorize = VALIDATE_EXCEPTION.objects.filter(exception=justException.id).filter(approver_id__in =approver_detail)
    approver_detail_pending = approver_detail.exclude(pk__in=authorize.values_list('approver_id'))

    context = {
        'justException':justException, #FRONTEND
        'patchObjects':patchObjects, #FRONTEND
        'approver_detail_pending':approver_detail_pending, #FRONTEND
        'validations':validations
    }

    return render(request, 'clients/exceptionDet.html', context)