from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ("login", "password1", "password2")


class CustomUserUpdateForm(forms.ModelForm):
    password1 =  forms.CharField(max_length=250)

    class Meta:
        model = get_user_model()
        fields = ["login", "password", "password1"]
