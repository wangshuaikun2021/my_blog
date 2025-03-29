# -*- coding:utf-8 -*-
# @FileName  :urls.py
# @Time      :2025/3/27 19:10
# @Author    :wsk

from django.urls import path
from . import views

app_name = "myauth"

urlpatterns = [
    path("sign_in/", views.sign_in, name="sign_in"),
    path("log_out/", views.log_out, name="log_out"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("captcha/", views.send_email_captcha, name="send_email_captcha"),
]
