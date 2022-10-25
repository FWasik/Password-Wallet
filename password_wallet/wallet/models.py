from django.db import models
from django.contrib.auth import get_user_model


class Password(models.Model):
    password_to_wallet = models.CharField(max_length=256)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user")
    web_address = models.CharField(max_length=256, default="", blank=True)
    login = models.CharField(max_length=50, default="", blank=True)
    nonce = models.CharField(max_length=256, default="", blank=True)
    tag = models.CharField(max_length=256, default="", blank=True)
    description = models.TextField(default="", blank=True)
