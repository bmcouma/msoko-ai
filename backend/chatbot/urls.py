from django.urls import path

from .views import (
    PreferenceView,
    ThreadDetailView,
    ThreadListCreateView,
    MessageListCreateView,
    chat_view,
    chat_stream_view,
    home_view,
    BusinessProfileView,
    DashboardView,
    GoalListCreateView,
    DocumentListCreateView,
)

urlpatterns = [
    path("chat/", chat_view, name="chat"),
    path("stream/", chat_stream_view, name="chat-stream"),
    path("threads/", ThreadListCreateView.as_view(), name="threads"),
    path("threads/<int:thread_id>/", ThreadDetailView.as_view(), name="thread-detail"),
    path(
        "threads/<int:thread_id>/messages/",
        MessageListCreateView.as_view(),
        name="thread-messages",
    ),
    path("preferences/", PreferenceView.as_view(), name="preferences"),
    path("profile/", BusinessProfileView.as_view(), name="business-profile"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("goals/", GoalListCreateView.as_view(), name="goals"),
    path("documents/", DocumentListCreateView.as_view(), name="documents"),
]
