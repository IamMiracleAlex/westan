from django.urls import path
from transactions import views

app_name = 'transactions'

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("dashboard/checkout-confirmation/", views.dashboard_checkout_confirmation, name="dashboard_checkout_confirmation"),
    path("dashboard/payment-success/", views.dashboard_payment_success, name="dashboard_payment_success"),
    path("invoice/", views.invoice, name="invoice"),
    path("test/", views.test, name="test"),
]
