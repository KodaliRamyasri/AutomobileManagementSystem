from django.shortcuts import render,redirect,reverse
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth
from adminApp.views import isMechanic
import adminApp.forms as adminApp_forms
import adminApp.models as adminApp_models

@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicDashboard(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    work_in_progress=adminApp_models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing').count()
    work_completed=adminApp_models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing Done').count()
    new_work_assigned=adminApp_models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Approved').count()
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_work_assigned':new_work_assigned,
    'salary':mechanic.salary,
    'mechanic':mechanic,
    }
    return render(request,'mechanicApp/mechanicDashboard.html',context=dict)

@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicWorkAssigned(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    works=adminApp_models.Request.objects.all().filter(mechanic_id=mechanic.id)
    return render(request,'mechanicApp/mechanicWorkAssigned.html',{'works':works,'mechanic':mechanic})


@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicUpdateStatus(request,pk):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    updateStatus=adminApp_forms.MechanicUpdateStatusForm()
    if request.method=='POST':
        updateStatus=adminApp_forms.MechanicUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x=adminApp_models.Request.objects.get(id=pk)
            enquiry_x.status=updateStatus.cleaned_data['status']
            enquiry_x.save()
            return HttpResponseRedirect(reverse('mechanicWorkAssigned'))
        else:
            print("form is invalid")
    return render(request,'mechanicApp/mechanicUpdateStatus.html',{'updateStatus':updateStatus,'mechanic':mechanic})


@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicAttendance(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    attendaces=adminApp_models.Attendance.objects.all().filter(mechanic=mechanic)
    return render(request,'mechanicApp/mechanicViewAttendance.html',{'attendaces':attendaces,'mechanic':mechanic})


@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicFeedback(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    feedback=adminApp_forms.FeedbackForm()
    if request.method=='POST':
        feedback=adminApp_forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'mechanicApp/feedbackSent.html',{'mechanic':mechanic})
    return render(request,'mechanicApp/mechanicFeedback.html',{'feedback':feedback,'mechanic':mechanic})

@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicSalary(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    workdone=adminApp_models.Request.objects.all().filter(mechanic_id=mechanic.id).filter(Q(status="Repairing Done") | Q(status="Released"))
    return render(request,'mechanicApp/mechanicSalary.html',{'workdone':workdone,'mechanic':mechanic})

@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def mechanicProfile(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    return render(request,'mechanicApp/mechanicProfile.html',{'mechanic':mechanic})

@login_required(login_url='mechanicLogin')
@user_passes_test(isMechanic)
def editMechanicProfile(request):
    mechanic=adminApp_models.Mechanic.objects.get(user_id=request.user.id)
    user=adminApp_models.User.objects.get(id=mechanic.user_id)
    userForm=adminApp_forms.MechanicUserForm(instance=user)
    mechanicForm=adminApp_forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanic':mechanic}
    if request.method=='POST':
        userForm=adminApp_forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=adminApp_forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('mechanicProfile')
    return render(request,'mechanicApp/editMechanicProfile.html',context=mydict)
