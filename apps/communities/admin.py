from django.contrib import admin
from .models import Community, CommunityModule


class CommunityModuleInline(admin.TabularInline):
    model = CommunityModule
    extra = 0


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "member_count")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CommunityModuleInline]


@admin.register(CommunityModule)
class CommunityModuleAdmin(admin.ModelAdmin):
    list_display = ("community", "key", "is_active", "order")
    list_filter = ("community", "is_active", "key")