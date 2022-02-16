from django.forms import ModelForm
from .models import Income, Source


class NewIncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'description', 'wallet', 'date']


class NewSourceForm(ModelForm):
    class Meta:
        model = Source
        fields = ['category']
