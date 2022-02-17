from django.urls import path
from . import views
urlpatterns = [
    path('addwallet/', views.AddWallet.as_view(), name='addwallet'),
    path('walletexpense/', views.WalletExpense.as_view(), name='walletexpense'),
    path('walletincome/', views.WalletIncome.as_view(), name='walletincome'),

]
