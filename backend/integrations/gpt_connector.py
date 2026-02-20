import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables (like OPENAI_API_KEY)
load_dotenv()

# Initialize OpenAI client with API key
api_key = os.getenv("OPENAI_API_KEY")
client = None

if api_key:
    client = OpenAI(api_key=api_key)

def ask_gpt(prompt):
    """
    Legacy function for OpenAI GPT API (not currently used in main flow).
    The main implementation uses OpenRouter via prompt_loader.py
    
    Args:
        prompt: User prompt/question
        
    Returns:
        str: GPT response or error message
    """
    if not client:
        return "Error: OPENAI_API_KEY not found in environment variables."
    
    if not prompt or not prompt.strip():
        return "Please provide a prompt."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to gpt-4 if available
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from GPT: {e}"
