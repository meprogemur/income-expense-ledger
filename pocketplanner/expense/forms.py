from django.forms import ModelForm
from .models import Expense, Category


class NewExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount',
                  'description', 'wallet', 'date']


class NewCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category']
