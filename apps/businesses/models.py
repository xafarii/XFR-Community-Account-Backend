from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Top-level business category. e.g. 'Branding & Creative'.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    """
    Optional finer-grained category. e.g. 'Logo Design' under 'Branding & Creative'.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("category", "name")
        verbose_name_plural = "Subcategories"
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.category.name} › {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Business(models.Model):
    """
    A business record. Can belong to zero or more Communities.
    Feeds AI retrieval in Phase 2.
    """

    VISIBILITY_CHOICES = [
        ("community", "Community only"),
        ("cross_community", "Visible to other communities"),
        ("platform", "Visible platform-wide"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_businesses",
    )
    communities = models.ManyToManyField(
        "communities.Community",
        related_name="businesses",
        blank=True,
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="businesses",
    )
    sub_categories = models.ManyToManyField(
        SubCategory,
        blank=True,
        related_name="businesses",
    )

    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)

    logo = models.URLField(blank=True)
    cover_image = models.URLField(blank=True)
    photos = models.JSONField(default=list, blank=True)

    instagram = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="community",
    )
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:260]
            slug = base
            n = 1
            while Business.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)