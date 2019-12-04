# from django import form
from django.db import models
from django import forms
# Create your models here.

class emp(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField(unique= True)
    password=models.CharField(max_length=50)
    otp = models.IntegerField(default = 459)