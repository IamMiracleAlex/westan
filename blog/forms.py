from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    body = forms.TextField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Question
        fields = '__all__'