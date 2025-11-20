# Simple intent recognizer using keywords. Replace with a model for production.

def get_intent(text: str) -> str:
    t = text.lower()
    if any(x in t for x in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "greeting"
    if any(x in t for x in ["help", "how to", "could you", "can you"]):
        return "help"
    if any(x in t for x in ["balance", "account", "statement"]):
        return "account_info"
    if any(x in t for x in ["order", "delivery", "status", "tracking"]):
        return "order_status"
    return "unknown"
