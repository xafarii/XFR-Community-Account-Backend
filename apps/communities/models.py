# Create your models here.
from django.db import models
from django.utils.text import slugify


class Community(models.Model):
    """
    A tenant on the Xafarii platform.
    Founder's Weight is the first Community row.
    """

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    logo = models.URLField(blank=True)
    cover_image = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Communities"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140] or "community"

        super().save(*args, **kwargs)

        default_modules = [
            ("home", True, 0),
            ("members", True, 1),
            ("events", False, 2),
            ("businesses", False, 3),
            ("discussions", False, 4),
            ("shop", False, 5),
            ("jobs", False, 6),
            ("projects", False, 7),
            ("resources", False, 8),
        ]

        for key, is_active, order in default_modules:
            if not self.modules.filter(key=key).exists():
                self.modules.create(key=key, is_active=is_active, order=order)

    @property
    def member_count(self):
        return self.memberships.filter(status="active").count()



class CommunityModule(models.Model):
    """
    A module (Home, Members, Events, Businesses, Discussions,
    Shop, Jobs, Projects, Resources) enabled or disabled for a community.
    """

    MODULE_CHOICES = [
        ("home", "Home"),
        ("members", "Members"),
        ("events", "Events"),
        ("businesses", "Businesses"),
        ("discussions", "Discussions"),
        ("shop", "Shop"),
        ("jobs", "Jobs"),
        ("projects", "Projects"),
        ("resources", "Resources"),
    ]


    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="modules",
    )
    key = models.CharField(max_length=40, choices=MODULE_CHOICES)
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    coming_soon_message = models.CharField(
        max_length=200,
        blank=True,
        default="Coming soon",
    )

    class Meta:
        unique_together = ("community", "key")
        ordering = ["order", "key"]

    def __str__(self):
        state = "ON" if self.is_active else "OFF"
        return f"{self.community.slug} › {self.key} [{state}]"