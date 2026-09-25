from rest_framework import serializers

from .models import Business, Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "icon", "description")


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug", "category")


class BusinessCardSerializer(serializers.ModelSerializer):
    """
    The business card shown in lists and in AI result cards.
    Lean: name, tagline, category, location, logo, slug.
    """

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Business
        fields = (
            "id",
            "name",
            "slug",
            "tagline",
            "logo",
            "category",
            "location",
            "is_verified",
        )


class BusinessSerializer(serializers.ModelSerializer):
    """
    Full business detail. Used on the business profile page.
    """

    category = CategorySerializer(read_only=True)
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    community_slugs = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = (
            "id",
            "name",
            "slug",
            "tagline",
            "description",
            "category",
            "sub_categories",
            "location",
            "website",
            "contact_email",
            "contact_phone",
            "whatsapp",
            "logo",
            "cover_image",
            "photos",
            "instagram",
            "linkedin",
            "twitter",
            "visibility",
            "is_active",
            "is_verified",
            "owner_username",
            "community_slugs",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "slug",
            "owner_username",
            "community_slugs",
            "created_at",
            "updated_at",
        )

    def get_community_slugs(self, obj):
        return list(obj.communities.values_list("slug", flat=True))


class BusinessWriteSerializer(serializers.ModelSerializer):
    """
    Used for create / update by the owner.
    Only the safe, member-editable fields.
    """

    class Meta:
        model = Business
        fields = (
            "name",
            "tagline",
            "description",
            "location",
            "website",
            "contact_email",
            "contact_phone",
            "whatsapp",
            "logo",
            "cover_image",
            "photos",
            "instagram",
            "linkedin",
            "twitter",
            "category",
            "sub_categories",
        )