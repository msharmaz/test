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

from environment.forms import UserForm, UserProfileForm, PostForm, CategoryForm, StatusForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.


def home(request):  # pk
    obj = Post.objects.all().order_by('-date')
    # status = get_object_or_404(Status, post=pk)
    return render(request, 'index.html', {'obj': obj})
    # ,'status': status})


def citymanager(request):
    obj = Status.objects.all()
    return render(request, 'citymanager.html', {'obj': obj})


@login_required
def post_create(request):
    """
    View for creating a new post.
    """
    if request.method == 'POST':
        # form is sent
        post_form = PostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            cd = post_form.cleaned_data
            new_item = post_form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            # tags = post_form.cleaned_data['tags']
            new_item.save()
            # for tag in tags:
            #     new_item.tags.add(tag)
            # new_item.save()
            # create_action(request.user, 'created a post:', new_item)
            messages.success(request, 'Post added successfully')
            post_form = PostForm()
        else:
            messages.error(request, 'Error adding new post')

    else:
        # build form
        post_form = PostForm(data=request.GET)

    return render(request, 'create_post.html', {'section': 'posts',
                                                'post_form': post_form})


@login_required
def post_remove(request, post_zipcode):
    Post.objects.filter(id=post_zipcode).delete()
    return redirect('posts:mypost')


@login_required
def post_edit(request, post_zipcode):
    item = Post.objects.get(pk=post_zipcode)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('posts:mypost')

    else:
        form = PostCreateForm(instance=item)

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('posts/post/post_edit.html', args)


def category_create(request):
    return render(request, 'create_category.html', {})


@staff_member_required
def add_status(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = StatusForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return home(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = StatusForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_status.html', {'form': form}, context)


@staff_member_required
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if category_form.is_valid():
            # Save the new category to the database.
            category_form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return home(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print category_form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        category_form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_category.html', {'category_form': category_form}, context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                  context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {}, context)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def search(request):
    if request.method == 'POST':
        # if 'dropdown' in request.POST:
        #     categoryValue = request.POST['dropdown']
        # else:
        #     categoryValue = False
        categoryValue = request.POST['dropdown']  # same as above function
        searchQuery = request.POST['srh']

        if categoryValue != "All":
            if searchQuery:
                sql_query = Post.objects.filter(Q(category__type__icontains=categoryValue) &
                                                Q(zipcode__exact=searchQuery)
                                                |
                                                (Q(title__icontains=searchQuery)))
            else:
                sql_query = Post.objects.filter(Q(category__type__icontains=categoryValue))

        elif categoryValue == "All":
            # if searchQuery:
            #     sql_query = Post.objects.filter(Q(zipcode__iexact=searchQuery) | (Q(title__icontains=searchQuery)))
            # else:
            return home(request)

        # results = establishDBConnection(request, sql_query)
        if sql_query:
            return render(request, 'search.html', {'obj1': sql_query})
        else:
            messages.error(request, 'No results found')

    return render(request, 'search.html')


def post_detail(request, pk):
    template = 'post_detail.html'

    post = get_object_or_404(Post, pk=pk)
    status = get_object_or_404(Status, post=pk)
    context = {
        'post': post,
        'status': status
    }
    return render(request, template, context)

# def search(request):
#     # obj1 = Post.objects.all().order_by('published_date')
# 	#some_category = Category.objects.get(category_name="SOMETHING")
# 	#products = Product.objects.all().filter(category=some_category)
#     if request.method == 'POST':
#         srch = request.POST['srh']
#
#         if srch:
#             match = Post.objects.filter(Q(zipcode__iexact=srch)|(Q(title__icontains=srch)))
#             # (Q(city__icontains=srch)|,(Q(title_iendswith=srch) ,
#             # Q(title__istartswith=srch) | Q(city__icontains=srch)bunch of other too
#             if match:
#                 return render(request, 'search.html', {'obj1': match})
#             else:
#                 messages.error(request, 'no result found')
#
#         else:
#             return HttpResponseRedirect('/search')
#     return render(request, 'search.html')


# class based and function based deatil view page not working april 10
# def post_detail(request, pk=None):
#     template = 'post_detail.html'
#
#     post = get_object_or_404(Post, pk=pk)
#     context = {
#         'post': post,
#     }
#     return render(request, template, context)


# class post_detail(DetailView):
#
#     model = Post
#
#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             return context
