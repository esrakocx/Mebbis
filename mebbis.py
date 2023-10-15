from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import mysql.connector
from flask_scss import Scss


app = Flask(__name__)
scss = Scss(app, static_dir='static', asset_dir='')

# MySql Veritabanı bağlantısı 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mebbis_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def login():
    return render_template('login.html')

# Mebbis Yöneticileri için sisteme giriş yapma işlemi
@app.route('/login', methods = ['POST'])
def check_login():
    email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM duzenlenmisveriler WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
        return redirect(url_for('main_screen'))
    else:
        return "Geçersiz şifre veya email!"

# Email ve Şifresi doğrulanan kullanıcıların ana menüye yönlendirilmesi ve seçenekler
@app.route("/main_screen")
def main_screen():
    return render_template("main_screen.html")

# Personel ve Bilgisayar Bilgilerinin Listelenmesi
@app.route('/bilgi')
def bilgi_goster():
    cursor.execute('SELECT * FROM duzenlenmisveriler2')
    bilgiler = cursor.fetchall()
    return render_template('personelbilgi.html', bilgiler=bilgiler)

# Mevcut Yazıcıların Listelenmesi ve Veri Tabanına yeni yazıcı tanımlanması
@app.route('/yazici')
def yazici_tanimla():
    cursor.execute('SELECT * FROM duzenlenmisveriler3')
    yazicilar = cursor.fetchall()
    return render_template('yazici.html', yazicilar=yazicilar)

@app.route('/guncelle/<int:yazici_no>', methods=['GET', 'POST'])
def guncelle(yazici_no):
    if request.method == 'POST':
        yeni_veri = request.form 
        sql = "UPDATE duzenlenmisveriler3 SET Sube_Birim_Personel=%s, Marka_Model=%s, Yazici_Adi=%s, Baglanti=%s, IP_No=%s, Kabinet_No=%s, Switch_No=%s, Port_No=%s WHERE Yazici_No=%s"
        values = (yeni_veri['Sube_Birim_Personel'], yeni_veri['Marka_Model'], yeni_veri['Yazici_Adi'], yeni_veri['Baglanti'], yeni_veri['IP_No'], yeni_veri['Kabinet_No'], yeni_veri['Switch_No'], yeni_veri['Port_No'], yazici_no)
        cursor.execute(sql, values)
        db.commit()
        return redirect(url_for('main_screen'))  

    cursor.execute("SELECT * FROM duzenlenmisveriler3 WHERE Yazici_No=%s", (yazici_no,))
    yazici = cursor.fetchone()
    return render_template('guncelle.html', yazici=yazici)


@app.route('/ekle', methods=['GET', 'POST'])
def ekle_yazici():
    if request.method == 'POST':
        yazici_no = request.form['Yazici_No']
        sube = request.form['Sube_Birim_Personel']
        marka_model = request.form['Marka_Model']
        yazici_adi = request.form['Yazici_Adi']
        baglanti = request.form['Baglanti']
        ip_adresi = request.form['IP_No']
        kabinet = request.form['Kabinet_No']
        switch = request.form['Switch_No']
        port_no = request.form['Port_No']

        # Veriyi MySQL veritabanına ekle
        cursor.execute("INSERT INTO duzenlenmisveriler3 (Yazici_No, Sube_Birim_Personel, Marka_Model, Yazici_Adi, Baglanti, IP_No, Kabinet_No, Switch_No, Port_No) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (yazici_no, sube, marka_model, yazici_adi, baglanti, ip_adresi, kabinet, switch, port_no))

        db.commit()
        return redirect(url_for('yazici_tanimla'))

# Mevcut Cihazların Listelenmesi ve Veri Tabanına yeni cihaz tanımlanması
@app.route('/cihaz')
def cihaz_tanimla():
    cursor.execute('SELECT * FROM duzenlenmisveriler4')
    cihazlar = cursor.fetchall()
    return render_template('cihaz.html', cihazlar=cihazlar)

@app.route('/ekle_cihaz', methods=['GET', 'POST'])
def ekle_cihaz():
    if request.method == 'POST':
        cihaz_no = request.form['Sira_No']
        kat_no = request.form['Kat_Numara']
        kabinet_no = request.form['Kabinet_No']
        switch_no = request.form['Switch_No']
        switch_port_no = request.form['Switch_Port_No']
        cihaz_adi = request.form['Cihaz_Name']
        switch_turu = request.form['Switch_Turu']
        marka = request.form['Marka']
        seri_no = request.form['Seri_No']
        ip_no = request.form['IP_No']
        aciklama = request.form['Aciklama']
        mac_adres = request.form['MAC_Adresi']

        # Veriyi MySQL veritabanına ekle
        cursor.execute("INSERT INTO duzenlenmisveriler4 (Sira_No, Kat_Numara, Kabinet_No, Switch_No, Switch_Port_No, Cihaz_Name, Switch_Turu, Marka, Seri_No, IP_No, Aciklama, MAC_Adresi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (cihaz_no, kat_no, kabinet_no, switch_no, switch_port_no, cihaz_adi, switch_turu, marka, seri_no, ip_no, aciklama, mac_adres))

        db.commit()

        return redirect(url_for('cihaz_tanimla'))


# Mevcut Kullanıcıların Listelenmesi ve Veri Tabanına yeni kullanıcı tanımlanması
@app.route('/ad')
def ad_kullanici_liste():
    cursor.execute('SELECT * FROM duzenlenmisveriler5')
    kullanicilar = cursor.fetchall()
    return render_template('adkullanici.html', kullanicilar=kullanicilar)

@app.route('/ekle_kullanici', methods=['GET', 'POST'])
def ekle_kullanici():
    if request.method == 'POST':
        sira_no = request.form['Sira_No']
        il_adi = request.form['IL_Adi']
        ad_soyad = request.form['Adi_Soyadi']
        calistigi_birim = request.form['Calistigi_Birim']
        mac_adres = request.form['MAC_Adresi']
        ip_no = request.form['IP_No']
        calisma_durumu = request.form['Calisma_Durumu']

        # Veriyi MySQL veritabanına ekle
        cursor.execute("INSERT INTO duzenlenmisveriler5 (Sira_No, IL_Adi, Adi_Soyadi, Calistigi_Birim, MAC_Adresi, IP_No, Calisma_Durumu) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (sira_no, il_adi, ad_soyad, calistigi_birim, mac_adres, ip_no, calisma_durumu))

        db.commit()

        return redirect(url_for('ad_kullanici_liste'))
    
@app.route('/guncelle_kullanici/<int:sira_no>', methods=['GET', 'POST'])
def guncelle_kullanici(sira_no):
    if request.method == 'POST':
        yeni_veri = request.form 
        sql = "UPDATE duzenlenmisveriler5 SET IL_Adi=%s, Adi_Soyadi=%s, Calistigi_Birim=%s, MAC_Adresi=%s, IP_No=%s, Calisma_Durumu=%s WHERE Sira_No=%s"
        values = (yeni_veri['IL_Adi'], yeni_veri['Adi_Soyadi'], yeni_veri['Calistigi_Birim'], yeni_veri['MAC_Adresi'], yeni_veri['IP_No'], yeni_veri['Calisma_Durumu'], sira_no)
        cursor.execute(sql, values)
        db.commit()
        return redirect(url_for('ad_kullanici_liste'))  

    cursor.execute("SELECT * FROM duzenlenmisveriler5 WHERE Sira_No=%s", (sira_no,))
    kullanici = cursor.fetchone()
    return render_template('guncelle_kullanici.html', kullanici=kullanici)

    
# Kabinet nezdinde Ağ Bilgilerinin Listelenmesi
@app.route('/ag_bilgileri', methods=['GET', 'POST'])
def ag_sorgula():
    if request.method == 'POST':
        button_type = request.form['button_type']

        if button_type == 'button1':
            cursor.execute('SELECT * FROM duzenlenmisveriler6 WHERE Kabinet_No = "1"')
        elif button_type == 'button2':
            cursor.execute('SELECT * FROM duzenlenmisveriler6 WHERE Kabinet_No = "2"')
        elif button_type == 'button3':
            cursor.execute('SELECT * FROM duzenlenmisveriler6 WHERE Kabinet_No = "3"')

        results = cursor.fetchall()
        return render_template('agbilgileri.html', results=results)
    
    return render_template('agbilgileri.html', results = [])

# Kayseri İL Milli Eğitim Müdürlüğü Görevleri ve İletişim
@app.route('/hakkinda')
def hakkinda():
    return render_template('hakkinda.html')

if __name__ == '__main__':
    app.run(debug=True)
