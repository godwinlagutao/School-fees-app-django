from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Custom auth URLs pointing to our templates
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='fees/login.html',
             redirect_authenticated_user=True
         ), 
         name='login'),
    
    path('logout/', LogoutView.as_view(next_page='logout_page'), name='logout'),
    path('logout-page/', TemplateView.as_view(template_name='fees/logout.html'), name='logout_page'),
    
    path('register/', views.register, name='register'),
    path('download-clearance/', views.download_clearance, name='download_clearance'),
]