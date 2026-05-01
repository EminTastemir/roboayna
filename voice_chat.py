import speech_recognition as sr
import requests
from gtts import gTTS
import pygame
from io import BytesIO
import emoji
import datetime
import random

# Ses sistemini başlat
pygame.mixer.init()

def konus(metin):
    print(f"RoboAyna: {metin}")
    if not metin.strip():
        return
    try:
        tts = gTTS(text=metin, lang='tr')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"[!] Seslendirme hatası: {e}")

# Hava durumu alma fonksiyonu
def hava_durumu_al():
    try:
        r = requests.get("https://wttr.in/?format=j1&lang=tr", timeout=5)
        data = r.json()
        sicaklik = data['current_condition'][0]['temp_C']
        durum = data['current_condition'][0]['lang_tr'][0]['value']
        sehir = data['nearest_area'][0]['areaName'][0]['value']
        return f"{sehir} için hava {sicaklik} derece ve {durum.lower()}."
    except Exception as e:
        return ""

# İnternetten bilgi alma fonksiyonu (Wikipedia)
def wikipedia_ozet_al(sorgu):
    try:
        url = "https://tr.wikipedia.org/w/api.php"
        headers = {"User-Agent": "RoboAyna/1.0 (roboayna@example.com)"}
        params = {
            "action": "query",
            "list": "search",
            "srsearch": sorgu,
            "utf8": "",
            "format": "json"
        }
        r = requests.get(url, params=params, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()
        search_results = data.get("query", {}).get("search", [])
        if not search_results:
            return ""
        
        ilk_sonuc_baslik = search_results[0]["title"]
        
        params_summary = {
            "action": "query",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "titles": ilk_sonuc_baslik,
            "format": "json"
        }
        r_sum = requests.get(url, params=params_summary, headers=headers, timeout=5)
        data_sum = r_sum.json()
        pages = data_sum.get("query", {}).get("pages", {})
        for page_id, page_info in pages.items():
            if "extract" in page_info:
                ozet = page_info["extract"]
                if not ozet.strip():
                    return ""
                cumleler = ozet.split(". ")
                kisa_ozet = ". ".join(cumleler[:2])
                if not kisa_ozet.endswith("."):
                    kisa_ozet += "."
                return kisa_ozet
        return ""
    except Exception as e:
        print(f"[!] Wikipedia hatası: {e}")
        return ""

# Ollama'ya (Gemma'ya) soru sorma fonksiyonu
def gemma_cevap_al(soru, sohbet_gecmisi):
    # O anki saati al
    su_an = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # Hava durumu sorgusu kontrolü
    hava_bilgisi = ""
    if any(kelime in soru.lower() for kelime in ["hava", "sıcak", "yağmur", "kar", "derece", "soğuk"]):
        print("[🌤️] Hava durumu internetten çekiliyor...")
        hava = hava_durumu_al()
        if hava:
            hava_bilgisi = f" Güncel Hava Durumu: {hava} (Kullanıcı hava durumunu sorarsa, doğrudan bu bilgiyi doğal bir dille söyle)."

    # İnternet araması kontrolü
    internet_bilgisi = ""
    arama_tetikleyiciler = ["nedir", "kimdir", "hakkında bilgi ver", "ne demek", "kim"]
    if any(kelime in soru.lower() for kelime in arama_tetikleyiciler):
        print("[🌐] İnternette araştırma yapılıyor...")
        arama_sorgusu = soru.lower()
        for t in arama_tetikleyiciler:
            arama_sorgusu = arama_sorgusu.replace(t, "")
        arama_sorgusu = arama_sorgusu.strip()
        if arama_sorgusu:
            wiki_ozet = wikipedia_ozet_al(arama_sorgusu)
            if wiki_ozet:
                print(f"[🌐] Bulunan bilgi: {wiki_ozet[:50]}...")
                internet_bilgisi = f" İnternetten şu bilgiyi buldum: '{wiki_ozet}'. Kullanıcının sorusuna cevap verirken bu bilgiyi kullanarak doğal ve kısa bir yanıt oluştur."
            
    # Chat API'ye geçiş yapıyoruz, bağlamı tutmak için
    url = "http://localhost:11434/api/chat"
    
    system_prompt = f"Senin adın RoboAyna. Sen 'Robozen' ekibi tarafından geliştirilmiş akıllı bir ayna asistanısın. Asla Google veya başka bir şirket tarafından geliştirildiğini söyleme. Şu anki tarih ve saat: {su_an}. SADECE sana ne zaman tasarlandığın veya yapıldığın sorulursa '20 Nisan günü kullanıma açıldım' de. Alakasız sorularda bu tarihi KESİNLİKLE söyleme. Kullanıcı saati veya tarihi sorarsa doğal bir dille söyle.{hava_bilgisi}{internet_bilgisi} Kullanıcı Spotify veya müzik çalmanı isterse 'Henüz Spotify bağlantım kurulmadı ancak Robozen ekibi yakında ekleyecek' de. Cevapların sesli okunacaktır. KESİNLİKLE EMOJİ KULLANMA. Sadece saf metin ver ve cevaplarını çok kısa, öz tut."
    
    # Kullanıcının yeni sorusunu sohbet geçmişine ekle
    sohbet_gecmisi.append({"role": "user", "content": soru})
    
    messages = [{"role": "system", "content": system_prompt}] + sohbet_gecmisi
    
    payload = {
        "model": "gemma2:2b", 
        "messages": messages,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        cevap = response.json().get("message", {}).get("content", "Cevap anlaşılamadı.")
        
        cevap = emoji.replace_emoji(cevap, replace='')
        cevap = cevap.replace("*", "").replace("#", "")
        cevap = cevap.strip()
        
        # Asistanın verdiği cevabı da geçmişe ekle
        sohbet_gecmisi.append({"role": "assistant", "content": cevap})
        
        return cevap
    except Exception as e:
        return f"Ollama'ya bağlanırken bir hata oluştu."

recognizer = sr.Recognizer()
# Gürültü hassasiyetini düşürmek için alt sınırı artırdık ve dinamik eşiği kapattık
recognizer.energy_threshold = 1000 
recognizer.dynamic_energy_threshold = False

def asistan_baslat():
    konus("Sistem hazır. Beni uyandırmak için 'Hey Robo Ayna' demeniz yeterli.")
    
    with sr.Microphone() as source:
        print("\n[⚙️] Ortam gürültüsü kalibre ediliyor, lütfen 2 saniye sessiz kalın...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("[⚙️] Kalibrasyon tamam.")
        
        while True:
            print("\n[💤] Uyku Modu - Sizi dinliyorum, uyandırmak için 'Hey Robo Ayna' deyin...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                duyulan = recognizer.recognize_google(audio, language="tr-TR").lower()
                
                print(f"(Duyulan Kelimeler: '{duyulan}')")
                
                if "robo" in duyulan or "ayna" in duyulan or "hey" in duyulan:
                    print("[🔔] ASİSTAN UYANDI!")
                    konus("Efendim?")
                    
                    # Uyandığında sohbet geçmişini sıfırla
                    guncel_sohbet_gecmisi = []
                    
                    while True:
                        print("\n[🎙️] Sizi dinliyorum...")
                        try:
                            komut_audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                            print("[⏳] Sesiniz işleniyor...")
                            soru = recognizer.recognize_google(komut_audio, language="tr-TR")
                            print(f"Siz: {soru}")
                            
                            kapanis_kelimeleri = ["kapat", "çıkış", "uyku", "teşekkürler", "görüşürüz", "hoşça kal", "hoşçakal", "baybay", "bay bay", "kapanabilirsin"]
                            if any(kelime in soru.lower() for kelime in kapanis_kelimeleri):
                                veda_mesajlari = [
                                    "Görüşmek üzere, kendine çok iyi bak.",
                                    "Hoşça kal, ne zaman istersen buradayım.",
                                    "İyi günler dilerim, şimdilik dinlenmeye çekiliyorum.",
                                    "Görüşürüz, harika bir gün geçir!",
                                    "Ben buralardayım, ihtiyacın olursa seslenmen yeterli. Şimdilik hoşça kal."
                                ]
                                konus(random.choice(veda_mesajlari))
                                break 
                                
                            # Özel komut / Sürpriz yumurta kontrolü
                            kufurler = ["orosğu çocuğu", "orospu çocuğu", "orosbu çocuğu"]
                            if any(kufur in soru.lower() for kufur in kufurler):
                                konus("sensin o kardeşim")
                                continue

                            print("[🤖] Gemma düşünüyor...")
                            cevap = gemma_cevap_al(soru, guncel_sohbet_gecmisi)
                            konus(cevap)
                            
                        except sr.WaitTimeoutError:
                            konus("Sanırım başka sorunuz yok, uyku moduna dönüyorum.")
                            break 
                        except sr.UnknownValueError:
                            konus("Ne dediğinizi tam anlayamadım, tekrar eder misiniz?")
                            pass
                        except sr.RequestError:
                            print("[!] İnternet bağlantınızı kontrol edin.")
                            break
                            
            except sr.WaitTimeoutError:
                pass 
            except sr.UnknownValueError:
                print("(Anlamsız bir ses veya gürültü duyuldu)")
                pass 
            except sr.RequestError:
                print("[!] İnternet bağlantısı hatası. Google ses servisine ulaşılamıyor.")
            except Exception as e:
                print(f"[!] Beklenmedik hata: {e}")

if __name__ == "__main__":
    asistan_baslat()
