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
    path('index', views.index, name='hr_index'),
    path('HR_login/', views.hr_login_page, name='HR_login'),
    path('HR_login_evalute/',views.hr_login_evalute,name='hr_login_evalute'),
    path('HR_Forgot_password/',views.hr_forgot_password,name="hr_forgot_password"),
    path('HR_OPT/',views.hr_otp, name='hr_otp'),
    path('HR_forgot_evalute/',views.hr_forgot_evalute,name='hr_forgot_evalute'),
    path('HR_otp_evalute/',views.hr_otp_evalute,name='hr_otp_evalute'),
    path('HR_Resend_otp/',views.resend_otp,name='resend_otp'),
    path('HR_new_password/',views.hr_new_password,name='hr_new_password'),
    path('HR_new_password_evalute/',views.hr_new_password_evaluate,name='hr_new_password_evaluate'),
    path('hr_logout/',views.hr_logout,name='hr_logout'),
    path('HR_cal/',views.events, name='hr_cal'),
    path('HR_employees/',views.hr_employees,name='hr_employees'),
    path('HR_emp_add/',views.hr_emp_add,name='hr_emp_add'),
    path('hr_employees_evolution/',views.hr_employees_evolution,name='hr_employees_evolution'),
    path('profile/',views.profile,name='profile'),
    path(r'^profile-evolution/(?P<pk>\d+)/$', views.profile_evolution, name='profile_evolution'),
    path('search_ev/',views.search_ev,name='search_ev'),
    path('emp_list/',views.emp_list,name='emp_list'),
    path('search_ev_list/',views.search_ev_list,name='search_ev_list'),
    path(r'^edit-profile/(?P<pk>\d+)/$', views.edit_profile, name='edit_profile'),
    path('update_emp_ev/',views.update_emp_ev,name='update_emp_ev'),
    path(r'^delete_emp/(?P<pk>\d+)/$', views.delete_emp, name='delete_emp'),
    path('hr_profile/',views.hr_profile,name='hr_profile'),
    path('hr_form/',views.hr_form,name='hr_form'),
    path(r'^hr_form_ev/(?P<pk>\d+)/$',views.hr_form_ev, name='hr_form_ev'),
    path('update_hr_profile/',views.update_hr_profile,name="update_hr_profile"),
    path('hr_leaves/',views.hr_leaves,name="hr_leaves"),
    path('hr_add_leaves/',views.hr_add_leaves,name="hr_add_leaves"),
    path('hr_leaves_ev/',views.hr_leaves_ev,name="hr_leaves_ev"),
    path(r'^delete_hr_leave/(?P<pk>\d+)/$', views.delete_hr_leave, name='delete_hr_leave'),
    path('edit_hr_leave_ev/',views.edit_hr_leave_ev,name='edit_hr_leave_ev'),
    path(r'^edit_hr_leave/(?P<pk>\d+)/$', views.edit_hr_leave, name='edit_hr_leave'),
    path(r'^hr_status/(?P<pk>\d+)/$', views.hr_status, name='hr_status'),
    ]

