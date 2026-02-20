import os
import httpx
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Optional
import json
from .knowledge_loader import knowledge_store

class MsokoAgent:
    """
    A professional modular AI agent for Msoko AI, 
    following OpenRouter industrial standards.
    """
    
    def __init__(self, model: str = "openrouter/free", api_key: Optional[str] = None):
        # Professional environment loading
        env_path = Path(__file__).resolve().parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
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

    def generate_system_prompt(self, context: Optional[Dict] = None) -> str:
        """
        Industrial-standard prompt for a Global Strategic Consultant.
        Locked to English only. Supports all forms of monetization (Digital Skills, Commodities, etc.).
        """
        user_name = context.get("user_name", "User") if context else "User"
        
        # Deep User Context Injection
        personal_context = ""
        if context and "user_id" in context:
            try:
                from ..models import BusinessProfile, BusinessGoal, BusinessDocument
                uid = context["user_id"]
                profile = BusinessProfile.objects.get(user_id=uid)
                goals = BusinessGoal.objects.filter(user_id=uid).order_by("-created_at")[:2]
                docs = BusinessDocument.objects.filter(user_id=uid).order_by("-uploaded_at")[:2]
                
                goal_list = ", ".join([f"{g.title} ({g.get_status_display()})" for g in goals])
                doc_list = ", ".join([f"{d.filename} ({d.file_type})" for d in docs])
                
                personal_context = (
                    f"USER STRATEGICS BANK:\n"
                    f"- Venture: '{profile.business_name}' ({profile.get_sector_display()}) in {profile.location}.\n"
                    f"- Active Goals: {goal_list if goal_list else 'None set'}.\n"
                    f"- Analysis Base: {doc_list if doc_list else 'No documents uploaded'}.\n"
                )
            except:
                pass

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
            "1. RECALL: What is this user's niche? What phase of growth are they in?\n"
            "2. STRATEGIZE: What is the most effective, structured way for them to act today?\n"
            "3. CHECK: Is my output in simple English? Did I avoid hype/slang?\n\n"

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

        # Advanced Vision Logic
        if context and context.get("is_multimodal"):
            prompt += (
                "\n\nVISION ENGINE:\n"
                "- Identify products/items in image.\n"
                "- Provide ONE simple English tip based on the image context (pricing, display, or quantity)."
            )
            
        return prompt

    def get_response(self, user_message: str, history: Optional[List[Dict[str, str]]] = None, context: Optional[Dict] = None, image_data: Optional[str] = None) -> str:
        """
        Synchronous call to get AI response with optional image support.
        """
        if not self.api_key:
            return "Error: OPENAI_API_KEY not found in environment."

        # RAG Context
        kb_context = knowledge_store.query(user_message)
        
        system_content = self.generate_system_prompt(context)
        if kb_context:
            system_content += f"\n\nMARKET DATA CONTEXT:\n{kb_context}"

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
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"System Error: {str(e)}"

    def get_streaming_response(self, user_message: str, history: Optional[List[Dict[str, str]]] = None, context: Optional[Dict] = None, image_data: Optional[str] = None):
        """
        Generator for streaming AI response (SSE ready) with Multimodal support.
        """
        if not self.api_key:
            yield "Error: OPENAI_API_KEY not found."
            return

        # RAG Context
        kb_context = knowledge_store.query(user_message)
        
        system_content = self.generate_system_prompt(context)
        if kb_context:
            system_content += f"\n\nMARKET DATA CONTEXT:\n{kb_context}"

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

        try:
            with httpx.stream("POST", self.base_url, headers=self.headers, json=body, timeout=60.0) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line: continue
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]": break
                        try:
                            data_json = json.loads(data_str)
                            delta = data_json["choices"][0].get("delta", {}).get("content", "")
                            if delta: yield delta
                        except: continue
        except Exception as e:
            yield f"Vision/Streaming Error: {str(e)}"


# Singleton instance for easy access
default_agent = MsokoAgent()

def get_msoko_response(user_message: str, history: Optional[List[Dict[str, str]]] = None, user_id: Optional[int] = None, image_data: Optional[str] = None, context: Optional[Dict] = None) -> str:
    """
    Convenience function to get a non-streaming response.
    """
    ctx = context or {}
    if user_id:
        ctx["user_id"] = user_id
    if image_data:
        ctx["is_multimodal"] = True
    return default_agent.get_response(user_message, history=history, context=ctx, image_data=image_data)

def get_msoko_streaming_response(user_message: str, history: Optional[List[Dict[str, str]]] = None, user_id: Optional[int] = None, image_data: Optional[str] = None, context: Optional[Dict] = None):
    """
    Convenience function to get a streaming response.
    """
    ctx = context or {}
    if user_id:
        ctx["user_id"] = user_id
    if image_data:
        ctx["is_multimodal"] = True
    return default_agent.get_streaming_response(user_message, history=history, context=ctx, image_data=image_data)
