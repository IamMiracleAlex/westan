from django.shortcuts import render


def test(request):
    return render(request, 'transactions/checkout.html')
    # return render(request, 'transactions/checkout_confirmation.html')
    # return render(request, 'transactions/confirm_purchase.html')
    # return render(request, 'transactions/payment_success.html')