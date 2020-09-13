from django.shortcuts import render



def checkout(request):
    return render(request, 'transactions/checkout.html')



def test(request):
    # return render(request, 'transactions/checkout_confirmation.html')
    # return render(request, 'transactions/confirm_purchase.html')
    return render(request, 'transactions/payment_success.html')