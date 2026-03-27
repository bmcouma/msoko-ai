import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# ─── Environment ──────────────────────────────────────────────────────────────
load_dotenv()  # loads backend/.env (or root .env when running via Docker)

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Security ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-fallback-change-in-production")
DEBUG = os.environ.get("DEBUG", "True").lower() in ("1", "true", "yes")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# ─── Application definition ───────────────────────────────────────────────────
INSTALLED_APPS = [
    "jazzmin",                          # Must be first — overrides Django admin templates
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",             # Required by allauth
    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Local
    "chatbot",
]

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",          # Must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",      # Static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",   # Required by allauth ≥0.56
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "chatbot.middleware.AIUsageMiddleware",           # Phase 1 observability
]

ROOT_URLCONF = "msoko_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "msoko_backend.wsgi.application"

# ─── Database ─────────────────────────────────────────────────────────────────
# Uses DATABASE_URL env var when set (production/Docker), otherwise SQLite (dev)
_DATABASE_URL = os.environ.get("DATABASE_URL")
if _DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(
            _DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─── Cache (Redis in production, in-memory in dev) ────────────────────────────
_REDIS_URL = os.environ.get("REDIS_URL")
if _REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": _REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }

# ─── Password validation ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Internationalization ─────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# ─── Static & Media files ─────────────────────────────────────────────────────
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── CORS ─────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Locked down in production
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if not DEBUG else []
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["*"]

# ─── Django REST Framework ────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # Kept for admin/browsable API
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}

# ─── SimpleJWT ────────────────────────────────────────────────────────────────
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,  # Enable if you add simplejwt.token_blacklist
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ─── dj-rest-auth ────────────────────────────────────────────────────────────
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "msoko-access",
    "JWT_AUTH_REFRESH_COOKIE": "msoko-refresh",
    "JWT_AUTH_HTTPONLY": True,        # Secure: JS can't access cookie
    "REGISTER_SERIALIZER": "chatbot.serializers.CustomRegisterSerializer",
}

# ─── django-allauth ───────────────────────────────────────────────────────────
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"  # Change to "mandatory" in production with email backend
ACCOUNT_UNIQUE_EMAIL = True

# ─── Email (for password reset / verification) ───────────────────────────────
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "Msoko AI <noreply@msoko.ai>")

# ─── Logging ──────────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
        "ai_usage": {
            "format": "[{asctime}] AI_USAGE {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "ai_usage_console": {
            "class": "logging.StreamHandler",
            "formatter": "ai_usage",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "chatbot": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "msoko.ai_usage": {              # Dedicated logger for AI call observability
            "handlers": ["ai_usage_console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# ─── Security hardening (production only) ────────────────────────────────────
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# ─── Teklini Strategic Hub — Premium Admin Theme ──────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "Teklini Strategic Hub",
    "site_header": "Msoko AI | Teklini Strategic Hub",
    "site_brand": "Teklini Technologies",
    "site_logo": "images/logo.png",
    "site_logo_classes": "img-circle",
    "site_icon": "images/logo.png",
    "welcome_sign": "Welcome to the Teklini Strategic Hub",
    "copyright": "© 2026 Teklini Technologies. All rights reserved.",
    "topmenu_links": [
        {"name": "🏠 Msoko AI", "url": "/", "new_window": False},
        {"name": "📊 Dashboard", "url": "admin:index"},
        {"name": "💬 WhatsApp", "url": "https://wa.me/254791832015", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "🌐 Live Site", "url": "/", "new_window": False, "icon": "fas fa-external-link-alt"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-shield-alt",
        "auth.user": "fas fa-user-tie",
        "auth.Group": "fas fa-users-cog",
        "chatbot.ChatThread": "fas fa-comments",
        "chatbot.ChatMessage": "fas fa-comment-dots",
        "chatbot.BusinessProfile": "fas fa-store",
        "chatbot.BusinessGoal": "fas fa-bullseye",
        "chatbot.BusinessDocument": "fas fa-file-alt",
        "chatbot.UserPreference": "fas fa-sliders-h",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
