from django.forms import ModelForm
from .models import Wallet


class NewWalletForm(ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance']
