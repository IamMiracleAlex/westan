from django.contrib import admin

from utils.handlers import ExportCsvMixin
from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin, ExportCsvMixin):

    actions = ["export_as_csv"] 
    date_hierarchy = 'created_at'
    ExportCsvMixin.export_as_csv.short_description = 'Export selected items to csv'

    list_display = ('reference','account_owner','listing','payment_type','teller_name', 'phone', 'price', 'amount_to_pay', 'amount_paid','status', 
                'bank',  'created_at', 'updated_at',)
    list_filter = ('status', 'payment_type', 'bank')
   
    search_fields = ('user__email', 'teller_name', 'reference')
    ordering = ('-created_at',)
    raw_id_fields = ['listing', 'user']


    def account_owner(self, obj):
        return obj.user.full_name()

    def phone(self, obj):
        return obj.user.phone

    def price(self, obj):
        return obj.listing.price

