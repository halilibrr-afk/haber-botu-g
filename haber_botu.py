import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# 1. HEDEF BİLGİLERİ (S25 Ultra çıktığında linki buraya güncelleyebilirsin)
# Şu an örnek olarak Amazon'dan bir S24 Ultra linki koyuyorum:
url = "https://www.amazon.com.tr/Samsung-Galaxy-Ultra-512GB-Titanyum/dp/B0CSKL979P"

# Amazon'un bizi engellememesi için kendimizi gerçek bir tarayıcı gibi tanıtıyoruz:
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

def fiyat_takibi():
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Amazon'da ürün başlığı genelde 'productTitle' id'si içindedir
        baslik = soup.find(id="productTitle").get_text().strip()
        
        # Amazon fiyatı genelde 'a-price-whole' class'ı içindedir
        fiyat_tam = soup.find("span", class_="a-price-whole").get_text()
        fiyat_kurus = soup.find("span", class_="a-price-fraction").get_text()
        
        guncel_fiyat = f"{fiyat_tam},{fiyat_kurus} TL"
        return f"{baslik}\nFiyat: {guncel_fiyat}"
    except Exception as e:
        return f"Hata oluştu: {e}. Amazon botu engellemiş olabilir."

def mail_at(icerik):
    gonderen = "halilibrrmcsgr" # Burayı kendi mailinle değiştir
    alici = "halilibrrmcsgr@gmail.com"    # Burayı kendi mailinle değiştir
    sifre = os.getenv('EMAIL_PASSWORD')

    msg = MIMEText(icerik)
    msg['Subject'] = "Amazon Fiyat Takipçisi"
    msg['From'] = gonderen
    msg['To'] = alici

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gonderen, sifre)
        server.send_message(msg)
        print("Mail başarıyla gönderildi!")

# Çalıştır
sonuc = fiyat_takibi()
print(sonuc)
mail_at(sonuc)
