from django.db import models

from listings.models import Listing
from users.models import User
from utils.tools import generate_unique_id


class Transaction(models.Model):
    TRANSFER, DEPOSIT  = 0, 1
    PAYMENT_CHOICES = (
        (TRANSFER, 'Bank Transfer'),
        (DEPOSIT, 'Bank Deposit'),  
    )
    ZENITH, FIDELITY, ACCESS = 0, 1, 2
    BANK_CHOICES = (
        (ZENITH, 'Zenith Bank'),
        (FIDELITY, 'Fidelity Bank'),
        (ACCESS, 'Access Bank'), 
    )
    SUBMITTED, PROCESSING, PAID, ALLOCATED = 0, 1, 2, 4
    STATUS_CHOICES = (
        (SUBMITTED, 'Submitted'),
        (PROCESSING, 'Processing'),
        (PAID, 'Paid'),
        (ALLOCATED, 'Allocated'),
    )
    file = models.FileField(upload_to='transactions', verbose_name='Teller Image/File', null=True, blank=True)
    teller_name = models.CharField(max_length=50, null=True, blank=True)
    bank_reference = models.CharField(max_length=50, unique=True, null=True, blank=True)
    bank = models.PositiveSmallIntegerField(choices=BANK_CHOICES, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_CHOICES, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    amount_to_pay = models.DecimalField(
		default=0.00,
		decimal_places=2,
		max_digits=12,
	)
    amount_paid = models.DecimalField(
		default=0.00,
		decimal_places=2,
		max_digits=12,
	)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference = generate_unique_id(Listing, 'reference', len=10)

        super().save(*args, **kwargs)


    def confirm(self):
        # change status and email user
        pass

    def reject(self):
        # change status and email user
        pass

    def notify_admins(self):
        # notify admins of a payment
        pass