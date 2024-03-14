from django.shortcuts import render, get_object_or_404, redirect
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
    
    context = {
        'post': post
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
            return redirect('blog:detail' , post_id=post.id)
