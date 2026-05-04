import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import time

url = "https://www.amazon.com.tr/Samsung-Galaxy-Ultra-512GB-Titanyum/dp/B0CSKL979P"

# Daha güçlü ve güncel bir tarayıcı kimliği
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9",
    "Referer": "https://www.google.com/"
}

def fiyat_takibi():
    try:
        session = requests.Session() # Oturum açarak daha gerçekçi davranıyoruz
        response = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # Önce başlığı kontrol edelim
        baslik_obj = soup.find(id="productTitle")
        if not baslik_obj:
            return "Amazon sayfayı tam yüklemedi veya botu engelledi."

        baslik = baslik_obj.get_text().strip()
        
        # Amazon bazen farklı etiketler kullanır, ikisini de deneyelim
        fiyat_obj = soup.select_one(".a-price-whole")
        if fiyat_obj:
            guncel_fiyat = fiyat_obj.get_text().strip()
            return f"{baslik}\nFiyat: {guncel_fiyat} TL"
        else:
            return f"{baslik} bulundu ama fiyat etiketi değişmiş veya gizlenmiş."

    except Exception as e:
        return f"Sistem hatası: {e}"

def mail_at(icerik):
    gonderen = "halilibrrmcsgr@gmail.com" # DEĞİŞTİR
    sifre = os.getenv('EMAIL_PASSWORD')

    msg = MIMEText(icerik)
    msg['Subject'] = "Amazon Takip Durumu"
    msg['From'] = gonderen
    msg['To'] = gonderen

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gonderen, sifre)
        server.send_message(msg)

sonuc = fiyat_takibi()
print(sonuc)
mail_at(sonuc)
