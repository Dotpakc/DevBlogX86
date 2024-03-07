from django.shortcuts import render, get_object_or_404

from .models import Post

# Create your views here.
def index(request):
    
    all_posts = Post.objects.all()
    
    context = {
        'all_posts': all_posts
    }
    
    return render(request, 'blog/index.html', context)

def detail(request, post_id):
    
    post = get_object_or_404(Post, pk=post_id)
    
    context = {
        'post': post
    }
    
    return render(request, 'blog/detail.html', context)