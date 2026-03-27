import os
import logging
import httpx
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Optional
import json
from ..rag.engine import rag_engine
from .workers import MarketResearcherAgent, GoalCoachAgent, VisionAnalystAgent

logger = logging.getLogger("msoko.ai_usage")

# Cost estimate per 1K tokens (USD) — ballpark for OpenRouter free tier
_COST_PER_1K = 0.0015

class MsokoAgent:
    """
    Core strategy engine for Msoko AI.
    Handles complex business logic and real-time strategic reasoning.
    """
    
    def __init__(self, model: str = "openrouter/free", api_key: Optional[str] = None):
        # Professional environment loading
        env_path = Path(__file__).resolve().parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.api_key = self.api_key.strip()
            
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://msoko-ai.vercel.app/",
            "X-Title": "Msoko AI",
            "Content-Type": "application/json"
        }
        
        # Initialize specialized agents
        self.market_agent = MarketResearcherAgent()
        self.goal_agent = GoalCoachAgent()
        self.vision_agent = VisionAnalystAgent()

    def generate_system_prompt(self, context: Optional[Dict] = None) -> str:
        """
        Generates the strategic core logic for the Senior Business Coach.
        Optimized for deep market analysis and sustainable growth guidance.
        """
        user_name = context.get("user_name", "User") if context else "User"
        
        # Deep User Context Injection
        personal_context = ""
        if context and "user_id" in context:
            uid = context["user_id"]
            # Basic profile info
            try:
                from ..models import BusinessProfile
                profile = BusinessProfile.objects.get(user_id=uid)
                personal_context += f"USER VENTURE: '{profile.business_name}' ({profile.get_sector_display()}) in {profile.location}.\n"
            except:
                pass
            
            # Goal Coach specialized injection
            goal_data = self.goal_agent.analyze(uid)
            if goal_data:
                personal_context += f"{goal_data}\n"

        prompt = (
            f"You are Msoko AI, an intelligent business assistant built by Teklini Technologies. "
            f"Your role is to act as a Senior Business Coach.\n"
            f"You are speaking to {user_name}.\n\n"
            f"{personal_context}\n"
            
            "MISSION & IDENTITY:\n"
            "Msoko AI helps entrepreneurs and growing businesses make smarter, data-driven decisions using structured reasoning and simple language. "
            "Your goal is to provide practical, sustainable growth guidance.\n\n"

            "STRATEGIC SCOPE:\n"
            "1. DIGITAL MONETIZATION: Advise on positioning and global selling for digital skills (engineering, design, creative).\n"
            "2. GLOBAL MARKET: Provide data-driven insights for both localized and international business landscapes.\n"
            "3. DECISION SUPPORT: Help business owners think clearly and act confidently.\n\n"

            "STRUCTURED REASONING (INTERNAL):\n"
            "1. RECALL: Identify user niche and current development stage.\n"
            "2. STRATEGIZE: Formulate the most effective, structured path for today's action.\n"
            "3. CHECK: Verify for professional clarity and simple English. Zero slang.\n\n"

            "STRICT OPERATING RULES:\n"
            "1. TONE: Professional, supportive, and direct. NO SLANG. NO UNNECESSARY HYPE.\n"
            "2. LANGUAGE: Clear, simple English only.\n"
            "3. REASONING: Always reason carefully before producing your final answer.\n"
            "4. INQUISITIVE: Ask one clarifying question if the context is broad to ensure practical value.\n"
            "5. OUTPUT: Concise, structured, and professional. Max 150 words.\n\n"
            
            "SUGGESTED FOLLOW-UPS:\n"
            "At the very end of your response, always provide 2-3 short 'Quick Reply' options in brackets:\n"
            "[Question 1] [Question 2] [Question 3]\n\n"
            
            "EXAMPLE:\n"
            "User: 'How do I sell my coding skills?'\n"
            "Response: 'Establish a portfolio on platforms like GitHub or Upwork. Target international clients by specializing in niche frameworks like React or Django. \n\nWhat specific programming languages or frameworks do you specialize in?'\n"
            "[How to find international clients?] [Review my GitHub profile] [Pricing strategies for freelancers]\n"
        )

        # Vision Logic: Visual Strategic Analysis
        if context and context.get("is_multimodal"):
            v_context = self.vision_agent.analyze("placeholder_image_trigger")
            prompt += f"\n\n{v_context}"

        # Core Logic: Real-time Market Access
        if context and context.get("search_enabled"):
            prompt += (
                "\n\nMARKET INTELLIGENCE (ACTIVE):\n"
                "- You have access to real-time global trends and business news.\n"
                "- Cross-reference internal logic with live market conditions.\n"
                "- Cite specific market trends when providing time-sensitive advice."
            )
            
        return prompt

    def get_response(self, user_message: str, history: Optional[List[Dict[str, str]]] = None, context: Optional[Dict] = None, image_data: Optional[str] = None) -> str:
        """
        Synchronous call to get AI response with optional image support.
        """
        if not self.api_key:
            return "Error: OPENAI_API_KEY not found in environment."

        # Multi-Agent Routing Context Gathering
        market_context = self.market_agent.analyze(user_message)
        
        system_content = self.generate_system_prompt(context)
        if market_context:
            system_content += f"\n\n{market_context}"

        messages = [{"role": "system", "content": system_content}]
        if history: messages.extend(history)
        
        # User message construct
        if image_data:
             try:
                header, base64_data = image_data.split(';base64,')
                mime_type = header.split(':')[-1]
                user_msg_content = [
                    {"type": "text", "text": user_message or "Analyze this image."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_data}"}}
                ]
             except: user_msg_content = user_message
        else:
            user_msg_content = user_message

        messages.append({"role": "user", "content": user_msg_content})

        body = {
            "model": self.model, 
            "messages": messages, 
            "temperature": 0.5,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(self.base_url, headers=self.headers, json=body)
                response.raise_for_status()
                result = response.json()
                usage = result.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)
                total_tokens = prompt_tokens + completion_tokens
                cost_usd = (total_tokens / 1000) * _COST_PER_1K
                logger.info(
                    f"mode=sync model={self.model} "
                    f"prompt_tokens={prompt_tokens} completion_tokens={completion_tokens} "
                    f"total_tokens={total_tokens} est_cost_usd={cost_usd:.6f}"
                )
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"OpenRouter sync error: {e}")
            return f"System Error: {str(e)}"

    def get_streaming_response(self, user_message: str, history: Optional[List[Dict[str, str]]] = None, context: Optional[Dict] = None, image_data: Optional[str] = None):
        """
        Generator for streaming AI response (SSE ready) with Multimodal support.
        """
        if not self.api_key:
            yield "Error: OPENAI_API_KEY not found."
            return

        # Multi-Agent Routing Context Gathering
        market_context = self.market_agent.analyze(user_message)
        
        system_content = self.generate_system_prompt(context)
        if market_context:
            system_content += f"\n\n{market_context}"

        messages = [{"role": "system", "content": system_content}]
        if history: messages.extend(history)
        
        # Construct User Message (Multimodal if image present)
        if image_data:
            # Extract mime-type and base64 string
            try:
                # Expected format: data:image/png;base64,...
                header, base64_data = image_data.split(';base64,')
                mime_type = header.split(':')[-1]
                
                user_msg_content = [
                    {"type": "text", "text": user_message or "Analyze this image for my business."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_data}"
                        }
                    }
                ]
            except Exception as e:
                user_msg_content = user_message # Fallback
        else:
            user_msg_content = user_message

        messages.append({"role": "user", "content": user_msg_content})

        body = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.5,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5,
            "stream": True
        }
        
        # If we have an image, we might want to use a vision model automatically
        if image_data and self.model == "openrouter/free":
            # Some free models don't support vision, fallback to a known good one if possible
            # But let's stick to the user's intent or openrouter/free for now.
            pass

        token_count = 0
        try:
            with httpx.stream("POST", self.base_url, headers=self.headers, json=body, timeout=60.0) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            delta = data_json["choices"][0].get("delta", {}).get("content", "")
                            if delta:
                                token_count += 1  # Approximate: 1 delta chunk ≈ 1-3 tokens
                                yield delta
                        except:
                            continue
            # Log after stream completes
            est_cost = (token_count / 1000) * _COST_PER_1K
            logger.info(
                f"mode=stream model={self.model} "
                f"approx_chunks={token_count} est_cost_usd={est_cost:.6f}"
            )
        except Exception as e:
            logger.error(f"OpenRouter stream error: {e}")
            yield f"Vision/Streaming Error: {str(e)}"


# Singleton instance for easy access
default_agent = MsokoAgent()

def get_msoko_response(user_message: str, history: Optional[List[Dict[str, str]]] = None, user_id: Optional[int] = None, image_data: Optional[str] = None, context: Optional[Dict] = None, search_enabled: bool = False) -> str:
    """
    Convenience function to get a non-streaming response.
    """
    ctx = context or {}
    if user_id:
        ctx["user_id"] = user_id
    if image_data:
        ctx["is_multimodal"] = True
    if search_enabled:
        ctx["search_enabled"] = True
    return default_agent.get_response(user_message, history=history, context=ctx, image_data=image_data)

def get_msoko_streaming_response(user_message: str, history: Optional[List[Dict[str, str]]] = None, user_id: Optional[int] = None, image_data: Optional[str] = None, context: Optional[Dict] = None, search_enabled: bool = False):
    """
    Convenience function to get a streaming response.
    """
    ctx = context or {}
    if user_id:
        ctx["user_id"] = user_id
    if image_data:
        ctx["is_multimodal"] = True
    if search_enabled:
        ctx["search_enabled"] = True
    return default_agent.get_streaming_response(user_message, history=history, context=ctx, image_data=image_data)
