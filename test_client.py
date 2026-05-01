import requests

URL = "http://127.0.0.1:5000/api/chat"

print("RoboAyna Test İstemcisi Başlatıldı. Çıkmak için 'çıkış' yazın.")
while True:
    try:
        user_input = input("\nSen: ")
        if user_input.lower() in ["çıkış", "exit", "quit"]:
            print("Çıkılıyor...")
            break
            
        if not user_input.strip():
            continue
            
        # Asistan çekirdeğine isteği gönder
        response = requests.post(URL, json={"text": user_input})
        
        if response.status_code == 200:
            data = response.json()
            print(f"RoboAyna: {data.get('response', '')}")
        else:
            print(f"Hata! Sunucu {response.status_code} kodu döndürdü.")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nHata: Sunucuya bağlanılamadı. Lütfen önce 'python assistant_core.py' komutuyla çekirdek servisi başlattığınızdan emin olun.")
    except Exception as e:
        print(f"\nBeklenmeyen bir hata oluştu: {e}")
