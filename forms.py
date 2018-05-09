from environment.models import UserProfile, Post, Category
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'description', 'city', 'state', 'zipcode', 'image', 'date', 'status']


class CategoryForm(forms.ModelForm):
    type = forms.CharField(help_text="Please enter new category:")

    class Meta:
        model = Category
        fields = ['type']

