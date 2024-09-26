import time
from datetime import date
from datetime import datetime  
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLabel, QGroupBox, QGridLayout, QPushButton, QLineEdit, QComboBox, QColorDialog, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt, QTimer# QThread
from PyQt5.QtGui import QPixmap, QFont, QTextCursor#, QColor
import json
import os
import subprocess
import asyncio
import websockets
import warnings
import requests
import re
import threading#multiprocessing
warnings.filterwarnings("ignore")

ilk = 0
logo_flag = 1
local_version = "5.11"
local_file = "Kortech_piyasa_websocket5.py"
github_url = "https://raw.githubusercontent.com/bcetisli/Kuyumcu/main/update.json"

address = "/home/Kortech/Downloads/"

# Altın fiyatlarının bulunduğu sayfanın URL'si
gold_prices_url = 'https://www.adadagold.com/'

#Türkçe gün ve ay isimleri
gun_isimleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
ay_isimleri = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
HAS_ALIS_OLD = 0.0
HAS_SATIS_OLD = 0.0
HAS_YUZDE_OLD =0.0
USD_ALIS_OLD = 0.0
USD_SATIS_OLD = 0.0
EUR_ALIS_OLD = 0.0
EUR_SATIS_OLD = 0.0
doviz_data = [("USD", 0.0, 0.0), ("EUR", 0.0, 0.0)]
#doviz_vitrin = [("USD", 0.0, 0.0, 0.0), ("EUR", 0.0, 0.0, 0.0)]
try:
    json_file_open = address +'default_factors1.json'
    with open(json_file_open, 'r', encoding = 'utf-8') as json_file:
        default_factors1 = json.load(json_file)
except FileNotFoundError:
    default_factors1 = {} 
try:
    json_file_open = address +'default_factors2.json'
    with open(json_file_open, 'r', encoding = 'utf-8') as json_file:
        default_factors2 = json.load(json_file)
except FileNotFoundError:
    default_factors2 = {} 
try:
    json_file_open = address +'default_factors_renk.json'
    with open(json_file_open, 'r', encoding = 'utf-8') as json_file:
        default_factors_renk = json.load(json_file)
except FileNotFoundError:
    default_factors_renk = {}
    
yazi_renk =	default_factors_renk['yazi_renk']['HEX']#"#ffffff"
arka_fon1 = default_factors_renk['arka_fon1']['HEX']#"lightBlue"
arka_fon2 =	default_factors_renk['arka_fon2']['HEX']#"darkBlue"


'''
# Varsayılan çarpanlar
default_factors = {
    "ÇEYREK": {"AlisY": 1.63, "SatisY": 1.64, "AlisE": 1.605, "SatisE": 0.0},
    "YARIM": {"AlisY": 3.26, "SatisY": 3.28, "AlisE": 3.20, "SatisE": 0.0},
    "TAM": {"AlisY": 6.50, "SatisY": 6.54, "AlisE": 6.40, "SatisE": 6.45},
    "ATA (Cumhuriyet)": {"AlisY": 6.60, "SatisY": 6.66, "AlisE": 0.0, "SatisE": 0.0},  # varsayılan çarpan 1
    "GREMSE": {"AlisY": 16.15, "SatisY": 16.30, "AlisE": 15.95, "SatisE": 16.20},
    "1gr 22": {"AlisY": 0.916, "SatisY": 0.930, "AlisE": 0.0, "SatisE": 0.0},
    "1gr 24": {"AlisY": 1.00, "SatisY": 1.002, "AlisE": 0.0, "SatisE": 0.0},    
    "24 paket": {"AlisY": 0.998, "SatisY": 1.002, "AlisE": 0.0, "SatisE": 0.0},
    "22 Bilezik": {"AlisY": 0.998, "SatisY": 1.002, "AlisE": 0.0, "SatisE": 0.0},
}
'''

class WifiManager(QWidget):
    def __init__(self):
        super().__init__()
        self.caps_lock_flag = True
        self.initUI()
        
    def initUI(self):
        grid_layout = QGridLayout()
        
        wifi_layout = QVBoxLayout()
        self.check_button =QPushButton("İnternet Bağlantısını kontrol et",self)
        self.check_button.clicked.connect(self.check_internet_connection)
        wifi_layout.addWidget(self.check_button)
        
        self.scan_button = QPushButton("Wifi Ağlarını tara", self)
        self.scan_button.clicked.connect(self.scan_wifi_networks)
        wifi_layout.addWidget(self.scan_button)
        
        self.combo =QComboBox(self)
        wifi_layout.addWidget(self.combo)
        
        self.password_label = QLabel('WIFI Şifresi:')
        wifi_layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit(self)
        self.password_input.mousePressEvent = self.set_active_input_password
        wifi_layout.addWidget(self.password_input)
        
        self.connect_button = QPushButton("Seçili Wifi ağına bağlan",self)
        self.connect_button.clicked.connect(self.connect_to_wifi)
        wifi_layout.addWidget(self.connect_button)
        
        grid_layout.addLayout(wifi_layout, 0, 0, 1, 1)
        #Keyboard Layout
        keyboard_layout = QHBoxLayout()
        #Butonlar
        self.add_keyboard_row(['1','2','3','4','5','6','7','8','9','0',], grid_layout, 5, 0, 1, 2)
        self.add_keyboard_row(['Q','W','E','R','T','Y','U','I','O','P','Ğ','Ü','~'], grid_layout, 6, 0, 1, 2)
        self.add_keyboard_row(['A','S','D','F','G','H','J','K','L','Ş','İ',',',';'], grid_layout, 7, 0, 1, 2)
        self.add_keyboard_row(['Z','X','C','V','B','N','M','Ö','Ç','.',':'], grid_layout, 8, 0, 1, 2)
        self.add_keyboard_row(['"','é','!','#','^','$','%','/','*','-','+','_'], grid_layout, 9, 0, 1, 2)
        #Delete Button
        delete_button =QPushButton('Delete',self)
        delete_button.clicked.connect(self.delete_char)
        keyboard_layout.addWidget(delete_button)
        #Space Button
        space_button =QPushButton('Space',self)
        space_button.clicked.connect(self.space_char)
        keyboard_layout.addWidget(space_button)
        #Caps Lock Button
        capslock_button =QPushButton('CapsLock',self)
        capslock_button.clicked.connect(self.toggle_caps_lock)
        keyboard_layout.addWidget(capslock_button)
        grid_layout.addLayout(keyboard_layout, 10, 0, 1, 2)
        
        self.setLayout(grid_layout)
        self.setWindowTitle("Wifi Yönetimi")
        self.show()
        
    def check_internet_connection(self):
        try:
            subprocess.check_output(["ping","-c","1","google.com"])
            QMessageBox.information(self,'Bağlantı Durumu','Bağlantı var')
        except subprocess.CalledProcessError:
            QMessageBox.warning(self,"Bağlantı Durumu","Bağlantı yok")
            
    def scan_wifi_networks(self):
        try:
            output = subprocess.run(["nmcli","-f","SSID","device","wifi","list"], capture_output=True,text=True)
            networks = output.stdout.strip().split('\n')[1:]
            self.combo.clear()
            self.combo.addItems(networks)
            QMessageBox.information(self,'Bağlantı Durumu','Bağlantı var')
        except Exception as e:
            QMessageBox.critical(self,"Hata ",str(e))     
    def set_active_input_password(self, event):
        self.active_input =self.password_input
        
    def connect_to_wifi(self):
        selected_network =self.combo.currentText()
        selected_network =selected_network.rstrip()
        if selected_network:
            #self.ssid_input.mousePressEvent = self.set_active_input_ssid
            password = self.active_input.text()#self,"Şifre Girin",f'{selected_network} ağı için şifre girin')
            #if ok:
            try:
               subprocess.run(["nmcli","device","wifi","connect",selected_network, "password",password],check=True)
               QMessageBox.information(self,'Bağlantı Durumu',f'{selected_network} ağına başarıyla bağlandı')
               for window in QApplication.topLevelWidgets():
                   window.close()
               self.close()
               self.window = MainWindow()
               self.window.show()
            except subprocess.CalledProcessError:
               QMessageBox.warning(self,"Bağlantı Durumu","Bağlantı başarısız")
        else:
            QMessageBox.warning(self,"Ağ seçilmedi","Lütfen bir ağ seçin")
    
    def add_keyboard_row(self,keys,layout, i, j , k, l):
        row_layout = QHBoxLayout()
        for key in keys:
            button =QPushButton(key,self)
            button.clicked.connect(self.type_char)
            row_layout.addWidget(button)
        layout.addLayout(row_layout, i, j, k, l)
    
        
    def type_char(self):
        msg = QMessageBox()
        msg.setWindowTitle('Yanlış Karakter Girişi')
        sender =self.sender()
        char = sender.text()
        if self.caps_lock_flag:
            char = char.upper()
        if active_input == self.logo_input:
            self.active_input.insertPlainText(sender.text())
        else:
            self.active_input.insert(sender.text())
    
    def delete_char(self):
        current_text = self.active_input.text()
        self.active_input.setText(current_text[:-1])
      
    def space_char(self):
        current_text = self.active_input.text()
        if active_input == self.logo_input:
            self.active_input.insertPlainText(" ")
        else:
            self.active_input.insert(" ")
    
    def toggle_caps_lock(self):
        self.caps_lock_flag = not self.caps_lock_flag
        self.CapsLock()
    
    def CapsLock(self):
        for button in self.findChildren(QPushButton):
            if button.text().isalpha():
                if self.caps_lock_flag:
                    button.setText(button.text().upper())
                else:
                    button.setText(button.text().lower())

response =requests.get(github_url)
#print(response.json())
if response.status_code == 200:
    latest_code = response.json()
    latest_version = float(latest_code["version"])
    if latest_version > float(local_version):
        update_url = latest_code["file_url"]
        try:
            with open(address+local_file,"w") as f:
                response =requests.get(update_url)
                if response.status_code == 200:
                    #print(response.text)
                    f.write(response.text)
                    subprocess.run("python3",address+local_file)
        except :
            QMessageBox.warning(self,"Güncelleme", "Güncel dosya kaydedilemedi")
            #print("dosya kaydedilemedi")
            

try:
    result = subprocess.check_output(['ifconfig', "wlan0"]).decode('utf-8')
    mac_address = re.search(r'ether ([\w:]+)',result).group(1)
    #print(mac_address)
except Exception as e:
    print(f"Hata MAC: {e}")
kayitli_MAC_address = default_factors_renk["ana_renk"]["HEX"]
temp = kayitli_MAC_address.split(":")
temp2 = temp[::-1]
kayitli_MAC_address =":".join(temp2)
#print(f"MAC Adress: {kayitli_MAC_address}")

async def connect_and_listen():
    global HAS_ALIS_OLD, HAS_SATIS_OLD, USD_ALIS_OLD, USD_SATIS_OLD, EUR_ALIS_OLD, EUR_SATIS_OLD, doviz_data, default_factors1
    uri = "wss://adadagold.com/wss/"
    deneme = 0
    max_deneme = 4
    has_altin = ('HAS', HAS_ALIS_OLD, HAS_SATIS_OLD)
    has = (0.0, 0.0)
    usd = (0.0, 0.0)
    eur = (0.0, 0.0)
    doviz_data = [('USD', USD_ALIS_OLD, USD_SATIS_OLD), ('EUR', EUR_ALIS_OLD, EUR_SATIS_OLD)]
    #while deneme < max_deneme:
    try:
        async with websockets.connect(uri, timeout = 10) as websocket:
            message = await websocket.recv()            
            try:
                veriler = json.loads(message)
                for veri in veriler:
                    if veri['kod'] == "HasAltin":
                        has_altin = ('HAS', veri['alis'], veri['satis'], 0.0)
                        has = (veri['alis'], veri['satis'])
                    elif veri['kod'] == "Usd":
                        alis = round(veri['alis'] + default_factors1["USD"]["AlisY"], 2)
                        satis = round(veri['satis'] + default_factors1["USD"]["SatisY"], 2)
                        usd = (alis, satis)#(veri['alis'], veri['satis'])
                    elif veri['kod'] == "Euro":
                        alis = round(veri['alis'] + default_factors1["EUR"]["AlisY"], 2)
                        satis = round(veri['satis'] + default_factors1["EUR"]["SatisY"], 2)
                        eur = (alis, satis)#(veri['alis'], veri['satis'])
                        #eur = (veri['alis'], veri['satis'])
                        doviz_data = [('USD', usd[0], usd[1]), ('EUR', eur[0], eur[1])]
                    if eur[0] > 0.0:
                        break
            except json.JSONDecodeError as ej:
                has_altin_tmp, doviz_data_tmp = await altinkaynak_fiyat_al()
                if has_altin_tmp[1] > 0.0:
                    has_altin = has_altin_tmp
                if doviz_data_tmp[0][1] > 0.0:
                   doviz_data = doviz_data_tmp 
    except asyncio.TimeoutError as e:
        has_altin_tmp, doviz_data_tmp = await altinkaynak_fiyat_al()
        if has_altin_tmp[1] > 0.0:
            has_altin = has_altin_tmp
        if doviz_data_tmp[0][1] > 0.0:
            doviz_data = doviz_data_tmp 
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 503 or usd[0] == 0.0 or has[0] == 0.0:
            has_altin_tmp, doviz_data_tmp = await altinkaynak_fiyat_al()
            if has_altin_tmp[1] > 0.0:
                has_altin = has_altin_tmp
            if doviz_data_tmp[0][1] > 0.0:
                doviz_data = doviz_data_tmp    
            #   break
            #await asyncio.sleep(gecikme)
        else:
            raise
    except Exception as e:
        has_altin_tmp, doviz_data_tmp = await altinkaynak_fiyat_al()
        if has_altin_tmp[1] > 0.0:
            has_altin = has_altin_tmp
        if doviz_data_tmp[0][1] > 0.0:
            doviz_data = doviz_data_tmp
                  
    return has_altin, doviz_data

def sarrafiye_hesapla(has_alis, has_satis):
    global default_factors2
    data = {}        
    i = 0
    for key, value in default_factors2.items():
        if key == "USD" or key == "EUR":
            continue
        else:
            altin_turu = key# Çeyrek altın için yapılacak işlemler
            alis_yeni = round(value['AlisY'] * has_alis) 
            satis_yeni = round(value['SatisY'] * has_satis) 
            k_karti = round(value['SatisY'] * has_satis * value['K_Karti']) 
            data[i] = (altin_turu, alis_yeni, satis_yeni, k_karti)#, satis_eski)
            i +=1
        
    return data

def doviz_hesapla():
    global default_factors1, doviz_data
    data = {}
    temp =list(doviz_data)
    i = 0
    for value in doviz_data:
        if value[0] == "USD":
            alis = round(value[1] + default_factors1["USD"]["AlisY"], 2)
            satis = round(value[2] + default_factors1["USD"]["SatisY"], 2)
            #k_karti = round((value[2] + default_factors1["USD"]["SatisY"]) * default_factors1["USD"]['K_Karti'], 2) 
        elif value[0] == "EUR":
            alis = round(value[1] + default_factors1["EUR"]["AlisY"], 2)
            satis = round(value[2] + default_factors1["EUR"]["SatisY"], 2)
            #k_karti = round((value[2] + default_factors1["EUR"]["SatisY"]) * default_factors1["EUR"]['K_Karti'], 2) 
        data[i] = (value[0], alis, satis)#, k_karti)#, satis_eski)
        i+=1
    return data
'''#Asyncio döngüsünü başlat
has_altin, doviz_data = asyncio.get_event_loop().run_until_complete(connect_and_listen())
HAS_GUN = has_altin[2]
'''
async def altinkaynak_fiyat_al():
    url = "https://rest.altinkaynak.com//Currency.json"
    response = requests.get(url)
    if response.status_code != 204:
        veri =response.json()
        for item in veri:
            if item["Kod"] =='USD':
                USD_alis = float(item["Alis"].replace(",","."))
                USD_satis = float(item["Satis"].replace(",","."))
                USD_alis = round(USD_alis + default_factors1["USD"]["AlisY"], 2)
                USD_satis = round(USD_satis + default_factors1["USD"]["SatisY"], 2)                        
            elif item["Kod"] == 'EUR':
                EUR_alis = float(item["Alis"].replace(",","."))
                EUR_satis = float(item["Satis"].replace(",","."))
                EUR_alis = round(EUR_alis + default_factors1["EUR"]["AlisY"], 2)
                EUR_satis = round(USD_satis + default_factors1["EUR"]["SatisY"], 2) 
                break
            
        doviz_data = [('USD', USD_alis, USD_satis), ('EUR', EUR_alis, EUR_satis)]
        
    url = "https://rest.altinkaynak.com//Gold.json"
    response = requests.get(url)
    if response.status_code != 204:
        veri =response.json()
        for item in veri:
            if item["Kod"] =='HH':
                alis = item["Alis"].replace(".","")
                has_alis = float(alis.replace(",","."))
                satis = item["Satis"].replace(".","")
                has_satis = float(satis.replace(",","."))
                has_altin = ('HAS', has_alis, has_satis, 0.0)
                break    
    return has_altin, doviz_data


class MainWindow(QMainWindow):
    def __init__(self):
        global ilk, HAS_GUN, has_altin, doviz_data, default_factors_renk
        super().__init__()
        self.flag_liste = 1
        self.setWindowTitle("Piyasa Fiyatları")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()
        #self.screen_width = self.screen().size().width()
        #print('Ekran genişliği', self.screen_width)
        # Arka plan rengini değiştirmek için stil sayfası ayarı
        #self.setStyleSheet('QWidget { background-color: lightblue; }')
        layout = QVBoxLayout()
        # Logo ve tarih-saat göstergesini içeren yatay düzen
        top_layout = QHBoxLayout()
                
        
        # Logo resmi ekleyin
        
        image_path = address +"logo.jpg"
        if not os.path.exists(image_path) or logo_flag == 0:
            QMessageBox.warning(self,"Logo", "logo.jpg resim dosyası bulunamadı.")
            #print("resim dosyası bulunamadı",image_path)
            text_font = default_factors_renk["logo_font"]
            
            self.logo_label = QLabel(default_factors_renk["logo_content"])
            text_fontsize = (int(default_factors_renk["logo_fontsize"]))
            #self.font = font_y
            text_backgrnd = default_factors_renk["logo_arka_fon"]["HEX"]
            text_color = default_factors_renk['logo_yazi_renk']["HEX"]
            text_bold = default_factors_renk["logo_fontweight"]
            text_bold = "bold"
            text_italic = default_factors_renk["logo_fontitalic"]
            '''
            if text_bold == 75:
                self.logo_label.setItalic()
            text_italic = default_factors_renk["logo_fontitalic"]
            '''
            if text_italic == True:
                text_italic = "italic"
            else:
                text_italic = ""
            
            text_alignment = default_factors_renk["logo_alignment"]            
            if text_alignment == 1:
                self.logo_label.setAlignment(Qt.AlignLeft)
            elif text_alignment == 2:
                self.logo_label.setAlignment(Qt.AlignRight)
            elif text_alignment == 8:
                self.logo_label.setAlignment(Qt.AlignJustify)    
            
            self.logo_label.setStyleSheet(f"font: {text_font}; font-size: {text_fontsize}px;background-color:{text_backgrnd};color:{text_color};font-weight: {text_bold};font-style: {text_italic};")#setFont(font_y)
            #self.logo_label.setStyleSheet("background-color: lightBlue;")
            top_layout.addWidget(self.logo_label,stretch=2)
        else:
            self.logo_label = QLabel()
            pixmap = QPixmap(image_path)  # Logonun dosya yolunu buraya ekleyin
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setStyleSheet("background-color: lightBlue;color: red; font-size: 36px;")
            top_layout.addWidget(self.logo_label,stretch=2)

        self.doviz_group = self.create_group_doviz("")
        top_layout.addWidget(self.doviz_group, stretch=2) 
        
        
        # Tarih ve gün bilgisini al
        now = datetime.now()
        gun = now.weekday()
        gun_adi = gun_isimleri[gun]
        gun = now.day
        ay = now.month - 1   # 0'dan başlıyor
        ay_adi = ay_isimleri[ay]
        yil = now.year
        saat = now.hour
        dakika = now.minute
        
        zmn_layout = QVBoxLayout()
        # Label'lar
        font = QFont("Times",40, QFont.ExtraBold)
        self.label_tarih = QLabel(now.strftime("%d.%m.%Y"), self)
        self.label_tarih.setAlignment(Qt.AlignCenter)  # Sağ hizalama
        self.label_tarih.setFont(font)#self.label_tarih.setAlignment(Qt.AlignCenter)
        self.label_tarih.setStyleSheet("background-color: lightBlue; color: green;border:3px solid lightBlue;")
        self.label_ay = QLabel(f"{ay_adi}", self)
        self.label_ay.setAlignment(Qt.AlignCenter)  # Sağ hizalama
        self.label_ay.setFont(font)#self.label_gun.setAlignment(Qt.AlignCenter)
        self.label_ay.setStyleSheet("background-color: lightBlue;color: green;border:3px solid lightBlue;")
        self.label_gun = QLabel(f"{gun_adi}", self)
        self.label_gun.setAlignment(Qt.AlignCenter)  # Sağ hizalama
        self.label_gun.setFont(font)#self.label_gun.setAlignment(Qt.AlignCenter)
        self.label_gun.setStyleSheet("background-color: lightBlue;color: green;border:3px solid lightBlue;")
        self.label_zaman = QLabel(f"{saat}:{dakika:02}", self)  # 2 haneli dakika
        self.label_zaman.setAlignment(Qt.AlignCenter)  # Sağ hizalama
        self.label_zaman.setStyleSheet("background-color: lightBlue;color: red;border:3px solid lightBlue;")  # Yazı rengi
        font = QFont("Times",40, QFont.ExtraBold)
        self.label_zaman.setFont(font)
        
        
        #self.label_zaman.setAlignment(Qt.AlignCenter)
        zmn_layout.addWidget(self.label_tarih)
        zmn_layout.addWidget(self.label_ay)
        zmn_layout.addWidget(self.label_gun)
        zmn_layout.addWidget(self.label_zaman)
        top_layout.addLayout(zmn_layout,stretch=1)
        
        Kortech_layout = QVBoxLayout()
        
        #Kortech Logo ekleme
        self.logo_label_Kortech = QLabel()
        image_path2 = address +"Kortech logo3.png"
        if not os.path.exists(image_path2):
            #print("resim dosyası bulunamadı",image_path2)
            return
        pixmap2 = QPixmap(image_path2)  # Logonun dosya yolunu buraya ekleyin
        self.logo_label_Kortech.setPixmap(pixmap2)
        self.logo_label_Kortech.setStyleSheet("background-color: lightBlue;")
        Kortech_layout.addWidget(self.logo_label_Kortech,stretch=0)
        
         
        #Buton ekleme
        self.ayar_button = QPushButton("AYARLAR")
        #ayar_button.setFlat(True)
        self.ayar_button.setStyleSheet("background-color:lightBlue;")
        self.ayar_button.setStyleSheet("color: darkBlue;font-size: 20px;")
        self.ayar_button.setStyleSheet("font-weight: bold;")


        #ayar_button.setObjectName("AYARLAR")
       

        #Buton kontrolü
        self.ayar_button.clicked.connect(self.ayar_penceresi)
        Kortech_layout.addWidget(self.ayar_button,stretch=0)
        top_layout.addLayout(Kortech_layout)
        
        layout.addLayout(top_layout)
        
        self.altin_group = self.create_group("")      
        
        layout.addWidget(self.altin_group, stretch=3)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        #Asyncio döngüsünü başlat
        has_altin, doviz_data = asyncio.run(connect_and_listen())#asyncio.get_event_loop().run_until_complete(connect_and_listen())
        HAS_GUN = has_altin[2]            
        self.update_data()
        self.create_grid()
        self.update_datetime()
        '''
        if ilk == 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect()
            self.timer.timeout.connect()
            self.timer.timeout.connect(e)
            self.timer.start(1000)  # 10 saniye (10,000 ms)
            ilk = 1
        #else:
        
            
            thread_data = threading.Thread(target = self.update_data)
            thread_grid = threading.Thread(target = self.update_grid)
            thread_data.start()
            thread_grid.start()
            thread_data.join()
            thread_grid.join()
            '''
        # Timer ayarla
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.timeout.connect(self.update_grid)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # 10 saniye (10,000 ms)
    
    def ayar_penceresi(self):        
        self.timer.stop()  # Timer'ı durdur
        self.window2 = Window2()
        self.window2.show()
           

    def create_group(self, title):        
        group = QGroupBox(title)               
        layout = QGridLayout()        
        group.setLayout(layout)
        return group
    
    def create_group_doviz(self, title):        
        group = QGroupBox(title)
        # QGroupBox başlık yazısının boyutu ve rengi burada ayarlanır
        group.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 36px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top center;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightslategrey;'  # Arka plan rengi
            'font-size: 40px;'  # Yazı boyutu
            '}'
        )
        layout = QGridLayout()        
        group.setLayout(layout)
        return group
    
    def update_data(self):
        
        global HAS_ALIS, HAS_SATIS, HAS_ALIS_OLD, HAS_SATIS_OLD,HAS_YUZDE, HAS_YUZDE_OLD
        global USD_ALIS_OLD,USD_SATIS_OLD, EUR_ALIS_OLD, EUR_SATIS_OLD, has_altin, doviz_data, altin_data 
        #Asyncio döngüsünü başlat
        has_altin, doviz_data = asyncio.run(connect_and_listen())#asyncio.get_event_loop().run_until_complete(connect_and_listen())                       
        HAS_ALIS = has_altin[1]
        HAS_SATIS = has_altin[2]
        if HAS_ALIS != HAS_ALIS_OLD or HAS_SATIS != HAS_SATIS_OLD:
            if HAS_ALIS is None:
                HAS_ALIS = HAS_ALIS_OLD
            else:
                HAS_ALIS_OLD = HAS_ALIS   
            
            if HAS_SATIS is None:
                HAS_SATIS = HAS_SATIS_OLD
            else:
                HAS_SATIS_OLD = HAS_SATIS
            HAS_YUZDE = 100 * (HAS_SATIS - HAS_GUN) / HAS_GUN#float(yuzde_degisim_element.text[1:].replace(",", "."))
            if HAS_YUZDE is None:
                HAS_YUZDE = HAS_YUZDE_OLD
            else:
                HAS_YUZDE_OLD = HAS_YUZDE
                   
        # Altın Fiyatları
        altin_data = sarrafiye_hesapla(has_altin[1], has_altin[2])
        # Döviz Kurları           
        if len(doviz_data) == 2:
            USD_ALIS_OLD = doviz_data[0][1]
            USD_SATIS_OLD = doviz_data[0][2]
            EUR_ALIS_OLD = doviz_data[1][1]
            EUR_SATIS_OLD = doviz_data[1][2]               
        elif doviz_data[0][1] is None:
                doviz_data[0][1] = USD_ALIS_OLD
        elif doviz_data[0][2] is None:
                doviz_data[0][2] = USD_SATIS_OLD
        elif doviz_data[1][1] is None:
                doviz_data[1][1] = EUR_ALIS_OLD
        elif doviz_data[1][2] is None:
                doviz_data[1][2] = EUR_SATIS_OLD
    
    def create_grid(self):        
        global has_altin, doviz_data, altin_data
        
        #try:       
        sayi = len(altin_data)
        if sayi == 7:
            self.altin_group = self.create_gridlayout_sarrafiye(self.altin_group, altin_data, has_altin[3])
        elif sayi > 7:
            fark = len(altin_data) - 7
            temp = altin_data 
            if self.flag_liste == 1:                                       
                for ss in range(7,sayi):
                    del temp[ss]
                self.altin_group = self.create_gridlayout_sarrafiye(self.altin_group, temp, has_altin[3])
                self.flag_liste = 0
            elif self.flag_liste == 0:                     
                for ss in range(7-fark,7):
                    del temp[ss]
                self.altin_group = self.create_gridlayout_sarrafiye(self.altin_group, temp, has_altin[3])
                self.flag_liste = 1
     
        self.create_gridlayout_doviz(self.doviz_group)       
            

        #except Exception as e:
        #    print(f"Hata:{e}")            
         
    def update_grid(self):        
        global has_altin, doviz_data, altin_data
        self.update_gridlayout_doviz(self.doviz_group)
        #try:       
        sayi = len(altin_data)
        if sayi == 7:
            self.altin_group = self.update_gridlayout_sarrafiye(self.altin_group, altin_data, has_altin[3])
        elif sayi > 7:
            fark = len(altin_data) - 7
            temp = altin_data 
            if self.flag_liste == 1:                                       
                for ss in range(7,sayi):
                    del temp[ss]
                self.altin_group = self.update_gridlayout_sarrafiye(self.altin_group, temp, has_altin[3])
                self.flag_liste = 0
            elif self.flag_liste == 0:                     
                for ss in range(7-fark,7):
                    del temp[ss]
                self.altin_group = self.update_gridlayout_sarrafiye(self.altin_group, temp, has_altin[3])
                self.flag_liste = 1
     
               
            

        #except Exception as e:
        #    print(f"Hata:{e}")            
         
    
    def create_label(self, text, HAS_YUZDE,row, ky):
        colors = [arka_fon1, arka_fon2]#colors = ["lightblue", "deepskyblue", "lightblue", "deepskyblue", "lightblue", "deepskyblue", "lightblue", "deepskyblue"]
        label = QLabel(text)
        font = QFont("Times")
        font.setBold(True)
        font.setPointSize(40)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Sağ hizalama        
        label.setFont(font)
       
        if HAS_YUZDE > 0.5:
            label.setStyleSheet(f"background-color: {colors[row % len(colors)]}; color: lime; border:3px solid black;")  # Yazı rengi
        elif HAS_YUZDE < -0.5:
            label.setStyleSheet(f"background-color: {colors[row % len(colors)]}; color: red; border:3px solid black;")  # Yazı rengi
        else:           
            label.setStyleSheet(f"background-color: {colors[row % len(colors)]};color: {yazi_renk}; border:3px solid black;")  # Yazı rengi
        return label
    
    
    def create_label2(self, text):
        label = QLabel(text)
        font = QFont("Times")
        font.setBold(True)
        font.setPointSize(30)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Sağ hizalama
        label.setFont(font)
        label.setStyleSheet("color: red;")  # Yazı rengi
        return label
    
    def create_label3(self, text, HAS_YUZDE,row):
        colors = [arka_fon1, arka_fon2]#colors = ["lightblue", "deepskyblue", "lightblue", "deepskyblue", "lightblue", "deepskyblue", "lightblue", "deepskyblue"]
        label = QLabel(text)
        font = QFont("Times")
        font.setBold(True)
        font.setPointSize(40)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Sağ hizalama        
        label.setFont(font)   
           
        if HAS_YUZDE > 0.5:
            label.setStyleSheet(f"background-color: {colors[row % len(colors)]}; color: lime; border:3px solid black;")  # Yazı rengi
        elif HAS_YUZDE < -0.5:
            label.setStyleSheet(f"background-color: {colors[row % len(colors)]}; color: red; border:3px solid black;")  # Yazı rengi
        else:           
            label.setStyleSheet(f"background-color: {colors[row % len(colors)]};color: {yazi_renk}; border:3px solid black;")  # Yazı rengi
        return label
    
    
    def update_datetime(self):
        now = datetime.now()
        gun = now.weekday()
        gun_adi = gun_isimleri[gun]
        gun = now.day
        ay = now.month - 1  # 0'dan başlıyor
        ay_adi = ay_isimleri[ay]
        yil = now.year
        saat = now.hour
        dakika = now.minute
        # Label'lar
        self.label_tarih.setText(now.strftime("%d.%m.%Y"))
        self.label_ay.setText(f"{ay_adi}")
        self.label_gun.setText(f"{gun_adi}")
        self.label_zaman.setText(f"{saat}:{dakika:02}")  # 2 haneli dakika     

    
    def create_gridlayout_sarrafiye(self, group, data, HAS_YUZDE):
        layout = group.layout()        
        group.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 36px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top center;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: white;'            
            'background-color:lightblue;'  # Arka plan rengi
            
            'font-size: 40px;'  # Yazı boyutu
            '}'
        )
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        row = 0
        layout.addWidget(self.create_label2("SARRAFİYE CİNSİ  "), row, 0)
        layout.addWidget(self.create_label2("ALIŞ    "), row, 1)
        layout.addWidget(self.create_label2("SATIŞ   "), row, 2)
        layout.addWidget(self.create_label2("K. KARTI       "), row, 3)        
        row += 1
         
        for key, value in data.items():            
            layout.addWidget(self.create_label3(f"{value[0]}  ", 0.0, row), row, 0)
            layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[1]))}  ", HAS_YUZDE, row), row, 1)
            layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[2]))}  ", HAS_YUZDE, row), row, 2)
            layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[3]))}       ", HAS_YUZDE, row), row, 3)
            row += 1
       
        return group
    
    def update_gridlayout_sarrafiye(self, group, data, HAS_YUZDE):
        layout = group.layout()
        #print(f"satır: {layout.rowCount()}")
        #print(f"sütun: {layout.columnCount()}")
        #print(data)
        veri =list(data)
        for row in range(1, layout.rowCount()):
            for col in range(layout.columnCount()):
                item = layout.itemAtPosition(row,col)
                if isinstance(item.widget(),QLabel):
                    label = item.widget()
                    #print(f'{label.objectName()} degeri: {label.text()}\n')
                    if col == 0:
                        label.setText(data[veri[row-1]][col])
                    elif col == 3:
                        label.setText(f"{self.format_number(self.round_number(data[veri[row-1]][col]))}       ")
                    else:
                        #print(data[row][col])
                        label.setText(f"{self.format_number(self.round_number(data[veri[row-1]][col]))}  ")
                    
#         for key, value in data.items():            
#             layout.addWidget(self.create_label3(f"{value[0]}  ", 0.0, row), row, 0)
#             layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[1]))}  ", HAS_YUZDE, row), row, 1)
#             layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[2]))}  ", HAS_YUZDE, row), row, 2)
#             layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[3]))}     ", HAS_YUZDE, row), row, 3)
#             row += 1
       
        return group
    
    def create_gridlayout_doviz(self, group):
        global default_factors1,doviz_data
        layout = group.layout()        
        group.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 36px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top center;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: white;'            
            'background-color:lightblue;'  # Arka plan rengi
            
            'font-size: 40px;'  # Yazı boyutu
            '}'
        )     
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        row = 0
        layout.addWidget(self.create_label2("DÖVİZ CİNSİ"),row, 0)
        layout.addWidget(self.create_label2("ALIŞ"),row, 1)
        layout.addWidget(self.create_label2("SATIŞ"),row, 2)        
        row += 1
        for value in doviz_data:
            layout.addWidget(self.create_label(f"{value[0]}  ",0.0,  row, 0), row, 0)
            if value[0] =="USD":
                alis = value[1]
                satis = value[2]
            elif value[0] =="EUR":
                alis = value[1]
                satis = value[2]
            alis_label = self.create_label(f"{alis:.2f} ", 0.0, row, 1)
            satis_label = self.create_label(f"{satis:.2f} ", 0.0, row, 2)
            layout.addWidget(alis_label, row, 1)
            layout.addWidget(satis_label, row, 2)            
            row += 1
    
    def update_gridlayout_doviz(self, group):
        global default_factors1, doviz_data
        layout = group.layout()
        #print(f"satır: {layout.rowCount()}")
        #print(f"sütun: {layout.columnCount()}")
        for row in range(1, layout.rowCount()):
            for col in range(layout.columnCount()):
                item = layout.itemAtPosition(row,col)
                if isinstance(item.widget(),QLabel):
                    label = item.widget()
                    #print(f'{label.objectName()} degeri: {label.text()}\n')
                    if col == 0:
                        label.setText(doviz_data[row-1][col])
                    elif col == 1:
                        alis = doviz_data[row-1][col]
                        label.setText(f"{alis:.2f} ")
                    else:
                        satis = doviz_data[row-1][col]
                        label.setText(f"{satis:.2f} ")
                    
#         for value in data:
#             layout.addWidget(self.create_label(f"{value[0]}  ",0.0,  row, 0), row, 0)
#             alis = round(value[1], 2) - 0.05
#             satis = round(value[2], 2) + 0.05
#             alis_label = self.create_label(f"{alis:.2f} ", 0.0, row, 1)
#             satis_label = self.create_label(f"{satis:.2f} ", 0.0, row, 2)
#             layout.addWidget(alis_label, row, 1)
#             layout.addWidget(satis_label, row, 2)            
#             row += 1
    
    
    def format_number(self, number):
        return "{:,}".format(number).replace(",", ".")
    
    def round_number(self, number):
        remainder = number % 10
        if remainder < 3:
            return number - remainder
        elif remainder < 8:
            return number - remainder + 5
        else:
            return number - remainder + 10

class Window2(QWidget):
    def __init__(self):
        global default_factors1, default_factors2
        super().__init__()
        self.caps_lock_flag = True
        self.active_input = None        
        self.setWindowTitle("Fiyat Ayarları")
        self.setGeometry(200, 200, 300, 150)
        self.move(20,40)
        row, col = 0, 0 
        # Comboboxlar ve input box'ı yerleştirmek için grid oluşturma
        grid_layout = QGridLayout()

        # Comboboxlar
        group_kayit = QGroupBox("Kayıtlı Sarrafiye Güncelleme")               
        group_kayit.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightslategrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
        group_kayit.setContentsMargins(10,20,10,10)
        hbox_kayit = QHBoxLayout()
        hbox_kayit.setContentsMargins(10,20,10,10)
        hbox_kayit.setSpacing(15)
        self.sarrafiye_label = QLabel('Sarrafiye Cinsi')
        self.sarrafiye_label.setFixedHeight(40)
        #self.sarrafiye_label.setFixedWidth(80)
        hbox_kayit.addWidget(self.sarrafiye_label, alignment = Qt.AlignLeft)
        self.altin_turu_combobox = QComboBox(self)
        self.altin_turu_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for key in default_factors2.keys():
            self.altin_turu_combobox.addItem(key)
        
        self.altin_turu_combobox.currentIndexChanged.connect(self.update_carpan_input_altin)
        self.altin_turu_combobox.setFixedHeight(40)
        #self.altin_turu_combobox.setFixedWidth(160)
        hbox_kayit.addWidget(self.altin_turu_combobox, alignment = Qt.AlignLeft)
              
        self.sarrafiye_alis_label = QLabel('ALIŞ')
        self.sarrafiye_alis_label.setFixedHeight(40)
        #self.sarrafiye_alis_label.setFixedWidth(100)
        hbox_kayit.addWidget(self.sarrafiye_alis_label, alignment = Qt.AlignRight)
        self.sarrafiye_alis_input = QLineEdit(self)
        #self.sarrafiye_alis_input.setText("0.000")
        self.sarrafiye_alis_input.setAlignment(Qt.AlignCenter)
        self.sarrafiye_alis_input.setMaxLength(6) 
        self.sarrafiye_alis_input.mousePressEvent = self.set_active_input_sarrafiye_alis
        self.sarrafiye_alis_input.setFixedHeight(40)
        hbox_kayit.addWidget(self.sarrafiye_alis_input, alignment = Qt.AlignLeft)
        
        self.sarrafiye_satis_label = QLabel('SATIŞ')
        self.sarrafiye_satis_label.setFixedHeight(40)
        hbox_kayit.addWidget(self.sarrafiye_satis_label, alignment = Qt.AlignRight)
        self.sarrafiye_satis_input = QLineEdit(self)
        self.sarrafiye_satis_input.setAlignment(Qt.AlignCenter)
        self.sarrafiye_satis_input.setMaxLength(6) 
        self.sarrafiye_satis_input.setFixedHeight(40)
        self.sarrafiye_satis_input.mousePressEvent = self.set_active_input_sarrafiye_satis
        hbox_kayit.addWidget(self.sarrafiye_satis_input, alignment = Qt.AlignLeft)
        
        self.sarrafiye_satis_kk_label = QLabel('SATIŞ K. KARTI')
        self.sarrafiye_satis_kk_label.setFixedHeight(40)
        hbox_kayit.addWidget(self.sarrafiye_satis_kk_label, alignment = Qt.AlignRight)
        self.sarrafiye_satis_kk_input = QLineEdit(self)
        #self.sarrafiye_satis_kk_input.setText("0.000")
        self.sarrafiye_satis_kk_input.setAlignment(Qt.AlignCenter)
        self.sarrafiye_satis_kk_input.setMaxLength(6) 
        self.sarrafiye_satis_kk_input.mousePressEvent = self.set_active_input_sarrafiye_satis_kk
        self.sarrafiye_satis_kk_input.setFixedHeight(40)
        hbox_kayit.addWidget(self.sarrafiye_satis_kk_input, alignment = Qt.AlignLeft)
        
        self.kaydet_button = QPushButton("KAYDET ALTIN", self)
        self.kaydet_button.setStyleSheet('QPushButton{'
        'font-size: 20px;'
        '}'
        ) 
        self.kaydet_button.clicked.connect(self.carpan_kaydet_altin)
        self.kaydet_button.setFixedHeight(40)
        hbox_kayit.addWidget(self.kaydet_button, alignment = Qt.AlignLeft)
        
        self.anasayfa_button = QPushButton("ANASAYFA", self)
        self.anasayfa_button.setStyleSheet('QPushButton{'
        'font-size: 20px;'
        '}'
        ) 
        self.anasayfa_button.clicked.connect(self.anasayfa)
        self.anasayfa_button.setFixedHeight(40)
        hbox_kayit.addWidget(self.anasayfa_button, alignment = Qt.AlignLeft)
        group_kayit.setLayout(hbox_kayit)
        grid_layout.addWidget(group_kayit,row , col, 1 , 5)
        row +=1
        
        #json data ekle
        group_ekle = QGroupBox("Yeni Sarrafiye Ekleme")
        group_ekle.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightgrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
        group_ekle.setContentsMargins(10,20,10,10)        
        hbox_ekle = QHBoxLayout()
        hbox_ekle.setContentsMargins(10,20,10,10)
        hbox_ekle.setSpacing(15)
        
        self.ekle_label = QLabel('Sarrafiye Cinsi')
        self.ekle_label.setFixedHeight(40)
        hbox_ekle.addWidget(self.ekle_label, alignment = Qt.AlignLeft)
        self.ekle_cins_input = QLineEdit(self)
        self.ekle_cins_input.mousePressEvent = self.set_active_input_ekle_cins
        self.ekle_cins_input.setFixedHeight(40)
        hbox_ekle.addWidget(self.ekle_cins_input, alignment = Qt.AlignLeft)
        
        self.ekle_alis_label = QLabel('ALIŞ')
        hbox_ekle.addWidget(self.ekle_alis_label, alignment = Qt.AlignRight)
        self.ekle_alis_label.setFixedHeight(40)
        self.ekle_alis_input = QLineEdit(self)
        self.ekle_alis_input.setAlignment(Qt.AlignCenter)
        self.ekle_alis_input.setMaxLength(6) 
        self.ekle_alis_input.mousePressEvent = self.set_active_input_ekle_alis
        self.ekle_alis_input.setFixedHeight(40)
        hbox_ekle.addWidget(self.ekle_alis_input, alignment = Qt.AlignLeft)
        
        self.ekle_satis_label = QLabel('SATIŞ')
        self.ekle_satis_label.setFixedHeight(40)
        hbox_ekle.addWidget(self.ekle_satis_label, alignment = Qt.AlignRight)
        self.ekle_satis_input = QLineEdit(self)
        self.ekle_satis_input.setAlignment(Qt.AlignCenter)
        self.ekle_satis_input.setMaxLength(6)
        self.ekle_satis_input.mousePressEvent = self.set_active_input_ekle_satis
        self.ekle_satis_input.setFixedHeight(40)
        hbox_ekle.addWidget(self.ekle_satis_input, alignment = Qt.AlignLeft)
        
        self.ekle_satis_kk_label = QLabel('SATIŞ K. KARTI')
        self.ekle_satis_kk_label.setFixedHeight(40)       
        hbox_ekle.addWidget(self.ekle_satis_kk_label, alignment = Qt.AlignRight)
        self.ekle_satis_kk_input = QLineEdit(self)
        self.ekle_satis_kk_input.setAlignment(Qt.AlignCenter)
        self.ekle_satis_kk_input.setMaxLength(6)
        self.ekle_satis_kk_input.mousePressEvent = self.set_active_input_ekle_satis_kk
        self.ekle_satis_kk_input.setFixedHeight(40)
        hbox_ekle.addWidget(self.ekle_satis_kk_input, alignment = Qt.AlignLeft)
        
        self.ekle_combobox = QComboBox(self)
        self.ekle_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for i in range(0, len(default_factors2)+1):
            self.ekle_combobox.addItem(str(i))
        
        #self.ekle_combobox.currentIndexChanged.connect(self.update_carpan_input_doviz)
        self.ekle_combobox.setFixedHeight(40)
        self.ekle_combobox.setToolTip("Ekran yerleşim sırasını gösterir")
        hbox_ekle.addWidget(self.ekle_combobox, alignment = Qt.AlignLeft) #
        
        self.ekle_button = QPushButton("EKLE")
        self.ekle_button.clicked.connect(self.sarrafiye_ekle)
        self.ekle_button.setFixedHeight(40)        
        hbox_ekle.addWidget(self.ekle_button, alignment = Qt.AlignLeft)
       
                
        self.ekle_durum_label = QLabel('')
        hbox_ekle.addWidget(self.ekle_durum_label)
        self.ekle_durum_label.setFixedHeight(40)       
        group_ekle.setLayout(hbox_ekle)
        grid_layout.addWidget(group_ekle,row , col, 1 , 3)
        row +=1
        #grid_layout.addLayout(hbox3, 2, 0, 1, 4)
        
        # Comboboxlar
        group_sil = QGroupBox("Kayıtlı Sarrafiye Silme")
        group_sil.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightslategrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
       
        group_sil.setContentsMargins(10,20,10,10)        
        hbox_sil = QHBoxLayout()
        hbox_sil.setContentsMargins(10,20,10,10)
        hbox_sil.setSpacing(15)
        
        self.sil_label = QLabel('Sarrafiye Cinsi')
        self.sil_label.setFixedHeight(40)
        hbox_sil.addWidget(self.sil_label, alignment = Qt.AlignLeft)
        self.sil_combobox = QComboBox(self)
        self.sil_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for key in default_factors2.keys():
            self.sil_combobox.addItem(key)
            
        self.sil_combobox.setFixedHeight(40)      
        
        #self.sil_combobox.currentIndexChanged.connect(self.update_carpan_input_altin)
        hbox_sil.addWidget(self.sil_combobox, alignment = Qt.AlignLeft) # 2 sütun genişliğinde
        
        
        self.sil_button = QPushButton("SİL")
        self.sil_button.clicked.connect(self.sarrafiye_sil)
        self.sil_button.setFixedHeight(40)        
        hbox_sil.addWidget(self.sil_button, alignment = Qt.AlignLeft)
        
        self.sil_durum_label = QLabel('')
        hbox_sil.addWidget(self.sil_durum_label)
        group_sil.setLayout(hbox_sil)
        grid_layout.addWidget(group_sil,row , col, 1 , 1)
        row +=1
        #grid_layout.addLayout(hbox_sil, 3, 0, 1, 4)
        
        
        # Döviz Ayar Satırı
        group_doviz = QGroupBox("Kayıtlı Döviz Güncelleme")
        group_doviz.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightgrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
        group_doviz.setContentsMargins(10,20,10,10)        
        hbox_doviz = QHBoxLayout()
        hbox_doviz.setContentsMargins(10,20,10,10)
        hbox_doviz.setSpacing(15)        
        
        self.doviz_label = QLabel('Döviz Cinsi           ')
        self.doviz_label.setFixedHeight(40)
        hbox_doviz.addWidget(self.doviz_label, alignment = Qt.AlignLeft)
        self.doviz_turu_combobox = QComboBox(self)
        self.doviz_turu_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for key in default_factors1.keys():
            self.doviz_turu_combobox.addItem(key)
        
        self.doviz_turu_combobox.currentIndexChanged.connect(self.update_carpan_input_doviz)
        self.doviz_turu_combobox.setFixedHeight(40)
        hbox_doviz.addWidget(self.doviz_turu_combobox, alignment = Qt.AlignLeft) # 2 sütun genişliğinde
        
        self.doviz_alis_label = QLabel('ALIŞ')
        self.doviz_alis_label.setFixedHeight(40)
        hbox_doviz.addWidget(self.doviz_alis_label, alignment = Qt.AlignRight)
        self.doviz_alis_input = QLineEdit(self)
        self.doviz_alis_input.setAlignment(Qt.AlignCenter)
        self.doviz_alis_input.setMaxLength(6) 
        self.doviz_alis_input.setFixedHeight(40)
        self.doviz_alis_input.mousePressEvent = self.set_active_input_doviz_alis
        hbox_doviz.addWidget(self.doviz_alis_input, alignment = Qt.AlignLeft)
        
        self.doviz_satis_label = QLabel('SATIŞ')
        self.doviz_satis_label.setFixedHeight(40)
        hbox_doviz.addWidget(self.doviz_satis_label, alignment = Qt.AlignRight)
        self.doviz_satis_input = QLineEdit(self)
        #self.sarrafiye_satis_input.setText("0.000")
        self.doviz_satis_input.setAlignment(Qt.AlignCenter)
        self.doviz_satis_input.setMaxLength(6) 
        self.doviz_satis_input.setFixedHeight(40)
        self.doviz_satis_input.mousePressEvent = self.set_active_input_doviz_satis
        hbox_doviz.addWidget(self.doviz_satis_input, alignment = Qt.AlignLeft)
        
        self.doviz_satis_kk_label = QLabel('SATIŞ K. KARTI')
        self.doviz_satis_kk_label.setFixedHeight(40)
        hbox_doviz.addWidget(self.doviz_satis_kk_label, alignment = Qt.AlignRight)
        self.doviz_satis_kk_input = QLineEdit(self)
        self.doviz_satis_kk_input.setAlignment(Qt.AlignCenter)
        self.doviz_satis_kk_input.setMaxLength(6) 
        self.doviz_satis_kk_input.mousePressEvent = self.set_active_input_doviz_satis_kk
        self.doviz_satis_kk_input.setFixedHeight(40)
        hbox_doviz.addWidget(self.doviz_satis_kk_input, alignment = Qt.AlignLeft)
        
        self.kaydet_button_doviz = QPushButton("KAYDET DOVIZ", self)
        self.kaydet_button_doviz.setStyleSheet('QPushButton{'
        'font-size: 20px;'
        '}'
        )
        self.kaydet_button_doviz.setFixedHeight(40)
        hbox_doviz.addWidget(self.kaydet_button_doviz, alignment = Qt.AlignLeft)
        self.kaydet_button_doviz.clicked.connect(self.carpan_kaydet_doviz)        
        group_doviz.setLayout(hbox_doviz)
        grid_layout.addWidget(group_doviz,row , col, 1 , 3)
        row +=1
    
        # WIFI bağlantısı
        group_WIFI = QGroupBox("WIFI Ayarları")
        group_WIFI.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightslategrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
        group_WIFI.setContentsMargins(10,20,10,10)        
        hbox_WIFI = QHBoxLayout()
        hbox_WIFI.setContentsMargins(10,20,10,10)
        hbox_WIFI.setSpacing(15)        
        self.scan_button = QPushButton("Wifi Ağlarını tara", self)
        self.scan_button.clicked.connect(self.scan_wifi_networks)
        hbox_WIFI.addWidget(self.scan_button)
        #grid_layout.addLayout(hbox_WIFI, row, 0, 1, 2)
        #row +=1
        
        #hbox_wifi_list = QHBoxLayout()
        self.combo =QComboBox(self)
        hbox_WIFI.addWidget(self.combo)
        #grid_layout.addLayout(hbox_wifi_list, row, 0, 1, 2)
        #row +=1
        
        #hbox_pass = QHBoxLayout()
        self.password_label = QLabel('WIFI Şifresi:')
        hbox_WIFI.addWidget(self.password_label)
        #grid_layout.addLayout(hbox_pass, row, 0, 1, 2)
        #row +=1
        
        #hbox_pass_in = QHBoxLayout()
        self.password_input = QLineEdit(self)
        self.password_input.mousePressEvent = self.set_active_input_password
        hbox_WIFI.addWidget(self.password_input)
        #grid_layout.addLayout(hbox_pass_in, row, 0, 1, 2)
        #row +=1
        
        #hbox_connect = QHBoxLayout()
        self.connect_button = QPushButton("Seçili Wifi ağına bağlan",self)
        self.connect_button.clicked.connect(self.connect_to_wifi)
        hbox_WIFI.addWidget(self.connect_button)        
        self.status_label = QLabel('')
        hbox_WIFI.addWidget(self.status_label)
        group_WIFI.setLayout(hbox_WIFI)
        grid_layout.addWidget(group_WIFI, row, 0, 1, 3)
        row +=1
        
        ######################################################
        group_yazi = QGroupBox("Tablo Yazı Ayarları")
        group_yazi.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightgrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
        group_yazi.setContentsMargins(10,20,10,10)        
        hbox_yazi = QHBoxLayout()
        hbox_yazi.setContentsMargins(10,20,10,10)
        hbox_yazi.setSpacing(15)        
               
        self.yazi_renk_button = QPushButton("Yazı Rengi")
        self.yazi_renk_button.clicked.connect(self.change_color)
        hbox_yazi.addWidget(self.yazi_renk_button)

        self.arka_fon1_button = QPushButton("Arka Fon Rengi-1")
        self.arka_fon1_button.clicked.connect(self.change_bckground1)
        hbox_yazi.addWidget(self.arka_fon1_button)
        
        self.arka_fon2_button = QPushButton("Arka Fon Rengi-2")
        self.arka_fon2_button.clicked.connect(self.change_bckground2)
        hbox_yazi.addWidget(self.arka_fon2_button)

        self.yazi_renk_label = QLabel('')
        hbox_yazi.addWidget(self.yazi_renk_label, alignment = Qt.AlignLeft)
        group_yazi.setLayout(hbox_yazi)
        grid_layout.addWidget(group_yazi,row , col, 1 , 2)
        row +=1
        ##############################################################
        group_logo = QGroupBox("Logo Yazı Ayarları")
        group_logo.setStyleSheet(
            'QGroupBox::title {'
            'color: Red;'  # Yazı rengi
            'font-size: 20px;'  # Yazı boyutu
            'subcontrol-origin: margin;'  # Başlık konumu
            'subcontrol-position: top left;'  # Başlığı ortala
            '}'
            'QGroupBox {'
            'color: black;'            
            'background-color: lightslategrey;'  # Arka plan rengi
            'font-size: 20px;'  # Yazı boyutu
            '}'
        )
        group_logo.setContentsMargins(10,20,10,10)        
        hbox_logo = QHBoxLayout()
        hbox_logo.setContentsMargins(10,20,10,10)
        hbox_logo.setSpacing(15)        
        self.toggle_btn = QPushButton("RESİM LOGO", self)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self.logo_sec)
        hbox_logo.addWidget(self.toggle_btn, alignment = Qt.AlignLeft)
        
        self.logo_label_in = QLabel("Logo Metni ")
        hbox_logo.addWidget(self.logo_label_in, alignment = Qt.AlignLeft)
        
        self.logo_input = QTextEdit(default_factors_renk["logo_content"])
        self.logo_input.mousePressEvent = self.set_active_input_logo
        ################################
        text_font = default_factors_renk["logo_font"]        
        text_fontsize = (int(default_factors_renk["logo_fontsize"]))
        #self.font = font_y
        text_backgrnd = default_factors_renk["logo_arka_fon"]["HEX"]
        text_color = default_factors_renk['logo_yazi_renk']["HEX"]
        text_bold = default_factors_renk["logo_fontweight"]
        text_italic = default_factors_renk["logo_fontitalic"]        
        if text_italic == True:
            text_italic = "italic"
        else:
            text_italic = ""
        
        text_alignment = default_factors_renk["logo_alignment"]            
        if text_alignment == 1:
            self.logo_input.setAlignment(Qt.AlignLeft)
        elif text_alignment == 2:
            self.logo_input.setAlignment(Qt.AlignRight)
        elif text_alignment == 8:
            self.logo_input.setAlignment(Qt.AlignJustify)    
        #font-size: {text_fontsize}px;
        self.logo_input.setStyleSheet(f"font: {text_font}; background-color:{text_backgrnd};color:{text_color};font-weight: {text_bold};font-style: {text_italic};")#setFont(font_y)
        #################################
        hbox_logo.addWidget(self.logo_input)
        
        self.yazi_renk_button = QPushButton("Yazı Rengi")
        self.yazi_renk_button.clicked.connect(self.change_color_logo)
        hbox_logo.addWidget(self.yazi_renk_button)

        self.logo_arka_fon_button = QPushButton("Logo Arka Fon Rengi")
        self.logo_arka_fon_button.clicked.connect(self.change_bckground_logo)
        hbox_logo.addWidget(self.logo_arka_fon_button)
        
        self.logo_font_combobox = QComboBox(self)
        self.logo_font_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        self.logo_font_combobox.addItem("Arial")
        self.logo_font_combobox.addItem("Times")
        self.logo_font_combobox.addItem("Courier")
        self.logo_font_combobox.addItem("Verdana")
        self.logo_font_combobox.addItem("Comic")
        self.logo_font_combobox.addItem("Helvetica")
        self.logo_font_combobox.addItem("Georgia")
        self.logo_font_combobox.addItem("Tahoma")
        self.logo_font_combobox.addItem("Trebuchet")


        self.logo_font_combobox.currentIndexChanged.connect(self.update_logo_font)
        self.logo_font_combobox.setFixedHeight(40)
        hbox_logo.addWidget(self.logo_font_combobox, alignment = Qt.AlignLeft) 
        
        self.logo_fontsize_combobox = QComboBox(self)
        self.logo_fontsize_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        self.logo_fontsize_combobox.addItem("40")
        self.logo_fontsize_combobox.addItem("48")
        self.logo_fontsize_combobox.addItem("56")
        self.logo_fontsize_combobox.addItem("62")
        self.logo_fontsize_combobox.addItem("70")
        self.logo_fontsize_combobox.addItem("76")
        self.logo_fontsize_combobox.addItem("84")       
        self.logo_fontsize_combobox.addItem("92") 

        self.logo_fontsize_combobox.currentIndexChanged.connect(self.update_logo_fontsize)
        self.logo_fontsize_combobox.setFixedHeight(40)
        hbox_logo.addWidget(self.logo_fontsize_combobox, alignment = Qt.AlignLeft)
               
        self.logo_yazi_renk_label = QLabel('')
        hbox_logo.addWidget(self.logo_yazi_renk_label, alignment = Qt.AlignLeft)
        group_logo.setLayout(hbox_logo)
        
        self.logo_app_button = QPushButton('Uygula')
        self.logo_app_button.clicked.connect(self.logo_app) 
        hbox_logo.addWidget(self.logo_app_button, alignment = Qt.AlignLeft)
        group_logo.setLayout(hbox_logo)
        grid_layout.addWidget(group_logo,row , 0, 3 , 3)
        row +=3


        #Keyboard Layout
        keyboard_layout = QHBoxLayout()
        #Butonlar
        self.add_keyboard_row(['1','2','3','4','5','6','7','8','9','0',], grid_layout, row, 0, 1, 2)
        row +=1
        self.add_keyboard_row(['Q','W','E','R','T','Y','U','I','O','P','Ğ','Ü','~'], grid_layout, row, 0, 1, 2)
        row +=1
        self.add_keyboard_row(['A','S','D','F','G','H','J','K','L','Ş','İ',',',';'], grid_layout, row, 0, 1, 2)
        row +=1
        self.add_keyboard_row(['Z','X','C','V','B','N','M','Ö','Ç','.',':'], grid_layout, row, 0, 1, 2)
        row +=1
        self.add_keyboard_row(['"','é','!','#','^','$','%','/','*','-','+','_'], grid_layout, row, 0, 1, 2)
        row +=1
        #Delete Button
        delete_button = QPushButton('Delete',self)
        delete_button.clicked.connect(self.delete_char)
        keyboard_layout.addWidget(delete_button)
        #Space Button
        space_button = QPushButton('Space',self)
        space_button.clicked.connect(self.space_char)
        keyboard_layout.addWidget(space_button)
        #Caps Lock Button
        capslock_button = QPushButton('CapsLock',self)
        capslock_button.clicked.connect(self.toggle_caps_lock)
        keyboard_layout.addWidget(capslock_button)
        #ENTER Button
        enter_button = QPushButton('ENTER',self)
        enter_button.clicked.connect(self.enter)
        keyboard_layout.addWidget(enter_button)
        #SOL Button
        SOL_button = QPushButton('SOL',self)
        SOL_button.clicked.connect(self.sol_hizala)
        keyboard_layout.addWidget(SOL_button)
        #SAG Button
        SAG_button = QPushButton('SAG',self)
        SAG_button.clicked.connect(self.sag_hizala)
        keyboard_layout.addWidget(SAG_button)
        #ORTALA Button
        enter_button = QPushButton('ORTALA',self)
        enter_button.clicked.connect(self.ortala_hizala)
        keyboard_layout.addWidget(enter_button)
        #KOYU Button
        KOYU_button = QPushButton('KOYU',self)
        KOYU_button.clicked.connect(self.koyu_renk)
        keyboard_layout.addWidget(KOYU_button)
        #ITALIC Button
        ITALIC_button = QPushButton('ITALIC',self)
        ITALIC_button.clicked.connect(self.italic_yazi)
        keyboard_layout.addWidget(ITALIC_button)
        
        UP_button = QPushButton('↑',self)
        UP_button.clicked.connect(self.up_direction)
        keyboard_layout.addWidget(UP_button)
        
        DOWN_button = QPushButton('↓',self)
        DOWN_button.clicked.connect(self.down_direction)
        keyboard_layout.addWidget(DOWN_button)
                
        LEFT_button = QPushButton('←',self)
        LEFT_button.clicked.connect(self.left_direction)
        keyboard_layout.addWidget(LEFT_button)
                
        RIGHT_button = QPushButton('→',self)
        RIGHT_button.clicked.connect(self.right_direction)
        keyboard_layout.addWidget(RIGHT_button)
        
        grid_layout.addLayout(keyboard_layout, row, 0, 1, 2)
        row +=1
        self.setLayout(grid_layout)
        self.active_input = self.logo_input  
        self.show()
        
    def logo_sec(self):
        global logo_flag
        if self.toggle_btn.isChecked():
            self.toggle_btn.setText("YAZI LOGO")
            logo_flag = 0
        else:
            self.toggle_btn.setText("RESİM LOGO")
            logo_flag = 1
        
    def change_color(self):
        global yazi_renk, default_factors_renk, address
        color = QColorDialog.getColor()
        if color.isValid():
            yazi_renk = color.name()            
            default_factors_renk['yazi_renk']['HEX'] = yazi_renk
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
            
            #print('Seçilen renk:', yazi_renk)
            self.yazi_renk_label.setText(str(color.name()+" rengini yazı rengi olarak seçtiniz"))
        # Change the text color of the label
        #self.label.setStyleSheet(f"color: {selected_color}; font-size: 18px;")
    
    def change_color_logo(self):
        global default_factors_renk
        color = QColorDialog.getColor()
        if color.isValid():
            logo_yazi_renk = color.name()
            #self.logo_input.setTextColor(color)
            default_factors_renk['logo_yazi_renk']['HEX'] = logo_yazi_renk
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)          
            
    
    def change_bckground1(self):
        global arka_fon1, default_factors_renk, address
        color = QColorDialog.getColor()
        if color.isValid():
            arka_fon1 = color.name()            
            default_factors_renk['arka_fon1']['HEX'] = arka_fon1
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
            
            #print('Seçilen renk:', arka_fon1)
            self.yazi_renk_label.setText(str(color.name()+" rengini yazı rengi olarak seçtiniz"))
        # Change the text color of the label
        #self.label.setStyleSheet(f"color: {selected_color}; font-size: 18px;")

    def change_bckground2(self):
        global arka_fon2, default_factors_renk, address
        color = QColorDialog.getColor()
        if color.isValid():
            arka_fon2 = color.name()            
            default_factors_renk['arka_fon2']['HEX'] = arka_fon2
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
            
            #print('Seçilen renk:', arka_fon2)
            self.yazi_renk_label.setText(str(color.name()+" rengini yazı rengi olarak seçtiniz"))
        # Change the text color of the label
    
    def change_bckground_logo(self):
        global logo_arka_fon, default_factors_renk, address
        color = QColorDialog.getColor()
        if color.isValid():
            logo_arka_fon = color.name()
            #self.logo_input.setTextBackgroundColor(logo_arka_fon)
            default_factors_renk['logo_arka_fon']['HEX'] = logo_arka_fon
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
            
            #print('Seçilen renk:', arka_fon1)
            self.logo_yazi_renk_label.setText(str(color.name()+" rengini yazı rengi olarak seçtiniz"))
        # Change the text color of the label
        #self.label.setStyleSheet(f"color: {selected_color}; font-size: 18px;")
    
    def update_logo_font(self):
        global default_factors_renk
        font = self.logo_font_combobox.currentText()
        #self.logo_label.setFont(self.font)
        default_factors_renk["logo_font"] = font
        with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
    
    def update_logo_fontsize(self):
        global default_factors_renk
        fontsize = self.logo_fontsize_combobox.currentText()
        #self.font.setPointSize(self.fontsize) 
        #self.logo_label.setFont(self.font)
        print(fontsize)
        default_factors_renk["logo_fontsize"] = fontsize
        with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
                
    def logo_app(self):
        global default_factors_renk
        text = self.logo_input.toPlainText()
        #self.logo_label.setText(text)
        font = self.active_input.font()        
        default_factors_renk["logo_content"] = text
        with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
                
    def set_active_input_sarrafiye_alis(self, event):
        self.active_input = self.sarrafiye_alis_input
        self.active_input.setToolTip("Alış Milyem katsayısını girin")
    
    def set_active_input_sarrafiye_satis(self, event):
        self.active_input = self.sarrafiye_satis_input
        self.active_input.setToolTip("Satış Milyem katsayısını girin")
        
    def set_active_input_sarrafiye_satis_kk(self, event):
        self.active_input = self.sarrafiye_satis_kk_input
        self.active_input.setToolTip("K. Kartı Satış komisyon yüzde değerini girin. Örneğin %04 için 1.04")

    def set_active_input_doviz_alis(self, event):
        self.active_input = self.doviz_alis_input
        self.active_input.setToolTip("Alış yüzde değerini girin. Örneğin %5 için -0.05")

    def set_active_input_doviz_satis(self, event):
        self.active_input = self.doviz_satis_input
        self.active_input.setToolTip("Satış yüzde değerini girin. Örneğin %5 için 0.05")
       
    def set_active_input_doviz_satis_kk(self, event):
        self.active_input = self.doviz_satis_kk_input
        self.active_input.setToolTip("K. Kartı Satış komisyon yüzde değerini girin. Örneğin %04 için 1.04")
        
    def set_active_input_ekle_cins(self, event):
        self.active_input = self.ekle_cins_input
        self.active_input.setToolTip("Eklemek istediğiniz Sarrafiye cinsini giriniz.")
    def set_active_input_ekle_alis(self, event):
        self.active_input = self.ekle_alis_input
        self.active_input.setToolTip("Alış Milyem katsayısını girin")
    
    def set_active_input_ekle_satis(self, event):
        self.active_input = self.ekle_satis_input
        self.active_input.setToolTip("Satış Milyem katsayısını girin")
   
    def set_active_input_ekle_satis_kk(self, event):
        self.active_input = self.ekle_satis_kk_input
        self.active_input.setToolTip("K. Kartı Satış komisyon yüzde değerini girin. Örneğin %04 için 1.04")
    
    def set_active_input_ssid(self, event):
        self.active_input = self.ssid_input
    
    def set_active_input_password(self, event):
        self.active_input =self.password_input
        
    def set_active_input_logo(self, event):
        self.active_input =self.logo_input       
    
    def add_keyboard_row(self,keys,layout, i, j , k, l):
        row_layout = QHBoxLayout()
        for key in keys:
            button =QPushButton(key,self)
            button.clicked.connect(self.type_char)
            row_layout.addWidget(button)
        layout.addLayout(row_layout, i, j, k, l)
        
    
    def type_char(self):
        msg = QMessageBox()
        msg.setWindowTitle('Yanlış Karakter Girişi')
        sender =self.sender()
        char = sender.text()
        if self.caps_lock_flag:
            char = char.upper()
        if  (self.active_input == self.ekle_alis_input or self.active_input == self.ekle_satis_input or self.active_input == self.ekle_satis_kk_input or
             self.active_input == self.sarrafiye_alis_input or self.active_input == self.sarrafiye_satis_input or self.active_input == self.sarrafiye_satis_kk_input) and char.isalpha():
            msg.setText('Milyem değeri giriş kutusuna sadece rakam girebilirsiniz')
            msg.exec_()                
        else:
            if self.active_input == self.logo_input:
                self.active_input.insertPlainText(sender.text())
            else:
                self.active_input.insert(sender.text())
                
    def delete_char(self):
        if self.active_input == self.logo_input:
            current_text = self.active_input.toPlainText()
            self.active_input.setText(current_text[:-1])
        else:            
            current_text = self.active_input.text()
            self.active_input.setText(current_text[:-1])
      
    def space_char(self):
        if self.active_input == self.logo_input:
            self.active_input.insertPlainText(' ')
        else:                
            self.active_input.insert(' ')
    
    def toggle_caps_lock(self):
        self.caps_lock_flag = not self.caps_lock_flag
        self.CapsLock()
    
    def CapsLock(self):
        for button in self.findChildren(QPushButton):
            if button.text().isalpha():
                if self.caps_lock_flag:
                    button.setText(button.text().upper())
                else:
                    button.setText(button.text().lower())
    
    def enter(self):        
        if self.active_input == self.logo_input:
            self.active_input.insertPlainText('\n')
        #else:
        #    self.active_input.insert('\n')
        
    def koyu_renk(self):
        global default_factors_renk
        current_font = self.active_input.font()
        if self.active_input == self.logo_input:            
            if current_font.weight() == QFont.Bold:
                current_font.setWeight(QFont.Normal)
            else:
                current_font.setWeight(QFont.Bold)
            default_factors_renk["logo_fontweight"] = current_font.weight()
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)    
        else:
            if current_font.weight() == QFont.Bold:
                current_font.setWeight(QFont.Normal)                
            else:
                current_font.setWeight(QFont.Bold)
        #self.active_input.font() = current_font
        self.active_input.setFont(current_font)
        
    def italic_yazi(self):        
        global default_factors_renk
        current_font = self.active_input.font()
        current_font.setItalic(not current_font.italic())
        if self.active_input == self.logo_input:            
            default_factors_renk["logo_fontitalic"] = current_font.italic()
            self.active_input.setFont(current_font)
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)    
        else:
            self.active_input.setFont(current_font)
        
    
    def sol_hizala(self):
        global default_factors_renk
        if self.active_input == self.logo_input:            
            default_factors_renk["logo_alignment"] = 1
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)  
        self.active_input.setAlignment(Qt.AlignLeft)
    
    def sag_hizala(self):
        global default_factors_renk
        if self.active_input == self.logo_input:            
            default_factors_renk["logo_alignment"] = 2
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
        self.active_input.setAlignment(Qt.AlignRight)
    
    def ortala_hizala(self):
        global default_factors_renk
        if self.active_input == self.logo_input:            
            default_factors_renk["logo_alignment"] = 8
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
        self.active_input.setAlignment(Qt.AlignCenter)
    
    def up_direction(self):
        cursor =self.logo_input.textCursor()
        cursor.movePosition(cursor.Up)
        self.logo_input.setTextCursor(cursor)
     
    def down_direction(self):
        cursor =self.logo_input.textCursor()
        cursor.movePosition(cursor.Down)
        self.logo_input.setTextCursor(cursor)
    
    def left_direction(self):
        cursor =self.logo_input.textCursor()
        cursor.movePosition(cursor.Left)
        self.logo_input.setTextCursor(cursor)
    
    def right_direction(self):
        cursor =self.logo_input.textCursor()
        cursor.movePosition(cursor.Right)
        self.logo_input.setTextCursor(cursor)
        
    def sarrafiye_ekle(self):
        global default_factors2, address
        sira = int(self.ekle_combobox.currentText())
        gold_type = self.ekle_cins_input.text()
        alis_type = self.ekle_alis_input.text()
        if ',' in alis_type:
            alis_type = alis_type.replace(",",".")
        try:
            alis_type = float(alis_type)
        except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")
        
        satis_type = self.ekle_satis_input.text()
        if ',' in satis_type:
            satis_type = satis_type.replace(",",".")
        try:
            satis_type = float(satis_type)
        except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")    
        
        satis_kk_type = self.ekle_satis_kk_input.text()
        if ',' in satis_kk_type:
            satis_kk_type = satis_kk_type.replace(",",".")
        try:
            satis_kk_type = float(satis_kk_type)
        except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")
        
        yeni_altin = {           
            "AlisY" : float(alis_type),
            "SatisY" : float(satis_type),
            "K_Karti" : float(satis_kk_type)
                
            }
        
        items = list(default_factors2.items())
        items.insert(sira,(gold_type, yeni_altin))
        default_factors2 = dict(items)
        with open(address +'default_factors2.json', 'w', encoding = 'utf-8') as json_file:
            json.dump(default_factors2, json_file, ensure_ascii = False, indent = 4)
            self.ekle_durum_label.setText(f'{gold_type} sarrafiye cinsi eklendi')
    
    def sarrafiye_sil(self):
        global default_factors2, address
        gold_type = self.sil_combobox.currentText()        
        del default_factors2[gold_type]
        with open(address +'default_factors2.json', 'w') as json_file:
            json.dump(default_factors2, json_file, ensure_ascii = False, indent = 4)
            self.sil_durum_label.setText(f'{gold_type} sarrafiye cinsi silindi')
            
    def toggle_password_visibility(self,state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            
    def scan_wifi_networks(self):
        try:
            output = subprocess.run(["nmcli","-f","SSID","device","wifi","list"], capture_output=True,text=True)
            networks = output.stdout.strip().split('\n')[1:]
            self.combo.clear()
            self.combo.addItems(networks)
            QMessageBox.information(self,'Bağlantı Durumu','Bağlantı var')
        except Exception as e:
            QMessageBox.critical(self,"Hata ",str(e))
            
    def connect_to_wifi(self):
        '''
ssid = self.ssid_input.text()
        password =self.password_input.text()
        
        try:
            command = f'nmcli dev wifi connect "{ssid}" password "{password}"'
            subprocess.run(command, shell = True, check = True)
            self.status_label.setText(f'{ssid} ağına bağlanıldı')
        except subprocess.CalledProcessError:
            self.status_label.setText('Bağlantı başarısız!')
'''
        ssid =self.combo.currentText()
        ssid =ssid.rstrip()
        if ssid:
            #self.ssid_input.mousePressEvent = self.set_active_input_ssid
            password = self.active_input.text()#self,"Şifre Girin",f'{selected_network} ağı için şifre girin')
            #if ok:
            try:
               subprocess.run(["nmcli","device","wifi","connect",ssid, "password",password],check=True)
               QMessageBox.information(self,'Bağlantı Durumu',f'{ssid} ağına başarıyla bağlandı')
            except subprocess.CalledProcessError:
               QMessageBox.warning(self,"Bağlantı Durumu","Bağlantı başarısız")
        else:
            QMessageBox.warning(self,"Ağ seçilmedi","Lütfen bir ağ seçin")
            
    def update_carpan_input_altin(self):
        global default_factors2

        gold_type = self.altin_turu_combobox.currentText()        
                
        if gold_type in default_factors2 :#and transaction_type in default_factors[gold_type]:
            current_factor = default_factors2[gold_type]['AlisY']
            self.sarrafiye_alis_input.setText(str(current_factor))
            current_factor = default_factors2[gold_type]['SatisY']
            self.sarrafiye_satis_input.setText(str(current_factor))
            current_factor = default_factors2[gold_type]['K_Karti']
            self.sarrafiye_satis_kk_input.setText(str(current_factor))                
        else:
            self.sarrafiye_alis_input.clear()
            self.sarrafiye_satis_input.clear()
            self.sarrafiye_satis_kk_input.clear()
        '''except FileNotFoundError:
            self.sarrafiye_alis_input.clear()
            self.sarrafiye_satis_input.clear()
            self.sarrafiye_satis_kk_input.clear()
'''
    def carpan_kaydet_altin(self): 
        # Seçili öğeleri al
        global default_factors2, address
        gold_type = self.altin_turu_combobox.currentText()        
        # JSON verisini güncelle
        if gold_type in default_factors2: 
            new_factor = self.sarrafiye_alis_input.text()
            if ',' in new_factor:
                new_factor = new_factor.replace(",", ".")
            try:
                default_factors2[gold_type]['AlisY'] = float(new_factor)
            except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")
            new_factor = self.sarrafiye_satis_input.text()
            if ',' in new_factor:
                new_factor = new_factor.replace(",", ".")
            try:
                default_factors2[gold_type]['SatisY'] = float(new_factor)
            except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")
            new_factor = self.sarrafiye_satis_kk_input.text()
            if ',' in new_factor:
                new_factor = new_factor.replace(",", ".")
            try:
                default_factors2[gold_type]['K_Karti'] = float(new_factor)
            except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 1.04 gibi sadece rakam ve nokta içermeli")    
        
            # Güncellenmiş veriyi JSON dosyasına yaz
            with open(address +'default_factors2.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors2, json_file, ensure_ascii = False, indent=4)
               
        
    def update_carpan_input_doviz(self):
        global default_factors1
        doviz_type = self.doviz_turu_combobox.currentText()
           
        if doviz_type in default_factors1 :
            current_factor = default_factors1[doviz_type]['AlisY']
            self.doviz_alis_input.setText(str(current_factor))
            current_factor = default_factors1[doviz_type]['SatisY']
            self.doviz_satis_input.setText(str(current_factor))
            current_factor = default_factors1[doviz_type]['K_Karti']
            self.doviz_satis_kk_input.setText(str(current_factor))                
        else:
            self.doviz_alis_input.clear()
            self.doviz_satis_input.clear()
            self.doviz_satis_kk_input.clear()
    '''except FileNotFoundError:
            self.doviz_alis_input.clear()
            self.doviz_satis_input.clear()
            self.doviz_satis_kk_input.clear()
            '''

    def carpan_kaydet_doviz(self):
        global default_factors1, address   
        
        doviz_type = self.doviz_turu_combobox.currentText()        
        # JSON verisini güncelle
        if doviz_type in default_factors1: 
            new_factor = self.doviz_alis_input.text()
            if ',' in new_factor:
                new_factor = new_factor.replace(",", ".")
            try:
                default_factors1[doviz_type]['AlisY'] = float(new_factor)
            except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")
            new_factor = self.doviz_satis_input.text()
            if ',' in new_factor:
                new_factor = new_factor.replace(",", ".")
            try:
                default_factors1[doviz_type]['SatisY'] = float(new_factor)
            except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 2.125 gibi sadece rakam ve nokta içermeli")
            new_factor = self.doviz_satis_kk_input.text()
            if ',' in new_factor:
                new_factor = new_factor.replace(",", ".")
            try:
                default_factors1[doviz_type]['K_Karti'] = float(new_factor)
            except ValueError:
                QMessageBox.warning(self,"Geçersiz giriş", "Girilen değer 1.04 gibi sadece rakam ve nokta içermeli")
            
            # Güncellenmiş veriyi JSON dosyasına yaz
            with open(address +'default_factors1.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors1, json_file, ensure_ascii = False, indent=4)
            
    
    def anasayfa(self):
        global ilk
        for window in QApplication.topLevelWidgets():
            window.close()
        self.close()
        self.window = MainWindow()
        self.window.show()
        ilk = 0
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    if kayitli_MAC_address == mac_address:
        try:            
            window = MainWindow()
        except subprocess.CalledProcessError:            
            window = WifiManager()
        window.show()
        sys.exit(app.exec_())#app.exec_()#
    else:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("MAC Uyumsuzluğu")
        msg_box.setText("Girilen MAC adresi bu cihaza ait değil")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
