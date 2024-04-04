from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#pagination
from django.core.paginator import Paginator



from .models import Profile, Notification
from .forms import ProfileForm

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
            profile = Profile(user=user)
            profile.save()
            login(request, user)
            messages.success(request, 'You have been signed up')
            return redirect('main:index')
        else:
            messages.error(request, 'Error signing up')
            
    return render(request, 'members/signup.html', {'form': form})

@login_required
def profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posts = Post.objects.filter(author=profile.user).prefetch_related('like').prefetch_related("author")
    #pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    created_form = PostForm()
    context = {
        'is_owner': request.user == profile.user,
        'is_following': request.user.profile.is_following(profile),
        'followers': profile.get_followers(),
        'following': profile.get_following(),
        'profile': profile,
        'posts': posts,
        'created_form': created_form,
    }
    return render(request, 'members/profile.html', context)


@login_required
def profile_edit_view(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('members:profile', pk=profile.pk)
        else:
            messages.error(request, 'Error updating profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'members/profile_edit.html', {'form': form})


@login_required
def follow_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.user != profile.user:
        user_profile = request.user.profile
        if user_profile.is_following(profile):
            user_profile.unfollow(profile)
            messages.info(request, 'You have unfollowed {}'.format(profile.user.username))
        else:
            user_profile.follow(profile)
            messages.info(request, 'You have followed {}'.format(profile.user.username))
    return redirect('members:profile', pk=pk)
        
    
@login_required
def notification_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect(notification.url)