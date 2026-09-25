from django.conf import settings
from django.db import models


class Event(models.Model):
    """
    A community event. Belongs to a Community.
    Optionally linked to a Business (e.g. hosted at a business).
    """

    community = models.ForeignKey(
        "communities.Community",
        on_delete=models.CASCADE,
        related_name="events",
    )
    business = models.ForeignKey(
        "businesses.Business",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        help_text="Optional. Set if the event is hosted by or at a business.",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_events",
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_online = models.BooleanField(default=False)
    online_url = models.URLField(blank=True)

    capacity = models.PositiveIntegerField(null=True, blank=True)
    is_free = models.BooleanField(default=True)
    price_note = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-starts_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.title)[:260] or "event"
            slug = base
            n = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)


class EventRegistration(models.Model):
    """
    Attendance record: user ↔ event.
    """

    STATUS_CHOICES = [
        ("registered", "Registered"),
        ("attended", "Attended"),
        ("cancelled", "Cancelled"),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="registered")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.user} → {self.event.title} ({self.status})"