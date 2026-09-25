from django.conf import settings
from django.db import models


class Conversation(models.Model):
    """
    An AI chat thread. Scoped to a user and (optionally) a community.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    community = models.ForeignKey(
        "communities.Community",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversations",
        help_text="If set, the conversation is community-scoped.",
    )
    title = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title or f"Conversation #{self.pk}"


class Message(models.Model):
    """
    One message in a conversation.
    Role = 'user' | 'assistant' | 'system'.
    For assistant messages, `entities` holds structured result cards.
    """

    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    content = models.TextField(blank=True)

    # Structured payload for assistant messages:
    # [{"type": "business", "id": 12, "name": "BrandHaus", ...}, ...]
    entities = models.JSONField(default=list, blank=True)

    # Optional: for debugging — what query was run, how many candidates
    meta = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}"