from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('like/<int:post_id>', views.like_view, name='like'),    #google.com/blog/like/
    
    
    path('', views.index, name='index'),    #google.com/blog/
    path('post/<int:post_id>/', views.detail, name='detail'),    #google.com/blog/1/
    path('create/', views.create_view, name='create'),    #google.com/blog/create/
    path('delete/<int:post_id>/', views.delete_view, name='delete'),    #google.com/blog/delete/1/
    path('update/<int:post_id>/', views.update_view, name='update'),    #google.com/blog/update/1/
]           