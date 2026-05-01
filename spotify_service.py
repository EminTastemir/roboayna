def play_music(song: str = ""):
    """
    Belirtilen şarkıyı Spotify'da çalar. Şarkı belirtilmemişse kaldığı yerden devam eder.
    Şimdilik sadece stub (iskelet) olarak çalışıyor.
    """
    if song:
        print(f"[Spotify Modülü] '{song}' isimli şarkı başlatılıyor...")
    else:
        print("[Spotify Modülü] Müzik oynatılmaya devam ediliyor...")
    
    # TODO: Gerçek Spotify API entegrasyonu (Spotipy kütüphanesi ile) eklenecek.

def pause_music():
    """
    Çalan müziği durdurur.
    Şimdilik sadece stub (iskelet) olarak çalışıyor.
    """
    print("[Spotify Modülü] Müzik durduruldu.")
    
    # TODO: Gerçek Spotify API entegrasyonu (Spotipy kütüphanesi ile) eklenecek.
