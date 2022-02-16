from django.shortcuts import render, redirect
import datetime
from django.views import View
from income.models import Income
from .forms import NewExpenseForm, NewCategoryForm
from wallet.models import Wallet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Category
from income.models import Income, Source
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


def expenseView(request):
    expense = Expense.objects.all()
    category = Category.objects.all()
    context = {
        'un': expense,
        'source': category}
    return render(request, 'expense/expense.html', context)


class AddExpense(View):
    def get(self, request):
        if not Wallet.objects.all():
            messages.error(request, 'Please add a wallet')
            return redirect('addwallet')
        if not Source.objects.all():
            messages.error(request, 'Please add a source')
            return redirect('addsource')
        if not Category.objects.all():
            messages.error(request, 'Please add a category')
            return redirect('addcategory')
        form = NewExpenseForm()
        return render(request, 'expense/add_expense.html', {'form': form})

    def post(self, request):
        form = NewExpenseForm(request.POST)
        if form.is_valid():
            wallet = Wallet.objects.get(name=form.cleaned_data['wallet'])
            if wallet.balance < form.cleaned_data['amount']:
                return render(request, 'expense/add_expense.html', {'form': form, 'error': 'Insufficient funds'})
            wallet.balance = round(
                wallet.balance - form.cleaned_data['amount'], 2)
            wallet.updated_at = datetime.datetime.now()
            wallet.save()
            obj = form.save(commit=False)
            obj.updated_at = datetime.datetime.now()
            obj.save()
        return redirect('statement')


@login_required(login_url='login')
def editExpence(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expense/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expense/edit_expense.html', context)
        description = request.POST['description']
        date = request.POST['#date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expence/edit_expense.html', context)

        wallet = Wallet.objects.get(name=expense.wallet)
        wallet.balance = round(wallet.balance + expense.amount, 2)

        expense.amount = amount
        expense. date = date
        expense.category = Category.objects.get(category=category)
        expense.description = description
        wallet.balance = round(wallet.balance - float(expense.amount), 2)
        if wallet.balance < 0:
            messages.error(request, 'Not Possible')
            return render(request, 'expense/edit_expense.html', context)
        wallet.save()
        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('statement')


@login_required(login_url='login')
def revertExpense(request, id):
    expense = Expense.objects.get(id=id)
    wallet = Wallet.objects.get(name=expense.wallet)
    wallet.balance = round(wallet.balance + expense.amount, 2)
    wallet.save()
    income = Income.objects.create(
        amount=expense.amount,
        category=Source.objects.get(category='revert'),
        description='expense revert',
        date=datetime.datetime.now(),
        wallet=expense.wallet,
        updated_at=datetime.datetime.now()
    )
    income.save()
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('statement')


class AddCategory(View):
    def get(self, request):
        form = NewCategoryForm()
        if not Category.objects.all():
            context = {'form': form, 'error': 'Please add a category',
                       'title': 'Add Category'}
        else:
            context = {'form': form, 'title': 'Add Category'}
        return render(request, 'expense/add_category.html', context)

    def post(self, request):
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('expense')


# @csrf_exempt
# def categoryData(request):
#     if request.method == 'GET':

#         return JsonResponse(res)
#     if request.method == 'POST':
#         print(request.POST['Quantity'])
#         return JsonResponse({'data': 'data'})


class ExpenseReport(View):
    def get(self, request):
        categories = Category.objects.all()
        labels = []
        data = []
        for category in categories:
            expense = Expense.objects.filter(category=category)
            total = expense.aggregate(Sum('amount'))
            labels.append(str(category.category))
            data.append(total['amount__sum'])
            print(labels, data)
        return render(request, 'expense/expense_report.html', {'type': 'doughnut', 'labels': labels, 'data': data})

    def post(self, request):
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        print(fromdate, todate)
        # fromdate = datetime(fromdate)
        # todate = datetime(todate)
        categories = Category.objects.all()
        expense = Expense.objects.filter(date__gte=fromdate, date__lte=todate)
        for ex in expense:
            print(ex.category, ex.amount)

        labels = []
        data = []
        for category in categories:
            total = sum(ex.amount for ex in expense if ex.category == category)
            print(total)
            labels.append(str(category.category))
            data.append(total)
            print(labels, data)
        return render(request, 'expense/expense_report.html', {'type': 'pie', 'labels': labels, 'data': data})
