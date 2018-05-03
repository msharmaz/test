"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^citymanager/$', views.citymanager, name='citymanager'),
    url(r'^search/$', views.search),
    url(r'^register/$', views.register, name='register'),  # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),  # added new
    url(r'^restricted/', views.restricted, name='restricted'),  # added
    url(r'^logout/$', views.user_logout, name='logout'),  # added
    url(r'^(?P<pk>\d+)/$', views.post_detail, name='post_detail'),  # added
    url(r'^create/$', views.post_create, name='create'),  # added for create post

    url(r'^category/$', views.category_create, name='category'),
    url(r'^remove/(?P<post_id>\d+)/$', views.post_remove, name='post_remove'),
    url(r'^edit/(?P<post_id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^add_category/$', views.add_category, name='add_category'),  # NEW MAPPING!
    url(r'^edit_status/$', views.add_status, name='edit_status'),  # NEW MAPPING!
    # url(r'^category/(?P<category_name_url>\w+)$', views.category, name='category'),
]
