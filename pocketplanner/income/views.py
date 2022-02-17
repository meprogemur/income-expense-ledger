from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, redirect
from .forms import NewIncomeForm, NewSourceForm
from wallet.models import Wallet
import datetime
from django.views import View
from .models import Income, Source
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from expense.models import Category
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
# Create your views here.


def incomeView(request):
    income = Income.objects.all()
    total = income.aggregate(Sum('amount'))
    source = Source.objects.all()
    context = {
        'un': income,
        'source': source,
        'total': total['amount__sum']}
    return render(request, 'income/income.html', context)


class AddIncome(View):
    def get(self, request):
        if not Wallet.objects.all():
            return redirect('addwallet')
        if not Source.objects.all():
            return redirect('addsource')
        if not Category.objects.all():
            return redirect('addcategory')
        form = NewIncomeForm()
        return render(request, 'income/add_income.html', {'form': form})

    def post(self, request):
        form = NewIncomeForm(request.POST)
        if form.is_valid():
            wallet = Wallet.objects.get(name=form.cleaned_data['wallet'])
            wallet.balance += round(form.cleaned_data['amount'], 2)
            wallet.updated_at = datetime.datetime.now()
            wallet.save()
            obj = form.save(commit=False)
            obj.updated_at = datetime.datetime.now()
            obj.save()
        return redirect('statement')


@login_required(login_url='login')
def editIncome(request, id):
    income = Income.objects.get(pk=id)
    category = Source.objects.all()
    context = {
        'expense': income,
        'values': income,
        'categories': category
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['#date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)

        wallet = Wallet.objects.get(name=income.wallet)
        wallet.balance = round(wallet.balance - income.amount, 2)

        income.amount = amount
        income.date = date
        income.category = Source.objects.get(category=category)
        income.description = description
        wallet.balance = round(wallet.balance + float(income.amount), 2)
        if wallet.balance < 0:
            messages.error(request, 'Not Possible')
            return render(request, 'income/edit_income.html', context)
        wallet.updated_at = datetime.datetime.now()
        wallet.save()
        income.save()
        messages.success(request, 'Income updated  successfully')

        return redirect('statement')


@login_required(login_url='login')
def revertIncome(request, id):
    income = Income.objects.get(id=id)
    wallet = Wallet.objects.get(name=income.wallet)
    wallet.balance = round(wallet.balance - income.amount, 2)
    if wallet.balance < 0:
        messages.error(request, 'Not Possible')
        return redirect('statement')
    wallet.save()
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('statement')


class AddSource(View):
    def get(self, request):
        form = NewSourceForm()
        if not Source.objects.all():
            context = {
                'form': form, 'error': 'Please add a source of income', 'title': 'Add Source'}
        else:
            context = {'form': form, 'title': 'Add Source'}
        return render(request, 'income/add_source.html', context)

    def post(self, request):
        form = NewSourceForm(request.POST)
        if form.is_valid():
            form.save()
            if not Category.objects.all():
                return redirect('addcategory')
            messages.success(request, 'Source added successfully')
            return redirect('income')


def sourceData(request):
    categories = Source.objects.all()
    res = {}
    for category in categories:
        expense = Income.objects.filter(category=category)
        total = expense.aggregate(Sum('amount'))
        res[category.category] = total['amount__sum']
        print(res)
    return JsonResponse(res)


class IncomeReport(View):
    def get(self, request):
        categories = Source.objects.all()
        labels = []
        data = []
        for category in categories:
            income = Income.objects.filter(category=category)
            total = income.aggregate(Sum('amount'))
            labels.append(str(category.category))
            data.append(total['amount__sum'])
            print(labels, data)
        return render(request, 'income/income_report.html', {'type': 'pie', 'labels': labels, 'data': data})

    def post(self, request):
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        print(fromdate, todate)
        # fromdate = datetime(fromdate)
        # todate = datetime(todate)
        categories = Source.objects.all()
        income = Income.objects.filter(date__gte=fromdate, date__lte=todate)
        for ex in income:
            print(ex.category, ex.amount)

        labels = []
        data = []
        for category in categories:
            total = sum(ex.amount for ex in income if ex.category == category)
            print(total)
            labels.append(str(category.category))
            data.append(total)
            print(labels, data)
        return render(request, 'income/income_report.html', {'type': 'pie', 'labels': labels, 'data': data})
