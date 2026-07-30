import re


BANNED_WORDS = [
    "aptal", "salak", "gerizekalı", "lan", "pislik"
]

SAFE_RESPONSE = "Ben daha yeni bir sistemim. Eğer bir hatam, şikayetin veya isteğin varsa robozentakimi@gmail.com üzerinden belirtebilirsin."

def check_abuse(text: str) -> bool:
    
    text_lower = text.lower()
    for word in BANNED_WORDS:
        
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text_lower):
            return True
    return False

def get_safe_response() -> str:
   
    return SAFE_RESPONSE
