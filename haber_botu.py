import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# 1. HEDEF BİLGİLERİ
# Örnek bir link (Sen ileride buraya gerçek bir S25 Ultra linki koyacaksın)
url = "https://www.ornek-teknoloji-sitesi.com/samsung-galaxy-s25-ultra"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def fiyat_kontrol_et():
    # Sayfayı indiriyoruz
    sayfa = requests.get(url, headers=headers)
    soup = BeautifulSoup(sayfa.content, 'html.parser')

    # BURASI KRİTİK: Sitedeki fiyat etiketini buluyoruz
    # Genelde fiyatlar <span class="price">75.000 TL</span> gibi görünür.
    # Biz 'span' etiketini ve içindeki class ismini hedef alıyoruz.
    urun_adi = soup.find("h1").text.strip() # Sayfanın ana başlığını alır
    fiyat = soup.find("span", class_="price-value").text.strip() # Fiyatı cımbızlar
    
    return urun_adi, fiyat

def mail_gonder(mesaj_icerigi):
    # Burası bir önceki botla aynı mantık (GitHub Secrets üzerinden)
    gonderen = "seninmailin@gmail.com"
    sifre = os.getenv('EMAIL_PASSWORD')
    
    msg = MIMEText(mesaj_icerigi)
    msg['Subject'] = "S25 Ultra Fiyat Güncellemesi!"
    msg['From'] = gonderen
    msg['To'] = gonderen

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gonderen, sifre)
        server.send_message(msg)

# ÇALIŞTIR
urun, fyt = fiyat_kontrol_et()
bilgi = f"{urun} için güncel fiyat: {fyt}"
print(bilgi)
mail_gonder(bilgi)
