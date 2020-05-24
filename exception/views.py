from django.shortcuts import redirect
from django.contrib import messages
from .models import exclude_patch

#from approvers.models import authorize_Exception
#from django.core.mail import send_mail

def exclude(request):
    if request.method == 'POST':
        client = request.user
        patch_id = request.POST['patch_id']
        title = request.POST['title']
        justification = request.POST['justification']
        exclude_date = request.POST['exclude_date']

        #Check if user has made inquiry already
        if request.user.is_authenticated:
            has_contacted = exclude_patch.objects.all().filter(patch_id=patch_id, client=client)
            if has_contacted:
                messages.error(request, 'You have already made an exception for this patch')
                return redirect('dashboard')
               
        exclude = exclude_patch(patch_id=patch_id, client=client, title=title, justification=justification, exclude_date=exclude_date)
        exclude.save()

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