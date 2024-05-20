from django.shortcuts import render, get_object_or_404

from .models import Page

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'main/page.html', {'page': page})