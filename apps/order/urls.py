from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
       path('cart_add/', views.CartHandler.as_view(), name='cart_add'),
]           