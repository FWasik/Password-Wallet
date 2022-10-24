from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.urls import views as auth_views
from users import views

app_name = "users"

urlpatterns = [
    path("", auth_views.LoginView.as_view(), name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("register/",  views.CustomUserCreateView.as_view(template_name="users/register.html"), name="register"),
    path("logout/", auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("update-password/", views.change_password, name="password-change"),
    path("<int:pk>/delete/", views.CustomUserDeleteView.as_view(template_name="users/delete.html"), name="delete")
]
