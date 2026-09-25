from django.shortcuts import render

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from communities.models import Community
from .models import Membership


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def onboard(request):
    """
    Onboard the current user into a community.

    Body:
        {
            "community_slug": "founders-weight",   (optional — defaults to founders-weight)
            "full_name": "...",
            "role": "...",
            "company": "...",
            "location": "...",
            "bio": "...",
            "interests": ["...", "..."],           (optional)
            "photo": "https://...",                (optional)
            "linkedin_url": "https://...",         (optional)
            "website_url": "https://...",          (optional)
        }

    Returns: profile + membership.
    """
    community_slug = request.data.get("community_slug") or "founders-weight"

    try:
        community = Community.objects.get(slug=community_slug, is_active=True)
    except Community.DoesNotExist:
        return Response(
            {"error": f"Community '{community_slug}' not found or inactive"},
            status=status.HTTP_404_NOT_FOUND,
        )

    with transaction.atomic():
        profile = request.user.profile

        # Update profile fields from the request (only those provided)
        for field in (
            "full_name",
            "role",
            "company",
            "location",
            "bio",
            "photo",
            "linkedin_url",
            "website_url",
        ):
            if field in request.data:
                setattr(profile, field, request.data.get(field) or "")

        if "interests" in request.data:
            interests = request.data.get("interests") or []
            if isinstance(interests, list):
                profile.interests = interests

        profile.save()

        membership, created = Membership.objects.get_or_create(
            user=request.user,
            community=community,
            defaults={"role": "member", "status": "active"},
        )

    return Response(
        {
            "profile": ProfileSerializer(profile).data,
            "membership": {
                "id": membership.id,
                "community": {
                    "id": community.id,
                    "name": community.name,
                    "slug": community.slug,
                    "tagline": community.tagline,
                    "logo": community.logo,
                },
                "role": membership.role,
                "status": membership.status,
                "joined_at": membership.joined_at,
                "created": created,
            },
        },
        status=status.HTTP_200_OK,
    )
