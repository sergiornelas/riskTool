from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404
from exception.choices import state_choices
from django.contrib import messages
from django.contrib.auth.models import User
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
    
    servers = SERVER.objects.filter(pk__in=takeServerID)
    
    takeHostnames = [o.hostname for o in servers]
    
    for hostname in takeHostnames:
        exceptionsApprover = EXCEPTION.objects.filter(content__contains=hostname) #tiene que ser el valor exacto.

    arreglin=[]
    
    for server_id in takeServerID:
        arreglin.extend(EXCEPTION.objects.filter(server_id__contains=server_id).values_list('id', flat=True))
    
    arreglin=set(arreglin)
    
    excepciones=EXCEPTION.objects.filter(pk__in=arreglin).exclude(state="Canceled")
    
    paginator = Paginator(excepciones, 8)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    #all = zip(excepciones, yourState) #ME LIMITABA LA SALIDA EL YOURSTATE

    context = {
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

    context = {
        'state_choices':state_choices,
        'excepciones': queryset_list,
        #'excepciones2': paged_listings2,
        'values': request.GET
    }

    return render(request, 'approvers/search.html', context)

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[ APPROVAL DETAIL ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

def approvalDet(request, exclude_patch_ID):
    justException = get_object_or_404(EXCEPTION, pk=exclude_patch_ID)

    exceptionQuery = EXCEPTION.objects.filter(pk=exclude_patch_ID)

    client_has_server=SERVER_USER_RELATION.objects.filter(user_id=request.user.id)

    servers_ids=[]
    for server in client_has_server:
        servers_ids.append(server.server_id)

    takeServers=SERVER.objects.filter(pk__in=servers_ids)

    takeServersFront= [o.hostname for o in takeServers] #FRONTEND
    takeExceptionPatchIDS=[]
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
    
    patchObjects = PATCHES.objects.filter(pk__in=takeExceptionPatchIDS).filter(server_id__in=takeServers)

    arrayAdvisories = []
    for a in patchObjects:
        arrayAdvisories.append(a.advisory_id)
    
    advisories = ADVISORY.objects.filter(pk__in=arrayAdvisories)
    
    takeExceptionServerID= [o.server_id for o in exceptionQuery]
    takeExceptionServerID=', '.join(takeExceptionServerID)
    takeExceptionServerID = takeExceptionServerID.split(",")
    takeExceptionServerID = list(map(str, takeExceptionServerID))

    usersApprover = Profile.objects.filter(role=2).values_list("user_id")

    getServerID = SERVER.objects.filter(pk__in=takeExceptionServerID).values_list("id")
    
    #CHANGE
    serverApprover = SERVER_USER_RELATION.objects.filter(user_id__in=usersApprover).filter(server_id__in=getServerID).values_list('user_id')
    print("AWUIIIIIIIIII")
    print(serverApprover)
    
    approver_detail = User.objects.filter(pk__in=serverApprover)

    authorize = VALIDATE_EXCEPTION.objects.filter(exception=justException.id).filter(approver_id__in =approver_detail)
    
    try:
        singleAuthorize = VALIDATE_EXCEPTION.objects.filter(exception=justException.id).get(approver_id =request.user.id)
    except:
        singleAuthorize = ""
    
    approver_detail_pending = approver_detail.exclude(pk__in=authorize.values_list('approver_id'))
    
    print("AWFAWEOFIAJWEFOIAWEN")
    pendingApprover = User.objects.filter(pk__in=approver_detail_pending).exclude(pk=request.user.id)

    takeApproverNames= [o.username for o in pendingApprover]
    print("HEREEEEE")

    takeApproverNames = ', '.join(takeApproverNames)
    takeApproverNames = takeApproverNames.replace(",", "")
    print(type(takeApproverNames))
    print(takeApproverNames)

    lastArray = []
    for a in pendingApprover:
        lastArray.append(a.username)

    print("LASTARRAY")
    print(lastArray)

    print("PENDING!")
    print(approver_detail_pending)
    print(pendingApprover)

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
            print("Approved")
            justException.state = 'Approved'
            justException.status_id = 1
            justException.save(update_fields=['state'])
            justException.save(update_fields=['status_id'])
            break
        if p.state == 'Rejected':
            print("Approver reject exception:", p)
            print("Rejected")
            justException.state = 'Rejected'
            justException.save(update_fields=['state'])
            break
        else: #in case is not approved or rejected or pending (avoiding bugs)
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
        
    validate = VALIDATE_EXCEPTION(exception_id=exception_id, approver=approver, state=state, comment=comment, approver_pending=approver_pending, risk_id=risk_id)
    validate.save()
    return redirect('approvalDet', exception_id)


#NOTAS:
    #get_object_or_404 will only return one object, get_list_or_404 multiple objects. Levanta la excepción Http404 si no existe el objeto.
        #get_object_or_404 uses get(), get_list_or_404 uses filter()

    #.values(,)
        #returns a QuerySet containing dictionaries
            #<QuerySet [{'comment_id': 1}, {'comment_id': 2}]>