from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
       path('', views.CatalogListView.as_view(), name='index'),
       path('<slug:slug>/', views.ProductByCategoryView.as_view(), name='product_by_category'),
       
       path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]           