from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
       path('cart/', views.CartHandler.as_view(), name='cart'),
       path('cart/add', views.CartAddHandler.as_view(), name='cart_add'),
       path('cart/remove/<int:pk>', views.CartDeleteHandler.as_view(), name='cart_remove'),
       path('cart/clear', views.CartClearHandler.as_view(), name='cart_clear'),
       
       path('checkout/', views.CheckoutHandler.as_view(), name='checkout'),
       path('complete/<int:order_id>', views.OrderCompleteHandler.as_view(), name='complete'),
]           