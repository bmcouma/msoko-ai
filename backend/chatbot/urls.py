from django.urls import path, include

from .views import (
    PreferenceView,
    ThreadDetailView,
    ThreadListCreateView,
    MessageListCreateView,
    chat_view,
    chat_stream_view,
    BusinessProfileView,
    DashboardView,
    GoalListCreateView,
    DocumentListCreateView,
    MemoryClearView,
    # Legacy session-based auth views (kept for backwards compat)
    RegisterView,
    LoginView,
    LogoutView,
    SessionView,
    PasswordResetRequestView,
)

urlpatterns = [
    # ── JWT Auth via dj-rest-auth (preferred for PWA / mobile) ──────────────
    # POST /api/auth/registration/  — register with first_name, last_name, email, password
    # POST /api/auth/login/         — returns access + refresh JWT cookies
    # POST /api/auth/logout/        — clears JWT cookies
    # POST /api/auth/token/refresh/ — refresh access token
    # POST /api/auth/password/reset/ — initiate password reset
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),

    # ── Legacy session-based auth (kept for Django admin & fallback) ─────────
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login-session/", LoginView.as_view(), name="login-session"),
    path("auth/logout-session/", LogoutView.as_view(), name="logout-session"),
    path("auth/session/", SessionView.as_view(), name="session"),
    path("auth/password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),

    # ── Chat ────────────────────────────────────────────────────────────────
    path("chat/", chat_view, name="chat"),
    path("stream/", chat_stream_view, name="chat-stream"),

    # ── Threads ─────────────────────────────────────────────────────────────
    path("threads/", ThreadListCreateView.as_view(), name="threads"),
    path("threads/<int:thread_id>/", ThreadDetailView.as_view(), name="thread-detail"),
    path(
        "threads/<int:thread_id>/messages/",
        MessageListCreateView.as_view(),
        name="thread-messages",
    ),

    # ── User Data ───────────────────────────────────────────────────────────
    path("preferences/", PreferenceView.as_view(), name="preferences"),
    path("profile/", BusinessProfileView.as_view(), name="business-profile"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("goals/", GoalListCreateView.as_view(), name="goals"),
    path("documents/", DocumentListCreateView.as_view(), name="documents"),
    path("memory/clear/", MemoryClearView.as_view(), name="memory-clear"),
]
