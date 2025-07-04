from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.core.paginator import Paginator

def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    return render(request, 'home.html', {'posts': posts})


def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

