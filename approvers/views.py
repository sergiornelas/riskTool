from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404
from exception.choices import state_choices
#message alerts
from django.contrib import messages
#user registration, model 
from django.contrib.auth.models import User
#user registration, login after register
from django.contrib import auth
from patches.models import PATCHES
from advisory.models import ADVISORY
import re
from roles.models import Profile
from exception.models import EXCEPTION
from exception.models import VALIDATE_EXCEPTION
from django.http import HttpResponse
from django import forms
from django.forms import ModelForm
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from servers.models import SERVER_USER_RELATION
from servers.models import SERVER

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ APPROVAL LIST ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def approvalsList(request):
    serversApprover = SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    
    takeServerID = [o.server_id for o in serversApprover]
    # print("----------------------")
    # print("tomamos servers id (tabla server_user_relation) del aprobador loggeado")
    # print(takeServerID)

    servers = SERVER.objects.filter(pk__in=takeServerID)
    # print("tomamos objetos (tabla servers) de los id de la tabla servreruserrelation")
    # print(servers)

    takeHostnames = [o.hostname for o in servers]
    # print("tomamos los puros hostname de los servidores del aprobador loggeado")
    # print(takeHostnames) #list

    #print(type(takeHostnames[1])) #str
   
    #si un field en la db contiene algun hostname
    for hostname in takeHostnames:
        exceptionsApprover = EXCEPTION.objects.filter(content__contains=hostname) #tiene que ser el valor exacto.
        #exceptionsID = EXCEPTION.objects.filter(content__icontains=hostname).values_list('id', flat=True) #tiene que ser el valor exacto.

    # print("tomamos los rows que contengan esos server names en la tabla EXCEPTIONS")
    # print(exceptionsApprover)

    #ME LIMITA LA IMPRESION DE TODAS LAS EXCEPCIONES.
    #yourState = VALIDATE_EXCEPTION.objects.filter(approver_id=request.user.id)

    #print("WOOOOOLA")

    """
    #-------------------patch_id mode

    patches = PATCHES.objects.filter(server_id__in=takeServerID)
    takePatchID = [o.id for o in patches]
    
    #print(takePatchID) #[1, 2, 3, 4, 5, 6, 7, 8, 9]
    #print(type(takePatchID)) #list
    #print(type(takePatchID[3])) #int

    patchArray=[]

    for x in takePatchID:
        patchArray.extend(EXCEPTION.objects.filter(patch_id__contains=x).values_list('id', flat=True))

    print(patchArray)       
    patchArray=set(patchArray)
    """

    #-------------------server_id mode (SOLO FUNCIONA SI EXISTEN 1-9 SERVIDORES (EL CONTAINS TOMA 10 COMO 1))

    arreglin=[]
    
    #print(takeServerID) #[1, 2]
    #print(type(takeServerID)) #list
    #print(type(takeServerID[0])) #int

    for server_id in takeServerID:
        arreglin.extend(EXCEPTION.objects.filter(server_id__contains=server_id).values_list('id', flat=True))
    
    arreglin=set(arreglin)
    
    #excepciones=EXCEPTION.objects.filter(pk__in=arreglin)
    excepciones=EXCEPTION.objects.filter(pk__in=arreglin).exclude(state="Canceled")
    
    paginator = Paginator(excepciones, 8)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    #para ordenarlo por fecha de creacion:
    #listings = Listing.objects.order_by('-list_date')

    #print(excepciones)

    """
    #-------------------
    #print(arreglin)
    #print(patchArray)

    #testing
    cadena = ('1,2,3,5,10,33')
    cadena = cadena.split(",") #<--
    cadena = list(map(int, cadena)) #<--
    
    # print(cadena)# [1, 2]
    # print(cadena[4])# 10
    # print(type(cadena)) #list
    # print(type(cadena[0])) #int

    #-------------------
    """

    #all = zip(excepciones, yourState) #ME LIMITABA LA SALIDA EL YOURSTATE

    context = {
        
        #'excepciones':excepciones
        'excepciones': paged_listings,
        'state_choices':state_choices
    }

    if request.user.is_authenticated:
        if request.user.profile.role == 2:
            return render(request, 'approvers/approvalsList.html', context)
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return render(request, 'pages/index.html')

#NUEVO!
def search(request):
    serversApprover = SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    takeServerID = [o.server_id for o in serversApprover]
    servers = SERVER.objects.filter(pk__in=takeServerID)
    takeHostnames = [o.hostname for o in servers]
    for hostname in takeHostnames:
        exceptionsApprover = EXCEPTION.objects.filter(content__contains=hostname) #tiene que ser el valor exacto.
    arreglin=[]
    for server_id in takeServerID:
        arreglin.extend(EXCEPTION.objects.filter(server_id__contains=server_id).values_list('id', flat=True))
    arreglin=set(arreglin)
    
    queryset_list=EXCEPTION.objects.filter(pk__in=arreglin)

    # paginator2 = Paginator(queryset_list, 3)
    # page2 = request.GET.get('page2')
    # paged_listings2 = paginator2.get_page(page2)

    if 'keywords' in request.GET:
        keywords = request.GET['keywords'] #"KEYWORDS" ES EL NAME EN HTML
        if keywords:
            #queryset_list = queryset_list.filter(risk_id__icontains=keywords) #contiene
            #SI ES POSIBLE FILTRAR NUEVAMENTE UN QUERYSET!!!
            queryset_list = queryset_list.filter(risk_id__iexact=keywords)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # paginator2 = Paginator(queryset_list, 3)
    # page2 = request.GET.get('page2')
    # paged_listings2 = paginator2.get_page(page2)

    context = {
        'state_choices':state_choices,
        'excepciones': queryset_list,
        #'excepciones2': paged_listings2,
        'values': request.GET
    }

    # excepciones=EXCEPTION.objects.filter(pk__in=arreglin)

    # paginator = Paginator(excepciones, 3)
    # page = request.GET.get('page')
    # paged_listings = paginator.get_page(page)

    # context = {
        
    #     #'excepciones':excepciones
    #     'excepciones': paged_listings,
    #     'state_choices':state_choices
    # }

    return render(request, 'approvers/search.html', context)

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ APPROVAL DETAIL ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def approvalDet(request, exclude_patch_ID):
    justException = get_object_or_404(EXCEPTION, pk=exclude_patch_ID)
    #EXCEPTION object (94)

    exceptionQuery = EXCEPTION.objects.filter(pk=exclude_patch_ID)
    #<QuerySet [<EXCEPTION: EXCEPTION object (94)>]>
    
        #-----------servers que el aprobador tiene#-----------

    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    #<QuerySet [<SERVER_USER_RELATION: SERVER_USER_RELATION object (7)>]>

        #almacenamos en una lista los id de los servidores del cliente loggeado.        
    servers_ids=[]
    for server in client_has_server:
        servers_ids.append(server.server_id)

    takeServers=SERVER.objects.filter(pk__in=servers_ids)
    #<QuerySet [<SERVER: wdcgz22050068>]>

    takeServersFront= [o.hostname for o in takeServers] #FRONTEND
    #['wdcgz22050068']
        
        #-----------takeException Case#-----------

    takeExceptionPatchIDS=[]
        #almacenamos un solo string a una lista porque vamos a necesitarla después.
    for x in exceptionQuery:
        #es una lista de un solo string: "1,2,3,4,5"
        takeExceptionPatchIDS.append(x.patch_id)

        #convertir la lista a un string
    takeExceptionPatchIDS =  ', '.join(takeExceptionPatchIDS)
        #el string quitar las comas y añadir espacios para convertirlo a lista nuevamente
    takeExceptionPatchIDS = takeExceptionPatchIDS.replace(",", " ")
        #se convierte a una lista (pero ahora cada id del parche esta en un indice diferente)
    takeExceptionPatchIDS = takeExceptionPatchIDS.split()
        #convertimos cada elemento string de la lista a entero (siguen siendo strings)
    for i in range(0, len(takeExceptionPatchIDS)): 
        #takeExceptionPatchIDS[i] = int(takeExceptionPatchIDS[i])
        takeExceptionPatchIDS[i] = str(takeExceptionPatchIDS[i])
    #[1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    patchObjects = PATCHES.objects.filter(pk__in=takeExceptionPatchIDS).filter(server_id__in=takeServers)
    #<QuerySet [<PATCHES: wdcgz22050068 : 'RHSA-2019:3538-01: yun security. bug fix. and enhancement update' , >,
    #<PATCHES: wdcgz22050068 : 'SUSE-SU-2019:3091-1: important: Securityupdate for ucode-intel' , >,
    #<PATCHES: wdcgz22050068 : 'Security Bulletin: Vulnerabilities in tcpdumb affect AIX' , >,
    #<PATCHES: wdcgz22050068 : 'Security Bulletin: Vulnerabilities tcpdumb foo RHEL' , >]>

    arrayAdvisories = []
    for a in patchObjects:
        arrayAdvisories.append(a.advisory_id)
    #[1, 2, 4, 6]
    
        #bug (no sale el total de los advisories (quita repetidos))
    advisories = ADVISORY.objects.filter(pk__in=arrayAdvisories)
    #<QuerySet [<ADVISORY: RHSA-2019:3538-01: yun security. bug fix. and enhancement update>,
    #<ADVISORY: SUSE-SU-2019:3091-1: important: Securityupdate for ucode-intel>,
    #<ADVISORY: Security Bulletin: Vulnerabilities in tcpdumb affect AIX>,
    #<ADVISORY: Security Bulletin: Vulnerabilities tcpdumb foo RHEL>]>

    #comienza la tabla de aprobadores xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#<takeException hostname from database>
    """
    takeExceptionHostnames=[]
        #almacenamos un solo string a una lista porque vamos a necesitarla después.
    for x in exceptionQuery:
        #es una lista de un solo string: "1,2,3,4,5"
        takeExceptionHostnames.append(x.content)

        #convertir la lista a un string
    takeExceptionHostnames =  ', '.join(takeExceptionHostnames)
        #el string quitar las comas y añadir espacios para convertirlo a lista nuevamente
    takeExceptionHostnames = takeExceptionHostnames.replace(",", " ")
        #se convierte a una lista (pero ahora cada id del parche esta en un indice diferente)
    takeExceptionHostnames = takeExceptionHostnames.split()
        #convertimos cada elemento string de la lista a entero (siguen siendo strings)
    #['wdcdmzyz22033245', 'wdcgz22050068']
    """

    """
    CONVERTIR UNA LISTA A UN STRING, PARA HACER SPLIT, Y CREAR UNA LISTA DE ENTEROS!!
    """

    takeExceptionServerID= [o.server_id for o in exceptionQuery]
    #['1']

    #print(takeExceptionServerID) #['1,2']
    #print(type(takeExceptionServerID)) #list

    takeExceptionServerID=', '.join(takeExceptionServerID)
    #print(takeExceptionServerID) #1,2
    #print(type(takeExceptionServerID)) #str

    takeExceptionServerID = takeExceptionServerID.split(",")
    #print(takeExceptionServerID)
    #takeExceptionServerID = list(map(int, takeExceptionServerID))
    takeExceptionServerID = list(map(str, takeExceptionServerID))
    #print(takeExceptionServerID)

#</takeException hostname from database>

    usersApprover = Profile.objects.filter(role=2).values_list("user_id")
    #<QuerySet [(4,), (5,), (6,)]>

    getServerID = SERVER.objects.filter(pk__in=takeExceptionServerID).values_list("id")
    #print(getServerID)
    #<QuerySet [(1,), (2,)]>
    
    #CHANGE
    serverApprover = SERVER_USER_RELATION.objects.filter(user_id__in=usersApprover).filter(server_id__in=getServerID).values_list('user_id')
    print("AWUIIIIIIIIII")
    print(serverApprover)
    
    
    #<QuerySet [(4,), (6,), (4,), (5,)]>  (+.values_list('user_id'))
        #<QuerySet [<SERVER_USER_RELATION: SERVER_USER_RELATION object (5)>,
        #<SERVER_USER_RELATION: SERVER_USER_RELATION object (8)>,
        #<SERVER_USER_RELATION: SERVER_USER_RELATION object (6)>,
        #<SERVER_USER_RELATION: SERVER_USER_RELATION object (7)>]>

    approver_detail = User.objects.filter(pk__in=serverApprover)
    #<QuerySet [<User: approver>, <User: approver2>, <User: approver3>]>

    authorize = VALIDATE_EXCEPTION.objects.filter(exception=justException.id).filter(approver_id__in =approver_detail)
    #<QuerySet [<VALIDATE_EXCEPTION: VALIDATE_EXCEPTION object (1)>,
    #<VALIDATE_EXCEPTION: VALIDATE_EXCEPTION object (2)>,
    #<VALIDATE_EXCEPTION: VALIDATE_EXCEPTION object (3)>]>

    try:
        singleAuthorize = VALIDATE_EXCEPTION.objects.filter(exception=justException.id).get(approver_id =request.user.id)
        #VALIDATE_EXCEPTION object (22)
        #TIENES QUE USAR GET CUANDO SOLO NECESITAS UN OBJETO, Y AL MOMENTO DE LLAMARLO AL FRONTEND SIN USAR FOR
    except:
        singleAuthorize = ""
        #""
    
    approver_detail_pending = approver_detail.exclude(pk__in=authorize.values_list('approver_id'))
    

    #pendingApprover2 = User.objects.filter(pk__in=approver_detail_pending).values_list('username', flat=True)
    print("AWFAWEOFIAJWEFOIAWEN")
    #print(pendingApprover2)
    pendingApprover = User.objects.filter(pk__in=approver_detail_pending).exclude(pk=request.user.id)

    #user_id=request.user.id)

    
    takeApproverNames= [o.username for o in pendingApprover]
    print("HEREEEEE")

    takeApproverNames = ', '.join(takeApproverNames)
    takeApproverNames = takeApproverNames.replace(",", "")
    print(type(takeApproverNames))
    print(takeApproverNames)
  

    lastArray = []
    for a in pendingApprover:
        lastArray.append(a.username)
    #lastArray = ', '.join(lastArray)
    #lastArray = lastArray.replace(",", "+")

    #if not lastArray:
    #    lastArray = "All approvers have taken action"

    print("LASTARRAY")
    print(lastArray)
    

    print("PENDING!")
    print(approver_detail_pending)
    print(pendingApprover)
    #<QuerySet [<User: approver>, <User: approver2>, <User: approver3>]>

    countTotal = 0
    for a in approver_detail:
        countTotal +=1
    print("")
    print("Total approval for this exception:",countTotal)

    countApproved = 0
    for p in authorize:
        if p.state == 'Approved':
            print("Approver approved it:", p)
            countApproved+=1
        if countApproved == countTotal:
            #print("Approver found it:", p)
            print("Approved")
            justException.state = 'Approved'
            justException.save(update_fields=['state'])
            break
        if p.state == 'Rejected':
            print("Approver reject exception:", p)
            print("Rejected")
            justException.state = 'Rejected'
            justException.save(update_fields=['state'])
            break
        else: #in case is not approved or rejected or pending (avoiding bugs)
            #print("Approver pending:", p)
            justException.state = 'Pending'
            justException.save(update_fields=['state'])

    context = {
        'justException':justException, #FRONTEND
        'patchObjects':patchObjects, #FRONTEND
        'advisories':advisories, #FRONTEND
        'takeServersFront':takeServersFront, #FRONTEND
        'approver_detail':approver_detail, #DATABASE
        'authorize':authorize, #DATABASE
        'singleAuthorize':singleAuthorize, #FRONTEND
        'pendingApprover':pendingApprover,
        'lastArray':lastArray,
        'takeApproverNames':takeApproverNames,
        #'pendingApprover2':pendingApprover2
    }

    #path = SERVER_USER_RELATION.objects.filter(user_id=request.user.id).filter(server_id__in=client_has_server.id).values_list('user_id', flat=True)
    #print(path)

    return render(request, 'approvers/approvalDetail.html', context)

def authorize(request):
    if request.method == 'POST':
        exception_id = request.POST['exception_id']
        approver = request.user
        state = request.POST['state']
        comment = request.POST['comment']
        risk_id = request.POST['risk_id']
        approver_pending = request.POST['approver_pending']
        #time = request.POST[time]
        
    #validate = VALIDATE_EXCEPTION(exception_id=exception_id, approver=approver, state=state, comment=comment, risk_id=risk_id)
    validate = VALIDATE_EXCEPTION(exception_id=exception_id, approver=approver, state=state, comment=comment, approver_pending=approver_pending, risk_id=risk_id)
    validate.save()
    #return redirect('approvalsList')
    return redirect('approvalDet', exception_id)


#NOTAS:
    #get_object_or_404 will only return one object, get_list_or_404 multiple objects. Levanta la excepción Http404 si no existe el objeto.
        #get_object_or_404 uses get(), get_list_or_404 uses filter()
        
    #__in se utiliza cuando quieres usar de referencia objetos con otros objetos.

    #.values(,)
        #returns a QuerySet containing dictionaries
            #<QuerySet [{'comment_id': 1}, {'comment_id': 2}]>

    #.values_list(,)
        #returns a QuerySet containing tuples
            #<QuerySet [(1,), (2,)]>

    #If you are using values_list() with a single field, you can use flat=True to return a QuerySet of single values instead of 1-tuples:
    #flat=True will remove the tuples and return the list
        #<QuerySet [1, 2]>