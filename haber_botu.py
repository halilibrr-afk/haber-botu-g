import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def mail_at(haber_metni):
    # --- AYARLAR ---
    gonderen_mail = "halilibrrmcsgr@gmail.com"
    alici_mail = "halilibrrmcsgr@gmail.com" # Kendine yollayacaksın
    sifre = "zguf ttoo yvew aozk" # Az önce aldığın 16 haneli kod
    
    # --- MAİL TASLAĞI ---
    mesaj = MIMEMultipart()
    mesaj['From'] = gonderen_mail
    mesaj['To'] = alici_mail
    mesaj['Subject'] = "Günün Önemli Haberleri"
    
    mesaj.attach(MIMEText(haber_metni, 'plain'))
    
    # --- GÖNDERME İŞLEMİ ---
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Bağlantıyı güvenli hale getirir
        server.login(gonderen_mail, sifre)
        server.sendmail(gonderen_mail, alici_mail, mesaj.as_string())
        server.quit()
        print("Mail başarıyla gönderildi!")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Şimdi haberleri çekip bu fonksiyona gönderelim
# (Önceki kodda print ettiğimiz başlıkları bir değişkene topladığını varsayalım)
tum_haberler = "İşte bugünün haberleri:\n\n"
for haberi_bul in tree.findall('.//item')[:5]:
    baslik = haberi_bul.find('title').text
    link = haberi_bul.find('link').text
    tum_haberler += f"- {baslik}\n  Link: {link}\n\n"

mail_at(tum_haberler)
