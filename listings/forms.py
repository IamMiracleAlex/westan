from django import forms

from ckeditor.widgets import CKEditorWidget
from django_google_maps.widgets import GoogleMapsAddressWidget

from listings.models import Listing



class ListingAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Listing
        fields = '__all__'



class ListingMapForm(forms.ModelForm):

    class Meta(object):
        model = Listing
        fields = ['address', 'geolocation']
        widgets = {
            "address": GoogleMapsAddressWidget,
        }
