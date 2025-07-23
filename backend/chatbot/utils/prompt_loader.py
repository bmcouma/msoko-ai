import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_prompt(name):
    """
    Loads a text prompt from the prompts directory.
    """
    base_path = os.path.join(os.path.dirname(__file__), '..', 'prompts')
    file_path = os.path.normpath(os.path.join(base_path, name))

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_msoko_response(user_message):
    system_prompt = (
        "You are Msoko AI, a smart business coach for informal sector entrepreneurs, like mama mbogas, boda riders, and small shop owners. "
        "Offer friendly, localized, and simplified advice. Focus on pricing tips, marketing ideas, customer care, record-keeping, expansion strategies, and savings."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"