from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.urls import views as auth_views
from wallet import views

app_name = "wallet"

urlpatterns = [
    path("wallet/", views.PasswordListView.as_view(template_name="wallet/wallet_list.html"), name="wallet"),
    path("wallet/add/", views.PasswordCreateView.as_view(template_name="wallet/password_add.html"), name="add"),
    path("wallet/<int:pk>/update/", views.PasswordUpdateView.as_view(template_name="wallet/password_update.html"),
         name="update"),
    path("wallet/<int:pk>/delete/", views.PasswordDeleteView.as_view(template_name="wallet/password_delete.html"),
         name="delete"),
    path("wallet/<int:pk>/show/", views.decrypting_password, name="show"),
]
