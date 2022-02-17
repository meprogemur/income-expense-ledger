import imp
from django.shortcuts import render, redirect
from expense.models import Expense
from .forms import NewWalletForm
from django.views import View
from income.models import Income, Source
from django.contrib import messages
from .models import Wallet
from django.db.models import Sum


class AddWallet(View):
    def get(self, request):
        form = NewWalletForm()
        if not Wallet.objects.all():
            context = {'form': form, 'error': 'Please add a wallet',
                       'title': 'Add Wallet'}
        else:
            context = {'form': form, 'title': 'Add Wallet'}
        return render(request, 'wallet/add_wallet.html', context)

    def post(self, request):
        form = NewWalletForm(request.POST)
        if form.is_valid():
            form.save()
            if not Source.objects.all():
                messages.error(request, 'Please add a source')
                return redirect('addsource')

        return redirect('statement')


class WalletIncome(View):
    def get(self, request):
        categories = Wallet.objects.all()
        labels = []
        data = []
        for category in categories:
            expense = Income.objects.filter(wallet=category)
            total = expense.aggregate(Sum('amount'))
            labels.append(str(category.name))
            data.append(total['amount__sum'])
            print(labels, data)
        return render(request, 'expense/expense_report.html', {'type': 'doughnut', 'labels': labels, 'data': data})

    def post(self, request):
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        print(fromdate, todate)
        # fromdate = datetime(fromdate)
        # todate = datetime(todate)
        categories = Wallet.objects.all()
        expense = Income.objects.filter(date__gte=fromdate, date__lte=todate)
        for ex in expense:
            print(ex.category, ex.amount)

        labels = []
        data = []
        for category in categories:
            total = sum(ex.amount for ex in expense if ex.wallet == category)
            print(total)
            labels.append(str(category.category))
            data.append(total)
            print(labels, data)
        return render(request, 'expense/expense_report.html', {'type': 'pie', 'labels': labels, 'data': data})


class WalletExpense(View):
    def get(self, request):
        categories = Wallet.objects.all()
        labels = []
        data = []
        for category in categories:
            expense = Expense.objects.filter(wallet=category)
            total = expense.aggregate(Sum('amount'))
            labels.append(str(category.name))
            data.append(total['amount__sum'])
            print(labels, data)
        return render(request, 'expense/expense_report.html', {'type': 'doughnut', 'labels': labels, 'data': data})

    def post(self, request):
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        print(fromdate, todate)
        # fromdate = datetime(fromdate)
        # todate = datetime(todate)
        categories = Wallet.objects.all()
        expense = Expense.objects.filter(date__gte=fromdate, date__lte=todate)
        for ex in expense:
            print(ex.category, ex.amount)

        labels = []
        data = []
        for category in categories:
            total = sum(ex.amount for ex in expense if ex.wallet == category)
            print(total)
            labels.append(str(category.category))
            data.append(total)
            print(labels, data)
        return render(request, 'expense/expense_report.html', {'type': 'pie', 'labels': labels, 'data': data})
