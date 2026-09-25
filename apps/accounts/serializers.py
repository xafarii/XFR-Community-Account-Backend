from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserBriefSerializer(serializers.ModelSerializer):
    """Minimal user info — used wherever we embed a user reference."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ProfileSerializer(serializers.ModelSerializer):
    """Full profile — used on the profile page and profile edit form."""

    user = UserBriefSerializer(read_only=True)
    primary_business = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "full_name",
            "photo",
            "role",
            "company",
            "location",
            "bio",
            "interests",
            "linkedin_url",
            "website_url",
            "primary_business",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at", "primary_business")

    def get_primary_business(self, obj):
        """
        The user's first active owned business, if any.
        Returned as a light dict — the full business serializer
        lives in the businesses app.
        """
        business = obj.user.owned_businesses.filter(is_active=True).first()
        if not business:
            return None
        return {
            "id": business.id,
            "name": business.name,
            "slug": business.slug,
            "tagline": business.tagline,
            "logo": business.logo,
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Used by PATCH /api/profile/ — allows editing but not user reassignment."""

    class Meta:
        model = Profile
        fields = (
            "full_name",
            "photo",
            "role",
            "company",
            "location",
            "bio",
            "interests",
            "linkedin_url",
            "website_url",
        )