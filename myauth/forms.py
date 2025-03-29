from django import forms
from django.contrib.auth import get_user_model

from .models import Captcha
User = get_user_model()


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, required=True, error_messages={
        "required": "用户名不能为空",
        "max_length": "用户名不能超过20个字符",
        "min_length": "用户名不能少于2个字符"
    })
    email = forms.EmailField(required=True, error_messages={
        "required": "邮箱不能为空",
        "invalid": "邮箱格式不正确"
    })
    captcha = forms.CharField(max_length=4, min_length=4, required=True, error_messages={
        "required": "验证码不能为空",
        "max_length": "验证码必须是4个字符",
        "min_length": "验证码必须是4个字符"
    })
    pwd = forms.CharField(max_length=20, min_length=6, required=True, error_messages={
        "required": "密码不能为空",
        "max_length": "密码不能超过20个字符",
        "min_length": "密码不能少于6个字符"
    })

    def clean_email(self):
        email = self.cleaned_data.get("email")
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("邮箱已经被注册")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get("captcha")
        email = self.cleaned_data.get("email")
        captcha_model = Captcha.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码错误")
        captcha_model.delete()
        return captcha


class LogInForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={
        "required": "邮箱不能为空",
        "invalid": "邮箱格式不正确"
    })
    pwd = forms.CharField(max_length=20, min_length=6, required=True, error_messages={
        "required": "密码不能为空",
        "max_length": "密码不能超过20个字符",
        "min_length": "密码不能少于6个字符"
    })
    remember = forms.BooleanField(required=False)
