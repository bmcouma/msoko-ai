import logging
from typing import Optional
from ..rag.engine import rag_engine

logger = logging.getLogger("msoko.ai_usage")

class MarketResearcherAgent:
    """Queries the local ChromaDB RAG for market trends and localized pricing."""
    def analyze(self, query: str) -> str:
        logger.info("Agent Routing: MarketResearcherAgent activated")
        context = rag_engine.query(query)
        if context:
            return f"MARKET RESEARCH DATA:\n{context}"
        return ""

class GoalCoachAgent:
    """Queries the Django DB for user milestones and formulates accountability context."""
    def analyze(self, user_id: int) -> str:
        try:
            from ..models import BusinessGoal
            goals = BusinessGoal.objects.filter(user_id=user_id, is_completed=False)
            if not goals.exists():
                return "GOAL COACH DATA: The user currently has no active business goals. Suggest setting a revenue or inventory milestone."
            
            goal_summaries = []
            for g in goals:
                goal_summaries.append(f"- {g.title}: Target {g.target_value}, currently at {g.progress}%.")
            
            logger.info("Agent Routing: GoalCoachAgent activated")
            return "GOAL COACH DATA (Current User Milestones):\n" + "\n".join(goal_summaries)
        except Exception as e:
            logger.error(f"GoalCoachAgent error: {e}")
            return ""

class VisionAnalystAgent:
    """Analyzes base64 image strings to provide visual context."""
    def analyze(self, image_data: Optional[str]) -> str:
        if not image_data:
            return ""
            
        logger.info("Agent Routing: VisionAnalystAgent activated")
        return (
            "VISION ANALYST INSTRUCTIONS: The user has attached an image of their inventory, storefront, or product. "
            "Please analyze the visual data carefully to provide actionable counts, pricing strategies, or restock advice "
            "specific to their localized business."
        )
