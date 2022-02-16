from django.urls import path
from . import views
urlpatterns = [
    path('addincome/', views.AddIncome.as_view(), name='addincome'),
    path('editincome/<int:id>/', views.editIncome, name='editincome'),
    path('revertincome/<int:id>', views.revertIncome, name='revertincome'),
    path('income/', views.incomeView, name='income'),
    path('addsource/', views.AddSource.as_view(), name='addsource'),
    path('sourcedata/', views.sourceData, name='sourcedata'),
    path('incomereport/', views.IncomeReport.as_view(), name='incomereport'),
]
