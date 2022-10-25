from django.contrib import admin
from .models import Password
from django import forms
from .aes import encrypt_AES_GCM, decrypt_AES_GCM


class PasswordCreationForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ("login", "password_to_wallet", "user", "web_address", "tag", "nonce", "description", )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_to_wallet")

        encrypted_msg = encrypt_AES_GCM(password)
        cleaned_data["password_to_wallet"] = encrypted_msg[0].decode("utf-8")
        cleaned_data["nonce"] = encrypted_msg[1].decode("utf-8")
        cleaned_data["tag"] = encrypted_msg[2].decode("utf-8")

        return cleaned_data


@admin.register(Password)
class CustomUserAdmin(admin.ModelAdmin):
    form = PasswordCreationForm

    list_display = ("id", "password_to_wallet", "user", "login", "nonce", "tag", "web_address", "description")

    ordering = ('id',)

