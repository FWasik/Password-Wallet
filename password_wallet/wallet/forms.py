from django.forms import ModelForm
from .models import Password
from .aes import encrypt_AES_GCM


class PasswordCreationAndUpdateForm(ModelForm):
	class Meta:
		model = Password
		fields = ("password_to_wallet", "login", "web_address", "description", )

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance and hasattr(self.instance, "password_to_wallet"):
			self.initial['password_to_wallet'] = ""

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get("password_to_wallet")

		encrypted_msg = encrypt_AES_GCM(password)
		cleaned_data["password_to_wallet"] = encrypted_msg[0]
		cleaned_data["nonce"] = encrypted_msg[1]
		cleaned_data["tag"] = encrypted_msg[2]

		return cleaned_data

