from django.db import models

# Create your models here.
class HR(models.Model):
    username=models.CharField(max_length = 20)
    email=models.EmailField(unique= True)
    password=models.CharField(max_length=50)
    otp = models.IntegerField(default = 459)
    