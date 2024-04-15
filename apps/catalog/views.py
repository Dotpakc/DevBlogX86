from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
#Q search
from django.db.models import Q

from .models import Category, Product
# Create your views here.

class CatalogListView(ListView):
    model = Category
    template_name = 'catalog/index.html'
    # context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(parent=None)
    

class ProductByCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_catalog.html'
    context_object_name = 'products'
    paginate_by = 6
    
    def get_queryset(self):
       self.category = Category.objects.get(slug=self.kwargs['slug'])
       self.parents_categories = Category.objects.filter(parent=self.category).select_related('parent')
       self.all_categories = self.parents_categories.get_descendants(include_self=True).values_list('id', flat=True) # вибираємо всі категорії, які є нащадками поточної категорії
       self.products = Product.objects.filter(Q(category__in=self.all_categories) | Q(category=self.category)).distinct()
       return self.parents_categories
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['products'] = self.products
        return context
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.main_image()
        return context