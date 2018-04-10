# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
from django_thumbs.db.models import ImageWithThumbsField


# Create your models here.

class Category(models.Model):
    type = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.type


class Post(models.Model):
    STATUS_CHOICES = (
        ('Resolved', 'Resolved'),
        ('Unresolved', 'Unresolved'),
    )
    category =models.ForeignKey(Category)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    zipcode = models.CharField(max_length=5, primary_key=True)
    image = ImageWithThumbsField(upload_to='images', sizes=(
        (125, 125), (200, 200)))  # models.FileField(upload_to='images', blank=True, null=True)
    image_second = ImageWithThumbsField(upload_to='images', blank=True, null=True)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, default='Unresolved', choices=STATUS_CHOICES)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def __str__(self):
        return self.title


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    user_id = models.CharField(max_length=11, db_column='User_id', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=45)
    user_password = models.CharField(db_column='User_password', max_length=45)  # Field name made lowercase.
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.user_id
