from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum

from listings.models import Listing
from transactions.models import Transaction



@login_required
def confirm_purchase(request, listing_id):

    listing = get_object_or_404(Listing, id=listing_id) 

    if request.method == "POST":
        amount_to_pay = request.POST.get('amount_to_pay')
        trans = Transaction.objects.create(listing=listing,
                                        user=request.user,
                                        amount_to_pay=amount_to_pay, 
                                        status=Transaction.SUBMITTED)
        return redirect(reverse('transactions:checkout', kwargs={'trans_id': trans.id}))


    context = {"listing": listing}
    return render(request, 'transactions/confirm_purchase.html', context)


@login_required
def checkout(request, trans_id):

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 0)

        trans = Transaction.objects.get(id=trans_id)
        trans.payment_type = payment_type
        trans.save()
        return redirect(reverse('transactions:checkout_confirmation', args=[trans_id]))

    return render(request, 'transactions/checkout.html', {'trans_id': trans_id} )



@login_required
def checkout_confirmation(request, trans_id):

    if request.method == 'POST':
        bank = request.POST.get('bank')
        teller_name = request.POST.get('teller_name')
        amount_paid = request.POST.get('amount_paid')
        file = request.FILES.get('file')
        bank_reference = request.POST.get('amount_paid')

        if file:
            fs = FileSystemStorage()
            fs.save(file.name, file)

        trans = Transaction.objects.get(id=trans_id)

        # incase of a subsequent or additional payment
        if trans.bank or trans.teller_name or trans.amount_paid:
            new_trans = Transaction.objects.create(
                                        listing = trans.listing,
                                        user = request.user,
                                        amount_to_pay = trans.amount_to_pay, 
                                        status = Transaction.PROCESSING,
                                        bank = bank,
                                        teller_name = teller_name,
                                        amount_paid = amount_paid,
                                        file=file
                                        )
        else:  
            # first payment made                              
            trans.bank = bank
            trans.teller_name = teller_name
            trans.bank_reference = bank_reference
            trans.status = Transaction.PROCESSING
            trans.file = file
            trans.amount_paid += Decimal(amount_paid)
            trans.save()
        return redirect(reverse('transactions:payment_success', args=[trans.listing.id]))

    return render(request, 'transactions/checkout_confirmation.html', {'trans_id': trans_id})


@login_required
def payment_success(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'transactions/payment_success.html', {'listing': listing})


def invoice(request, listing_id):

    trans = Transaction.objects.filter(listing_id=listing_id, user=request.user, status__in=[Transaction.SUBMITTED, Transaction.PROCESSING, Transaction.CONFIRMED])
    last_trans = trans.last()
    listing = last_trans.listing
    sum_paid = trans.aggregate(Sum('amount_paid'))['amount_paid__sum']
    balance = listing.price - sum_paid
    context = {
        "listing": listing,
        "sum_paid": sum_paid,
        "last_trans": last_trans,
        "balance": balance,
    }
    return render(request, 'transactions/invoice.html', context)


def test(request):
    return render(request, 'transactions/dashboard_payment_success.html')
