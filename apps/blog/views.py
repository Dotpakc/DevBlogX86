from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import JsonResponse, HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
#pagination
from django.core.paginator import Paginator
#Q
from django.db.models import Q, Count

from .models import Post, Comment
from .forms import PostForm, CommentForm

from apps.members.models import Notification

# Create your views here.

def index(request):
    # print(request.GET.get('page', 1))   
    all_posts = Post.objects.all().prefetch_related("author").prefetch_related("like")
    if request.GET.get('sort_by') == 'p':
        all_posts = all_posts.annotate(like_count=Count('like')).order_by('-like_count')
    elif request.GET.get('sort_by') == 'o':
        all_posts = all_posts.order_by('created_at')
    else:
        all_posts = all_posts.order_by('-created_at')
    
    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    all_posts_page = paginator.get_page(page)

    
    context = {
        'all_posts': all_posts_page,
        'created_form': PostForm(),
    }
    return render(request, 'blog/index.html', context)


@login_required
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    post = Post.objects.prefetch_related('comments').prefetch_related('comments__author').prefetch_related('comments__like').get(pk=post_id)
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
            form.save_m2m()
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
            
        if request.user != post.author:
            print('notification')
            Notification().add_like(post, request.user)
            
            
        
        return JsonResponse( {'like_count': post.like.count(), 'user_like': user_like} )


@login_required
def like_comment_view(request, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user in comment.like.all():
            comment.like.remove(request.user)
            user_like = False
        else:
            comment.like.add(request.user)
            user_like = True
        return JsonResponse( {'like_count': comment.like.count(), 'user_like': user_like} )
    
@login_required
def comment_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=form.cleaned_data['content']
            )
            messages.success(request, 'Comment created successfully')
        else:
            messages.error(request, 'Error creating comment')
    return redirect('blog:detail', post_id=post_id)

def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', "")
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)).prefetch_related("author").prefetch_related("like")
        if request.GET.get('sort_by') == 'p':
            all_posts = posts.annotate(like_count=Count('like')).order_by('-like_count')
        elif request.GET.get('sort_by') == 'o':
            all_posts = posts.order_by('created_at')
        else:
            all_posts = posts.order_by('-created_at')
    
        
        paginator = Paginator(all_posts, 3)
        page = request.GET.get('page')
        all_posts_page = paginator.get_page(page)

        context = {
            'all_posts': all_posts_page,
            'created_form': PostForm()
        }
        return render(request, 'blog/index.html', context)
    return redirect('blog:index')