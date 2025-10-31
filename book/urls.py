from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('about/', views.about, name='about'),
    path('logout/', views.user_logout, name='user_logout'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    path('like/<int:book_id>/', views.toggle_like, name='toggle_like'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]
