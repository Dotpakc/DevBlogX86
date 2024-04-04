from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('follow/<int:pk>/', views.follow_view, name='follow'),
    
    path('notifications/<uuid:pk>/', views.notification_view, name='notification'),
]