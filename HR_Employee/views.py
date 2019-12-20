from django.shortcuts import render
from .models import *
from myapp.models import HR_emp
from random import *
from django.core.mail import send_mail
import re

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
    try:
        hemail=request.POST['email']
        # request.session['email_otp'] = hemail
        uid=HR_emp.objects.get(email=hemail)
        print("----------------> uid ",uid)
        if uid:        
            otp=randint(1111,9999)
            uid.otp=otp
            uid.save()
            subject="OTP"
            msg=str(otp)
            send_mail(subject,msg, 'anjali.20.learn@gmail.com',[hemail])
            return render(request,"HR_Employee/emp_otp.html",{'uid':uid, 'email': hemail})
        
    except :
        msg="Invalid email address"
        return render(request,"HR_Employee/emp_forgot_password.html",{'msg':msg})
    
def emp_otp(request):
    return render(request,"HR_Employee/emp_otp.html")

def emp_new_password(request):
    return render(request,"HR_Employee/emp_new_password.html")

def emp_otp_ev(request):
    try:
        hemail=request.POST['email']
        #hemail = request.session. get('email_otp', 'red')
        otp1=request.POST['otp1']
        otp2=request.POST['otp2']
        otp3=request.POST['otp3']
        otp4=request.POST['otp4']
        otp=otp1+otp2+otp3+otp4
        print("--------------->",otp)
        print("---------------->",)
        uid=HR_emp.objects.get(email=hemail)
        if uid:
            if str(uid.otp)==otp:
                return render(request,"HR_Employee/emp_new_password.html",{'email':hemail})
            else:   
                msg="Invalid OPT"
                return render(request,"HR_Employee/emp_otp.html",{'msg':msg ,'email':hemail})
        else:
            msg="Invalid OPT"
            return render(request,"HR_Employee/emp_opt.html",{'msg':msg ,'email':hemail})
    except :
        msg="Invalid OPT"
        return render(request,"HR_Employee/emp_opt.html",{'msg':msg ,'email':hemail})

def emp_resend_otp(request):
    hemail=request.POST['email']
    otp=randint(1111,9999)
    subject="OTP"
    msg=str(otp)
    
    uid=HR_emp.objects.get(email=hemail)
    uid.otp=otp
    uid.save()
    send_mail(subject,msg, 'anjali.20.learn@gmail.com',[hemail])
    
    if send_mail:
        msg="OTP Send Successfully"
        return render(request,"HR_Employee/emp_otp.html",{'msg2':msg ,'email':hemail})
    else:
        msg="OTP Send Unsccessfully"
        return render(request,"HR_Employee/emp_otp.html",{'msg3':msg ,'email':hemail})




def emp_new_password_ev(request):
    email=request.POST['password']
    password=request.POST['newpassword']
    repassword=request.POST['repassword']

    print("---------------------->",email)
    print("---------------------->",password)
    print("---------------------->",repassword)
    
    uid=HR_emp.objects.get(email=email)
    if uid:
        if password==repassword:
            if password==uid.password:
                msg="Repeat Password!"
                return render(request,"HR_Employee/emp_new_password.html",{'msg':msg ,'email':email})
            else:
                uid.password=password
                uid.save()
                msg2="Change Password Successfully"
                return render(request,"HR_Employee/emp_login.html",{'msg2':msg2,'email':email})
        else:
            msg="Password Not Match"
            return render(request,"HR_Employee/emp_new_password.html",{'msg':msg,'email':email})
    else:
        msg="Password Not Match"
        return render(request,"HR_Employee/emp_new_password.html",{'msg':msg,'email':email})

def emp_logout(request):
    del request.session['username']
    del request.session['id']
    del request.session['email']
    return render(request,"HR_Employee/emp_login.html")