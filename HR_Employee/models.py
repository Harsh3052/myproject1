# from django import form
from django.db import models
from django import forms
from myapp.models import HR_emp
# Create your models here.

class emp_leaves(models.Model):
    emp_leave_type = models.CharField(max_length=30)
    emp_date_start = models.CharField(max_length=30)  
    emp_date_end = models.CharField(max_length = 20)
    emp_leave_reason = models.EmailField(max_length=50)
    emp_no_day = models.CharField(max_length=20)
    emp_hr_nm=models.CharField(max_length=50,default='')
    emp_hr_lv_status=models.CharField(max_length=50,default='pending')
    emp_id=models.CharField(max_length=50,default='')
    
class emp_atd(models.Model):
    emp_id = models.ForeignKey(HR_emp , on_delete=''  ,default='')
    td_date = models.CharField(max_length=50)
    pi_time = models.CharField(max_length=50)
    po_time = models.CharField(max_length=50)
    total_time = models.CharField(max_length=50)
    over_time = models.CharField(max_length=50)
    punch_type = models.CharField(max_length=50,default='')
