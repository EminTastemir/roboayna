import requests
def hava_durumu_al():
    try:
        r = requests.get("https://wttr.in/?format=j1&lang=tr", timeout=5)
        data = r.json()
        sicaklik = data['current_condition'][0]['temp_C']
        durum = data['current_condition'][0]['lang_tr'][0]['value']
        sehir = data['nearest_area'][0]['areaName'][0]['value']
        print(f"{sehir} için hava şu an {sicaklik} derece ve {durum.lower()}.")
    except Exception as e:
        print("Hata:", e)

hava_durumu_al()
