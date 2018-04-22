from environment.models import UserProfile, Post, Category
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category','title', 'description', 'city', 'state', 'zipcode', 'image', 'status']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['type']