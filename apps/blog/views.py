from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm
# Create your views here.
def index(request):
    
    all_posts = Post.objects.all()
    
    context = {
        'all_posts': all_posts,
        'created_form': PostForm()
    }
    
    return render(request, 'blog/index.html', context)

def detail(request, post_id):
    
    post = get_object_or_404(Post, pk=post_id)
    
    context = {
        'post': post
    }
    
    return render(request, 'blog/detail.html', context)

def create_view(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:detail' , post_id=post.id)
