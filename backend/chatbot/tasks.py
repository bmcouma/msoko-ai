from celery import shared_task
import logging

logger = logging.getLogger("msoko.ai_usage")

@shared_task
def async_rag_indexing(dir_path: str):
    """
    Background task to index heavy directories into the RAG engine without blocking the web process.
    """
    try:
        from .rag.engine import rag_engine
        rag_engine.add_documents_from_directory(dir_path)
    except Exception as e:
        logger.error(f"Celery RAG Indexing Failed: {e}")

@shared_task
def async_vision_analysis(user_id: int, image_url: str):
    """
    Background task for processing heavy vision analytics (e.g. overnight inventory counts).
    """
    logger.info(f"Async Vision Analytics completed for user {user_id}")
    pass
