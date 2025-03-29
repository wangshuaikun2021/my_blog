from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .models import BlogCategory, Blog, BlogComment
from .forms import PubBlogForm


# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    return render(request, "index.html", context={"blogs": blogs})
    # return HttpResponse("Hello, Django!")


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist as e:
        return HttpResponse(e)
    return render(request, "blog_detail.html", context={"blog": blog})


@login_required(login_url=reverse_lazy('myauth:sign_in'))
@require_http_methods(["GET", "POST"])
def pub_blog(request):
    if request.method == "GET":
        categories = BlogCategory.objects.all()
        return render(request, "pub_blog.html", context={"categories": categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            category = form.cleaned_data.get("category")
            print("验证通过的数据：", title, content, category)
            blog = Blog.objects.create(title=title, content=content, category_id=category, author=request.user)
            return JsonResponse({"code": 200, "msg": "发布成功", "data": {'blog_id': blog.id}})
        else:
            print("表单验证失败：", form.errors)
            print("表单数据：", form.cleaned_data)
            return JsonResponse({"code": 400, "msg": "表单验证失败"})


@require_POST
@login_required(login_url=reverse_lazy('myauth:sign_in'))
def submit_comment(request):
    blog_id = request.POST.get("blog_id")
    content = request.POST.get("content")
    print("blog_id:", blog_id)
    print("content:", content)
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    return redirect(reverse("blog:blog_detail", kwargs={"blog_id": blog_id}))


@require_GET
def search(request):
    keyword = request.GET.get("keyword")
    if not keyword:
        return redirect(reverse("blog:index"))
    blogs = Blog.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword)).all()
    return render(request, "index.html", context={"blogs": blogs})
