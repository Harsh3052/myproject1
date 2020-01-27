from django.shortcuts import render
from .models import *
from random import *
from HR_Employee.models import emp_leaves
from django.core.mail import send_mail
import re
from datetime import datetime
from datetime import date

# Create your views here.


def index(request):
    total_emp = HR_emp.objects.all().count()
    hid = HR.objects.get(id=request.session['id'])
    leave_info = emp_leaves.objects.filter(emp_hr_lv_status='pending')
    hr = {
        "num_emp": total_emp,
        "hid": hid
    }
    return render(request, "myapp/index.html", {'hr': hr , 'leave_info': leave_info })


def events(request):
    return render(request, "myapp/events.html")


def hr_login_page(request):
    return render(request, "myapp/HR_login.html")


def hr_login_evalute(request):
    try:
        hemail = request.POST['email']
        hpassword = request.POST['password']
        uid = HR.objects.get(email=hemail)
        # data1=HR_emp.objects.all()
        # data=len(data1)
        if uid:
            if uid.password == hpassword:
                request.session['username'] = uid.username
                request.session['id'] = uid.id
                request.session['email'] = uid.email
                request.session['hr_first_name'] = uid.hr_first_name
                total_emp = HR_emp.objects.all().count()    
                print("---------------------------->", total_emp)
                hid = HR.objects.get(id=request.session['id'])
                print("---------------------------->", hid.username)
                hr = {
                    "num_emp": total_emp,
                    "hid": hid
                }
                leave_info = emp_leaves.objects.filter(emp_hr_lv_status='pending')
                return render(request, "myapp/index.html", {'hr': hr , 'leave_info': leave_info})

            else:
                msg = "invalid password"
                return render(request, "myapp/HR_login.html", {'msg': msg})
        else:
            msg = "Invali email address"
            return render(request, "myapp/HR_login.html", {'msg': msg})

    except HR.DoesNotExist:
        msg = "Invalid Email"
        return render(request, "myapp/HR_login.html", {'msg': msg})


def hr_forgot_password(request):
    return render(request, "myapp/hr_forgot_password.html")


def hr_otp(request):
    return render(request, "myapp/hr_otp.html")


def hr_forgot_evalute(request):
    try:
        hemail = request.POST['email']
        # request.session['email_otp'] = hemail
        uid = HR.objects.get(email=hemail)
        print("----------------> uid ", uid)
        otp = randint(1111, 9999)
        uid.otp = otp
        uid.save()
        subject = "OTP"
        msg = str(otp)
        send_mail(subject, msg, 'anjali.20.learn@gmail.com', [hemail])
        return render(request, "myapp/hr_otp.html", {'uid': uid, 'email': hemail})

    except:
        msg = "Invalid email address"
        return render(request, "myapp/hr_forgot_password.html", {'msg': msg})


def hr_otp_evalute(request):
    try:
        hemail = request.POST['email']
        #hemail = request.session. get('email_otp', 'red')
        otp1 = request.POST['otp1']
        otp2 = request.POST['otp2']
        otp3 = request.POST['otp3']
        otp4 = request.POST['otp4']
        otp = otp1+otp2+otp3+otp4
        print("--------------->", otp)
        print("---------------->",)
        uid = HR.objects.get(email=hemail)
        if uid:
            if str(uid.otp) == otp:
                return render(request, "myapp/hr_new_password.html", {'email': hemail})
            else:
                msg = "Invalid OPT"
                return render(request, "myapp/hr_otp.html", {'msg': msg, 'email': hemail})
        else:
            msg = "Invalid OPT"
            return render(request, "myapp/hr_opt.html", {'msg': msg, 'email': hemail})
    except:
        msg = "Invalid OPT"
        return render(request, "myapp/hr_opt.html", {'msg': msg, 'email': hemail})


def resend_otp(request):
    hemail = request.POST['email']
    otp = randint(1111, 9999)
    subject = "OTP"
    msg = str(otp)

    uid = HR.objects.get(email=hemail)
    uid.otp = otp
    uid.save()
    send_mail(subject, msg, 'anjali.20.learn@gmail.com', [hemail])

    if send_mail:
        msg = "OTP Send Successfully"
        return render(request, "myapp/hr_otp.html", {'msg2': msg, 'email': hemail})
    else:
        msg = "OTP Send Unsccessfully"
        return render(request, "myapp/hr_otp.html", {'msg3': msg, 'email': hemail})


def hr_new_password(request):
    return render(request, "myapp/hr_new_password.html")


def hr_new_password_evaluate(request):
    email = request.POST['password']
    password = request.POST['newpassword']
    repassword = request.POST['repassword']

    print("---------------------->", email)
    print("---------------------->", password)
    print("---------------------->", repassword)

    uid = HR.objects.get(email=email)
    if uid:
        if password == repassword:
            if password == uid.password:
                msg = "Repeat Password!"
                return render(request, "myapp/hr_new_password.html", {'msg': msg, 'email': email})
            else:
                uid.password = password
                uid.save()
                msg2 = "Change Password Successfully"
                return render(request, "myapp/HR_login.html", {'msg2': msg2, 'email': email})
        else:
            msg = "Password Not Match"
            return render(request, "myapp/hr_new_password.html", {'msg': msg, 'email': email})
    else:
        msg = "Password Not Match"
        return render(request, "myapp/hr_new_password.html", {'msg': msg, 'email': email})

    # return render(request,"myapp/HR_login.html")


def hr_logout(request):
    del request.session['username']
    del request.session['id']
    del request.session['email']
    return render(request, "myapp/HR_login.html")


def hr_employees(request):
    data = HR_emp.objects.all()
    return render(request, "myapp/hr_employees.html", {'data': data})


def hr_emp_add(request):
    return render(request, "myapp/hr_emp_add.html")


def hr_employees_evolution(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    phone = request.POST["phone"]
    company = request.POST["company"]
    department = request.POST["department"]
    designation = request.POST["designation"]

    uid = HR_emp.objects.filter(email=email)
    uid2 = HR_emp.objects.filter(username=username)
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "phone": phone,
        "company": company,
        "department": department,
        "designation": designation,
        "msg": "",

    }
    if uid:
        data["msg"] = "Email Aready Exist !!"
        return render(request, "myapp/hr_emp_add.html", {'data': data})
    elif uid2:
        data["msg"] = "Username Aready Exist !!"
        return render(request, "myapp/hr_emp_add.html", {'data': data})
    else:
        if isinstance(phone, str) == True and len(phone) == 10:
            print("------------------->phone: ", phone)
            insert = HR_emp.objects.create(first_name=first_name, last_name=last_name, username=username, email=email,
            password=password, phone=phone, company=company, department=department, designation=designation)
            msg2 = "Employee Successfully Add!!"
            data = HR_emp.objects.all()
            return render(request, "myapp/hr_employees.html", {'msg2': msg2, 'data': data})
        else:
            data["msg"] = "Invalid Number !!"
            return render(request, "myapp/hr_emp_add.html", {'data': data})


def profile(request):
    return render(request, "myapp/profile.html")


def profile_evolution(request, pk=None):
    # data=HR_emp.objects.all().value('username')
    emp = HR_emp.objects.get(id=pk)
    print("------------> uid ", emp)
    return render(request, "myapp/profile.html", {'emp': emp})


def search_ev(request):
    e_name = request.POST['emp_name']
    print("EMP_NAME:==============================================>", e_name)
    emp_data = HR_emp.objects.filter(first_name=e_name)
    print("emp_data:============================================>", emp_data)
    return render(request, "myapp/hr_employees.html", {'emp_data': emp_data})


def emp_list(request):
    data = HR_emp.objects.all()
    return render(request, "myapp/emp_list.html", {'data': data})


def search_ev_list(request):
    if str(request.POST.get('emp_id')) and request.POST.get('emp_name'):
        emp_name = request.POST['emp_name']
        emp_id = request.POST['emp_id']
        data = HR_emp.objects.filter(id=emp_id, first_name=emp_name)
        return render(request, "myapp/emp_list.html", {'emp_data': data})
    else:
        try:
            if not request.POST['emp_id'] and not request.POST['emp_name']:
                data = HR_emp.objects.all()
                print("-----------------------==================Else>")
                return render(request, "myapp/emp_list.html", {'emp_data': data})
            elif not request.POST['emp_id'] and request.POST['emp_name']:
                emp_name = request.POST['emp_name']
                data = HR_emp.objects.filter(first_name=emp_name)
                return render(request, "myapp/emp_list.html", {'emp_data': data})
            elif request.POST['emp_id'] and not request.POST['emp_name']:
                emp_id = request.POST['emp_id']
                data = HR_emp.objects.filter(id=emp_id)
                return render(request, "myapp/emp_list.html", {'emp_data': data})

        except:
            data = HR_emp.objects.all()
            print("-----------------------==================Exception>")
            return render(request, "myapp/emp_list.html", {'emp_data': data})


def edit_profile(request, pk=None):
    # data=HR_emp.objects.all().value('username')
    emp = HR_emp.objects.get(id=pk)
    print("------------> uid ", emp)
    return render(request, "myapp/edit_profile.html", {'emp': emp})


def update_emp_ev(request, pk=None):
    id = request.POST['id']
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    phone = request.POST["phone"]
    company = request.POST["company"]
    department = request.POST["department"]
    designation = request.POST["designation"]
    uid = HR_emp.objects.get(id=id)

    if uid:
        uid.first_name = first_name
        uid.last_name = last_name
        uid.username = username
        uid.email = email
        uid.password = password
        uid.phone = phone
        uid.company = company
        uid.department = department
        uid.designation = designation
        uid.save()
        msg2 = " EDIT Employee Successfully!!"
        data = HR_emp.objects.all()
        return render(request, "myapp/hr_employees.html", {'msg2': msg2, 'data': data})


def delete_emp(request, pk=None):
    # data=HR_emp.objects.all().value('username')
    emp = HR_emp.objects.get(id=pk)
    print("------------> uid ", emp)

    emp.delete()
    msg2 = " DELETE Employee Successfully!!"
    data = HR_emp.objects.all()
    return render(request, "myapp/hr_employees.html", {'msg2': msg2, 'data': data})


def hr_profile(request):
    data = HR.objects.all()
    return render(request, "myapp/hr_profile.html", {'data': data})


def hr_form(request):
    return render(request, "myapp/hr_form.html")


def hr_form_ev(request, pk=None):
    hr_info = HR.objects.get(id=pk)
    print("------------> uid ", hr_info)
    return render(request, "myapp/hr_form.html", {'hr_info': hr_info})


def update_hr_profile(request):
    if "pic" in request.FILES:
        pic = request.FILES['pic']
        id = request.POST['id']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        uid = HR.objects.get(id=id)
        if uid:
            uid.profile_pic = pic
            uid.hr_first_name = fname
            uid.hr_last_name = lname
            uid.email = email
            uid.phone = phone
            uid.save()
            msg2 = " Edit HR Successfully!!"
            data = HR.objects.all()
            return render(request, "myapp/hr_profile.html", {'msg2': msg2, 'data': data})
    else:
        try:
            id = request.POST['id']
            # pic=request.FILES['pic']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            phone = request.POST['phone']
            uid = HR.objects.get(id=id)
            if uid:
                # uid.profile_pic=pic
                uid.hr_first_name = fname
                uid.hr_last_name = lname
                uid.email = email
                uid.phone = phone
                uid.save()
                msg2 = " Edit HR Successfully!!"
                data = HR.objects.all()
                return render(request, "myapp/hr_profile.html", {'msg2': msg2, 'data': data})
        except:
            msg2 = " Edit HR Successfully!!"
            data = HR.objects.all()
            return render(request, "myapp/hr_profile.html", {'msg2': msg2, 'data': data})


def hr_leaves(request):
    total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
    approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
    declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
    pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
    totals={
        "total_pending": total_pending,
        "approved":approved,
        "declined":declined,
        "pending":pending
    }
    leave_info = HR_leave.objects.filter(hr_lv_status="pending")
    return render(request, "myapp/hr_leaves.html", {'leave_info': leave_info , 'totals':totals})

def hr_add_leaves(request):
    return render(request, "myapp/hr_add_leaves.html")


def hr_leaves_ev(request):
    leave_type = request.POST["leave_type"]
    s1 = request.POST["date_start"]
    print("DATE=======================================>", s1)
    dt_obj = datetime.strptime(s1, '%d/%m/%Y')
    date_start = datetime.strftime(dt_obj, '%Y-%m-%d ')
    s2 = request.POST["date_end"]
    dt_obj1 = datetime.strptime(s2, '%d/%m/%Y')
    date_end = datetime.strftime(dt_obj1, '%Y-%m-%d ')
    day = abs(dt_obj1-dt_obj)
    print("DAYS===========================>", day.days)
    leave_reason = request.POST["leave_reason"]
    no_day = day.days
    print("DATE=======================================>", date_start)
    hr_nm = request.session['hr_first_name']
    reason = {
        "leave_reason": leave_reason,
        "msg": "",
    }
    if dt_obj.date() < date.today():
        reason["msg"] = "Start date cannot be before the current date."
        return render(request, "myapp/hr_add_leaves.html", {'reason': reason})
    elif dt_obj.date() > dt_obj1.date():
        reason["msg"] = "End date cannot be before start date."
        return render(request, "myapp/hr_add_leaves.html", {'reason': reason})
    else:
        insert = HR_leave.objects.create(leave_type=leave_type, date_start=date_start,
        date_end=date_end, leave_reason=leave_reason, no_day=no_day, hr_nm=hr_nm)
        msg2 = " Leave Add Successfully"
        leave_info = HR_leave.objects.filter(hr_lv_status='pending')
        # hrid=HR.objects.get(id=request.session['id'])
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info, 'totals':totals})

def delete_hr_leave(request, pk=None):
    hr_lv_info = HR_leave.objects.get(id=pk)
    if hr_lv_info.hr_nm == request.session['hr_first_name'] and hr_lv_info.hr_lv_status == "pending":
        HR_leave.objects.filter(id=pk).delete()
        msg2="Delete Leave Successfully"
        leave_info = HR_leave.objects.filter(hr_lv_status="pending")
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info , 'totals':totals})
    else :
        msg2="Can Not Delete This User"
        leave_info = HR_leave.objects.filter(hr_lv_status="pending")
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info , 'totals':totals })

def edit_hr_leave(request , pk=None):
    hr_lv_info = HR_leave.objects.get(id=pk)
    print("========================================>HR_LEAVE_INFO",hr_lv_info.hr_nm)
    print("========================================>Session_ID",request.session['hr_first_name'])
    if hr_lv_info.hr_nm == request.session['hr_first_name'] and hr_lv_info.hr_lv_status == "pending":
        return render(request, "myapp/edit_hr_leave.html", {'hr_lv_info': hr_lv_info })
    else :
        msg2="Can Not Edit This User"
        leave_info = HR_leave.objects.filter(hr_lv_status="pending")
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info , 'totals':totals})
    
def edit_hr_leave_ev(request):
    id = request.POST['id']
    # pic=request.FILES['pic']
    leave_type = request.POST['leave_type']
    s1 = request.POST['date_start']
    dt_obj = datetime.strptime(s1, '%d/%m/%Y')
    date_start = datetime.strftime(dt_obj, '%Y-%m-%d ')

    s2 = request.POST['date_end']
    dt_obj1 = datetime.strptime(s2, '%d/%m/%Y')
    date_end = datetime.strftime(dt_obj1, '%Y-%m-%d ')
    
    day = abs(dt_obj1-dt_obj)
    no_day = day.days
    leave_reason = request.POST['leave_reason']

    if dt_obj.date() < date.today():
        msg = "Start date cannot be before the current date."
        hr_lv_info = HR_leave.objects.get(id=id)
        return render(request, "myapp/edit_hr_leave.html", {'hr_lv_info':hr_lv_info , 'msg': msg  })
    elif dt_obj.date() > dt_obj1.date():
        msg = "End date cannot be before start date."
        hr_lv_info = HR_leave.objects.get(id=id)
        return render(request,"myapp/edit_hr_leave.html", {'hr_lv_info': hr_lv_info , 'msg': msg  })

    uid = HR_leave.objects.get(id=id)
    if uid:
        # uid.profile_pic=pic
        uid.leave_type = leave_type
        uid.date_start = date_start
        uid.date_end = date_end
        uid.leave_reason =leave_reason
        uid.no_day=no_day
        uid.save()
        msg2 = " Edit Leave Successfully!!"
        leave_info = HR_leave.objects.filter(hr_lv_status="pending")
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info , 'totals':totals})


def hr_status(request , pk=None):
    hr_st_info = HR_leave.objects.get(id=pk)
    if hr_st_info.hr_nm != request.session['hr_first_name'] and hr_st_info.hr_lv_status == "pending" :
        return render(request, "myapp/hr_status.html", {'hr_st_info': hr_st_info})
    else :
        msg2="Can Not Change Status"
        leave_info = HR_leave.objects.filter(hr_lv_status="pending")
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info , 'totals':totals})

def hr_status_ev(request):
    id = request.POST['id']
    leave_status=request.POST['leave_status']
    uid = HR_leave.objects.get(id=id)
    if uid:
        uid.hr_lv_status= leave_status
        uid.save()
        msg2 = " Edit Status Successfully!!"
        leave_info = HR_leave.objects.filter(hr_lv_status="pending")
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'msg2': msg2, 'leave_info': leave_info ,'totals':totals})

def search_leave(request):
    if request.POST.get('status_type'):
        status = request.POST['status_type']
        leave_data = HR_leave.objects.filter(hr_lv_status=status)
        total_pending=HR_leave.objects.filter(hr_lv_status="pending").count()
        approved=HR_leave.objects.filter(hr_lv_status="Approve",hr_nm=request.session['hr_first_name']).count()
        declined=HR_leave.objects.filter(hr_lv_status="Decline",hr_nm=request.session['hr_first_name']).count()
        pending=HR_leave.objects.filter(hr_lv_status="pending",hr_nm=request.session['hr_first_name']).count()
        totals={
            "total_pending": total_pending,
            "approved":approved,
            "declined":declined,
            "pending":pending
        }
        return render(request, "myapp/hr_leaves.html", {'leave_data': leave_data , 'totals':totals})
    

def emp_status(request , pk=None):
    emp_st_info = emp_leaves.objects.get(id=pk)
    if  emp_st_info.emp_hr_lv_status == "pending" :
        return render(request, "myapp/emp_status.html", {'emp_st_info': emp_st_info})
    else :
        msg2="Can Not Change Status"
        leave_info = emp_leaves.objects.filter(emp_hr_lv_status='pending')
        
        return render(request, "myapp/index.html", {'msg2': msg2, 'leave_info': leave_info })

def emp_status_ev(request):
    id = request.POST['id']
    emp_leave_status=request.POST['emp_leave_status']
    uid = emp_leaves.objects.get(id=id)
    if uid:
        uid.emp_hr_lv_status= emp_leave_status
        uid.save()
        msg2 = " Edit Status Successfully!!"
        leave_info = emp_leaves.objects.filter(emp_hr_lv_status='pending')
        
        return render(request, "myapp/index.html", {'msg2': msg2, 'leave_info': leave_info })

def emp_search_leave(request):
    if request.POST.get('status_type'):
        status = request.POST['status_type']
        leave_data = emp_leaves.objects.filter(emp_hr_lv_status=status)
        
        return render(request, "myapp/index.html", {'leave_data': leave_data })

def email_leave(request):
    return render(request, "myapp/email_leave.html")