from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<slug:slug>/', views.page_view, name='page'),
]