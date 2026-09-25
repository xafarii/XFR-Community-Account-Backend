from rest_framework import serializers

from .models import Community, CommunityModule


class CommunityModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityModule
        fields = ("id", "key", "is_active", "order", "coming_soon_message")


class CommunitySerializer(serializers.ModelSerializer):
    """Full community detail — used on the community home page."""

    member_count = serializers.IntegerField(read_only=True)
    modules = CommunityModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = (
            "id",
            "name",
            "slug",
            "tagline",
            "description",
            "logo",
            "cover_image",
            "location",
            "is_active",
            "member_count",
            "modules",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CommunityBriefSerializer(serializers.ModelSerializer):
    """Lightweight — used in lists, memberships, business cards."""

    class Meta:
        model = Community
        fields = ("id", "name", "slug", "tagline", "logo")