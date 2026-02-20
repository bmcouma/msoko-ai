from django.contrib import admin
from .models import ChatThread, ChatMessage, BusinessProfile, UserPreference, BusinessGoal, BusinessDocument

# Custom Admin Branding
admin.site.site_header = "Msoko AI | Teklini Strategic Hub | Teklini Technologies"
admin.site.site_title = "Teklini Strategic Hub"
admin.site.index_title = "Strategic Hub Management"

@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "user__username")

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("thread", "role", "kind", "created_at")
    list_filter = ("role", "kind", "created_at")
    search_fields = ("content", "thread__title", "thread__user__username")

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "user", "sector", "location", "created_at")
    list_filter = ("sector", "created_at")
    search_fields = ("business_name", "user__username", "location")

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "language", "voice_enabled")
    list_filter = ("theme", "language")
    search_fields = ("user__username",)

@admin.register(BusinessGoal)
class BusinessGoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "goal_type", "target_value", "is_completed", "deadline")
    list_filter = ("goal_type", "is_completed", "deadline")
    search_fields = ("title", "user__username")

@admin.register(BusinessDocument)
class BusinessDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "doc_type", "created_at")
    list_filter = ("doc_type", "created_at")
    search_fields = ("name", "user__username")
