from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, UserBriefSerializer


def _tokens_for_user(user):
    """Return access + refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new account.
    Body:
        {
            "email": "...",
            "password": "...",
            "username": "...",   (optional — falls back to email prefix)
            "full_name": "..."   (optional)
        }
    Returns: user, profile, tokens.
    """
    email = (request.data.get("email") or "").strip().lower()
    password = request.data.get("password") or ""
    username = (request.data.get("username") or "").strip()
    full_name = (request.data.get("full_name") or "").strip()

    if not email or not password:
        return Response(
            {"error": "email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email__iexact=email).exists():
        return Response(
            {"error": "An account with this email already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not username:
        username = email.split("@")[0]
        # ensure uniqueness
        base = username
        n = 1
        while User.objects.filter(username=username).exists():
            n += 1
            username = f"{base}{n}"

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "That username is taken"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        # Profile is auto-created by signal; fill in full_name if provided
        if full_name:
            profile = user.profile
            profile.full_name = full_name
            profile.save()

    tokens = _tokens_for_user(user)
    return Response(
        {
            "user": UserBriefSerializer(user).data,
            "profile": ProfileSerializer(user.profile).data,
            **tokens,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Login with email + password.
    Body: {"email": "...", "password": "..."}
    """
    email = (request.data.get("email") or "").strip().lower()
    password = request.data.get("password") or ""

    if not email or not password:
        return Response(
            {"error": "email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.check_password(password):
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return Response(
            {"error": "Account is inactive"},
            status=status.HTTP_403_FORBIDDEN,
        )

    tokens = _tokens_for_user(user)
    return Response(
        {
            "user": UserBriefSerializer(user).data,
            "profile": ProfileSerializer(user.profile).data,
            **tokens,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    Return the current user + profile.
    Used by the frontend on page load to restore session.
    """
    return Response(
        {
            "user": UserBriefSerializer(request.user).data,
            "profile": ProfileSerializer(request.user.profile).data,
        }
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the current user's profile.
    Body: any subset of ProfileUpdateSerializer fields.
    """
    serializer = ProfileUpdateSerializer(
        request.user.profile,
        data=request.data,
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(ProfileSerializer(request.user.profile).data)