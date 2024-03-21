from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.blog.models import Post
from apps.blog.forms import PostForm

# Create your views here.
def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('main:index')
        else:
            messages.error(request, 'Error logging in')
    
    return render(request, 'members/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('main:index')

def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have been signed up')
            return redirect('main:index')
        else:
            messages.error(request, 'Error signing up')
            
    return render(request, 'members/signup.html', {'form': form})

@login_required
def profile_view(request):
    posts = Post.objects.filter(author=request.user)
    created_form = PostForm()
    context = { 
        'posts': posts,
        'created_form': created_form,
    }
    return render(request, 'members/profile.html', context)