import re

# Genişletilebilir basit bir küfür/argo listesi (Örnek amaçlıdır)
BANNED_WORDS = [
    "aptal", "salak", "gerizekalı", "lan", "pislik"
]

SAFE_RESPONSE = "Ben daha yeni bir sistemim. Eğer bir hatam, şikayetin veya isteğin varsa robozentakimi@gmail.com üzerinden belirtebilirsin."

def check_abuse(text: str) -> bool:
    """
    Kullanıcı girdisinde küfür veya hakaret olup olmadığını kontrol eder.
    True dönerse filtreye takılmış demektir.
    """
    text_lower = text.lower()
    for word in BANNED_WORDS:
        # Kelime bazlı arama (sadece tam kelime eşleşmesi)
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text_lower):
            return True
    return False

def get_safe_response() -> str:
    """
    Küfür/Hakaret algılandığında verilecek sabit cevabı döndürür.
    """
    return SAFE_RESPONSE
