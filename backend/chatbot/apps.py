import sys
from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"

    def ready(self):
        # Only run on actual server startup, not migrations
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv or any('wsgi' in arg for arg in sys.argv):
            try:
                from .rag.engine import rag_engine
                from pathlib import Path
                data_dir = str(Path(__file__).resolve().parent / 'rag' / 'data')
                rag_engine.add_documents_from_directory(data_dir)
            except Exception as e:
                import logging
                logging.getLogger("msoko.ai_usage").error(f"Failed to seed RAG docs: {e}")
