from django import forms

from blog.models import Post

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    body = forms.TextField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'