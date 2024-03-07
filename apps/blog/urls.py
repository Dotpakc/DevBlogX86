from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),    #google.com/blog/
    path('post/<int:post_id>/', views.detail, name='detail'),    #google.com/blog/1/
    path('create/', views.create_view, name='create'),    #google.com/blog/create/
]   