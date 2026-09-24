from django.contrib import admin
from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "community", "role", "status", "joined_at")
    list_filter = ("community", "role", "status")
    search_fields = ("user__username", "user__email", "community__name")