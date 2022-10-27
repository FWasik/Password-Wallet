from django.forms import ModelForm
from .models import Password
from .aes import AESCipher
from users.models import CustomUser
from django import forms


class PasswordCreationAndUpdateForm(ModelForm):

	class Meta:
		model = Password
		fields = ("password_to_wallet", "login", "web_address", "description", )
		widgets = {
			"password_to_wallet": forms.PasswordInput(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance and hasattr(self.instance, "password_to_wallet"):
			self.initial['password_to_wallet'] = ""

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get("password_to_wallet")

		cipher = AESCipher()

		enc_pass = cipher.encrypt(password)
		cleaned_data["password_to_wallet"] = enc_pass.decode()

		return cleaned_data


class PasswordCheckForm(ModelForm):
	class Meta:
		model = CustomUser
		fields = ("password", )
		widgets = {
			"password": forms.PasswordInput()
		}
