from decimal import Decimal

from django.db import models


class Transaction(models.Model):
    SUBMITTED, PROCESSING, SUCCESS, FAILED, CANCELED = range(5)
    TRANSACTION_STATUS = (
        (SUBMITTED, 'SUBMITTED'),
        (PROCESSING, 'PROCESSING'),
        (CANCELED, 'CANCELED'),
        (SUCCESS, 'SUCCESS'),
        (FAILED, 'FAILED'),
    )

    Deposit, Withdraw, Transfer, Payment, Interest = range(5)
    TRANSACTION_TYPES = (
        (Deposit, 'Deposit'),
        (Withdraw, 'Withdraw'),
        (Transfer, 'Transfer'),
        (Payment, 'Payment'),
        (Interest, 'Interest'),
    )

    type_of_transaction = models.PositiveSmallIntegerField(
		choices=TRANSACTION_TYPES,
		default=Deposit
	)
	status = models.PositiveSmallIntegerField(
		choices=TRANSACTION_STATUS,
		default=SUBMITTED
	)
	reference = models.CharField(max_length=50, unique=True, null=True, blank=True)
	amount = models.DecimalField(
		default=0.00,
		decimal_places=2,
		max_digits=12,
		validators=[MinValueValidator(Decimal('0.00'))]
	)
	
	# fee = models.DecimalField(
	# 	default=0.00,
	# 	decimal_places=2,
	# 	max_digits=12,
	# 	validators=[MinValueValidator(Decimal('0.00'))]
	# )
	total = models.DecimalField(
		default=0.00,
		decimal_places=2,
		max_digits=12,
		validators=[MinValueValidator(Decimal('0.00'))]
	)
	memo = models.CharField(max_length=200, null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
