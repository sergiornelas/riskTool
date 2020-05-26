from django.shortcuts import redirect
from django.contrib import messages
from .models import exclude_patch
#from .models import approve_Exception
#from approvers.models import authorize_Exception

#from django.core.mail import send_mail

def exclude(request):
    if request.method == 'POST':
        #exclude_patch model
        patch_id = request.POST['patch_id']
        client = request.user
        title = request.POST['title']
        justification = request.POST['justification']
        exclude_date = request.POST['exclude_date']

        #approve_Exception model
        # state = "Pending"
        # comment = "Pending"
        # exception_id = 0
        # patch_id = 
        # approver = 0
        
        #Check if user has made inquiry already
        if request.user.is_authenticated:
            has_contacted = exclude_patch.objects.all().filter(patch_id=patch_id, client=client)
            if has_contacted:
                messages.error(request, 'You have already made an exception for this patch')
                return redirect('dashboard')
               
        exclude = exclude_patch(patch_id=patch_id, client=client, title=title, justification=justification, exclude_date=exclude_date)
        exclude.save()

        # validate = approve_Exception(state=state, comment=comment)
        # validate2 = approve_Exception(state=state, comment=comment)
        # validate.save()
        # validate2.save()

        messages.success(request, "Your request has been submitted, an approver will get back to you soon")

        return redirect('dashboard')

# def approvalDetail2(request):
#     if request.method == 'POST':
#             #authorize_Exception model
#         #exception_id = request.POST
#         #approver
#         #exception_id = exclude_patch.id
#         state = "Pending"
#         comment = "Pending"
                
#         #authorize = authorize_Exception(exception_id=exception_id, state=state, comment=comment)
#         authorize = authorize_Exception(state=state, comment=comment)
#         authorize.save()


# def approveException(request):
#     if request.method == 'POST':
#         state = "Pending"
#         comment = "Pending"
#         #exception_id = request.POST['exception_id']
#         approver = request.user
#         #state = request.POST['state']
    
#     validate = approve_Exception(approver=approver, state=state, comment=comment)
#     validate.save()
#     return redirect('approvalsList')