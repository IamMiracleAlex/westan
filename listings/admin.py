from django.contrib import admin

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from listings.models import Listing, WishList
from listings.forms import ListingAdminForm





@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    form = ListingAdminForm  
    
    list_display = ('reference','title','price', 'status', 'availability', 'type','views','state', 'featured','created_at', 'updated_at')
    list_filter = ('status', 'availability','featured', 'type')
    search_fields = ('title', 'reference')
    date_hierarchy = 'created_at'
    exclude = ['slug', 'views', 'reference']

    # formfield_overrides = {
    #     map_fields.AddressField: {
    #       'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    # }

@admin.register(WishList)
class WishList(admin.ModelAdmin):
    list_display = ('user','listing', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__first_name')
    date_hierarchy = 'created_at'
