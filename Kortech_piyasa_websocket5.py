
import time
from datetime import date
from datetime import datetime  
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGroupBox, QGridLayout, QPushButton, QLineEdit, QComboBox, QColorDialog, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt, QTimer# QThread
from PyQt5.QtGui import QPixmap, QFont#, QColor
import json
import os
import subprocess
import asyncio
import websockets
import warnings
warnings.filterwarnings("ignore")

local_version = "5.1"
local_file = "Kortech_piyasa_websocket5.py"
github_url = "https://raw.githubusercontent.com/bcetisli/Kuyumcu/main/update.json"

address = "/home/Kortech/Downloads/"
response =requests.get(github_url)
if response.status_code == 200:
    latest_code = response.json()
    latest_version = float(latest_code["version"])
    if latest_version > float(local_version):
        update_url = latest_code["file_url"]
        try:
            with open(address+local_file,"w") as f:
                response =requests.get(update_url)
                if response.status_code == 200:
                    f.write(response)
                    subprocess.run("python3",address+local_file)
        except Error as e:
            print("dosya kaydedilemedi")
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
        self.active_input.insert(sender.text())
    
    def delete_char(self):
        current_text = self.active_input.text()
        self.active_input.setText(current_text[:-1])
      
    def space_char(self):
        current_text = self.active_input.text()
        
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
                    
async def connect_and_listen():
    global HAS_ALIS_OLD, HAS_SATIS_OLD, USD_ALIS_OLD, USD_SATIS_OLD, EUR_ALIS_OLD, EUR_SATIS_OLD
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
        async with websockets.connect(uri) as websocket:
            message = await websocket.recv()
            veriler = json.loads(message)                
            for veri in veriler:
                if veri['kod'] == "HasAltin":
                    has_altin = ('HAS', veri['alis'], veri['satis'], 0.0)
                    has = (veri['alis'], veri['satis'])
                elif veri['kod'] == "Usd":
                    usd = (veri['alis'], veri['satis'])
                elif veri['kod'] == "Euro":
                    eur = (veri['alis'], veri['satis'])
                    doviz_data = [('USD', usd[0], usd[1]), ('EUR', eur[0], eur[1])]
                if eur[0] > 0.0:
                    break
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
    return has_altin, doviz_data

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
            elif item["Kod"] == 'EUR':
                EUR_alis = float(item["Alis"].replace(",","."))
                EUR_satis = float(item["Satis"].replace(",","."))
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
                alis = item["Satis"].replace(".","")
                has_satis = float(satis.replace(",","."))
                has_altin = ('HAS', has_alis, has_satis, 0.0)
                break    
    return has_altin, doviz_data
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag_liste = 1
        self.setWindowTitle("Piyasa Fiyatları")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()
        self.screen_width = self.screen().size().width()
        #print('Ekran genişliği', self.screen_width)
        # Arka plan rengini değiştirmek için stil sayfası ayarı
        #self.setStyleSheet('QWidget { background-color: lightblue; }')
        layout = QVBoxLayout()
        # Logo ve tarih-saat göstergesini içeren yatay düzen
        top_layout = QHBoxLayout()
                
        
        # Logo resmi ekleyin
        self.logo_label = QLabel()
        image_path = address +"Uslu_kuyumculuk2.jpg"
        if not os.path.exists(image_path):
            print("resim dosyası bulunamadı",image_path)
            return
        pixmap = QPixmap(image_path)  # Logonun dosya yolunu buraya ekleyin
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setStyleSheet("background-color: lightBlue;")
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
            print("resim dosyası bulunamadı",image_path2)
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
        
        # Timer ayarla
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
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
        global default_factors2, HAS_ALIS, HAS_SATIS, HAS_ALIS_OLD, HAS_SATIS_OLD,HAS_YUZDE, HAS_YUZDE_OLD
        global USD_ALIS_OLD,USD_SATIS_OLD, EUR_ALIS_OLD, EUR_SATIS_OLD
        try:
        
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
                altin_data = self.sarrafiye_hesapla(has_altin[1], has_altin[2])
                sayi = len(altin_data)
            if sayi == 7:
                self.altin_group = self.update_group_sarrafiye(self.altin_group, altin_data, has_altin[3])
            elif sayi > 7:
                fark = len(altin_data) - 7
                temp = altin_data 
                if self.flag_liste == 1:                                       
                    for ss in range(7,sayi):
                        del temp[ss]
                    self.altin_group = self.update_group_sarrafiye(self.altin_group, temp, has_altin[3])
                    self.flag_liste = 0
                elif self.flag_liste == 0:                     
                    for ss in range(7-fark,7):
                        del temp[ss]
                    self.altin_group = self.update_group_sarrafiye(self.altin_group, temp, has_altin[3])
                    self.flag_liste = 1
                    
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
            
            '''
            print(f'USD Alış Fiyatı: {doviz_data[0][1]}') 
            print(f'USD Satış Fiyatı: {doviz_data[0][2]}')
            print(f'EUR Alış Fiyatı: {doviz_data[1][1]}') 
            print(f'EUR Satış Fiyatı: {doviz_data[1][2]}')
            '''
            self.update_group_doviz(self.doviz_group, doviz_data)       
            

        except Exception as e:
            print(f"Hata:{e}")            
    
   
    def sarrafiye_hesapla(self, has_alis, has_satis):
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

    
    def update_group_sarrafiye(self, group, data, HAS_YUZDE):
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
            layout.addWidget(self.create_label3(f"{self.format_number(self.round_number(value[3]))}     ", HAS_YUZDE, row), row, 3)
            row += 1
       
        return group
    def update_group_doviz(self, group, data):
        layout = group.layout()
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
        for value in data:
            layout.addWidget(self.create_label(f"{value[0]}  ",0.0,  row, 0), row, 0)
            alis = round(value[1], 2) - 0.05
            satis = round(value[2], 2) + 0.05
            alis_label = self.create_label(f"{alis:.2f} ", 0.0, row, 1)
            satis_label = self.create_label(f"{satis:.2f} ", 0.0, row, 2)
            layout.addWidget(alis_label, row, 1)
            layout.addWidget(satis_label, row, 2)            
            row += 1
    
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

        # Comboboxlar ve input box'ı yerleştirmek için grid oluşturma
        grid_layout = QGridLayout()

        # 1. Satır: Comboboxlar
        hbox0 = QHBoxLayout()
        self.sarrafiye_label = QLabel('Mevcut Sarrafiye Cinsi')
        self.sarrafiye_label.setFixedHeight(40)
        #self.sarrafiye_label.setFixedWidth(80)
        hbox0.addWidget(self.sarrafiye_label, alignment = Qt.AlignLeft)
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
        hbox0.addWidget(self.altin_turu_combobox, alignment = Qt.AlignLeft)
              
        self.sarrafiye_alis_label = QLabel('ALIŞ')
        self.sarrafiye_alis_label.setFixedHeight(40)
        #self.sarrafiye_alis_label.setFixedWidth(100)
        hbox0.addWidget(self.sarrafiye_alis_label, alignment = Qt.AlignRight)
        self.sarrafiye_alis_input = QLineEdit(self)
        #self.sarrafiye_alis_input.setText("0.000")
        self.sarrafiye_alis_input.setAlignment(Qt.AlignCenter)
        self.sarrafiye_alis_input.setMaxLength(6) 
        self.sarrafiye_alis_input.mousePressEvent = self.set_active_input_sarrafiye_alis
        self.sarrafiye_alis_input.setFixedHeight(40)
        hbox0.addWidget(self.sarrafiye_alis_input, alignment = Qt.AlignLeft)
        
        self.sarrafiye_satis_label = QLabel('SATIŞ')
        self.sarrafiye_satis_label.setFixedHeight(40)
        hbox0.addWidget(self.sarrafiye_satis_label, alignment = Qt.AlignRight)
        self.sarrafiye_satis_input = QLineEdit(self)
        self.sarrafiye_satis_input.setAlignment(Qt.AlignCenter)
        self.sarrafiye_satis_input.setMaxLength(6) 
        self.sarrafiye_satis_input.setFixedHeight(40)
        self.sarrafiye_satis_input.mousePressEvent = self.set_active_input_sarrafiye_satis
        hbox0.addWidget(self.sarrafiye_satis_input, alignment = Qt.AlignLeft)
        
        self.sarrafiye_satis_kk_label = QLabel('SATIŞ K. KARTI')
        self.sarrafiye_satis_kk_label.setFixedHeight(40)
        hbox0.addWidget(self.sarrafiye_satis_kk_label, alignment = Qt.AlignRight)
        self.sarrafiye_satis_kk_input = QLineEdit(self)
        #self.sarrafiye_satis_kk_input.setText("0.000")
        self.sarrafiye_satis_kk_input.setAlignment(Qt.AlignCenter)
        self.sarrafiye_satis_kk_input.setMaxLength(6) 
        self.sarrafiye_satis_kk_input.mousePressEvent = self.set_active_input_sarrafiye_satis_kk
        self.sarrafiye_satis_kk_input.setFixedHeight(40)
        hbox0.addWidget(self.sarrafiye_satis_kk_input, alignment = Qt.AlignLeft)
        
        self.kaydet_button = QPushButton("KAYDET ALTIN", self)
        self.kaydet_button.setStyleSheet('QPushButton{'
        'font-size: 20px;'
        '}'
        ) 
        self.kaydet_button.clicked.connect(self.carpan_kaydet_altin)
        self.kaydet_button.setFixedHeight(40)
        hbox0.addWidget(self.kaydet_button, alignment = Qt.AlignLeft)
        
        self.anasayfa_button = QPushButton("ANASAYFA", self)
        self.anasayfa_button.setStyleSheet('QPushButton{'
        'font-size: 20px;'
        '}'
        ) 
        self.anasayfa_button.clicked.connect(self.anasayfa)
        self.anasayfa_button.setFixedHeight(40)
        hbox0.addWidget(self.anasayfa_button, alignment = Qt.AlignLeft)
        grid_layout.addLayout(hbox0, 0, 0, 1, 5)
        
        
        # 4. Satır: Döviz Ayar Satırı
        hbox1 = QHBoxLayout()
        self.doviz_label = QLabel('Döviz Cinsi           ')
        self.doviz_label.setFixedHeight(40)
        hbox1.addWidget(self.doviz_label, alignment = Qt.AlignLeft)
        self.doviz_turu_combobox = QComboBox(self)
        self.doviz_turu_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for key in default_factors1.keys():
            self.doviz_turu_combobox.addItem(key)
        
        self.doviz_turu_combobox.currentIndexChanged.connect(self.update_carpan_input_doviz)
        self.doviz_turu_combobox.setFixedHeight(40)
        hbox1.addWidget(self.doviz_turu_combobox, alignment = Qt.AlignLeft) # 2 sütun genişliğinde
        
        self.doviz_alis_label = QLabel('ALIŞ')
        self.doviz_alis_label.setFixedHeight(40)
        hbox1.addWidget(self.doviz_alis_label, alignment = Qt.AlignRight)
        self.doviz_alis_input = QLineEdit(self)
        self.doviz_alis_input.setAlignment(Qt.AlignCenter)
        self.doviz_alis_input.setMaxLength(6) 
        self.doviz_alis_input.setFixedHeight(40)
        self.doviz_alis_input.mousePressEvent = self.set_active_input_doviz_alis
        hbox1.addWidget(self.doviz_alis_input, alignment = Qt.AlignLeft)
        
        self.doviz_satis_label = QLabel('SATIŞ')
        self.doviz_satis_label.setFixedHeight(40)
        hbox1.addWidget(self.doviz_satis_label, alignment = Qt.AlignRight)
        self.doviz_satis_input = QLineEdit(self)
        #self.sarrafiye_satis_input.setText("0.000")
        self.doviz_satis_input.setAlignment(Qt.AlignCenter)
        self.doviz_satis_input.setMaxLength(6) 
        self.doviz_satis_input.setFixedHeight(40)
        self.doviz_satis_input.mousePressEvent = self.set_active_input_doviz_satis
        hbox1.addWidget(self.doviz_satis_input, alignment = Qt.AlignLeft)
        
        self.doviz_satis_kk_label = QLabel('SATIŞ K. KARTI')
        self.doviz_satis_kk_label.setFixedHeight(40)
        hbox1.addWidget(self.doviz_satis_kk_label, alignment = Qt.AlignRight)
        self.doviz_satis_kk_input = QLineEdit(self)
        self.doviz_satis_kk_input.setAlignment(Qt.AlignCenter)
        self.doviz_satis_kk_input.setMaxLength(6) 
        self.doviz_satis_kk_input.mousePressEvent = self.set_active_input_doviz_satis_kk
        self.doviz_satis_kk_input.setFixedHeight(40)
        hbox1.addWidget(self.doviz_satis_kk_input, alignment = Qt.AlignLeft)
        
        self.kaydet_button_doviz = QPushButton("KAYDET DOVIZ", self)
        self.kaydet_button_doviz.setStyleSheet('QPushButton{'
        'font-size: 20px;'
        '}'
        )
        self.kaydet_button_doviz.setFixedHeight(40)
        hbox1.addWidget(self.kaydet_button_doviz, alignment = Qt.AlignLeft)
        self.kaydet_button_doviz.clicked.connect(self.carpan_kaydet_doviz)        
        grid_layout.addLayout(hbox1, 1, 0, 1, 4)
                
        
        #7. satır json data ekle
        hbox3 = QHBoxLayout()
        self.ekle_label = QLabel('Yeni Sarrafiye Cinsi')
        self.ekle_label.setFixedHeight(40)
        hbox3.addWidget(self.ekle_label, alignment = Qt.AlignLeft)
        self.ekle_cins_input = QLineEdit(self)
        self.ekle_cins_input.mousePressEvent = self.set_active_input_ekle_cins
        self.ekle_cins_input.setFixedHeight(40)
        hbox3.addWidget(self.ekle_cins_input, alignment = Qt.AlignLeft)
        
        self.ekle_alis_label = QLabel('ALIŞ')
        hbox3.addWidget(self.ekle_alis_label, alignment = Qt.AlignRight)
        self.ekle_alis_label.setFixedHeight(40)
        self.ekle_alis_input = QLineEdit(self)
        self.ekle_alis_input.setAlignment(Qt.AlignCenter)
        self.ekle_alis_input.setMaxLength(6) 
        self.ekle_alis_input.mousePressEvent = self.set_active_input_ekle_alis
        self.ekle_alis_input.setFixedHeight(40)
        hbox3.addWidget(self.ekle_alis_input, alignment = Qt.AlignLeft)
        
        self.ekle_satis_label = QLabel('SATIŞ')
        self.ekle_satis_label.setFixedHeight(40)
        hbox3.addWidget(self.ekle_satis_label, alignment = Qt.AlignRight)
        self.ekle_satis_input = QLineEdit(self)
        self.ekle_satis_input.setAlignment(Qt.AlignCenter)
        self.ekle_satis_input.setMaxLength(6)
        self.ekle_satis_input.mousePressEvent = self.set_active_input_ekle_satis
        self.ekle_satis_input.setFixedHeight(40)
        hbox3.addWidget(self.ekle_satis_input, alignment = Qt.AlignLeft)
        
        self.ekle_satis_kk_label = QLabel('SATIŞ K. KARTI')
        self.ekle_satis_kk_label.setFixedHeight(40)       
        hbox3.addWidget(self.ekle_satis_kk_label, alignment = Qt.AlignRight)
        self.ekle_satis_kk_input = QLineEdit(self)
        self.ekle_satis_kk_input.setAlignment(Qt.AlignCenter)
        self.ekle_satis_kk_input.setMaxLength(6)
        self.ekle_satis_kk_input.mousePressEvent = self.set_active_input_ekle_satis_kk
        self.ekle_satis_kk_input.setFixedHeight(40)
        hbox3.addWidget(self.ekle_satis_kk_input, alignment = Qt.AlignLeft)
        
        self.ekle_combobox = QComboBox(self)
        self.ekle_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for i in range(0, len(default_factors2)+1):
            self.ekle_combobox.addItem(str(i))
        
        self.ekle_combobox.currentIndexChanged.connect(self.update_carpan_input_doviz)
        self.ekle_combobox.setFixedHeight(40)
        self.ekle_combobox.setToolTip("Ekran yerleşim sırasını gösterir")
        hbox3.addWidget(self.ekle_combobox, alignment = Qt.AlignLeft) #
        
        self.ekle_button = QPushButton("EKLE")
        self.ekle_button.clicked.connect(self.sarrafiye_ekle)
        self.ekle_button.setFixedHeight(40)        
        hbox3.addWidget(self.ekle_button, alignment = Qt.AlignLeft)
       
                
        self.ekle_durum_label = QLabel('')
        hbox3.addWidget(self.ekle_durum_label)
        self.ekle_durum_label.setFixedHeight(40)       
        
        grid_layout.addLayout(hbox3, 2, 0, 1, 4)
        
        # 1. Satır: Comboboxlar
        hbox4 = QHBoxLayout()
        self.sil_label = QLabel('Silinecek Sarrafiye Cinsi')
        self.sil_label.setFixedHeight(40)
        hbox4.addWidget(self.sil_label, alignment = Qt.AlignLeft)
        self.sil_combobox = QComboBox(self)
        self.sil_combobox.setStyleSheet('QComboBox{'
        'font-size: 20px;'
        '}'
        )
        
        for key in default_factors2.keys():
            self.sil_combobox.addItem(key)
            
        self.sil_combobox.setFixedHeight(40)      
        
        #self.sil_combobox.currentIndexChanged.connect(self.update_carpan_input_altin)
        hbox4.addWidget(self.sil_combobox, alignment = Qt.AlignLeft) # 2 sütun genişliğinde
        
        
        self.sil_button = QPushButton("SİL")
        self.sil_button.clicked.connect(self.sarrafiye_sil)
        self.sil_button.setFixedHeight(40)        
        hbox4.addWidget(self.sil_button, alignment = Qt.AlignLeft)
        
        self.sil_durum_label = QLabel('')
        hbox4.addWidget(self.sil_durum_label)
        grid_layout.addLayout(hbox4, 3, 0, 1, 4)
        
        # 8. satır WIFI bağlantısı
        hbox5 = QHBoxLayout()
        self.ssid_label = QLabel('WIFI Kullanıcı Adı:')
        hbox5.addWidget(self.ssid_label)
        self.ssid_input = QLineEdit(self)
        self.ssid_input.mousePressEvent = self.set_active_input_ssid
        hbox5.addWidget(self.ssid_input)
        
        self.password_label = QLabel('WIFI Şifresi:')
        hbox5.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.mousePressEvent = self.set_active_input_password        
        hbox5.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox('Şifreyi Göster')
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        hbox5.addWidget(self.show_password_checkbox)
        
        self.connect_button = QPushButton('Bağlan',self)
        self.connect_button.clicked.connect(self.connect_to_wifi)
        hbox5.addWidget(self.connect_button)
        
        self.status_label = QLabel('')
        hbox5.addWidget(self.status_label)
        
        grid_layout.addLayout(hbox5, 4, 0, 1, 2)
        
        ######################################################
        hbox6 = QHBoxLayout()
        
        self.yazi_renk_button = QPushButton("Yazı Rengi")
        self.yazi_renk_button.clicked.connect(self.change_color)
        hbox6.addWidget(self.yazi_renk_button)

        self.arka_fon1_button = QPushButton("Arka Fon Rengi-1")
        self.arka_fon1_button.clicked.connect(self.change_bckground1)
        hbox6.addWidget(self.arka_fon1_button)
        
        self.arka_fon2_button = QPushButton("Arka Fon Rengi-2")
        self.arka_fon2_button.clicked.connect(self.change_bckground2)
        hbox6.addWidget(self.arka_fon2_button)

        self.yazi_renk_label = QLabel('')
        hbox6.addWidget(self.yazi_renk_label, alignment = Qt.AlignLeft)
        grid_layout.addLayout(hbox6, 5, 0, 1, 2)
        ##############################################################



        #Keyboard Layout
        keyboard_layout = QHBoxLayout()
        #Butonlar
        self.add_keyboard_row(['1','2','3','4','5','6','7','8','9','0',], grid_layout, 6, 0, 1, 2)
        self.add_keyboard_row(['Q','W','E','R','T','Y','U','I','O','P','Ğ','Ü','~'], grid_layout, 7, 0, 1, 2)
        self.add_keyboard_row(['A','S','D','F','G','H','J','K','L','Ş','İ',',',';'], grid_layout, 8, 0, 1, 2)
        self.add_keyboard_row(['Z','X','C','V','B','N','M','Ö','Ç','.',':'], grid_layout, 9, 0, 1, 2)
        self.add_keyboard_row(['"','é','!','#','^','$','%','/','*','-','+','_'], grid_layout, 10, 0, 1, 2)
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
        grid_layout.addLayout(keyboard_layout, 11, 0, 1, 2)
        self.setLayout(grid_layout)
        self.show()

    def change_color(self):
        global yazi_renk, default_factors_renk, address
        color = QColorDialog.getColor()
        if color.isValid():
            yazi_renk = color.name()            
            default_factors_renk['yazi_renk']['HEX'] = yazi_renk
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
            
            print('Seçilen renk:', yazi_renk)
            self.yazi_renk_label.setText(str(color.name()+" rengini yazı rengi olarak seçtiniz"))
        # Change the text color of the label
        #self.label.setStyleSheet(f"color: {selected_color}; font-size: 18px;")
    
    def change_bckground1(self):
        global arka_fon1, default_factors_renk, address
        color = QColorDialog.getColor()
        if color.isValid():
            arka_fon1 = color.name()            
            default_factors_renk['arka_fon1']['HEX'] = arka_fon1
            with open(address +'default_factors_renk.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(default_factors_renk, json_file, ensure_ascii = False, indent = 4)
            
            print('Seçilen renk:', arka_fon1)
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
            
            print('Seçilen renk:', arka_fon2)
            self.yazi_renk_label.setText(str(color.name()+" rengini yazı rengi olarak seçtiniz"))
        # Change the text color of the label
    
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
            self.active_input.insert(sender.text())    
    def delete_char(self):
        current_text = self.active_input.text()
        self.active_input.setText(current_text[:-1])
      
    def space_char(self):
        current_text = self.active_input.text()
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
            
    def connect_to_wifi(self):
        ssid = self.ssid_input.text()
        password =self.password_input.text()
        
        try:
            command = f'nmcli dev wifi connect "{ssid}" password "{password}"'
            subprocess.run(command, shell = True, check = True)
            self.status_label.setText(f'{ssid} ağına bağlanıldı')
        except subprocess.CalledProcessError:
            self.status_label.setText('Bağlantı başarısız!')
      
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
        for window in QApplication.topLevelWidgets():
            window.close()
        self.close()
        self.window = MainWindow()
        self.window.show()
  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        subprocess.check_output(["ping","-c","1","google.com"])
        print('Bağlantı var')
        #Asyncio döngüsünü başlat
        has_altin, doviz_data = asyncio.run(connect_and_listen())#asyncio.get_event_loop().run_until_complete(connect_and_listen())
        HAS_GUN = has_altin[2]
        window = MainWindow()
    except subprocess.CalledProcessError:
        print("Bağlantı yok")
        window = WifiManager()
    window.show()
    sys.exit(app.exec_())
    


