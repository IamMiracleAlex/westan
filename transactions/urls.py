from django.urls import path
from transactions import views

app_name = 'transactions'

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("test/", views.test, name="test"),
]
