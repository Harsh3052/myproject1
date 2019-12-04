from django.shortcuts import render
from .models import *
from myapp.models import HR_emp

# Create your views here.
def emp_login(request):
    return render(request,"HR_Employee/emp_login.html")

def emp_login_evalute(request):
    try:
        huser=request.POST['username']
        hpassword=request.POST['password']
        uid=HR_emp.objects.get(username = huser)
        if uid:
            if uid.password==hpassword:
                    request.session['username']=uid.username 
                    request.session['id']=uid.id
                    request.session['email']=uid.email
                    return render(request,"HR_Employee/emp_index.html")
            else:
                    msg="invalid password"
                    return render(request,"HR_Employee/emp_login.html",{'msg':msg})
        else:
                msg="Invali Username"
                return render(request,"HR_Employee/emp_login.html",{'msg':msg})
    except HR_emp.DoesNotExist:
        msg="Invalid Username"
        return render(request,"HR_Employee/emp_login.html",{'msg':msg})

def emp_index(request):
    return render(request,"HR_Employee/emp_index.html")

def emp_forgot_password(request):
    return render(request,"HR_Employee/emp_forgot_password.html")

def emp_forgot_password_ev(request):
    
    return render(request,"HR_Employee/emp_forgot_password.html")