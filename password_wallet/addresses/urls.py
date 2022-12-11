from django.urls import path
from addresses import views

app_name = "addresses"

urlpatterns = [
    path("addresses-list", views.get_logs_view, name="list"),
    path("address-unblocked/<int:pk>/", views.unblock_address_view, name="unblock"),
    path("address-delete/<int:pk>/", views.delete_address_view, name="delete"),
    path("address-delete-log/<int:pk>/", views.delete_address_log_view, name="delete-log"),
    path("address-delete-all-logs/", views.delete_all_address_logs_view, name="delete-all-logs"),
]