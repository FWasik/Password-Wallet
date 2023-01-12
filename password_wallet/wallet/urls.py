from django.urls import path
from wallet import views

app_name = "wallet"

urlpatterns = [
    path("wallet/", views.PasswordListView.as_view(template_name="wallet/wallet_list.html"), name="wallet"),
    path("wallet/add/", views.PasswordCreateView.as_view(template_name="wallet/password_add.html"), name="add"),
    path("wallet/<int:pk>/update/", views.PasswordUpdateView.as_view(template_name="wallet/password_update.html"),
         name="update"),
    path("wallet/<int:pk>/delete/", views.PasswordDeleteView.as_view(template_name="wallet/password_delete.html"),
         name="delete"),
    path("wallet/<int:pk>/show/", views.DecryptingPasswordView.as_view(template_name="wallet/password_show.html"),
         name="show"),
    path("wallet/<int:pk>/check/", views.IfCheckedView.as_view(template_name="wallet/master_password_check.html"),
         name="check"),
    path("wallet/<int:pk>/share/", views.share_password_view, name="share"),
    path("wallet/<int:pk>/clear/", views.clear_sharing_password_view, name="clear"),
    path("wallet/shared/", views.PasswordSharedListView.as_view(template_name="wallet/wallet_share_list.html"),
         name="wallet-shared")
]
