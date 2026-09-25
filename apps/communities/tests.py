from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.businesses.models import Business
from apps.communities.models import Community

User = get_user_model()


class CommunityModelTests(TestCase):
    def test_founders_weight_community_creates_default_modules(self):
        community = Community.objects.create(name="Founder's Weight")

        self.assertTrue(community.modules.filter(key="home").exists())
        self.assertTrue(community.modules.get(key="home").is_active)
        self.assertTrue(community.modules.filter(key="members").exists())

    def test_business_visibility_flags_are_supported(self):
        community = Community.objects.create(name="Lagos Circle")
        user = User.objects.create_user(username="owner", password="StrongPass123!")

        business = Business.objects.create(
            community=community,
            owner=user,
            name="Northwind Studio",
            slug="northwind-studio",
            show_cross_community=True,
            show_platform=True,
        )

        self.assertTrue(business.show_cross_community)
        self.assertTrue(business.show_platform)
