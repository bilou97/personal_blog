from django import forms

from .models import Post
from .widgets import ToastUIEditorWidget


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {"content": ToastUIEditorWidget()}
