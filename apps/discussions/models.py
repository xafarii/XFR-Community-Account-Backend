from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    A discussion post inside a community feed.
    Simple: text-first, with optional image.
    """

    KIND_CHOICES = [
        ("update", "Update"),
        ("announcement", "Announcement"),
        ("question", "Question"),
        ("poll", "Poll"),
        ("wins", "Wins" ),
        ("advice", "Advice"),
        ("general", "General"),
    ]

    community = models.ForeignKey(
        "communities.Community",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="update")
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    image = models.URLField(blank=True)

    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title or f"Post by {self.author} in {self.community.slug}"




class Comment(models.Model):
    """
    A reply on a post.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"