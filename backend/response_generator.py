import os
import requests
from dotenv import load_dotenv
from nlp_intent import get_intent
from database import get_faq_answer

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def groq_generate(prompt: str) -> str:
    """
    Call GROQ LLM. If the call fails, return a fallback message.
    """
    if not GROQ_API_KEY:
        return "AI key missing. Please set GROQ_API_KEY in .env."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=15)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        # Debug prints go to server console
        print("Groq error:", e)
        try:
            print("Groq full response:", res.text)
        except:
            pass
        return "Sorry — AI failed to respond. Try again."

def generate_response(text: str) -> str:
    """
    Top-level function used by the FastAPI route.
    First try rule-based intents, then FAQ DB, then AI fallback.
    """
    try:
        # Simple logging
        print("User said:", text)

        # Intent detection (small rule-based stub)
        intent = get_intent(text)
        print("Detected intent:", intent)

        if intent == "greeting":
            return "Hello! How can I assist you today?"
        if intent == "help":
            return "I can help with account queries, orders, or general FAQs."
        if intent == "account_info":
            return "Your current account balance is ₹10,500."
        if intent == "order_status":
            return "Your order will arrive tomorrow."

        # Check FAQ DB
        faq = get_faq_answer(text)
        if faq:
            return faq

        # Fall back to LLM
        return groq_generate(text)

    except Exception as e:
        print("generate_response error:", e)
        return "Server error when generating response."
