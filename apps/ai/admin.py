from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("role", "content", "entities", "meta", "created_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "community", "title", "updated_at")
    list_filter = ("community",)
    search_fields = ("title", "user__username")
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "role", "created_at", "short_content")
    list_filter = ("role",)

    @admin.display(description="content")
    def short_content(self, obj):
        return obj.content[:60]