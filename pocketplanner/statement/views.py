from tkinter import font
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense
from django.core.paginator import Paginator
from wallet.models import Wallet
from django.db.models import Sum
import datetime
import csv
import xlwt


@login_required(login_url='login')
def statement(request):
    income = Income.objects.all()
    expense = Expense.objects.all()
    transac = list(income)+list(expense)
    transac.sort(key=lambda x: x.date, reverse=True)
    transacpage = Paginator(transac, 10)
    pageno = request.GET.get('pageno')
    transacobj = Paginator.get_page(transacpage, pageno)
    wallet = Wallet.objects.all()
    total = wallet.aggregate(Sum('balance'))
    context = {'un': transacobj, 'source': wallet,
               'totalbal': total['balance__sum']}
    return render(request, 'statement/statement.html', context)


def exportCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=transaction' + \
        str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Description', 'Amount', 'Date',
                    'Category', 'Wallet', 'Type'])
    income = Income.objects.all()
    expense = Expense.objects.all()
    transac = list(income)+list(expense)
    transac.sort(key=lambda x: x.date, reverse=True)
    for element in transac:
        writer.writerow([element.description, element.amount,
                        element.date, element.category, element.wallet, element.type])
    writer.writerow([''])
    writer.writerow(['Wallet', 'Balance'])
    wallet = Wallet.objects.all()
    for element in wallet:
        writer.writerow([element.name, element.balance])
    return response


def exportExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=transaction' + \
        str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Statement')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Description', 'Amount', 'Date',
               'Category', 'Wallet', 'Type']

    font_style = xlwt.XFStyle()
    for col in range(len(columns)):
        ws.write(row_num, col, columns[col], font_style)

    income = Income.objects.all().values_list('description', 'amount',
                                              'date', 'category', 'wallet', 'type')
    expense = Expense.objects.all().values_list('description', 'amount',
                                                'date', 'category', 'wallet', 'type')
    print(income, expense)
    transac = list(income)+list(expense)
    transac.sort(key=lambda x: x[1])
    for row in transac:
        row_num += 1
        for col in range(len(row)):
            ws.write(row_num, col, str(row[col]), font_style)
    wb.save(response)
    return response
