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
from HR_Employee import views

urlpatterns = [
#  path('', views.index, name='hr_index'),
    path('emp_login/', views.emp_login, name='emp_login'),
    path('emp_index/',views.emp_index, name='emp_index'),
    path('emp_login_evalute/',views.emp_login_evalute,name='emp_login_evalute'),
    path('emp_forgot_password/',views.emp_forgot_password,name='emp_forgot_password'),
    path('emp_forgot_password_ev/',views.emp_forgot_password_ev,name='emp_forgot_password_ev'),
    path('emp_otp/',views.emp_otp, name='emp_otp'),
    path('emp_otp_ev/',views.emp_otp_ev, name='emp_otp_ev'),
    path('emp_resend_otp/',views.emp_resend_otp, name='emp_resend_otp'),
    path('emp_new_password/',views.emp_new_password, name='emp_new_password'),
    path('emp_new_password_ev/',views.emp_new_password_ev, name='emp_new_password_ev'),
    path('emp_logout/',views.emp_logout, name='emp_logout'),
]





