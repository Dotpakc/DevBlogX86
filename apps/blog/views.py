from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import JsonResponse, HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
#pagination
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm

# Create your views here.

def index(request):
    # print(request.GET.get('page', 1))   
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    all_posts_page = paginator.get_page(page)

    context = {
        'all_posts': all_posts_page,
        'created_form': PostForm()
    }
    return render(request, 'blog/index.html', context)


@login_required
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    update_form = PostForm(instance=post)
    context = {
        'post': post,
        'update_form': update_form
    }
    return render(request, 'blog/detail.html', context)

@login_required
def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('blog:detail' , post_id=post.id)
        else:
            messages.error(request, 'Error creating post')
    return redirect('blog:index')

@login_required
def delete_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id, author=request.user)
        post.delete()
        messages.success(request, 'Post deleted successfully')
    return redirect('blog:index')

@login_required
def update_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id, author=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
        else:
            messages.error(request, 'Error updating post')
        return redirect('blog:detail', post_id=post.id)
    return redirect('blog:index')

@login_required
def like_view(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.like.all():
            post.like.remove(request.user)
            user_like = False
        else:
            post.like.add(request.user)
            user_like = True
        return JsonResponse( {'like_count': post.like.count(), 'user_like': user_like} )