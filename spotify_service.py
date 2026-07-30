def play_music(song: str = ""):
   
    if song:
        print(f"[Spotify Modülü] '{song}' isimli şarkı başlatılıyor...")
    else:
        print("[Spotify Modülü] Müzik oynatılmaya devam ediliyor...")
    

def pause_music():
   
    print("[Spotify Modülü] Müzik durduruldu.")
    
