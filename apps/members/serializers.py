from rest_framework import serializers

from .models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    """
    Full membership record. Used on admin-ish views and the user's
    own membership list.
    """

    community = serializers.SerializerMethodField()
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Membership
        fields = (
            "id",
            "user",
            "user_username",
            "community",
            "role",
            "status",
            "joined_at",
        )
        read_only_fields = ("id", "user", "joined_at")

    def get_community(self, obj):
        return {
            "id": obj.community.id,
            "name": obj.community.name,
            "slug": obj.community.slug,
            "tagline": obj.community.tagline,
            "logo": obj.community.logo,
        }


class MemberCardSerializer(serializers.Serializer):
    """
    Shape of the member card shown in the Figma design:
    avatar, name, role, company, location, interest tags, short bio.
    Built manually from Profile + Membership — not a ModelSerializer
    because it composes across three models (User, Profile, Membership).
    """

    user_id = serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField(allow_blank=True)
    photo = serializers.CharField(allow_blank=True)
    role = serializers.CharField(allow_blank=True)
    company = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)
    interests = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    membership_role = serializers.CharField()
    joined_at = serializers.DateTimeField()