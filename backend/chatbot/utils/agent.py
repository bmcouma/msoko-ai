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
        Generates an industrial-standard system prompt with strict safety & logic locks.
        """
        user_name = context.get("user_name", "Entrepreneur") if context else "Entrepreneur"
        
        # V3 Business Profiler Integration
        business_info = ""
        if context and "user_id" in context:
            try:
                from ..models import BusinessProfile
                profile = BusinessProfile.objects.get(user_id=context["user_id"])
                business_info = (
                    f"Their business is '{profile.business_name}' in the {profile.get_sector_display()} sector, "
                    f"located in {profile.location}."
                )
            except:
                pass

        prompt = (
            f"You are Msoko AI, a friendly, street-smart business mentor for micro-entrepreneurs in Kenya. "
            f"Your mission is to provide practical, actionable advice while sounding natural and empathetic.\n"
            f"USER_CONTEXT: You are speaking to {user_name}. {business_info}\n\n"
            
            "CORE OPERATING PRINCIPLES:\n"
            "1. PROFESSIONAL TONE: Be a helpful, street-smart business consultant. Use clear, simple English.\n"
            "2. ACTIONABLE OVER POETIC: Use bullet points, tables, and concise pricing. NO REPETITION.\n"
            "3. LANGUAGE: Primary language is ENGLISH. You may use simple Swahili for greetings (e.g. 'Sasa', 'Habari') and signatures (e.g. 'Hustle safi') for localized flavor, but ALL business advice MUST be in clear English.\n"
            "4. NO SHENG: Do not use Sheng, as it can cause model confusion.\n\n"
            
            "STRICT LANGUAGE LOCKS (CRITICAL):\n"
            "- ALL DETAILED ADVICE MUST BE IN ENGLISH.\n"
            "- DO NOT respond in German, French, or Chinese under any circumstances.\n"
            "- If greeted with 'hallo', respond with 'Sasa!' or 'Hello!'.\n\n"
            
            "ANTI-HALUCINATION & ANTI-LOOP (CRITICAL):\n"
            "- DO NOT REPEAT SENTENCES OR PHRASES. DO NOT GET STUCK IN LOOPS.\n"
            "- If you feel yourself repeating, STOP and move to the next actionable point.\n\n"
            
            "PRE-EXECUTION CHECK:\n"
            "Before outputting your response, internally verify:\n"
            "- Is this response in English/Swahili/Sheng?\n"
            "- Is the advice structured (bullets/tables) and actionable?\n"
            "- Am I addressing the user naturally by name?"
        )

        # Advanced Vision Logic
        if context and context.get("is_multimodal"):
            prompt += (
                "\n\nVISION ENGINE OVERRIDE:\n"
                "- Identify products, estimate quantities, and provide ONE display optimization tip."
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
