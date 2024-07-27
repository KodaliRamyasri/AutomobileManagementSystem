from django.shortcuts import render,redirect,reverse
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q, Sum
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth
from adminApp.views import isCustomer
import adminApp.forms as adminApp_forms
import adminApp.models as adminApp_models

@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerDashboard(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    work_in_progress=adminApp_models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
    work_completed=adminApp_models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
    new_request_made=adminApp_models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
    bill=adminApp_models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
    print(bill)
    dict={
    'work_in_progress':work_in_progress,
    'work_completed':work_completed,
    'new_request_made':new_request_made,
    'bill':bill['cost__sum'],
    'customer':customer,
    }
    return render(request,'customerApp/customerDashboard.html',context=dict)

@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerRequest(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    return render(request,'customerApp/customerRequest.html',{'customer':customer})


@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerViewRequest(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    enquiries=adminApp_models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'customerApp/customerViewRequest.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerDeleteRequest(request,pk):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    enquiry=adminApp_models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customerViewRequest')

@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerViewApprovedRequest(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    enquiries=adminApp_models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'customerApp/customerViewApprovedRequest.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerViewApprovedRequestInvoice(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    enquiries=adminApp_models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'customerApp/customerViewApprovedRequestInvoice.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerAddRequest(request):
    customer = adminApp_models.Customer.objects.get(user_id=request.user.id)
    enquiry = adminApp_forms.RequestForm()
    if request.method == 'POST':
        enquiry = adminApp_forms.RequestForm(request.POST)
        if enquiry.is_valid():
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.customer = customer
            enquiry_x.save()
            return HttpResponseRedirect('customerDashboard')
        else:
            print("form is invalid")
            print(enquiry.errors)
    return render(request, 'customerApp/customerAddRequest.html', {'enquiry': enquiry, 'customer': customer})

@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerProfile(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    return render(request,'customerApp/customerProfile.html',{'customer':customer})


@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def editCustomerProfile(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    user=adminApp_models.User.objects.get(id=customer.user_id)
    userForm=adminApp_forms.CustomerUserForm(instance=user)
    customerForm=adminApp_forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=adminApp_forms.CustomerUserForm(request.POST,instance=user)
        customerForm=adminApp_forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customerProfile')
    return render(request,'customerApp/editCustomerProfile.html',context=mydict)


@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerInvoice(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    enquiries=adminApp_models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'customerApp/customerInvoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerLogin')
@user_passes_test(isCustomer)
def customerFeedback(request):
    customer=adminApp_models.Customer.objects.get(user_id=request.user.id)
    feedback=adminApp_forms.FeedbackForm()
    if request.method=='POST':
        feedback=adminApp_forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'customerApp/feedbackSentByCustomer.html',{'customer':customer})
    return render(request,'customerApp/customerFeedback.html',{'feedback':feedback,'customer':customer})

