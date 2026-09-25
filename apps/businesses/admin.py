from django.contrib import admin
from .models import Category, SubCategory, Business


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "location",
        "visibility",
        "is_active",
        "is_verified",
    )
    list_filter = ("category", "visibility", "is_active", "is_verified")
    search_fields = ("name", "description", "location")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("communities", "sub_categories")