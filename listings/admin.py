from django.contrib import admin

from listings.models import Listing
from listings.forms import ListingAdminForm




@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    form = ListingAdminForm
    
    list_display = ('reference','title', 'status', 'availability', 'type','views','state', 'featured','created_at', 'updated_at')
    list_filter = ('status', 'availability','featured', 'type')
    search_fields = ('title', 'reference')
    date_hierarchy = 'created_at'
    exclude = ['slug', 'views', 'reference']
