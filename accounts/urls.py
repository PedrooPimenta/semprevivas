from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
from .views import SignUpView


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path("signup/", SignUpView.as_view(), name="signup"),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
