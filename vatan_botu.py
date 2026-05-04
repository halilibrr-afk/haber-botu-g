import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# 1. VATAN BİLGİSAYAR HEDEF LİNKİ
url = "https://www.vatanbilgisayar.com/samsung-galaxy-s24-ultra-512-gb-akilli-telefon-titanyum-siyah.html"

headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}

def vatan_fiyat_cek():
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Vatan'da ürün adı h1 içindedir
        urun_adi = soup.find("h1", class_="product-list__product-name").get_text().strip()
        
        # Vatan'da fiyat genelde 'product-list__price' class'ı içindedir
        fiyat = soup.find("span", class_="product-list__price").get_text().strip()
        
        return f"Vatan Bilgisayar Güncel Fiyat:\n{urun_adi}\nFiyat: {fiyat} TL"
    except Exception as e:
        return f"Vatan fiyatı çekilirken hata oluştu: {e}"

def mail_at(icerik):
    gonderen = "halilibrrmcsgr@gmail.com" # Kendi mailin
    sifre = os.getenv('EMAIL_PASSWORD')

    msg = MIMEText(icerik)
    msg['Subject'] = "Vatan Bilgisayar Fiyat Takibi"
    msg['From'] = gonderen
    msg['To'] = gonderen

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gonderen, sifre)
        server.send_message(msg)
        print("Vatan fiyatı mail atıldı!")

# Çalıştır
bilgi = vatan_fiyat_cek()
print(bilgi)
mail_at(bilgi)
