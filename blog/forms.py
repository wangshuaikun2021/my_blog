# -*- coding:utf-8 -*-
# @FileName  :forms.py.py
# @Time      :2025/3/28 2:34
# @Author    :wsk


from django import forms


class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=1, required=True, error_messages={
        "required": "标题不能为空",
        "max_length": "标题不能超过100个字符",
        "min_length": "标题不能少于1个字符"
    })
    content = forms.CharField(required=True, error_messages={
        "required": "内容不能为空"
    })
    category = forms.IntegerField(required=True, error_messages={
        "required": "分类不能为空"
    })
