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

