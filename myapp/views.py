from django.shortcuts import render
from .models import *
from random import *
from django.core.mail import send_mail
import re

# Create your views here.
def index(request):
    return render(request,"myapp/index.html")
    

def events(request):
    return render(request,"myapp/events.html")

def hr_login_page(request):
    return render(request,"myapp/HR_login.html")

def hr_login_evalute(request):
    try:
        hemail=request.POST['email']
        hpassword=request.POST['password']
        uid=HR.objects.get(email=hemail)
        if uid:
            if uid.password==hpassword:
                request.session['username']=uid.username 
                request.session['id']=uid.id
                request.session['email']=uid.email

                return render(request,"myapp/index.html")
                
                
            else:
                msg="invalid password"
                return render(request,"myapp/HR_login.html",{'msg':msg})
        else:
            msg="Invali email address"
            return render(request,"myapp/HR_login.html",{'msg':msg})
            
    except HR.DoesNotExist:
        msg="Invalid Email"
        return render(request,"myapp/HR_login.html",{'msg':msg})

def hr_forgot_password(request):
    return render(request,"myapp/hr_forgot_password.html")

def hr_otp(request):
    return render(request,"myapp/hr_otp.html")

def hr_forgot_evalute(request):
    try:
        hemail=request.POST['email']
        # request.session['email_otp'] = hemail
        uid=HR.objects.get(email=hemail)
        print("----------------> uid ",uid)        
        otp=randint(1111,9999)
        uid.otp=otp
        uid.save()
        subject="OTP"
        msg=str(otp)
        send_mail(subject,msg, 'anjali.20.learn@gmail.com',[hemail])
        return render(request,"myapp/hr_otp.html",{'uid':uid, 'email': hemail})
        
    except :
        msg="Invalid email address"
        return render(request,"myapp/hr_forgot_password.html",{'msg':msg})



def hr_otp_evalute(request):
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
        uid=HR.objects.get(email=hemail)
        if uid:
            if str(uid.otp)==otp:
                return render(request,"myapp/hr_new_password.html",{'email':hemail})
            else:
                msg="Invalid OPT"
                return render(request,"myapp/hr_otp.html",{'msg':msg ,'email':hemail})
        else:
            msg="Invalid OPT"
            return render(request,"myapp/hr_opt.html",{'msg':msg ,'email':hemail})
    except :
        msg="Invalid OPT"
        return render(request,"myapp/hr_opt.html",{'msg':msg ,'email':hemail})

def resend_otp(request):
    hemail=request.POST['email']
    otp=randint(1111,9999)
    subject="OTP"
    msg=str(otp)
    
    uid=HR.objects.get(email=hemail)
    uid.otp=otp
    uid.save()
    send_mail(subject,msg, 'anjali.20.learn@gmail.com',[hemail])
    
    if send_mail:
        msg="OTP Send Successfully"
        return render(request,"myapp/hr_otp.html",{'msg2':msg ,'email':hemail})
    else:
        msg="OTP Send Unsccessfully"
        return render(request,"myapp/hr_otp.html",{'msg3':msg ,'email':hemail})

def hr_new_password(request):
    return render(request,"myapp/hr_new_password.html")


def hr_new_password_evaluate(request):
    email=request.POST['password']
    password=request.POST['newpassword']
    repassword=request.POST['repassword']

    print("---------------------->",email)
    print("---------------------->",password)
    print("---------------------->",repassword)
    
    uid=HR.objects.get(email=email)
    if uid:
        if password==repassword:
            if password==uid.password:
                msg="Repeat Password!"
                return render(request,"myapp/hr_new_password.html",{'msg':msg ,'email':email})
            else:
                uid.password=password
                uid.save()
                msg2="Change Password Successfully"
                return render(request,"myapp/HR_login.html",{'msg2':msg2,'email':email})
        else:
            msg="Password Not Match"
            return render(request,"myapp/hr_new_password.html",{'msg':msg,'email':email})
    else:
        msg="Password Not Match"
        return render(request,"myapp/hr_new_password.html",{'msg':msg,'email':email})
    
    #return render(request,"myapp/HR_login.html")

def hr_employees(request):
    data=HR_emp.objects.all()
    return render(request,"myapp/hr_employees.html",{'data':data})

def hr_emp_add(request):
    return render(request,"myapp/hr_emp_add.html")

def hr_employees_evolution(request):
    first_name=request.POST["first_name"]
    last_name=request.POST["last_name"]
    username=request.POST["username"]
    email= request.POST["email"]
    password = request.POST["password"]
    phone = request.POST["phone"]
    company = request.POST["company"]
    department = request.POST["department"]
    designation = request.POST["designation"]

    uid=HR_emp.objects.filter(email=email)
    uid2=HR_emp.objects.filter(username=username)
    data={
        "first_name":first_name,
        "last_name":last_name,
        "username":username,
        "email":email,
        "phone":phone,
        "company":company,
        "department":department,
        "designation":designation,
        "msg":"",
        
    }
    if uid:
        data["msg"]="Email Aready Exist !!"
        return render(request,"myapp/hr_emp_add.html",{'data': data})
    elif uid2:
        data["msg"]="Username Aready Exist !!"
        return render(request,"myapp/hr_emp_add.html",{'data': data})
    else:
        if len(phone)==10 and isinstance(phone , int):
            print("------------------->phone: ",phone)
            insert=HR_emp.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,password=password,phone=phone,company=company,department=department,designation=designation)    
            msg2="Employee Successfully Add!!"
            data=HR_emp.objects.all()
            return render(request,"myapp/hr_employees.html",{'msg2': msg2 ,'data':data})
        else:
            data["msg"]="Invalid Number !!"
            return render(request,"myapp/hr_emp_add.html",{'data': data})
        
def profile(request):
    return render(request,"myapp/profile.html") 


