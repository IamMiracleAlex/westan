from django import forms

from ckeditor.widgets import CKEditorWidget

from listings.models import Listing



class ListingAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Listing
        fields = '__all__'

