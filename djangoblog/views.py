from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .settings import EMAIL_HOST_USER
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
def post_list(request, tag_slug = None):
    posts = Post.objects.filter(status = Post.Status.PUBLISHED)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'posts': posts, 'tag': tag})


def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-created_date')[:4]


    return render(request, 'post_detail.html', {'post': post,
                                                'comments': comments,
                                                "form": form,
                                                "similar_posts": similar_posts})

def post_share(request,id):
    post = get_object_or_404(Post, id=id, status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you {post.title}"
            message = f"Read {post.title} url: {post_url}"
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    print("uruchiomiono")
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'content')).filter(search=query)
    return render(request,'search.html',{'form':form,'results':results,'query':query})

