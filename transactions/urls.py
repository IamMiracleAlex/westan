from django.urls import path
from transactions import views

app_name = 'transactions'

urlpatterns = [
    path("confirm-purchase/<int:listing_id>/", views.confirm_purchase, name="confirm_purchase"),
    path("checkout/<int:trans_id>/", views.checkout, name="checkout"),
    path("checkout-confirmation/<int:trans_id>/", views.checkout_confirmation, name="checkout_confirmation"),
    path("payment-success/<int:listing_id>/", views.payment_success, name="payment_success"),
    path("invoice/<int:listing_id>/", views.invoice, name="invoice"),
    path("test/", views.test, name="test"),
]
