from django import forms
from django.db import models


# Create your models here.
class HR(models.Model):
    username=models.CharField(max_length = 20)
    email=models.EmailField(unique= True)
    password=models.CharField(max_length=50)
    otp = models.IntegerField(default = 459)
    profile_pic=models.FileField(upload_to='myapp/assets/img/',default='emp.jpg')
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
