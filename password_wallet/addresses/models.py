from django.db import models
from BruteBuster.models import FailedAttempt


class Address(models.Model):
    IP = models.GenericIPAddressField()
    username = models.CharField(max_length=256)
    is_successful = models.BooleanField()
    time = models.DateTimeField(auto_now=True)
    log = models.ForeignKey(FailedAttempt, null=True, on_delete=models.CASCADE)
