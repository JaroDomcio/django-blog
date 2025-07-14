from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.filter(status = Post.Status.PUBLISHED).count()

@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(status = Post.Status.PUBLISHED).order_by('-created_date')[:count]
    return {'latest_posts':latest_posts}


# @register.simple_tag
# def get_most_commented_posts(count=5):
#     return Post.objects.filter(status = Post.Status.PUBLISHED).order_by('-created_date')[:count]