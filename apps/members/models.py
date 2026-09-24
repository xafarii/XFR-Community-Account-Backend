from django.conf import settings
from django.db import models


class Membership(models.Model):
    """
    A person's membership in a community.
    User  ── Membership ──  Community
    """

    ROLE_CHOICES = [
        ("member", "Member"),
        ("admin", "Admin"),
        ("owner", "Owner"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending"),
        ("inactive", "Inactive"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    community = models.ForeignKey(
        "communities.Community",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "community")
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user} @ {self.community.slug} ({self.role})"
