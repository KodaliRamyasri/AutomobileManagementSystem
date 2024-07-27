from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User,auth
def homeView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'adminApp/index.html')

def aboutUs(request):
    return render(request,'adminApp/aboutUs.html')

def contactUs(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(
                f'{name} || {email}',  # Subject
                message,               # Message
                settings.EMAIL_HOST_USER,  # From email
                [settings.EMAIL_RECEIVING_USER],  # To email (must be a list)
                fail_silently=False
            )
            return render(request, 'adminApp/contactUsSuccess.html')
    return render(request, 'adminApp/contactUs.html', {'form': sub})

def customerClick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'adminApp/customerClick.html')

def mechanicsClick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request,'adminApp/mechanicsClick.html')

def adminClick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return HttpResponseRedirect('adminLogin')

def customerSignup(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerLogin')
    return render(request,'adminApp/customerSignup.html',context=mydict)


def mechanicSignup(request):
    userForm=forms.MechanicUserForm()
    mechanicForm=forms.MechanicForm()
    mydict={'userForm':userForm,'mechanicForm':mechanicForm}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic=mechanicForm.save(commit=False)
            mechanic.user=user
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
        return HttpResponseRedirect('mechanicLogin')
    return render(request,'adminApp/mechanicSignup.html',context=mydict)


#for checking user customer, mechanic or admin(by sumit)
def isCustomer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def isMechanic(user):
    return user.groups.filter(name='MECHANIC').exists()

def afterLogin(request):
    if isCustomer(request.user):
        return redirect('customerDashboard')
    elif isMechanic(request.user):
        accountapproval=models.Mechanic.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('mechanicDashboard')
        else:
            return render(request,'mechanicApp/mechanicWaitForApproval.html')
    else:
        return redirect('adminDashboard')

@login_required(login_url='adminLogin')
def adminDashboard(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'adminApp/adminDashboard.html',context=dict)

@login_required(login_url='adminLogin')
def adminCustomer(request):
    return render(request,'adminApp/adminCustomer.html')

@login_required(login_url='adminLogin')
def adminViewCustomer(request):
    customers=models.Customer.objects.all()
    return render(request,'adminApp/adminViewCustomer.html',{'customers':customers})


@login_required(login_url='adminLogin')
def deleteCustomer(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('adminViewCustomer')


@login_required(login_url='adminLogin')
def updateCustomer(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('adminViewCustomer')
    return render(request,'adminApp/updateCustomer.html',context=mydict)


@login_required(login_url='adminLogin')
def adminAddCustomer(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/adminViewCustomer')
    return render(request,'adminApp/adminAddCustomer.html',context=mydict)


@login_required(login_url='adminLogin')
def adminViewCustomerEnquiry(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'adminApp/adminViewCustomerEnquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminLogin')
def adminViewCustomerInvoice(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'adminApp/adminViewCustomerInvoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminLogin')
def adminMechanic(request):
    return render(request,'adminApp/adminMechanic.html')

@login_required(login_url='adminlogin')
def adminViewMechanic(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'adminApp/adminViewMechanic.html',{'mechanics':mechanics})

@login_required(login_url='adminLogin')
def adminApproveMechanic(request):
    mechanics=models.Mechanic.objects.all().filter(status=False)
    return render(request,'adminApp/adminApproveMechanic.html',{'mechanics':mechanics})

@login_required(login_url='adminLogin')
def approveMechanic(request,pk):
    mechanicSalary=forms.MechanicSalaryForm()
    if request.method=='POST':
        mechanicSalary=forms.MechanicSalaryForm(request.POST)
        if mechanicSalary.is_valid():
            mechanic=models.Mechanic.objects.get(id=pk)
            mechanic.salary=mechanicSalary.cleaned_data['salary']
            mechanic.status=True
            mechanic.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/adminApproveMechanic')
    return render(request,'adminApp/adminApproveMechanicDetails.html',{'mechanicSalary':mechanicSalary})


@login_required(login_url='adminLogin')
def deleteMechanic(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('adminApproveMechanic')


@login_required(login_url='adminLogin')
def adminAddMechanic(request):
    userForm=forms.MechanicUserForm()
    mechanicForm=forms.MechanicForm()
    mechanicSalary=forms.MechanicSalaryForm()
    mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanicSalary':mechanicSalary}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES)
        mechanicSalary=forms.MechanicSalaryForm(request.POST)
        if userForm.is_valid() and mechanicForm.is_valid() and mechanicSalary.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic=mechanicForm.save(commit=False)
            mechanic.user=user
            mechanic.status=True
            mechanic.salary=mechanicSalary.cleaned_data['salary']
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
            return HttpResponseRedirect('adminViewMechanic')
        else:
            print('problem in form')
    return render(request,'adminApp/adminAddMechanic.html',context=mydict)


@login_required(login_url='adminLogin')
def adminViewMechanic(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'adminApp/adminViewMechanic.html',{'mechanics':mechanics})


@login_required(login_url='adminLogin')
def deleteMechanic(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('adminViewMechanic')


@login_required(login_url='adminLogin')
def updateMechanic(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    userForm=forms.MechanicUserForm(instance=user)
    mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('adminViewMechanic')
    return render(request,'adminApp/updateMechanic.html',context=mydict)

@login_required(login_url='adminLogin')
def adminViewMechanicSalary(request):
    mechanics=models.Mechanic.objects.all()
    return render(request,'adminApp/adminViewMechanicSalary.html',{'mechanics':mechanics})

@login_required(login_url='adminLogin')
def updateSalary(request,pk):
    mechanicSalary=forms.MechanicSalaryForm()
    if request.method=='POST':
        mechanicSalary=forms.MechanicSalaryForm(request.POST)
        if mechanicSalary.is_valid():
            mechanic=models.Mechanic.objects.get(id=pk)
            mechanic.salary=mechanicSalary.cleaned_data['salary']
            mechanic.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/adminViewMechanicSalary')
    return render(request,'adminApp/adminApproveMechanicDetails.html',{'mechanicSalary':mechanicSalary})

@login_required(login_url='adminLogin')
def adminMechanicAttendance(request):
    return render(request, 'adminApp/adminMechanicAttendance.html')


@login_required(login_url='adminLogin')
def adminTakeAttendance(request):
    mechanics = models.Mechanic.objects.all().filter(status=True)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()

                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                print(mechanics[i].id)
                print(int(mechanics[i].id))
                mechanic = models.Mechanic.objects.get(id=int(mechanics[i].id))
                AttendanceModel.mechanic = mechanic
                AttendanceModel.save()
            return redirect('adminViewAttendance')
        else:
            print('form invalid')
    return render(request, 'adminApp/adminTakeAttendance.html', {'mechanics': mechanics, 'aform': aform})

@login_required(login_url='adminLogin')
def adminViewAttendance(request):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.all().filter(date=date)
            mechanicdata = models.Mechanic.objects.all().filter(status=True)
            mylist = zip(attendancedata, mechanicdata)
            return render(request, 'adminApp/adminViewAttendancePage.html', {'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'adminApp/adminViewAttendanceAskDate.html', {'form': form})

@login_required(login_url='adminLogin')
def adminRequest(request):
    return render(request,'adminApp/adminRequest.html')

@login_required(login_url='adminLogin')
def adminViewRequest(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'adminApp/adminViewRequest.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminLogin')
def changeStatus(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/adminViewRequest')
    return render(request,'adminApp/adminApproveRequestDetails.html',{'adminenquiry':adminenquiry})


@login_required(login_url='adminLogin')
def adminDeleteRequest(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('adminViewRequest')



@login_required(login_url='adminLogin')
def adminAddRequest(request):
    enquiry=forms.RequestForm()
    adminenquiry=forms.AdminRequestForm()
    mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
    if request.method=='POST':
        enquiry=forms.RequestForm(request.POST)
        adminenquiry=forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=adminenquiry.cleaned_data['customer']
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status='Approved'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('adminViewRequest')
    return render(request,'adminApp/adminAddRequest.html',context=mydict)

@login_required(login_url='adminLogin')
def adminApproveRequest(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'adminApp/adminApproveRequest.html',{'enquiry':enquiry})

@login_required(login_url='adminLogin')
def approveRequest(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/adminApproveRequest')
    return render(request,'adminApp/adminApproveRequestDetails.html',{'adminenquiry':adminenquiry})

@login_required(login_url='adminlogin')
def adminViewServiceCost(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'adminApp/adminViewServiceCost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def updateCost(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/adminViewServiceCost')
    return render(request,'adminApp/updateCost.html',{'updateCostForm':updateCostForm})

@login_required(login_url='adminLogin')
def adminReport(request):
    reports = models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict = {
        'reports': reports,
    }
    return render(request, 'adminApp/adminReport.html', context=dict)

@login_required(login_url='adminLogin')
def adminFeedback(request):
    feedback = models.Feedback.objects.all().order_by('-id')
    return render(request, 'adminApp/adminFeedback.html', {'feedback': feedback})

def logout(request):
    auth.logout(request)
    return redirect('')