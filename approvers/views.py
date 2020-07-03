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
from patches.models import PATCHES
from advisory.models import ADVISORY

from roles.models import Profile
from exception.models import exclude_patch
from exception.models import EXCEPTION
from exception.models import AUTHORIZE_EXCEPTION
from .models import patchApproverRelationship
from .models import authorize_Exception
from django.http import HttpResponse
from django import forms
from django.forms import ModelForm
from django.core import serializers

from servers.models import SERVER_USER_RELATION
from servers.models import SERVER

def approvalsList(request):

    serversApprover = SERVER_USER_RELATION.objects.filter(user_id=request.user.id)
    
    takeServerID = [o.server_id for o in serversApprover]
    print("----------------------")
    print("tomamos servers id (tabla server_user_relation) del aprobador loggeado")
    print(takeServerID)

    servers = SERVER.objects.filter(pk__in=takeServerID)
    print("tomamos objetos (tabla servers) de los id de la tabla servreruserrelation")
    print(servers)

    takeHostnames = [o.hostname for o in servers]
    print("tomamos los puros hostname de los servidores del aprobador loggeado")
    print(takeHostnames) #list

    #print(type(takeHostnames[1])) #str
   
    #si un field en la db contiene algun hostname
    for hostname in takeHostnames:
        exceptionsApprover = EXCEPTION.objects.filter(content__icontains=hostname) #tiene que ser el valor exacto.

    print("tomamos los rows que contengan esos server names en la tabla EXCEPTIONS")
    print(exceptionsApprover)


    context = {
        'exceptions': exceptionsApprover
    }

    if request.user.is_authenticated:
        if request.user.profile.role == 2:
            return render(request, 'approvers/approvalsList.html', context)            
        else:
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return render(request, 'pages/index.html')



def approvalDetail(request, exclude_patch_ID):
    #FRONTEND SIMPLE QUERIES
        # exclude_patch_ID = 8

    exceptionQuery = get_object_or_404(exclude_patch, pk=exclude_patch_ID)
        #Selecciona el objeto que contiene el {id 8 en exclude_patch model}:
            #<id=8, title=elID2, just=awef, patch_id=2>
    patch_exc = get_object_or_404(patch, pk=exceptionQuery.patch_id)
        #Selecciona el objeto que contiene en el id, dentro del patch model, el {valor de patch_id en el objeto exception}:
            #<id=2, server=Linux, crit=Medium, client_id=3>

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    approver_detail = User.objects.filter(pk__in=patchApproverRelationship.objects.filter(patch=exceptionQuery.patch_id).values_list('approver_id'))
                                                                                                                        #con values_list le damos a entender que queremos los valores de approver_id
                                                                                                                        # y no los del id directo de pachapproverrelationship
    
    authorize = authorize_Exception.objects.filter(exception_id=exceptionQuery.id).filter(approver_id__in =approver_detail)

    approver_detail_pending = approver_detail.exclude(pk__in=authorize.values_list('approver_id'))

    # TESTING
    # print("exclude_patch_ID = ", exclude_patch_ID, "\n")
    # print("excepcion = " , exception, "\n")
    # print("patch_exc = " , patch_exc, "\n")
    # print("approver_detail ",approver_detail)
    # print("")
    # print("authorize ",authorize)
    # print("")
    # print("approver_detail_pending ",approver_detail_pending)
    
    # for i in approver_detail:
    #     for j in authorize:
    #         if i.id == j.approver_id:
    #             print(i," y ",j," tienen el mismo id")
    #         else:
    #             print(i," y ",j," NO tienen el mismo id")
      

    # approveObjects = zip(authorize, approver_detail_pending)
    
    # if authorize:
    #     print ("\nExisten autorizaciones de los aprobadores responsables en la excepcion dentro de la tabla\n")
    # else:
    #     print ("\nNo existen autorizaciones de los aprobadores responsables en la excepcion dentro de la tabla\n")

    context = {
        'exceptionQuery': exceptionQuery,
        'patch_exc':patch_exc,
        'approver_detail':approver_detail,
        'authorize':authorize,
        'approver_detail_pending':approver_detail_pending,
    }

    path = patchApproverRelationship.objects.filter(approver_id=request.user.id).filter(patch_id=patch_exc.id).values_list('approver_id', flat=True)
    
    if request.user.is_authenticated:
        try:
            #if request.user.profile.role == 2:
            if request.user.id == path[0]:
                return render(request, 'approvers/approvalDetail.html', context)
        #else:
        except:    
            messages.error(request, 'Not allowed to enter here')
            return redirect('index')
    else:
        return redirect('login')







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
        takeExceptionPatchIDS[i] = int(takeExceptionPatchIDS[i])
    #[1, 2, 3, 4, 5, 6, 7, 8, 9]
    
        #patchObjects = PATCHES.objects.filter(pk__in=takeExceptionPatchIDS) (salia informacion de servidores que no le pertenece)
        #JUST FRONTEND:
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
        # necesitareEsto = zip(authorize, approver_detail_pending)
        #JUST FRONTEND:
    advisories = ADVISORY.objects.filter(pk__in=arrayAdvisories)
    #<QuerySet [<ADVISORY: RHSA-2019:3538-01: yun security. bug fix. and enhancement update>,
    #<ADVISORY: SUSE-SU-2019:3091-1: important: Securityupdate for ucode-intel>,
    #<ADVISORY: Security Bulletin: Vulnerabilities in tcpdumb affect AIX>,
    #<ADVISORY: Security Bulletin: Vulnerabilities tcpdumb foo RHEL>]>

    
    
    
    
    #comienza la tabla de aprobadores xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    #-----------takeException Hostname#-----------

    #takeExceptionPatchIDS -> takeExceptionHostnames

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

    usersApprover = Profile.objects.filter(role=2).values_list("user_id")
    #<QuerySet [(4,), (5,), (6,)]>

    getServerID = SERVER.objects.filter(hostname__in=takeExceptionHostnames).values_list("id")
    #<QuerySet [(1,), (2,)]>

    serverApprover = SERVER_USER_RELATION.objects.filter(user_id__in=usersApprover).filter(server_id__in=getServerID).values_list('user_id')
    #<QuerySet [(4,), (6,), (4,), (5,)]>  (+.values_list('user_id'))
        #<QuerySet [<SERVER_USER_RELATION: SERVER_USER_RELATION object (5)>,
        #<SERVER_USER_RELATION: SERVER_USER_RELATION object (8)>,
        #<SERVER_USER_RELATION: SERVER_USER_RELATION object (6)>,
        #<SERVER_USER_RELATION: SERVER_USER_RELATION object (7)>]>

    approver_detail = User.objects.filter(pk__in=serverApprover)
    #<QuerySet [<User: approver>, <User: approver2>, <User: approver3>]>

    #authorize = authorize_Exception.objects.filter(exception_id=exceptionQuery.id).filter(approver_id__in =approver_detail)
    #authorize = AUTHORIZE_EXCEPTION.objects.filter(exception_id=justException.id)
    #authorize = AUTHORIZE_EXCEPTION.objects.get(exception_id=94)
    #authorize = AUTHORIZE_EXCEPTION.objects.all()
    #print(authorize)

    #justException = get_object_or_404(EXCEPTION, pk=exclude_patch_ID)
    #EXCEPTION object (94)


    # necesitareEsto = zip(authorize, approver_detail_pending)
    context = {
        'justException':justException,
        #'exceptionQuery': exceptionQuery,
        'patchObjects':patchObjects,
        'advisories':advisories
    }

    return render(request, 'approvers/approvalDetail.html', context)







def authorize(request):
    if request.method == 'POST':
        exception_id = request.POST['exception_id']
        approver = request.user
        state = request.POST['state']
        comment = request.POST['comment']
        
    validate = authorize_Exception(exception_id=exception_id, approver=approver, state=state, comment=comment)
    validate.save()
    return redirect('approvalsList')


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