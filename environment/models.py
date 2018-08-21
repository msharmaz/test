# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
from django_thumbs.db.models import ImageWithThumbsField
from django.contrib.auth.models import User

#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    type = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.type


class Post(models.Model):
    # STATUS_CHOICES = (
    #     ('Resolved', 'Resolved'),
    #     ('Unresolved', 'Unresolved'),
    # )
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=50)
    description = models.TextField()
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    zipcode = models.CharField(max_length=5, primary_key=True)
    image = ImageWithThumbsField(upload_to='images', sizes=(
        (125, 125), (200, 200)))  # models.FileField(upload_to='images', blank=True, null=True)
    date = models.DateField(default=date.today)
# status = models.CharField(max_length=10, default='Unresolved', choices=STATUS_CHOICES)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def __str__(self):
        return self.title


class Status(models.Model):
    STATUS_CHOICES = (
        ('Resolved', 'Resolved'),
        ('Unresolved', 'Unresolved'),
        ('In Progress', 'Inprogress'),
    )
    post = models.OneToOneField(Post, unique=True)
    status = models.CharField(max_length=15, default='Unresolved', choices=STATUS_CHOICES)

    def __str__(self):
        return self.status


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    #user = models.OneToOneField(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
'''
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


'''
