# # from decimal import Decimal

# from django.db import models

# from listings.models import Listing
# from users.models import User

# class Transaction(models.Model):
#     TRANSFER, DEPOSIT  = range(2)
#     PAYMENT_CHOICES = (
#         (TRANSFER, 'Bank Transfer'),
#         (DEPOSIT, 'Bank Deposit'),  
#     )
#     ZENITH, FIDELITY, ACCESS = range(3)
#     BANK_CHOICES = (
#         (ZENITH, 'Zenith Bank'),
#         (FIDELITY, 'Fidelity Bank'),
#         (ACCESS, 'Access Bank'), 
#     )
#     SUBMITTED, PENDING, ALLOCATED = range(3)
#     TRANSACTION_CHOICES = (
#         (SUBMITTED, 'Submitted'),
#         (PENDING, 'Pending'),
#         (ALLOCATED, 'Allocated'), 
#     )
#     image = models.ImageField(upload_to='transactions', verbose_name='Teller Image')
#     teller_name = models.CharField(max_length=50, null=True, blank=True)
#     bank_reference = models.CharField(max_length=50, unique=True, null=True, blank=True)
#     bank_paid_to = models.PositiveSmallIntegerField(choices=BANK_CHOICES, default=ZENITH)
#     listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
#     payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_CHOICES, default=TRANSFER)
#     status = models.PositiveSmallIntegerField(choices=TRANSACTION_STATUS)
#     reference = models.CharField(max_length=50, null=True, blank=True)
#     amount = models.DecimalField(
# 		default=0.00,
# 		decimal_places=2,
# 		max_digits=12,
# 	)
#     memo = models.CharField(max_length=200, null=True, blank=True)
#     buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True)
    
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.reference = generate_unique_id(Listing, 'reference', len=10)

#         super().save(*args, **kwargs)
