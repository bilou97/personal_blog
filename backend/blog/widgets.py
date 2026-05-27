from django.forms import Textarea

_TOASTUI = "blog/admin/toastuieditor"


class ToastUIEditorWidget(Textarea):
    class Media:
        css = {"all": (
            f"{_TOASTUI}/toastui-editor.min.css",
            "blog/admin/editor_admin.css",
        )}
        js = (
            f"{_TOASTUI}/toastui-editor-all.min.js",
            "blog/admin/editor_init.js",
        )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "toastuieditor-target"
        super().__init__(*args, **kwargs)
