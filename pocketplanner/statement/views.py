from multiprocessing import context
from operator import iconcat
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense
from django.core.paginator import Paginator
from wallet.models import Wallet


@login_required(login_url='login')
def statement(request):
    income = Income.objects.all()
    expense = Expense.objects.all()
    # print(list(income))
    transac = list(income)+list(expense)
    transac.sort(key=lambda x: x.date, reverse=True)
    transacpage = Paginator(transac, 10)
    pageno = request.GET.get('pageno')
    transacobj = Paginator.get_page(transacpage, pageno)
    wallet = Wallet.objects.all()

    context = {'un': transacobj, 'source': wallet}
    return render(request, 'statement/statement.html', context)
