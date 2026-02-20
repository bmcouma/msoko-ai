import json
from pathlib import Path
from typing import Dict, Any, Optional

class KnowledgeStore:
    def __init__(self):
        self.kb_path = Path(__file__).parent / "knowledge_base.json"
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        try:
            with open(self.kb_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return {}

    def query(self, query_text: str) -> Optional[str]:
        """
        Refined tag-based retrieval for V3.
        """
        query_text = query_text.lower()
        context_parts = []
        
        # Tag Mapping
        tag_map = {
            "price": ["nairobi_cbd", "gikomba_wholesale"],
            "cost": ["nairobi_cbd"],
            "trend": ["market_trends"],
            "market": ["market_trends", "gikomba_wholesale"],
            "credit": ["business_advice"],
            "debt": ["business_advice"],
            "marketing": ["marketing_tips"],
            "sell": ["marketing_tips"],
            "growth": ["scaling_wisdom"],
            "scale": ["scaling_wisdom"],
            "mitumba": ["gikomba_wholesale"]
        }

        found_keys = set()
        for tag, keys in tag_map.items():
            if tag in query_text:
                for k in keys: found_keys.add(k)

        for k in found_keys:
            val = self.data.get(k)
            if val:
                context_parts.append(f"{k.replace('_', ' ').title()}: {val}")

        if not context_parts:
            # Fallback advice
            return f"Business Advice: {self.data.get('business_advice')}"
            
        return "\n".join(context_parts)

# Singleton
knowledge_store = KnowledgeStore()
