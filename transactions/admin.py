from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages

from utils.handlers import ExportCsvMixin, send_transaction_status_email
from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin, ExportCsvMixin):

    actions = ["export_as_csv"] 
    date_hierarchy = 'created_at'
    ExportCsvMixin.export_as_csv.short_description = 'Export selected items to csv'

    list_display = ('reference','account_owner','listing','payment_type','teller_name', 'phone', 'price', 'amount_to_pay', 'amount_paid','status', 
                'bank',  'created_at', 'updated_at','custom_actions')
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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:id>/confirm/', self.admin_site.admin_view(self.confirm_payment), name='confirm_payment')
        ]
        return my_urls + urls

    def custom_actions(self, obj):
        # send notifications button
        return format_html(
            '<a class="button" href="{}">Confirm</a>',
            reverse('admin:confirm_payment', args=[obj.id])
        )
    
    custom_actions.short_description = 'Confirm Payment'

    def confirm_payment(self, request, id):

        trans = self.get_object(request, id)
        trans.status = Transaction.CONFIRMED
        trans.save()
        trans.refresh_from_db()

        send_transaction_status_email(trans)

        self.message_user(request, f'Success, Transaction with Reference: "{trans.reference}" was confirmed successfully.')
        return HttpResponseRedirect(reverse("admin:transactions_transaction_changelist"))
   