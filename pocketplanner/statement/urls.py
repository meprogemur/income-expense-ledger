from django.urls import path
from . import views
urlpatterns = [
    path('', views.statement, name='statement'),
    path('exportcsv', views.exportCsv, name='exportcsv'),
    path('exportexcel', views.exportExcel, name='exportexcel'),
]
