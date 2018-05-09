# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.sites.models import Site

# Register your models here.

from models import Post, Status

import models

admin.site.register(models.Category)
admin.site.register(models.UserProfile)
admin.site.register(models.Status)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'category', 'city', 'state', 'date')
    list_filter = ( 'category', 'city', 'date')
    search_fields = ('city', 'title')


admin.site.register(Post, PostAdmin)

#
# class StatusAdmin(admin.ModelAdmin):
#     list_display = ('post', 'status')
#     list_filter = ('post', 'status')
#     search_fields = ('post', 'status')
#
#
# admin.site.register(Status, StatusAdmin)
#

