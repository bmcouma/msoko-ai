"""
URL configuration for msoko_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Simple home view for root "/"
def home(request):
    return JsonResponse({"message": "Welcome to Msoko AI Backend"})

def health(request):
    """Lightweight liveness probe."""
    return JsonResponse({"status": "ok"})

def ready(request):
    """Readiness probe (extend with DB checks if needed)."""
    return JsonResponse({"status": "ready"})

from django.conf import settings
from django.conf.urls.static import static
from chatbot.views import home_view, services_view, terms_view, privacy_view

urlpatterns = [
    path('', home_view, name='home'),  # serves the professional frontend
    path('services/', services_view, name='services'), # Teklini Authority Hub
    path('terms/', terms_view, name='terms'), # Legal
    path('privacy/', privacy_view, name='privacy'), # Privacy
    path('healthz/', health, name="healthz"),
    path('readyz/', ready, name="readyz"),
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
