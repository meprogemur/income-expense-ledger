from django.db import models
from django.utils.timezone import now
from wallet.models import Wallet
# Create your models here.


class Source(models.Model):
    category = models.CharField(max_length=100, default='nosource')
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.category


class Income(models.Model):
    category = models.ForeignKey(Source, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(default=now)
    description = models.CharField(max_length=100)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default='income')
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.source) + str(self.date) + str(self.amount)
