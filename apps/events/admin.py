from django.contrib import admin
from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "community", "starts_at", "location", "is_published")
    list_filter = ("community", "is_published", "is_free")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventRegistrationInline]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "status", "registered_at")
    list_filter = ("status", "event")