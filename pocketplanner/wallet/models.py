from unicodedata import name
from django.db import models
from django.utils.timezone import now
# Create your models here.


class Wallet(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=now)
    balance = models.FloatField(default=0)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
