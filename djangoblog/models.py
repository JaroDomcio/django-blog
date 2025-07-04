from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', "Draft"
        PUBLISHED = 'PB', "Published"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)


    def __str__(self):
        return self.title

    def Meta(self):
        ordering = ('-created_date')


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})