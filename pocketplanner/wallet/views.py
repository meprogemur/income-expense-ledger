import imp
from multiprocessing import context
from django.shortcuts import render, redirect
from .forms import NewWalletForm
from django.views import View
from income.models import Source
from django.contrib import messages
from .models import Wallet


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
