from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.urls import views as auth_views
from users import views

app_name = "users"

urlpatterns = [
    path("", views.login, name="login"),
    path("register/",  views.CustomUserCreateView.as_view(template_name="users/register.html"), name="register"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("update-password/", views.change_password, name="password-change"),
    path("user/<int:pk>/delete/", views.CustomUserDeleteView.as_view(template_name="users/user_delete.html"),
         name="delete"),
    path("user/<int:pk>/", views.CustomUserDetailView.as_view(template_name="users/profile.html"),
         name="profile")
]
