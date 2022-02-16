from django.urls import path
from . import views
urlpatterns = [
    path('addwallet/', views.AddWallet.as_view(), name='addwallet'),
]
