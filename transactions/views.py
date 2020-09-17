from django.shortcuts import render



def checkout(request):
    return render(request, 'transactions/checkout.html')

def checkout_confirmation(request):
    return render(request, 'transactions/checkout_confirmation.html')


def confirm_purchase(request):
    return render(request, 'transactions/confirm_purchase.html')


def payment_success(request):
    return render(request, 'transactions/payment_success.html')


def dashboard_checkout_confirmation(request):
    return render(request, 'transactions/dashboard_checkout_confirmation.html')

def dashboard_payment_success(request):
    return render(request, 'transactions/dashboard_payment_success.html')

def invoice(request):
    return render(request, 'transactions/invoice.html')


def test(request):
    return render(request, 'transactions/dashboard_payment_success.html')
