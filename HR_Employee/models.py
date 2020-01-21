# from django import form
from django.db import models
from django import forms
# Create your models here.

class emp(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField(unique= True)
    password=models.CharField(max_length=50)
    otp = models.IntegerField(default = 459)

class emp_leave(models.Model):
    emp_leave_type = models.CharField(max_length=30)
    emp_date_start = models.CharField(max_length=30)  
    emp_date_end = models.CharField(max_length = 20)
    emp_leave_reason = models.EmailField(max_length=50)
    emp_no_day = models.CharField(max_length=20)
    emp_hr_nm=models.CharField(max_length=50,default='')
    emp_hr_lv_status=models.CharField(max_length=50,default='pending')