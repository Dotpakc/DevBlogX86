from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
       path('cart/', views.CartHandler.as_view(), name='cart'),
       path('cart/add', views.CartAddHandler.as_view(), name='cart_add'),
       path('cart/remove/<int:pk>', views.CartDeleteHandler.as_view(), name='cart_remove'),
]           