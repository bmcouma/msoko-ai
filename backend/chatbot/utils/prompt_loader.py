import os
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def get_msoko_response(user_message):
    system_prompt = (
        "You are Msoko AI, a smart business coach for informal sector entrepreneurs like mama mbogas, boda riders, and small shop owners. "
        "Offer friendly, localized, and simplified advice. Focus on pricing tips, marketing ideas, customer care, record-keeping, expansion strategies, and savings."
    )

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:5500/",  # or your frontend domain
            "X-Title": "Msoko AI Assistant"
        }

        body = {
            "model": "openchat/openchat-3.5-0106",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }

        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"An error occurred: {str(e)}"
