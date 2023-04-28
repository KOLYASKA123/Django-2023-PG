from django.urls import path, include
from users.views import Register
from django.contrib.auth import views as auth_views
import django.contrib.auth.urls


urlpatterns = [
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
]
