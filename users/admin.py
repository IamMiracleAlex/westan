from django.contrib import admin

from utils.mixins import ExportCsvMixin
from users.models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):

    actions = ["export_as_csv"] 
    date_hierarchy = 'date_joined'
    ExportCsvMixin.export_as_csv.short_description = 'Export selected users to csv'

    list_display = ('first_name','last_name','email','phone','refered_by','refer_code', 
                'no_of_referrals', 'email_verified', 'is_client', 'is_marketer',
                'is_active', 'is_staff',  'created_at', 'updated_at',)
    list_filter = ('is_staff', 'is_active', 'is_client', 'is_marketer')
   
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    raw_id_fields = ['referer']


    def no_of_referrals(self, obj):
        return obj.referrals.all().count()

    def refered_by(self, obj):
        if obj.referer:
            return obj.referer.full_name()
        return None



@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['email', 'active', 'created_at', 'updated_at' ]
    list_filters = ['active', 'created_at']
    search_fields = ('email',)

    actions = ["export_as_csv"] 

