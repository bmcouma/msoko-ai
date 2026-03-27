from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ChatThread, ChatMessage, UserPreference, BusinessProfile, BusinessGoal, BusinessDocument


class BusinessDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocument
        fields = ["id", "file", "name", "doc_type", "summary", "created_at"]
        read_only_fields = ["id", "summary", "created_at"]


class BusinessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessGoal
        fields = ["id", "title", "goal_type", "target_value", "current_value", "deadline", "is_completed"]


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = [
            "business_name",
            "sector",
            "location",
            "inventory_size",
            "monthly_revenue_target",
        ]


User = get_user_model()


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "thread",
            "role",
            "content",
            "kind",
            "media_url",
            "transcript",
            "created_at",
        ]
        read_only_fields = ["id", "thread", "role", "created_at"]


class ChatThreadSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatThread
        fields = ["id", "title", "created_at", "updated_at", "latest_message"]
        read_only_fields = ["id", "created_at", "updated_at", "latest_message"]

    def get_latest_message(self, obj):
        msg = obj.messages.order_by("-created_at").first()
        if not msg:
            return None
        return {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content[:200],
            "created_at": msg.created_at,
        }


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            "theme",
            "language",
            "tone",
            "tts_enabled",
            "voice_enabled",
        ]


# ─── dj-rest-auth Custom Registration Serializer ──────────────────────────────
# This adds first_name / last_name to the default allauth registration flow
# and auto-creates a BusinessProfile on first sign-up.

try:
    from dj_rest_auth.registration.serializers import RegisterSerializer

    class CustomRegisterSerializer(RegisterSerializer):
        first_name = serializers.CharField(max_length=150, required=True)
        last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

        def get_cleaned_data(self):
            data = super().get_cleaned_data()
            data["first_name"] = self.validated_data.get("first_name", "")
            data["last_name"] = self.validated_data.get("last_name", "")
            return data

        def save(self, request):
            user = super().save(request)
            user.first_name = self.validated_data.get("first_name", "")
            user.last_name = self.validated_data.get("last_name", "")
            user.save(update_fields=["first_name", "last_name"])
            # Auto-create a BusinessProfile for the new user
            BusinessProfile.objects.get_or_create(
                user=user,
                defaults={"business_name": f"{user.first_name}'s Venture"},
            )
            return user

except ImportError:
    # dj-rest-auth not installed yet — graceful fallback during migration
    pass
