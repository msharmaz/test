from environment.models import UserProfile, Post, Category, Status
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
'''
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')	
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2', )
'''


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    bio = forms.CharField(help_text="Please enter your short Bio.", max_length=500, required=False)
    location = forms.CharField(help_text="Please enter your Location/State.", max_length=30, required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture', 'bio', 'location']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'description', 'city', 'state', 'zipcode', 'image', 'date']


class CategoryForm(forms.ModelForm):
    type = forms.CharField(help_text="Please enter new category:")

    class Meta:
        model = Category
        fields = ['type']


class StatusForm(forms.ModelForm):
    # status = forms.CharField(help_text="Please enter new category:")
    # post = forms.CharField(help_text="Please enter new category:")

    class Meta:
        model = Status
        fields = ['status', 'post']
