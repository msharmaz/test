# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import *
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


# Create your views here.


def home(request):
    obj = Post.objects.all().order_by('-published_date')
    return render(request, 'index.html', {'obj': obj})


def search(request):
    # obj1 = Post.objects.all().order_by('published_date')
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match = Post.objects.filter(Q(zipcode__iexact=srch)|(Q(title__icontains=srch)))
            # (Q(city__icontains=srch)|,(Q(title_iendswith=srch) ,
            # Q(title__istartswith=srch) | Q(city__icontains=srch)bunch of other too
            if match:
                return render(request, 'search.html', {'obj1': match})
            else:
                messages.error(request, 'no result found')

        else:
            return HttpResponseRedirect('/search')
    return render(request, 'search.html')


def post_detail(request, slug):
    template = 'post_detail.html'

    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
    }
    return render(request, template, context)
