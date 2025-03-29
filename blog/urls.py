# -*- coding:utf-8 -*-
# @FileName  :urls.py.py
# @Time      :2025/3/27 16:32
# @Author    :wsk
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("blog/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("blog/pub/", views.pub_blog, name="pub_blog"),
    path("blog/submit_comment/", views.submit_comment, name="submit_comment"),
    path("search/", views.search, name="search"),
]
