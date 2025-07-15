from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.filter(status = Post.Status.PUBLISHED).count()

@register.inclusion_tag('post_enumerating_template.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(status = Post.Status.PUBLISHED).order_by('-created_date')[:count]
    return {'posts':latest_posts}


@register.inclusion_tag('post_enumerating_template.html')
def show_most_commented_posts(count=5):
    most_commented_posts = Post.objects.filter(status = Post.Status.PUBLISHED).annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'posts':most_commented_posts}

@register.filter(name='markdown')
def markdown_text(text):
    return mark_safe(markdown.markdown(text))

