# urls.py
from django.urls import path
from .views import index, minimize_cash_flow

urlpatterns = [
    path('', index, name='index'),  # Main page to input transactions
    path('minimize_cash_flow/', minimize_cash_flow, name='minimize_cash_flow'),  # Endpoint to minimize cash flow
]