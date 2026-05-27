import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, max_length=500)
    cover_image = models.ImageField(upload_to="posts/", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    views = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.cover_image:
            self._resize_cover_image()

    def _resize_cover_image(self, max_width=1200):
        try:
            path = self.cover_image.path
            img = Image.open(path)
            if img.width <= max_width:
                return
            ratio = max_width / img.width
            img = img.resize(
                (max_width, int(img.height * ratio)), Image.LANCZOS
            )
            ext = os.path.splitext(path)[1].lower()
            fmt_map = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
            fmt = fmt_map.get(ext, "JPEG")
            if fmt == "JPEG" and img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            save_kw = {"format": fmt}
            if fmt == "JPEG":
                save_kw.update({"quality": 85, "optimize": True})
            img.save(path, **save_kw)
        except Exception:
            pass

    def __str__(self):
        return self.title


class Reaction(models.Model):
    EMOJIS = [("like", "👍"), ("love", "❤️"), ("fire", "🔥")]
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="reactions"
    )
    emoji = models.CharField(max_length=10, choices=EMOJIS)
    ip_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("post", "emoji", "ip_hash")]

    def __str__(self):
        return f"{self.emoji} on {self.post.slug}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=2000)
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
