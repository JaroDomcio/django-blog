"""
URL configuration for djangoblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import post_list, post_detail, post_share, post_search
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", post_list, name="post_list"),
    path("search/", post_search, name="post_search"),
    path("tag/<slug:tag_slug>", post_list, name="post_list_by_tag"),
    path("<slug:slug>/", post_detail, name="post_detail"),
    path("<int:id>/share/", post_share, name="post_share"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
