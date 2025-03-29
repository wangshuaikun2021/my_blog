import random

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods

from .models import Captcha
from .forms import SignUpForm, LogInForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User


# Create your views here.
@require_http_methods(["GET", "POST"])
def sign_in(request):
    if request.method == "GET":
        return render(request, "sign_in.html")
    else:
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("pwd")
            remember = form.cleaned_data.get("remember")
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                auth_login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect(reverse("blog:index"))
            else:
                return render(request, "sign_in.html", {"msg": "邮箱或密码错误"})


def log_out(request):
    auth_logout(request)
    return redirect(reverse("myauth:sign_in"))


@require_http_methods(["POST", "GET"])
def sign_up(request):
    if request.method == "GET":
        return render(request, "sign_up.html")
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("pwd")
            print("验证通过的数据：", username, email, password)
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse("myauth:sign_in"))
        else:
            print("表单验证失败：", form.errors)  # 打印具体的错误信息
            print("表单数据：", form.cleaned_data)  # 打印已清理的数据
            return render(request, "sign_up.html", {"form": form})


def send_email_captcha(request):
    email = request.GET.get("email")
    print(email)
    if not email:
        return JsonResponse({"code": 400, "msg": "邮箱不能为空"})
    # 生成验证码
    captcha = random.sample("0123456789", 4)
    captcha = "".join(captcha)
    # 保存验证码
    Captcha.objects.update_or_create(email=email, defaults={"captcha": captcha})
    send_mail("【Django学习】邮箱验证码", f"您的验证码是{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "msg": "验证码发送成功"})
