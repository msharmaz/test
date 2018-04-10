# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

import models


admin.site.register(models.User)
admin.site.register(models.Post)
admin.site.register(models.Category)


# To create in the search by admin
# import
#
#
# class UserAdmin(admin.ModelAdmin):
#     # exclude = ('slug',)
#     list_display = ('first_name', 'last_name', 'email',)
#     list_filter = ('user_id',)
#     search_fields = ('first_name', 'last_name')
#
#
# admin.site.register(User, UserAdmin)
#
#
# class PostAdmin(admin.ModelAdmin):
#     # exclude = ('slug',)
#     list_display = ('title', 'description', 'date',)
#     list_filter = ('city',)  # can be date
#     search_fields = ('city', 'title')
#
#
# admin.site.register(Post, UserAdmin)

