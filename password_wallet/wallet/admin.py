from django.contrib import admin
from .models import Password
from django import forms
from .aes import AESCipher


class PasswordCreationForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ("login", "password_to_wallet", "user", "web_address", "description", )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_to_wallet")

        cipher = AESCipher()

        enc_pass = cipher.encrypt(password)
        cleaned_data["password_to_wallet"] = enc_pass.decode()

        return cleaned_data


@admin.register(Password)
class CustomUserAdmin(admin.ModelAdmin):
    form = PasswordCreationForm

    list_display = ("id", "password_to_wallet", "user", "login", "web_address", "description")

    ordering = ('id',)

