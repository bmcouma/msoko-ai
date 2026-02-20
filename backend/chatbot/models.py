from django.conf import settings
from django.db import models


class ChatThread(models.Model):
    """A conversation container owned by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads",
        null=True, blank=True
    )
    title = models.CharField(max_length=255, default="New chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.title} ({self.user})"


class ChatMessage(models.Model):
    """A message in a thread. Can be text or media-backed."""

    ROLE_CHOICES = [
        ("user", "User"),
        ("ai", "AI"),
        ("system", "System"),
    ]

    KIND_CHOICES = [
        ("text", "Text"),
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Video"),
        ("file", "File"),
    ]

    thread = models.ForeignKey(
        ChatThread, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    content = models.TextField(blank=True)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default="text")
    media_url = models.TextField(blank=True) # Changed from URLField
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.role}: {self.content[:40]}"


class BusinessProfile(models.Model):
    """Detailed profile of the user's business for precision coaching."""
    
    SECTOR_CHOICES = [
        ("retail", "Retail / Kiosk"),
        ("services", "Services (Boda, Salon, etc.)"),
        ("wholesale", "Wholesale / Mitumba"),
        ("agri", "Agribusiness"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_profile"
    )
    business_name = models.CharField(max_length=255, blank=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default="retail")
    location = models.CharField(max_length=255, help_text="e.g. Gikomba, CBD, Eastleigh", blank=True)
    inventory_size = models.CharField(max_length=50, blank=True)
    monthly_revenue_target = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.business_name} ({self.user.username})"

class UserPreference(models.Model):
    """Per-user personalization settings."""

    THEME_CHOICES = [
        ("system", "System"),
        ("light", "Light"),
        ("dark", "Dark"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences"
    )
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="system")
    language = models.CharField(max_length=10, default="en")
    tone = models.CharField(max_length=32, default="friendly")
    tts_enabled = models.BooleanField(default=False)
    voice_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Preferences for {self.user}"


class BusinessGoal(models.Model):
    """User-defined targets (Revenue, Inventory, etc.)"""
    
    GOAL_TYPES = [
        ("revenue", "Revenue Target"),
        ("inventory", "Inventory Milestone"),
        ("savings", "Savings Goal"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=255)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, default="revenue")
    target_value = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.get_goal_type_display()}: {self.title}"


class BusinessDocument(models.Model):
    """Uploaded records (Excel, CSV, PDF) for AI analysis."""
    
    DOC_TYPES = [
        ("sales", "Sales Record"),
        ("inventory", "Inventory List"),
        ("expenses", "Expense Sheet"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="business_docs/%Y/%m/%d/")
    name = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default="sales")
    summary = models.TextField(blank=True, help_text="AI-generated summary of the data")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_doc_type_display()})"
