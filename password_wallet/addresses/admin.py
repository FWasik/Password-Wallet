from django.contrib import admin
from .models import Address

# Register your models here.


@admin.register(Address)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "IP", "username", "is_successful", "time", "log")

    ordering = ('id',)
