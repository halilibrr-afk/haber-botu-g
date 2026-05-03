import requests
import os
from xml.etree import ElementTree
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. HABERLERİ ÇEKELİM
url = "https://www.donanimhaber.com/rss/tum/"
response = requests.get(url)
tree = ElementTree.fromstring(response.content)

tum_haberler = "İşte bugünün önemli haberleri:\n\n"

for haber in tree.findall('.//item')[:5]:
    baslik = haber.find('title').text
    link = haber.find('link').text
    tum_haberler += f"- {baslik}\n  Link: {link}\n\n"

# 2. MAİL ATALIM
def mail_at(icerik):
    gonderen = "seninmailin@gmail.com" # BURAYI DÜZELT
    alici = "seninmailin@gmail.com"    # BURAYI DÜZELT
    sifre = os.getenv('EMAIL_PASSWORD') # Kasadaki şifreyi kullanır

    mesaj = MIMEMultipart()
    mesaj['From'] = gonderen
    mesaj['To'] = alici
    mesaj['Subject'] = "Günün Haber Paketi"
    mesaj.attach(MIMEText(icerik, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderen, sifre)
        server.sendmail(gonderen, alici, mesaj.as_string())
        server.quit()
        print("Bot görevini başarıyla tamamladı!")
    except Exception as e:
        print(f"Hata çıktı: {e}")

mail_at(tum_haberler)
