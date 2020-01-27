from django import forms
from django.db import models


# Create your models here.
class HR(models.Model):
    username=models.CharField(max_length = 20)
    email=models.EmailField(unique= True)
    password=models.CharField(max_length=50)
    otp = models.IntegerField(default = 459)
    profile_pic=models.FileField(upload_to='myapp/assets/img/',default='emp.jpg',blank=True)
    hr_first_name=models.CharField(max_length=30)
    hr_last_name=models.CharField(max_length=30)
    phone = models.CharField(max_length = 10)


class HR_emp(models.Model):
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)  
    username = models.CharField(max_length = 20)
    email= models.EmailField(unique= True)
    password = models.CharField(max_length=50)
    joiningdate = models.DateTimeField(auto_now_add=True,blank=False)
    phone = models.CharField(max_length = 10)
    company = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    profile_pic=models.FileField(upload_to='myapp/assets/img/',default='emp.jpg')
    otp = models.IntegerField(default = 459)


class HR_leave(models.Model):
    hr_id = models.ForeignKey(HR ,on_delete=models.CASCADE ,default='')
    leave_type = models.CharField(max_length=30)
    date_start = models.CharField(max_length=30)  
    date_end = models.CharField(max_length = 20)
    leave_reason = models.EmailField(max_length=50)
    no_day = models.CharField(max_length=20)
    hr_nm=models.CharField(max_length=50,default='')
    hr_lv_status=models.CharField(max_length=50,default='pending')