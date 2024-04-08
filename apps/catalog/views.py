from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Category
# Create your views here.

class CatalogListView(ListView):
    model = Category
    template_name = 'catalog/index.html'
    # context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(parent=None)
    

class ProductByCategoryView(ListView):
    model = Category
    template_name = 'catalog/index.html'
    context_object_name = 'category'
    
    def get_queryset(self):
       self.category = Category.objects.get(slug=self.kwargs['slug'])
       self.parents_categories = Category.objects.filter(parent=self.category)
       return self.parents_categories
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
        