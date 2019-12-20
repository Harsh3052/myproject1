from django.shortcuts import render
from .models import *
from random import *
from django.core.mail import send_mail
import re

# Create your views here.
def index(request):
    data1=HR_emp.objects.all()
    data=len(data1)
    return render(request,"myapp/index.html",{'data':data})
    

def events(request):
    return render(request,"myapp/events.html")

def hr_login_page(request):
    return render(request,"myapp/HR_login.html")

def hr_login_evalute(request):
    try:
        hemail=request.POST['email']
        hpassword=request.POST['password']
        uid=HR.objects.get(email=hemail)
        data1=HR_emp.objects.all()
        data=len(data1)
        if uid:
            if uid.password==hpassword:
                request.session['username']=uid.username 
                request.session['id']=uid.id
                request.session['email']=uid.email
                return render(request,"myapp/index.html",{'data':data})
                
                
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
        if  isinstance(phone , str)== True and len(phone)==10 :
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

def profile_evolution(request,pk=None):
    # data=HR_emp.objects.all().value('username')
    emp=HR_emp.objects.get(id=pk)
    print("------------> uid ",emp)
    return render(request,"myapp/profile.html",{'emp':emp})

def search_ev(request):
    e_name=request.POST['emp_name']
    print("EMP_NAME:==============================================>",e_name)
    emp_data=HR_emp.objects.filter(first_name=e_name)
    print("emp_data:============================================>",emp_data)
    return render(request,"myapp/hr_employees.html",{'emp_data': emp_data}) 

def emp_list(request):
    data=HR_emp.objects.all()
    return render(request,"myapp/emp_list.html",{'data':data}) 

def search_ev_list(request):
    e_name=request.POST['emp_name']
    e_id=request.POST['emp_id']
    print("EMP_NAME:==============================================>",e_name)
    data=HR_emp.objects.filter(first_name=e_name,id=e_id)
    print("emp_data:============================================>",data)
    return render(request,"myapp/emp_list.html",{'emp_data': data}) 


def edit_profile(request,pk=None):
    # data=HR_emp.objects.all().value('username')
    emp=HR_emp.objects.get(id=pk)
    print("------------> uid ",emp)
    return render(request,"myapp/edit_profile.html",{'emp':emp})

def update_emp_ev(request,pk=None):
    id=request.POST['id']
    first_name=request.POST["first_name"]
    last_name=request.POST["last_name"]
    username=request.POST["username"]
    email= request.POST["email"]
    password = request.POST["password"]
    phone = request.POST["phone"]
    company = request.POST["company"]
    department = request.POST["department"]
    designation = request.POST["designation"]
    uid=HR_emp.objects.get(id=id)

    if uid:
        uid.first_name=first_name
        uid.last_name=last_name
        uid.username=username
        uid.email=email
        uid.password=password
        uid.phone=phone
        uid.company=company
        uid.department=department
        uid.designation=designation
        uid.save()
        msg2=" EDIT Employee Successfully!!"
        data=HR_emp.objects.all()
        return render(request,"myapp/hr_employees.html",{'msg2': msg2,'data': data})

def delete_emp(request,pk=None):
    # data=HR_emp.objects.all().value('username')
    emp=HR_emp.objects.get(id=pk)
    print("------------> uid ",emp)

    emp.delete()
    msg2=" DELETE Employee Successfully!!"
    data=HR_emp.objects.all()
    return render(request,"myapp/hr_employees.html",{'msg2': msg2,'data': data})

def hr_profile(request):
    data=HR.objects.all()
    return render(request,"myapp/hr_profile.html",{'data' : data})

def hr_form(request):
    return render(request,"myapp/hr_form.html")

def hr_form_ev(request,pk=None):
    hr_info=HR.objects.get(id=pk)
    print("------------> uid ",hr_info)
    return render(request,"myapp/hr_form.html",{'hr_info':hr_info})

def update_hr_profile(request):
    id=request.POST['id']
    pic=request.FILES['pic']
    fname=request.POST['fname']
    lname=request.POST['lname']
    email=request.POST['email']
    phone=request.POST['phone']
    uid=HR.objects.get(id=id)
    if uid:
        uid.profile_pic=pic
        uid.hr_first_name=fname
        uid.hr_last_name=lname
        uid.email=email
        uid.phone=phone
        uid.save()
        msg2=" Edit HR Successfully!!"
        data=HR.objects.all()
        return render(request,"myapp/hr_profile.html",{'msg2': msg2 , 'data' : data})
