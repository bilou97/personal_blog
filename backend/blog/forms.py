from django import forms

from .models import Post, SiteConfig
from .widgets import ToastUIEditorWidget


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {"content": ToastUIEditorWidget()}


class SiteConfigAdminForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = "__all__"
        widgets = {"bio_content": ToastUIEditorWidget()}
