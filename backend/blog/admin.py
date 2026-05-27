from django.contrib import admin
from django.utils import timezone

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "statut", "published_at", "created_at"]
    list_filter = ["published", "category", "tags"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    filter_horizontal = ["tags"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        (None, {"fields": ["title", "slug", "category", "tags", "cover_image"]}),
        ("Contenu", {"fields": ["excerpt", "content"]}),
        (
            "Publication",
            {
                "fields": ["published", "published_at"],
                "description": (
                    "Pour <strong>planifier</strong> un article : définir une date future dans "
                    "<em>published_at</em> et laisser <em>published</em> décoché. "
                    "Le système publiera automatiquement à l'heure prévue."
                ),
            },
        ),
        (
            "Métadonnées",
            {"fields": ["created_at", "updated_at"], "classes": ["collapse"]},
        ),
    ]

    @admin.display(description="Statut")
    def statut(self, obj):
        if obj.published:
            return "✓ Publié"
        if obj.published_at and obj.published_at > timezone.now():
            return f"⏱ {obj.published_at.strftime('%d.%m %H:%M')}"
        return "— Brouillon"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "approved", "created_at"]
    list_filter = ["approved"]
    list_editable = ["approved"]
    search_fields = ["content", "author__username"]
