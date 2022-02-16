from django.urls import path
from . import views
urlpatterns = [
    path('', views.statement, name='statement'),
]
