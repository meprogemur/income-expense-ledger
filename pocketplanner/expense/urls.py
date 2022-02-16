from django.urls import path
from . import views


urlpatterns = [
    path('addexpense', views.AddExpense.as_view(), name='addexpense'),
    path('editexpense/<int:id>', views.editExpence, name='okok'),
    path('revertexpense/<int:id>', views.revertExpense, name='revertexpense'),
    path('expense/', views.expenseView, name='expense'),
    path('addcategory/', views.AddCategory.as_view(), name='addcategory'),
    # path('categorydata/', views.categoryData, name='categorydata'),
    path('expensereport/', views.ExpenseReport.as_view(), name='expensereport'),
]
