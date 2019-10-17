"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='hr_index'),
    path('HR_login/', views.hr_login_page, name='HR_login'),
    path('HR_login_evalute/',views.hr_login_evalute,name='hr_login_evalute'),
    path('HR_Forgot_password/',views.hr_forgot_password,name="hr_forgot_password"),
    path('HR_OPT/',views.hr_otp, name='hr_otp'),
    path('HR_forgot_evalute/',views.hr_forgot_evalute,name='hr_forgot_evalute'),
    path('HR_otp_evalute/',views.hr_otp_evalute,name='hr_otp_evalute'),
    path('HR_new_password/',views.hr_new_password,name='hr_new_password'),
    path('HR_new_password_evalute/',views.hr_new_password_evaluate,name='hr_new_password_evaluate'),
    
]
