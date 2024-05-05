import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

baglanti = sql.connect("proje.db")

# sql komutlarını python içinde de çalıştırabilmek için
cursor = baglanti.cursor()


class Gemi:

    def __init__(self, seri_numarasi, ad, agirlik, yapim_yili, gemi_turu, yolcu_kapasitesi=None, petrol_kapasitesi=None,
                 konteyner_sayisi=None, maksimum_agirlik=None):
        self.seri_numarasi = seri_numarasi

        self.ad = ad

        self.agirlik = agirlik

        self.yapim_yili = yapim_yili

        self.gemi_turu = gemi_turu

        self.yolcu_kapasitesi = yolcu_kapasitesi

        self.petrol_kapasitesi = petrol_kapasitesi

        self.konteyner_sayisi = konteyner_sayisi

        self.maksimum_agirlik = maksimum_agirlik

    @staticmethod
    def gemi_sil(seri_numarasi):
        print(seri_numarasi)
        cursor.execute('''SELECT gemi_turu FROM gemiler WHERE seri_no = ?''', (seri_numarasi,))
        gemi_turu = cursor.fetchone()[0]
        print(gemi_turu)

        # gemi_turu'na göre ilgili tabloyu seçerek gemiyi silebilirsiniz.
        if gemi_turu == "yolcu_gemileri":
            cursor.execute('''DELETE FROM yolcu_gemileri WHERE seri_no = ?''', (seri_numarasi,))
        elif gemi_turu == "petrol_tankerleri":
            cursor.execute('''DELETE FROM petrol_tankerleri WHERE seri_no = ?''', (seri_numarasi,))
        elif gemi_turu == "konteyner_gemileri":
            cursor.execute('''DELETE FROM konteyner_gemileri WHERE seri_no = ?''', (seri_numarasi,))

        cursor.execute('''DELETE FROM gemiler WHERE seri_no = ?''', (seri_numarasi,))
        baglanti.commit()


    @staticmethod
    def gemi_duzenle(seri_numarasi):

        Gemi_Pencereleri.gemi_ozellikleri_goster(seri_numarasi)

        baglanti.commit()

    def gemi_degistir(g_id, ozellik, degisen, ozellikler2, sutunlar, gemitur):
        tablo = ""
        if ozellik in ozellikler2:
            tablo = "gemiler"
        if ozellik in sutunlar:
            tablo = gemitur
        print(degisen, tablo, ozellik)
        cursor.execute('''UPDATE {} SET {} = ? WHERE seri_no = ?'''.format(tablo, ozellik),
                       (degisen, g_id))
        baglanti.commit()
        print("{} özelliği güncellendi.".format(ozellik))


class YolcuGemi(Gemi):
    def __init__(self, seri_numarasi, ad, agirlik, yapim_yili, yolcu_kapasitesi):
        super().__init__(seri_numarasi, ad, agirlik, yapim_yili, "Yolcu Gemi")
        self.yolcu_kapasitesi = yolcu_kapasitesi

    @staticmethod
    def gemi_ekle(seri_no, ad, agirlik, yapim_yili, yolcu_kapasitesi):
        cursor.execute('''INSERT INTO gemiler(seri_no, ad, agirlik, yapim_yili, gemi_turu) VALUES (?, ?, ?, ?, ?)''',
                       (seri_no, ad, agirlik, yapim_yili, "yolcu_gemileri"))

        cursor.execute('''INSERT INTO yolcu_gemileri(seri_no, yolcu_kapasitesi) VALUES (?, ?)''',
                       (seri_no, yolcu_kapasitesi))
        baglanti.commit()
        print("Yolcu gemisi eklendi.")


    @staticmethod
    def gemi_duzenle(seri_numarasi, ad, agirlik, yapim_yili, yolcu_kapasitesi):
        cursor.execute('''UPDATE gemiler SET ad = ?, agirlik = ?, yapim_yili = ? WHERE seri_no = ?''',
                       (ad, agirlik, yapim_yili, seri_numarasi))
        cursor.execute('''UPDATE yolcu_gemileri SET yolcu_kapasitesi = ? WHERE seri_no = ?''',
                       (yolcu_kapasitesi, seri_numarasi))
        baglanti.commit()
        print("Yolcu gemisi düzenlendi.")


class PetrolTankeri(Gemi):
    def __init__(self, seri_numarasi, ad, agirlik, yapim_yili, petrol_kapasitesi, petrol_birimi):
        super().__init__(seri_numarasi, ad, agirlik, yapim_yili, "Petrol Tankeri")
        self.petrol_kapasitesi = petrol_kapasitesi
        self.petrol_birimi = petrol_birimi

    @staticmethod
    def gemi_ekle(seri_no, ad, agirlik, yapim_yili, petrol_kapasitesi, petrol_birimi):
        cursor.execute('''INSERT INTO gemiler(seri_no, ad, agirlik, yapim_yili, gemi_turu) VALUES (?, ?, ?, ?, ?)''',
                       (seri_no, ad, agirlik, yapim_yili, "petrol_tankerleri"))

        cursor.execute('''INSERT INTO petrol_tankerleri(seri_no, petrol_kapasitesi, petrol_birimi) VALUES (?, ?, ?)''',
                       (seri_no, petrol_kapasitesi, petrol_birimi))
        baglanti.commit()
        print("Petrol tankeri eklendi.")


class KonteynerGemisi(Gemi):
    def __init__(self, seri_numarasi, ad, agirlik, yapim_yili, konteyner_sayisi, maksimum_agirlik):
        super().__init__(seri_numarasi, ad, agirlik, yapim_yili, "Konteyner Gemisi")
        self.konteyner_sayisi = konteyner_sayisi
        self.maksimum_agirlik = maksimum_agirlik

    @staticmethod
    def gemi_ekle(seri_no, ad, agirlik, yapim_yili, konteyner_sayisi, maksimum_agirlik):
        cursor.execute('''INSERT INTO gemiler(seri_no, ad, agirlik, yapim_yili, gemi_turu) VALUES (?, ?, ?, ?, ?)''',
                       (seri_no, ad, agirlik, yapim_yili, "konteyner_gemileri"))
        cursor.execute(
            '''INSERT INTO konteyner_gemileri(seri_no, konteyner_sayısı_kapasitesi, max_agırlık) VALUES (?, ?, ?)''',
            (seri_no, konteyner_sayisi, maksimum_agirlik))
        baglanti.commit()
        print("Konteyner gemisi eklendi.")


class Sefer:

    def __init__(self, s_id, gemi_id, cikis_tarihi, donus_tarihi, kalkis_liman):
        self.id = s_id

        self.gemi_id = gemi_id

        self.cikis_tarihi = cikis_tarihi

        self.donus_tarihi = donus_tarihi

        self.kalkis_liman = kalkis_liman

    def sefer_sil(s_id):
        cursor.execute('''DELETE FROM seferler WHERE id = ?''',
                       (s_id,))
        baglanti.commit()

    def sefer_ekle(seri_no, gemi_id, cikis_t, donus_t, kalkis_liman):
        cursor.execute('''INSERT INTO seferler(id, gemi_id, cikis_tarihi, donus_tarihi, kalkis_liman) VALUES (?, ?, ?, ?, ?)''',
                       (seri_no, gemi_id, cikis_t, donus_t, kalkis_liman))

        baglanti.commit()
        print("Sefer eklendi.")

    @staticmethod
    def sefer_degistir(s_id, ozellik, degisen):
        if ozellik == "Çıkış Tarihi":
            cursor.execute('''UPDATE seferler SET cikis_tarihi = ? WHERE id = ?''', (degisen, s_id))
        elif ozellik == "Dönüş Tarihi":
            cursor.execute('''UPDATE seferler SET donus_tarihi = ? WHERE id = ?''', (degisen, s_id))
        elif ozellik == "Kalkış Limanı":
            cursor.execute('''UPDATE seferler SET kalkis_liman = ? WHERE id = ?''', (degisen, s_id))
        else:
            # Geçersiz özellik durumu
            print("Geçersiz özellik!")

        baglanti.commit()



class Kaptan:

    def __init__(self, kaptan_id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans_no,
                 lisans_alis_tarihi):
        self.kaptan_id = kaptan_id

        self.ad = ad

        self.soyad = soyad

        self.adres = adres

        self.vatandaslik = vatandaslik

        self.dogum_tarihi = dogum_tarihi

        self.ise_giris_tarihi = ise_giris_tarihi

        self.lisans_no = lisans_no

        self.lisans_alis_tarihi = lisans_alis_tarihi

    def kaptan_sil(k_id):
        cursor.execute('''DELETE FROM kaptanlar WHERE id = ?''',
                       (k_id,))
        baglanti.commit()

    def kaptan_ekle(kaptan_id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans_no,
                 lisans_alis_tarihi):
        cursor.execute('''INSERT INTO kaptanlar(id, ad, soyad, adres, vatandaslik, dogum_tarihi,
         ise_giris_tarihi, lisans_no, lisans_alıs_tarihi) VALUES (?, ?, ?, ? , ?, ?, ?, ?, ?)''',
                       (kaptan_id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans_no,
                 lisans_alis_tarihi))

        baglanti.commit()
        print("Kaptan eklendi.")

    @staticmethod
    def kaptan_degistir(k_id, ozellik, degisen):
        cursor.execute('''UPDATE kaptanlar SET {} = ? WHERE ID = ?'''.format(ozellik),
                           (degisen, k_id))
        baglanti.commit()
        print("{} özelliği güncellendi.".format(ozellik))


class Murettebat:

    def __init__(self, m_id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev):
        self.id = m_id

        self.ad = ad

        self.soyad = soyad

        self.adres = adres

        self.vatandaslik = vatandaslik

        self.dogum_tarihi = dogum_tarihi

        self.ise_giris_tarihi = ise_giris_tarihi

        self.gorev = gorev

    def mur_sil(mur_id):
        cursor.execute('''DELETE FROM murettebat WHERE id = ?''',
                       (mur_id,))
        baglanti.commit()

    def mur_ekle(m_id, m_ad, m_soyad, m_adres, m_vatand,m_dogumt, m_is_t, m_gorev):
        cursor.execute('''INSERT INTO murettebat(id, ad, soyad, adres, vatandaslik, dogum_tarihi,
         ise_giris_tarihi, gorev) VALUES (?, ?, ?, ? , ?, ?, ?, ?)''',
                       (m_id, m_ad, m_soyad, m_adres, m_vatand, m_dogumt, m_is_t, m_gorev))

        baglanti.commit()
        print("Murettebat eklendi.")

    @staticmethod
    def mur_degistir(m_id, ozellik, degisen):
        cursor.execute('''UPDATE murettebat SET {} = ? WHERE ID = ?'''.format(ozellik),
                           (degisen, m_id))
        baglanti.commit()
        print("{} özelliği güncellendi.".format(ozellik))



class Liman:

    def __init__(self, liman_adi, ulke, nufus, pasaport_istiyor_mu, demirleme_ucreti):
        self.liman_adi = liman_adi

        self.ulke = ulke

        self.nufus = nufus

        self.pasaport_istiyor_mu = pasaport_istiyor_mu

        self.demirleme_ucreti = demirleme_ucreti


    def liman_ekle(l_ad, l_ulke, l_nufus, l_pasaport, l_demirleme):
        cursor.execute('''INSERT INTO limanlar(liman_adı, ulke, nufus, pasaport_istiyor_mu, demirleme_ucreti) VALUES (?, ?, ?, ?, ?)''',
                       (l_ad, l_ulke, l_nufus, l_pasaport, l_demirleme))

        baglanti.commit()
        print("Murettebat eklendi.")

    def liman_degistir(l_id, ozellik, degisen):
        cursor.execute('''UPDATE limanlar SET {} = ? WHERE liman_adı = ?'''.format(ozellik),
                           (degisen, l_id))
        baglanti.commit()
        print("{} özelliği güncellendi.".format(ozellik))

    def liman_sil(liman_adi):
        cursor.execute('''DELETE FROM limanlar WHERE liman_adı = ?''',
                       (liman_adi,))
        baglanti.commit()



# Gemiler için tablo oluşturma
cursor.execute('''CREATE TABLE IF NOT EXISTS gemiler (

                    seri_no INTEGER PRIMARY KEY,

                    ad VARCHAR(40),

                    agirlik DECIMAL(10,2),

                    yapim_yili INTEGER,

                    gemi_turu VARCHAR(40)

                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS yolcu_gemileri (

                    seri_no INTEGER PRIMARY KEY,
                    
                    yolcu_kapasitesi INTEGER,
                    
                    FOREIGN KEY(seri_no) REFERENCES gemiler(seri_no)

                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS petrol_tankerleri (

                    seri_no INTEGER PRIMARY KEY,

                    petrol_kapasitesi INTEGER,
                    
                    petrol_birimi VARCHAR(5),

                    FOREIGN KEY(seri_no) REFERENCES gemiler(seri_no)

                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS konteyner_gemileri (

                    seri_no INTEGER PRIMARY KEY,
                    
                    konteyner_sayısı_kapasitesi INTEGER,

                    max_agırlık DECIMAL(10,2),

                    FOREIGN KEY(seri_no) REFERENCES gemiler(seri_no)

                )''')

# Seferler için tablo oluşturma
cursor.execute('''CREATE TABLE IF NOT EXISTS seferler (

                    id INTEGER PRIMARY KEY,

                    gemi_id INTEGER,

                    cikis_tarihi DATE,

                    donus_tarihi DATE,

                    kalkis_liman VARCHAR(40),

                    FOREIGN KEY(gemi_id) REFERENCES gemiler(seri_no)

                )''')

# Kaptanlar için tablo oluşturma
cursor.execute('''CREATE TABLE IF NOT EXISTS kaptanlar (

                    id INTEGER PRIMARY KEY,

                    ad VARCHAR(25),

                    soyad VARCHAR(25),

                    adres VARCHAR(40),

                    vatandaslik VARCHAR(25),

                    dogum_tarihi DATE,

                    ise_giris_tarihi DATE,

                    lisans_no INTEGER,
                    
                    lisans_alıs_tarihi DATE

                )''')

# Mürettebat için tablo
cursor.execute('''CREATE TABLE IF NOT EXISTS murettebat (

                    id INTEGER PRIMARY KEY,

                    ad VARCHAR(25),

                    soyad VARCHAR(25),

                    adres VARCHAR(40),
                    
                    vatandaslik VARCHAR(25),

                    dogum_tarihi DATE,

                    ise_giris_tarihi DATE,

                    gorev VARCHAR(30)

                )''')

# Limanlar için tablo oluşturma
cursor.execute('''CREATE TABLE IF NOT EXISTS limanlar (

                    liman_adı VARCHAR(40),
    
                    ulke VARCHAR(25),

                    nufus INTEGER,

                    pasaport_istiyor_mu BOOLEAN,

                    demirleme_ucreti DECIMAL(10,2),
                    
                    PRIMARY KEY(liman_adı, ulke) -- liman_adı ve ulke sütunlarını birincil anahtar olarak belirler

                )''')

baglanti.commit()

class Gemi_Pencereleri:

    def gemiler_pencere():
        global gemiler_p
        gemiler_p = Tk()

        gemiler_p.title("Gemiler")
        gemiler_p.iconbitmap("gemilogo2.ico")
        gemiler_p.configure(bg="#06141A")
        gemiler_p.geometry("1530x750+0+0")

        gemiler_p.columnconfigure(0, weight=100)
        gemiler_p.columnconfigure(1, weight=300)
        gemiler_p.columnconfigure(2, weight=100)

        g_baslik = Label(gemiler_p, text="Gezgin Gemi \n Company", bg="#06141A", fg="#E5ECFF",
                         font=("Times New Roman", 40))
        g_baslik.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        g_geri_tusu = Button(gemiler_p, text="Menü", font=("Times New Roman", 10), bg="#5f92b0", padx=20, pady=5,
                             command=gemiler_p.destroy)
        g_geri_tusu.grid(row=0, column=0, padx=2, pady=5, sticky="nw")

        gemi_ekleme = Label(gemiler_p, text="Gemi Ekleme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        gemi_ekleme.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        gemi_silme = Label(gemiler_p, text="Gemi Silme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        gemi_silme.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        gemi_duzenle = Label(gemiler_p, text="Gemi Düzenleme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        gemi_duzenle.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        gemi_d_baslik = Label(gemiler_p, text="Düzenlenecek geminin ID'sini giriniz:", bg="#06141A", fg="#E5ECFF",
                              font=("Times New Roman", 15))

        gemi_d_baslik.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        gemi_d_entry = Entry(gemiler_p, width=20)
        gemi_d_entry.grid(row=5, column=2, padx=10, pady=15)

        gemi_d_buton = Button(gemiler_p, text="Gemi Düzenle", font=("Times New Roman", 15), bg="#A5C0D0", padx=20,
                              pady=5,
                              command=lambda: gemi_ozellikleri_goster(gemi_d_entry.get()))
        gemi_d_buton.grid(row=6, column=2, padx=10, pady=10)

        gemi_s_baslik = Label(gemiler_p, text="Silinecek geminin ID'sini giriniz:", bg="#06141A",
                              fg="#E5ECFF", font=("Times New Roman", 15))
        gemi_s_baslik.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        gemi_s_entry = Entry(gemiler_p, width=20)
        gemi_s_entry.grid(row=5, column=0, padx=10, pady=15)

        gemi_s_buton = Button(gemiler_p, text="Gemi Sil", font=("Times New Roman", 15), bg="#A5C0D0",
                              padx=20, pady=5, command=lambda: Gemi.gemi_sil(gemi_s_entry.get()))
        gemi_s_buton.grid(row=6, column=0, padx=10, pady=10)

        global gemi_e_yolcu
        gemi_e_yolcu = Button(gemiler_p, text="Yolcu Gemisi Ekle", font=("Times New Roman", 15), bg="#A5C0D0",
                              padx=20, pady=5, command=lambda: Gemi_Pencereleri.yolcu_gemisi_ekleme_p())
        gemi_e_yolcu.grid(row=4, column=1, padx=10, pady=10)

        global gemi_e_petrol
        gemi_e_petrol = Button(gemiler_p, text="Petrol Gemisi Ekle", font=("Times New Roman", 15), bg="#A5C0D0",
                               padx=20,
                               pady=5, command=lambda: Gemi_Pencereleri.petrol_gemi_ekleme_p())
        gemi_e_petrol.grid(row=5, column=1, padx=10, pady=10)

        global gemi_e_kont
        gemi_e_kont = Button(gemiler_p, text="Konteyner Gemisi Ekle", font=("Times New Roman", 15), bg="#A5C0D0",
                             padx=20,
                             pady=5, command=lambda: Gemi_Pencereleri.konteyner_gemi_ekleme_p())
        gemi_e_kont.grid(row=6, column=1, padx=10, pady=10)

        gemiler_p.mainloop()

    def yolcu_gemisi_ekleme_p():
        gemi_e_kont.destroy()
        gemi_e_yolcu.destroy()
        gemi_e_petrol.destroy()

        ygemi_id = Label(gemiler_p, text="Seri No:", bg="#06141A",
                              fg="#E5ECFF", font=("Times New Roman", 15))
        ygemi_id.grid(row=5, column=1, sticky="w", padx=(230, 5), pady=5)

        ygemi_id_entry = Entry(gemiler_p, width=20)
        ygemi_id_entry.grid(row=5, column=1, padx=(5, 280), pady=15, sticky="e")

        ygemi_ad = Label(gemiler_p, text="Ad:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        ygemi_ad.grid(row=6, column=1, sticky="w", padx=(270, 5), pady=5)

        ygemi_ad_entry = Entry(gemiler_p, width=20)
        ygemi_ad_entry.grid(row=6, column=1, padx=(5, 280), pady=15, sticky="e")

        ygemi_ton = Label(gemiler_p, text="Ağırlık:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        ygemi_ton.grid(row=7, column=1, sticky="w", padx=(235, 5), pady=5)

        ygemi_ton_entry = Entry(gemiler_p, width=20)
        ygemi_ton_entry.grid(row=7, column=1, padx=(5, 280), pady=15, sticky="e")

        ygemi_yil = Label(gemiler_p, text="Yapım Yılı:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        ygemi_yil.grid(row=8, column=1, sticky="w", padx=(220, 5), pady=5)

        ygemi_yil_entry = Entry(gemiler_p, width=20)
        ygemi_yil_entry.grid(row=8, column=1, padx=(5, 280), pady=15, sticky="e")

        ygemi_kapasite = Label(gemiler_p, text="Yolcu Kapasitesi:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        ygemi_kapasite.grid(row=9, column=1, sticky="w", padx=(170, 5), pady=5)

        ygemi_kapasite_entry = Entry(gemiler_p, width=20)
        ygemi_kapasite_entry.grid(row=9, column=1, padx=(5, 280), pady=15, sticky="e")

        gemi_e_yolcu2 = Button(gemiler_p, text="Yolcu Gemisi Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                              padx=20, pady=5, command=lambda: YolcuGemi.gemi_ekle(ygemi_id_entry.get(), ygemi_ad_entry.get(),
                                                                        ygemi_ton_entry.get(), ygemi_yil_entry.get(), ygemi_kapasite_entry.get()))
        gemi_e_yolcu2.grid(row=11, column=1, padx=10, pady=(50,5))


    def petrol_gemi_ekleme_p():
        gemi_e_kont.destroy()
        gemi_e_yolcu.destroy()
        gemi_e_petrol.destroy()

        pgemi_id = Label(gemiler_p, text="Seri No:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        pgemi_id.grid(row=5, column=1, sticky="w", padx=(230, 5), pady=5)

        pgemi_id_entry = Entry(gemiler_p, width=20)
        pgemi_id_entry.grid(row=5, column=1, padx=(5, 280), pady=15, sticky="e")

        pgemi_ad = Label(gemiler_p, text="Ad:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        pgemi_ad.grid(row=6, column=1, sticky="w", padx=(270, 5), pady=5)

        pgemi_ad_entry = Entry(gemiler_p, width=20)
        pgemi_ad_entry.grid(row=6, column=1, padx=(5, 280), pady=15, sticky="e")

        pgemi_ton = Label(gemiler_p, text="Ağırlık:", bg="#06141A",
                          fg="#E5ECFF", font=("Times New Roman", 15))
        pgemi_ton.grid(row=7, column=1, sticky="w", padx=(235, 5), pady=5)

        pgemi_ton_entry = Entry(gemiler_p, width=20)
        pgemi_ton_entry.grid(row=7, column=1, padx=(5, 280), pady=15, sticky="e")

        pgemi_yil = Label(gemiler_p, text="Yapım Yılı:", bg="#06141A",
                          fg="#E5ECFF", font=("Times New Roman", 15))
        pgemi_yil.grid(row=8, column=1, sticky="w", padx=(220, 5), pady=5)

        pgemi_yil_entry = Entry(gemiler_p, width=20)
        pgemi_yil_entry.grid(row=8, column=1, padx=(5, 280), pady=15, sticky="e")

        pgemi_kapasite = Label(gemiler_p, text="Petrol Kapasitesi:", bg="#06141A",
                               fg="#E5ECFF", font=("Times New Roman", 15))
        pgemi_kapasite.grid(row=9, column=1, sticky="w", padx=(170, 5), pady=5)

        pgemi_kapasite_entry = Entry(gemiler_p, width=20)
        pgemi_kapasite_entry.grid(row=9, column=1, padx=(5, 280), pady=15, sticky="e")

        gemi_e_petrol2 = Button(gemiler_p, text="Petrol Tankeri \n Gemisi Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                               padx=20, pady=5,
                               command=lambda: PetrolTankeri.gemi_ekle(pgemi_id_entry.get(), pgemi_ad_entry.get(),
                                                                   pgemi_ton_entry.get(), pgemi_yil_entry.get(),
                                                                   pgemi_kapasite_entry.get(), "Litre"))
        gemi_e_petrol2.grid(row=11, column=1, padx=10, pady=(50, 5))

    def konteyner_gemi_ekleme_p():
        gemi_e_kont.destroy()
        gemi_e_yolcu.destroy()
        gemi_e_petrol.destroy()

        kgemi_id = Label(gemiler_p, text="Seri No:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        kgemi_id.grid(row=5, column=1, sticky="w", padx=(230, 5), pady=5)

        kgemi_id_entry = Entry(gemiler_p, width=20)
        kgemi_id_entry.grid(row=5, column=1, padx=(5, 280), pady=15, sticky="e")

        kgemi_ad = Label(gemiler_p, text="Ad:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        kgemi_ad.grid(row=6, column=1, sticky="w", padx=(270, 5), pady=5)

        kgemi_ad_entry = Entry(gemiler_p, width=20)
        kgemi_ad_entry.grid(row=6, column=1, padx=(5, 280), pady=15, sticky="e")

        kgemi_ton = Label(gemiler_p, text="Ağırlık:", bg="#06141A",
                          fg="#E5ECFF", font=("Times New Roman", 15))
        kgemi_ton.grid(row=7, column=1, sticky="w", padx=(235, 5), pady=5)

        kgemi_ton_entry = Entry(gemiler_p, width=20)
        kgemi_ton_entry.grid(row=7, column=1, padx=(5, 280), pady=15, sticky="e")

        kgemi_yil = Label(gemiler_p, text="Yapım Yılı:", bg="#06141A",
                          fg="#E5ECFF", font=("Times New Roman", 15))
        kgemi_yil.grid(row=8, column=1, sticky="w", padx=(220, 5), pady=5)

        kgemi_yil_entry = Entry(gemiler_p, width=20)
        kgemi_yil_entry.grid(row=8, column=1, padx=(5, 280), pady=15, sticky="e")

        kgemi_kapasite = Label(gemiler_p, text="Konteyner Sayı Kapasitesi:", bg="#06141A",
                               fg="#E5ECFF", font=("Times New Roman", 15))
        kgemi_kapasite.grid(row=9, column=1, sticky="w", padx=(100, 5), pady=5)

        kgemi_kapasite_entry = Entry(gemiler_p, width=20)
        kgemi_kapasite_entry.grid(row=9, column=1, padx=(5, 280), pady=15, sticky="e")

        kgemi_max_a = Label(gemiler_p, text="Max Ağırlık:", bg="#06141A",
                               fg="#E5ECFF", font=("Times New Roman", 15))
        kgemi_max_a.grid(row=10, column=1, sticky="w", padx=(190, 5), pady=5)

        kgemi_max_a_entry = Entry(gemiler_p, width=20)
        kgemi_max_a_entry.grid(row=10, column=1, padx=(5, 280), pady=15, sticky="e")

        gemi_e_konteyner2 = Button(gemiler_p, text="Konteyner \n Gemisi Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                               padx=20, pady=5,
                               command=lambda: KonteynerGemisi.gemi_ekle(kgemi_id_entry.get(), kgemi_ad_entry.get(),
                                                                   kgemi_ton_entry.get(), kgemi_yil_entry.get(),
                                                                   kgemi_kapasite_entry.get(), kgemi_max_a_entry.get() ))
        gemi_e_konteyner2.grid(row=12, column=1, padx=10, pady=(50, 5))


    def gemi_ozellikleri_goster(seri_numarasi):

        # Seri numarasına göre gemi özelliklerini sorgula
        cursor.execute("SELECT * FROM gemiler WHERE seri_no = ?", (seri_numarasi,))
        gemi = cursor.fetchone()

        if gemi:
            # Tek satırlık tabloyu oluştur
            table_frame = LabelFrame(gemiler_p, text="Gemi Özellikleri")
            table_frame.grid(row=7, column=2, sticky="nsew", padx=10, pady=10)

            # Başlıklar
            columns = ["Seri Numarası", "Adı", "Ağırlık", "Yapım Yılı", "Tip"]

            # Başlıkları ekleme
            for col_index, col_name in enumerate(columns):
                label = Label(table_frame, text=col_name, padx=10, pady=5, relief="ridge")
                label.grid(row=0, column=col_index, sticky="nsew")

            # Verileri ekleme
            for col_index, col_data in enumerate(gemi):
                label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
                label.grid(row=1, column=col_index, sticky="nsew")
        else:
            messagebox.showerror("Hata", "Belirtilen seri numarasına sahip gemi bulunamadı.")

class Kaptanlar:

    def kaptanlar_pencere():
        global kaptanlar_p
        kaptanlar_p = Tk()

        kaptanlar_p.title("Gemiler")
        kaptanlar_p.iconbitmap("gemilogo2.ico")
        kaptanlar_p.configure(bg="#06141A")
        kaptanlar_p.geometry("1530x750+0+0")

        kaptanlar_p.columnconfigure(0, weight=100)
        kaptanlar_p.columnconfigure(1, weight=300)
        kaptanlar_p.columnconfigure(2, weight=100)

        k_baslik = Label(kaptanlar_p, text="Gezgin Gemi \n Company", bg="#06141A", fg="#E5ECFF",
                         font=("Times New Roman", 40))
        k_baslik.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        k_geri_tusu = Button(kaptanlar_p, text="Menü", font=("Times New Roman", 10), bg="#5f92b0", padx=20, pady=5,
                             command=kaptanlar_p.destroy)
        k_geri_tusu.grid(row=0, column=0, padx=2, pady=5, sticky="nw")

        kaptan_ekleme = Label(kaptanlar_p, text="Kaptan Ekleme", bg="#06141A", fg="#E5ECFF",
                              font=("Times New Roman", 20))
        kaptan_ekleme.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        kaptan_silme = Label(kaptanlar_p, text="Kaptan Silme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        kaptan_silme.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        kaptan_duzenle = Label(kaptanlar_p, text="Kaptan Düzenleme", bg="#06141A",
                               fg="#E5ECFF", font=("Times New Roman", 20))
        kaptan_duzenle.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        kaptan_d_baslik = Label(kaptanlar_p, text="Düzenlenecek kaptanın ID'sini giriniz:", bg="#06141A", fg="#E5ECFF",
                                font=("Times New Roman", 15))

        kaptan_d_baslik.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        kaptan_d_entry = Entry(kaptanlar_p, width=20)
        kaptan_d_entry.grid(row=5, column=2, padx=10, pady=15)

        kaptan_d_buton = Button(kaptanlar_p, text="Kaptan Getir", font=("Times New Roman", 15), bg="#A5C0D0",
                                padx=20, pady=5, command=lambda: Kaptanlar.kaptan_ozellikleri_goster(kaptan_d_entry.get()))
        kaptan_d_buton.grid(row=6, column=2, padx=10, pady=10)

        kaptan_s_baslik = Label(kaptanlar_p, text="Silinecek kaptanın ID'sini giriniz:", bg="#06141A",
                                fg="#E5ECFF", font=("Times New Roman", 15))
        kaptan_s_baslik.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        kaptan_s_entry = Entry(kaptanlar_p, width=20)
        kaptan_s_entry.grid(row=5, column=0, padx=10, pady=15)

        kaptan_s_buton = Button(kaptanlar_p, text="Kaptan Sil", font=("Times New Roman", 15), bg="#A5C0D0",
                                padx=20, pady=5, command=lambda: Kaptan.kaptan_sil(kaptan_s_entry.get()))
        kaptan_s_buton.grid(row=6, column=0, padx=10, pady=10)

        k_id = Label(kaptanlar_p, text="Seri No:", bg="#06141A",
                     fg="#E5ECFF", font=("Times New Roman", 15))
        k_id.grid(row=5, column=1, sticky="w", padx=(240, 5), pady=5)

        k_id_entry = Entry(kaptanlar_p, width=20)
        k_id_entry.grid(row=5, column=1, padx=(5, 280), pady=15, sticky="e")

        k_ad = Label(kaptanlar_p, text="Kaptan Ad:", bg="#06141A",
                      fg="#E5ECFF", font=("Times New Roman", 15))
        k_ad.grid(row=6, column=1, sticky="w", padx=(220, 5), pady=5)

        k_ad_entry = Entry(kaptanlar_p, width=20)
        k_ad_entry.grid(row=6, column=1, padx=(5, 280), pady=15, sticky="e")

        k_soyad = Label(kaptanlar_p, text="Soyad:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        k_soyad.grid(row=7, column=1, sticky="w", padx=(250, 5), pady=5)

        k_soyad_entry = Entry(kaptanlar_p, width=20)
        k_soyad_entry.grid(row=7, column=1, padx=(5, 280), pady=15, sticky="e")

        k_adres = Label(kaptanlar_p, text="Adres:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        k_adres.grid(row=8, column=1, sticky="w", padx=(250, 5), pady=5)

        k_adres_entry = Entry(kaptanlar_p, width=20)
        k_adres_entry.grid(row=8, column=1, padx=(5, 280), pady=15, sticky="e")

        k_vatand = Label(kaptanlar_p, text="Vatandaşlık:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        k_vatand.grid(row=9, column=1, sticky="w", padx=(200, 5), pady=5)

        k_vatand_entry = Entry(kaptanlar_p, width=20)
        k_vatand_entry.grid(row=9, column=1, padx=(5, 280), pady=15, sticky="e")

        k_dogumt = Label(kaptanlar_p, text="Doğum Tarihi:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        k_dogumt.grid(row=10, column=1, sticky="w", padx=(190, 5), pady=5)

        k_dogumt_entry = Entry(kaptanlar_p, width=20)
        k_dogumt_entry.grid(row=10, column=1, padx=(5, 280), pady=15, sticky="e")

        k_is_t = Label(kaptanlar_p, text="İşe Giriş T.:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        k_is_t.grid(row=11, column=1, sticky="w", padx=(200, 5), pady=5)

        k_is_t_entry = Entry(kaptanlar_p, width=20)
        k_is_t_entry.grid(row=11, column=1, padx=(5, 280), pady=15, sticky="e")

        k_lisans_n = Label(kaptanlar_p, text="Lisans No:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        k_lisans_n.grid(row=12, column=1, sticky="w", padx=(220, 5), pady=5)

        k_lisans_n_entry = Entry(kaptanlar_p, width=20)
        k_lisans_n_entry.grid(row=12, column=1, padx=(5, 280), pady=15, sticky="e")

        k_lisans_t = Label(kaptanlar_p, text="Lisans Tarihi:", bg="#06141A",
                           fg="#E5ECFF", font=("Times New Roman", 15))
        k_lisans_t.grid(row=13, column=1, sticky="w", padx=(200, 5), pady=5)

        k_lisans_t_entry = Entry(kaptanlar_p, width=20)
        k_lisans_t_entry.grid(row=13, column=1, padx=(5, 280), pady=15, sticky="e")

        kaptan_e = Button(kaptanlar_p, text="Sefer Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Kaptan.kaptan_ekle(k_id_entry.get(), k_ad_entry.get(),
                                                        k_soyad_entry.get(), k_adres_entry.get(), k_vatand_entry.get(),
                                                        k_dogumt_entry.get(), k_is_t_entry.get(), k_lisans_n_entry.get(),k_lisans_t_entry.get()))
        kaptan_e.grid(row=14, column=1, padx=10, pady=(50, 5))

        kaptanlar_p.mainloop()

    def kaptan_ozellikleri_goster(seri_numarasi):

        # Seri numarasına göre gemi özelliklerini sorgula
        cursor.execute("SELECT * FROM kaptanlar WHERE id = ?", (seri_numarasi,))
        kaptan = cursor.fetchone()

        if kaptan:
            # Tek satırlık tabloyu oluştur
            table_frame = LabelFrame(kaptanlar_p, text="Kaptan Özellikleri")
            table_frame.grid(row=7, column=2, sticky="n", padx=0, pady=0)

            # Başlıklar
            columns = ["Id", "Ad", "Soyad", "Adres", "Vatandaşlık", "Doğum T.", "İşe Giriş T.", "Lisans No", "Lisans Tarihi"]

            # Başlıkları ekleme
            for col_index, col_name in enumerate(columns):
                label = Label(table_frame, text=col_name, padx=10, pady=5, relief="ridge")
                label.grid(row=0, column=col_index, sticky="nsew")

            # Verileri ekleme
            for col_index, col_data in enumerate(kaptan):
                label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
                label.grid(row=1, column=col_index, sticky="nsew")
        else:
            messagebox.showerror("Hata", "Belirtilen Id sahip sefer bulunamadı.")

        ozellikler = ["ad", "soyad", "adres", "vatandaslik", "dogum_tarihi", "ise_giris_tarihi", "lisans_no", "lisans_alıs_tarihi"]

        # Combobox oluştur
        degisiklik_combobox = Combobox(kaptanlar_p, values=ozellikler)
        degisiklik_combobox.grid(row=9, column=2, sticky="n")

        k_degis = Entry(kaptanlar_p, width=20)
        k_degis.grid(row=10, column=2, padx=15, pady=20, sticky="n")

        kaptan_db = Button(kaptanlar_p, text="Kaptan Değiştir", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Kaptan.kaptan_degistir(seri_numarasi, degisiklik_combobox.get(), k_degis.get()))
        kaptan_db.grid(row=11, column=2, padx=10, pady=20)




class Seferler:

    def seferler_pencere():
        global seferler_p

        seferler_p = Tk()

        seferler_p.title("Gemiler")
        seferler_p.iconbitmap("gemilogo2.ico")
        seferler_p.configure(bg="#06141A")
        seferler_p.geometry("1530x750+0+0")

        seferler_p.columnconfigure(0, weight=100)
        seferler_p.columnconfigure(1, weight=300)
        seferler_p.columnconfigure(2, weight=100)

        s_baslik = Label(seferler_p, text="Gezgin Gemi \n Company", bg="#06141A", fg="#E5ECFF",
                         font=("Times New Roman", 40))
        s_baslik.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        s_geri_tusu = Button(seferler_p, text="Menü", font=("Times New Roman", 10), bg="#5f92b0", padx=20, pady=5,
                             command=seferler_p.destroy)
        s_geri_tusu.grid(row=0, column=0, padx=2, pady=5, sticky="nw")

        sefer_ekleme = Label(seferler_p, text="Sefer Ekleme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        sefer_ekleme.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        s_silme = Label(seferler_p, text="Sefer Silme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        s_silme.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        s_duzenle = Label(seferler_p, text="Sefer Düzenleme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        s_duzenle.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        s_d_baslik = Label(seferler_p, text="Düzenlenecek Seferin ID'sini giriniz:", bg="#06141A", fg="#E5ECFF",
                           font=("Times New Roman", 15))

        s_d_baslik.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        s_d_entry = Entry(seferler_p, width=20)
        s_d_entry.grid(row=5, column=2, padx=10, pady=15)

        s_d_buton = Button(seferler_p, text="Sefer Getir", font=("Times New Roman", 15), bg="#A5C0D0", padx=20,
                           pady=5,
                           command=lambda: Seferler.sefer_ozellikleri_goster(s_d_entry.get()))
        s_d_buton.grid(row=6, column=2, padx=10, pady=10)

        s_s_baslik = Label(seferler_p, text="Silinecek Seferin ID'sini giriniz:", bg="#06141A",
                           fg="#E5ECFF", font=("Times New Roman", 15))
        s_s_baslik.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        s_s_entry = Entry(seferler_p, width=20)
        s_s_entry.grid(row=5, column=0, padx=10, pady=15)

        s_s_buton = Button(seferler_p, text="Sefer Sil", font=("Times New Roman", 15), bg="#A5C0D0",
                           padx=20, pady=5, command=lambda: Sefer.sefer_sil(s_s_entry.get()))
        s_s_buton.grid(row=6, column=0, padx=10, pady=10)

        s_id = Label(seferler_p, text="Seri No:", bg="#06141A",
                     fg="#E5ECFF", font=("Times New Roman", 15))
        s_id.grid(row=5, column=1, sticky="w", padx=(250, 5), pady=5)

        s_id_entry = Entry(seferler_p, width=20)
        s_id_entry.grid(row=5, column=1, padx=(5, 240), pady=15, sticky="e")

        sg_id = Label(seferler_p, text="Gemi Id:", bg="#06141A",
                      fg="#E5ECFF", font=("Times New Roman", 15))
        sg_id.grid(row=6, column=1, sticky="w", padx=(250, 5), pady=5)

        sg_id_entry = Entry(seferler_p, width=20)
        sg_id_entry.grid(row=6, column=1, padx=(5, 240), pady=15, sticky="e")

        s_ctarih = Label(seferler_p, text="Çıkış Tarihi:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        s_ctarih.grid(row=7, column=1, sticky="w", padx=(220, 5), pady=5)

        s_ctarih_entry = Entry(seferler_p, width=20)
        s_ctarih_entry.grid(row=7, column=1, padx=(5, 240), pady=15, sticky="e")

        s_dtarih = Label(seferler_p, text="Dönüş Tarihi:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        s_dtarih.grid(row=8, column=1, sticky="w", padx=(210, 5), pady=5)

        s_dtarih_entry = Entry(seferler_p, width=20)
        s_dtarih_entry.grid(row=8, column=1, padx=(5, 240), pady=15, sticky="e")

        kalkis_l = Label(seferler_p, text="Kalkış Limanı:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        kalkis_l.grid(row=9, column=1, sticky="w", padx=(200, 5), pady=5)

        kalkis_l_entry = Entry(seferler_p, width=20)
        kalkis_l_entry.grid(row=9, column=1, padx=(5, 240), pady=15, sticky="e")

        sefer_e = Button(seferler_p, text="Sefer Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Sefer.sefer_ekle(s_id_entry.get(), sg_id_entry.get(),
                                                                           s_ctarih_entry.get(), s_dtarih_entry.get(),
                                                                           kalkis_l_entry.get()))
        sefer_e.grid(row=11, column=1, padx=10, pady=(50, 5))

        seferler_p.mainloop()

    def sefer_ozellikleri_goster(seri_numarasi):

        # Seri numarasına göre gemi özelliklerini sorgula
        cursor.execute("SELECT * FROM seferler WHERE id = ?", (seri_numarasi,))
        sefer = cursor.fetchone()

        if sefer:
            # Tek satırlık tabloyu oluştur
            table_frame = LabelFrame(seferler_p, text="Sefer Özellikleri")
            table_frame.grid(row=7, column=2, sticky="n", padx=0, pady=0)

            # Başlıklar
            columns = ["Id", "Gemi Id", "Çıkış T.", "Dönüş T.", "Kalkış Limanı"]

            # Başlıkları ekleme
            for col_index, col_name in enumerate(columns):
                label = Label(table_frame, text=col_name, padx=10, pady=5, relief="ridge")
                label.grid(row=0, column=col_index, sticky="nsew")

            # Verileri ekleme
            for col_index, col_data in enumerate(sefer):
                label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
                label.grid(row=1, column=col_index, sticky="nsew")
        else:
            messagebox.showerror("Hata", "Belirtilen Id sahip sefer bulunamadı.")

        ozellikler = ["Çıkış Tarihi", "Dönüş Tarihi", "Kalkış Limanı"]

        # Combobox oluştur
        degisiklik_combobox = Combobox(seferler_p, values=ozellikler)
        degisiklik_combobox.grid(row=9, column=2, sticky="n")

        s_degis = Entry(seferler_p, width=20)
        s_degis.grid(row=10, column=2, padx=15, pady=20, sticky="n")

        sefer_db = Button(seferler_p, text="Sefer Değiştir", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Sefer.sefer_degistir(seri_numarasi, degisiklik_combobox.get(), s_degis.get()))
        sefer_db.grid(row=11, column=2, padx=10, pady=20)


class Limanlar:
    def limanlar_pencere():
        global limanlar_p
        limanlar_p = Tk()

        limanlar_p.title("Gemiler")
        limanlar_p.iconbitmap("gemilogo2.ico")
        limanlar_p.configure(bg="#06141A")
        limanlar_p.geometry("1530x750+0+0")

        limanlar_p.columnconfigure(0, weight=100)
        limanlar_p.columnconfigure(1, weight=300)
        limanlar_p.columnconfigure(2, weight=100)

        l_baslik = Label(limanlar_p, text="Gezgin Gemi \n Company", bg="#06141A", fg="#E5ECFF",
                         font=("Times New Roman", 40))
        l_baslik.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        l_geri_tusu = Button(limanlar_p, text="Menü", font=("Times New Roman", 10), bg="#5f92b0", padx=20, pady=5,
                             command=limanlar_p.destroy)
        l_geri_tusu.grid(row=0, column=0, padx=2, pady=5, sticky="nw")

        l_ekleme = Label(limanlar_p, text="Liman Ekleme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        l_ekleme.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        l_silme = Label(limanlar_p, text="Liman Silme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        l_silme.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        l_duzenle = Label(limanlar_p, text="Liman Düzenleme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        l_duzenle.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        l_d_baslik = Label(limanlar_p, text="Düzenlenecek Limanın ID'sini giriniz:", bg="#06141A", fg="#E5ECFF",
                           font=("Times New Roman", 15))

        l_d_baslik.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        l_d_entry = Entry(limanlar_p, width=20)
        l_d_entry.grid(row=5, column=2, padx=10, pady=15)

        l_d_buton = Button(limanlar_p, text="Liman Düzenle", font=("Times New Roman", 15), bg="#A5C0D0", padx=20, pady=5,
                           command=lambda: Limanlar.liman_ozellikleri_goster(l_d_entry.get()))
        l_d_buton.grid(row=6, column=2, padx=10, pady=10)

        l_s_baslik = Label(limanlar_p, text="Silinecek Limanın ID'sini giriniz:", bg="#06141A",
                           fg="#E5ECFF", font=("Times New Roman", 15))
        l_s_baslik.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        l_s_entry = Entry(limanlar_p, width=20)
        l_s_entry.grid(row=5, column=0, padx=10, pady=15)

        l_s_buton = Button(limanlar_p, text="Liman Sil", font=("Times New Roman", 15), bg="#A5C0D0",
                           padx=20, pady=5, command=lambda: Liman.liman_sil(l_s_entry.get()))
        l_s_buton.grid(row=6, column=0, padx=10, pady=10)

        l_ad = Label(limanlar_p, text="Liman Ad:", bg="#06141A",
                      fg="#E5ECFF", font=("Times New Roman", 15))
        l_ad.grid(row=6, column=1, sticky="w", padx=(220, 5), pady=5)

        l_ad_entry = Entry(limanlar_p, width=20)
        l_ad_entry.grid(row=6, column=1, padx=(5, 280), pady=15, sticky="e")

        l_ulke = Label(limanlar_p, text="Ülke:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        l_ulke.grid(row=7, column=1, sticky="w", padx=(250, 5), pady=5)

        l_ulke_entry = Entry(limanlar_p, width=20)
        l_ulke_entry.grid(row=7, column=1, padx=(5, 280), pady=15, sticky="e")

        l_nufus = Label(limanlar_p, text="Nüfus:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        l_nufus.grid(row=8, column=1, sticky="w", padx=(240, 5), pady=5)

        l_nufus_entry = Entry(limanlar_p, width=20)
        l_nufus_entry.grid(row=8, column=1, padx=(5, 280), pady=15, sticky="e")

        l_pasaport = Label(limanlar_p, text="Pasaport İsteği:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        l_pasaport.grid(row=9, column=1, sticky="w", padx=(180, 5), pady=5)

        l_pasaport_entry = Entry(limanlar_p, width=20)
        l_pasaport_entry.grid(row=9, column=1, padx=(5, 280), pady=15, sticky="e")

        l_demirleme = Label(limanlar_p, text="Demirleme Ücreti:", bg="#06141A",
                           fg="#E5ECFF", font=("Times New Roman", 15))
        l_demirleme.grid(row=10, column=1, sticky="w", padx=(160, 5), pady=5)

        l_demirleme_entry = Entry(limanlar_p, width=20)
        l_demirleme_entry.grid(row=10, column=1, padx=(5, 280), pady=15, sticky="e")

        liman_e = Button(limanlar_p, text="Liman Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Liman.liman_ekle(l_ad_entry.get(), l_ulke_entry.get(),
                                                                           l_nufus_entry.get(), l_pasaport_entry.get(),
                                                                           l_demirleme_entry.get()))
        liman_e.grid(row=11, column=1, padx=10, pady=(50, 5))

        limanlar_p.mainloop()

    def liman_ozellikleri_goster(seri_numarasi):

        # Seri numarasına göre gemi özelliklerini sorgula
        cursor.execute("SELECT * FROM limanlar WHERE liman_adı = ?", (seri_numarasi,))
        liman = cursor.fetchone()

        if liman:
            # Tek satırlık tabloyu oluştur
            table_frame = LabelFrame(limanlar_p, text="Liman Özellikleri")
            table_frame.grid(row=7, column=2, sticky="n", padx=0, pady=0)

            # Başlıklar
            columns = ["Liman Ad", "Ülke", "Nüfus", "Pasaport İsteği", "Demirleme Ücret"]

            # Başlıkları ekleme
            for col_index, col_name in enumerate(columns):
                label = Label(table_frame, text=col_name, padx=10, pady=5, relief="ridge")
                label.grid(row=0, column=col_index, sticky="nsew")

            # Verileri ekleme
            for col_index, col_data in enumerate(liman):
                label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
                label.grid(row=1, column=col_index, sticky="nsew")
        else:
            messagebox.showerror("Hata", "Belirtilen Id sahip liman bulunamadı.")

        ozellikler = ["liman_adı", "ulke", "nufus", "pasaport_istiyor_mu", "demirleme_ucreti"]

        # Combobox oluştur
        degisiklik_combobox = Combobox(limanlar_p, values=ozellikler)
        degisiklik_combobox.grid(row=9, column=2, sticky="n")

        l_degis = Entry(limanlar_p, width=20)
        l_degis.grid(row=10, column=2, padx=15, pady=20, sticky="n")

        liman_db = Button(limanlar_p, text="Liman Değiştir", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Liman.liman_degistir(seri_numarasi, degisiklik_combobox.get(), l_degis.get()))
        liman_db.grid(row=11, column=2, padx=10, pady=20)



class Murettebatlar:
    def murettebat_pencere():
        global murettebat_p
        murettebat_p = Tk()

        murettebat_p.title("Gemiler")
        murettebat_p.iconbitmap("gemilogo2.ico")
        murettebat_p.configure(bg="#06141A")
        murettebat_p.geometry("1530x750+0+0")

        murettebat_p.columnconfigure(0, weight=100)
        murettebat_p.columnconfigure(1, weight=300)
        murettebat_p.columnconfigure(2, weight=100)

        m_baslik = Label(murettebat_p, text="Gezgin Gemi \n Company", bg="#06141A", fg="#E5ECFF",
                         font=("Times New Roman", 40))
        m_baslik.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        m_geri_tusu = Button(murettebat_p, text="Menü", font=("Times New Roman", 10), bg="#5f92b0", padx=20, pady=5,
                             command=murettebat_p.destroy)
        m_geri_tusu.grid(row=0, column=0, padx=2, pady=5, sticky="nw")

        m_ekleme = Label(murettebat_p, text="Mürettebat Ekleme", bg="#06141A", fg="#E5ECFF",
                         font=("Times New Roman", 20))
        m_ekleme.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        m_silme = Label(murettebat_p, text="Mürettebat Silme", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 20))
        m_silme.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        m_duzenle = Label(murettebat_p, text="Mürettebat Düzenleme", bg="#06141A", fg="#E5ECFF",
                          font=("Times New Roman", 20))
        m_duzenle.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        m_d_baslik = Label(murettebat_p, text="Düzenlenecek Mürettebatın ID'sini giriniz:", bg="#06141A", fg="#E5ECFF",
                           font=("Times New Roman", 15))

        m_d_baslik.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        m_d_entry = Entry(murettebat_p, width=20)
        m_d_entry.grid(row=5, column=2, padx=10, pady=15)

        m_d_buton = Button(murettebat_p, text="Mürettebat Getir", font=("Times New Roman", 15), bg="#A5C0D0", padx=20,
                           pady=5,
                           command=lambda: Murettebatlar.mur_ozellikleri_goster(m_d_entry.get()))
        m_d_buton.grid(row=6, column=2, padx=10, pady=10)

        m_s_baslik = Label(murettebat_p, text="Silinecek Mürettebatın ID'sini giriniz:", bg="#06141A",
                           fg="#E5ECFF", font=("Times New Roman", 15))
        m_s_baslik.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        m_s_entry = Entry(murettebat_p, width=20)
        m_s_entry.grid(row=5, column=0, padx=10, pady=15)

        m_s_buton = Button(murettebat_p, text="Mürettebat Sil", font=("Times New Roman", 15), bg="#A5C0D0",
                           padx=20, pady=5, command=lambda: Murettebat.mur_sil(m_s_entry.get()))
        m_s_buton.grid(row=6, column=0, padx=10, pady=10)

        m_id = Label(murettebat_p, text="Personel No:", bg="#06141A",
                     fg="#E5ECFF", font=("Times New Roman", 15))
        m_id.grid(row=5, column=1, sticky="w", padx=(160, 5), pady=5)

        m_id_entry = Entry(murettebat_p, width=20)
        m_id_entry.grid(row=5, column=1, padx=(5, 280), pady=15, sticky="e")

        m_ad = Label(murettebat_p, text="Ad:", bg="#06141A",
                     fg="#E5ECFF", font=("Times New Roman", 15))
        m_ad.grid(row=6, column=1, sticky="w", padx=(230, 5), pady=5)

        m_ad_entry = Entry(murettebat_p, width=20)
        m_ad_entry.grid(row=6, column=1, padx=(5, 280), pady=15, sticky="e")

        m_soyad = Label(murettebat_p, text="Soyad:", bg="#06141A",
                        fg="#E5ECFF", font=("Times New Roman", 15))
        m_soyad.grid(row=7, column=1, sticky="w", padx=(210, 5), pady=5)

        m_soyad_entry = Entry(murettebat_p, width=20)
        m_soyad_entry.grid(row=7, column=1, padx=(5, 280), pady=15, sticky="e")

        m_adres = Label(murettebat_p, text="Adres:", bg="#06141A",
                        fg="#E5ECFF", font=("Times New Roman", 15))
        m_adres.grid(row=8, column=1, sticky="w", padx=(210, 5), pady=5)

        m_adres_entry = Entry(murettebat_p, width=20)
        m_adres_entry.grid(row=8, column=1, padx=(5, 280), pady=15, sticky="e")

        m_vatand = Label(murettebat_p, text="Vatandaşlık:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        m_vatand.grid(row=9, column=1, sticky="w", padx=(160, 5), pady=5)

        m_vatand_entry = Entry(murettebat_p, width=20)
        m_vatand_entry.grid(row=9, column=1, padx=(5, 280), pady=15, sticky="e")

        m_dogumt = Label(murettebat_p, text="Doğum Tarihi:", bg="#06141A",
                         fg="#E5ECFF", font=("Times New Roman", 15))
        m_dogumt.grid(row=10, column=1, sticky="w", padx=(150, 5), pady=5)

        m_dogumt_entry = Entry(murettebat_p, width=20)
        m_dogumt_entry.grid(row=10, column=1, padx=(5, 280), pady=15, sticky="e")

        m_is_t = Label(murettebat_p, text="İşe Giriş T.:", bg="#06141A",
                       fg="#E5ECFF", font=("Times New Roman", 15))
        m_is_t.grid(row=11, column=1, sticky="w", padx=(170, 5), pady=5)

        m_is_t_entry = Entry(murettebat_p, width=20)
        m_is_t_entry.grid(row=11, column=1, padx=(5, 280), pady=15, sticky="e")

        m_gorev = Label(murettebat_p, text="Görev:", bg="#06141A",
                           fg="#E5ECFF", font=("Times New Roman", 15))
        m_gorev.grid(row=12, column=1, sticky="w", padx=(210, 5), pady=5)

        m_gorev_entry = Entry(murettebat_p, width=20)
        m_gorev_entry.grid(row=12, column=1, padx=(5, 280), pady=15, sticky="e")

        murettebat_e = Button(murettebat_p, text="Murettebat Ekle", font=("Times New Roman", 12), bg="#A5C0D0",
                          padx=20, pady=5, command=lambda: Murettebat.mur_ekle(m_id_entry.get(), m_ad_entry.get(),
                                                                              m_soyad_entry.get(), m_adres_entry.get(),
                                                                              m_vatand_entry.get(),
                                                                              m_dogumt_entry.get(), m_is_t_entry.get(),
                                                                              m_gorev_entry.get()))
        murettebat_e.grid(row=14, column=1, padx=10, pady=(50, 5))

        murettebat_p.mainloop()

    def mur_ozellikleri_goster(seri_numarasi):

        # Seri numarasına göre gemi özelliklerini sorgula
        cursor.execute("SELECT * FROM murettebat WHERE id = ?", (seri_numarasi,))
        murt = cursor.fetchone()

        if murt:
            # Tek satırlık tabloyu oluştur
            table_frame = LabelFrame(murettebat_p, text="Sefer Özellikleri")
            table_frame.grid(row=7, column=2, sticky="n", padx=0, pady=0)

            # Başlıklar
            columns = ["Id", "Ad", "Soyad", "Adres", "Vatandaşlık", "Doğum Tarihi", "İşe Giriş Tarihi", "Görev"]

            # Başlıkları ekleme
            for col_index, col_name in enumerate(columns):
                label = Label(table_frame, text=col_name, padx=10, pady=5, relief="ridge")
                label.grid(row=0, column=col_index, sticky="nsew")

            # Verileri ekleme
            for col_index, col_data in enumerate(murt):
                label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
                label.grid(row=1, column=col_index, sticky="nsew")
        else:
            messagebox.showerror("Hata", "Belirtilen Id sahip murettebat bulunamadı.")

        ozellikler = ["ad", "soyad", "adres", "vatandaslik", "dogum_tarihi", "ise_giris_tarihi", "gorev"]

        # Combobox oluştur
        degisiklik_combobox = Combobox(murettebat_p, values=ozellikler)
        degisiklik_combobox.grid(row=9, column=2, sticky="n")

        m_degis = Entry(murettebat_p, width=20)
        m_degis.grid(row=10, column=2, padx=15, pady=20, sticky="n")

        murt_db = Button(murettebat_p, text="Murettebat Değiştir", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Murettebat.mur_degistir(seri_numarasi, degisiklik_combobox.get(), m_degis.get()))
        murt_db.grid(row=11, column=2, padx=10, pady=20)


penc = Tk()

penc.title("Gezgin Gemi Şirketi")
penc.iconbitmap("gemilogo2.ico")
penc.configure(bg="#06141A")
penc.geometry("1530x750+0+0")


def gemiler_tablosu_olusturma():
    global table_frame2
    global table_frame
    global table_frame3
    global table_frame4

    # Tablo oluşturma
    table_frame = LabelFrame(penc, text="Gemiler Tablosu")
    table_frame.grid(row=1, column=0, sticky="nw", padx=10, pady=(10,100))

    # Başlıklar
    columns = ["Seri Numarası", "Adı", "Ağırlık", "Yapım Yılı", "Tip"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columns):
        label = Label(table_frame, text=col_name, padx=5, pady=5, relief="ridge")
        label.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM gemiler")
    rows = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rows, start=1):
        for col_index, col_data in enumerate(row_data):
            label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
            label.grid(row=row_index, column=col_index, sticky="nsew")

    # Tablo oluşturma
    table_frame2 = LabelFrame(penc, text="Yolcu Gemileri Tablosu")
    table_frame2.grid(row=1, column=0, sticky="nw", padx=10, pady=(200,200))

    # Başlıklar
    columns2 = ["Seri Numarası", "Yolcu Kapasitesi"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columns2):
        label2 = Label(table_frame2, text=col_name, padx=5, pady=5, relief="ridge")
        label2.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM yolcu_gemileri")
    rows2 = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rows2, start=1):
        for col_index, col_data in enumerate(row_data):
            label2 = Label(table_frame2, text=col_data, padx=10, pady=5, relief="ridge")
            label2.grid(row=row_index, column=col_index, sticky="nsew")

    # Petrol Gemisi Tablo oluşturma
    table_frame3 = LabelFrame(penc, text="Petrol Tankerleri Gemileri Tablosu")
    table_frame3.grid(row=1, column=0, sticky="nw", padx=10, pady=(350, 100))

    # Başlıklar
    columns3 = ["Seri Numarası", "Petrol Kapasitesi", "Petrol Birimi"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columns3):
        label3 = Label(table_frame3, text=col_name, padx=5, pady=5, relief="ridge")
        label3.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM petrol_tankerleri")
    rows3 = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rows3, start=1):
        for col_index, col_data in enumerate(row_data):
            label3 = Label(table_frame3, text=col_data, padx=10, pady=5, relief="ridge")
            label3.grid(row=row_index, column=col_index, sticky="nsew")

    # Konteyner Gemisi Tablo oluşturma
    table_frame4 = LabelFrame(penc, text="Konteyner Gemileri Tablosu")
    table_frame4.grid(row=1, column=0, sticky="nw", padx=10, pady=(480, 10))

    # Başlıklar
    columns4 = ["Seri Numarası", "Konteyner Sayısı Kapasitesi", "Max. Ağırlık"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columns4):
        label4 = Label(table_frame4, text=col_name, padx=5, pady=5, relief="ridge")
        label4.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM konteyner_gemileri")
    rows4 = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rows4, start=1):
        for col_index, col_data in enumerate(row_data):
            label4 = Label(table_frame4, text=col_data, padx=10, pady=5, relief="ridge")
            label4.grid(row=row_index, column=col_index, sticky="nsew")

def gemi_tablolar():
    table_frame2.destroy()
    table_frame.destroy()
    table_frame3.destroy()
    table_frame4.destroy()
    table_frame_s.destroy()
    table_frame_k.destroy()
    table_frame_l.destroy()
    table_frame_m.destroy()

    gemiler_tablosu_olusturma()
    diger_tablolar_olusturma()

def diger_tablolar_olusturma():
    global table_frame_k
    global table_frame_s
    global table_frame_l
    global table_frame_m

    # Tablo oluşturma
    table_frame_k = LabelFrame(penc, text="Kaptanlar Tablosu")
    table_frame_k.grid(row=1, column=2, sticky="nw", padx=5, pady=(10,100))

    # Başlıklar
    columnsk = ["Seri Numarası", "Adı", "Soyad", "Adres", "Vatandaşlık", "Doğum T.", "İşe Giriş T.", "Lisans No", "Lisans Tarihi"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columnsk):
        labelk = Label(table_frame_k, text=col_name, padx=5, pady=5, relief="ridge")
        labelk.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM kaptanlar")
    rowsk = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rowsk, start=1):
        for col_index, col_data in enumerate(row_data):
            labelk = Label(table_frame_k, text=col_data, padx=10, pady=5, relief="ridge")
            labelk.grid(row=row_index, column=col_index, sticky="nsew")

    # Tablo oluşturma
    table_frame_s = LabelFrame(penc, text="Seferler Tablosu")
    table_frame_s.grid(row=1, column=2, sticky="nw", padx=10, pady=(150,200))

    # Başlıklar
    columns_s = ["Seri No", "Gemi Id", "Çıkış T.", "Dönüş T.", "Kalkış Limanı"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columns_s):
        labels = Label(table_frame_s, text=col_name, padx=5, pady=5, relief="ridge")
        labels.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM seferler")
    rows_s = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rows_s, start=1):
        for col_index, col_data in enumerate(row_data):
            labels = Label(table_frame_s, text=col_data, padx=10, pady=5, relief="ridge")
            labels.grid(row=row_index, column=col_index, sticky="nsew")

    # Limanlar Tablo oluşturma
    table_frame_l = LabelFrame(penc, text="Limanlar Tablosu")
    table_frame_l.grid(row=1, column=2, sticky="nw", padx=10, pady=(300, 100))

    # Başlıklar
    columnsl = ["Liman Adı", "Ülke", "Nüfus", "Pasaport Gereksinimi", "Demirleme Ücret"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columnsl):
        label_l = Label(table_frame_l, text=col_name, padx=5, pady=5, relief="ridge")
        label_l.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM limanlar")
    rowsl = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rowsl, start=1):
        for col_index, col_data in enumerate(row_data):
            label_l = Label(table_frame_l, text=col_data, padx=10, pady=5, relief="ridge")
            label_l.grid(row=row_index, column=col_index, sticky="nsew")

    # Murettebat Tablo oluşturma
    table_frame_m = LabelFrame(penc, text="Murettebat Tablosu")
    table_frame_m.grid(row=1, column=2, sticky="nw", padx=10, pady=(430, 100))

    # Başlıklar
    columnsm = ["Personal Id", "Ad", "Soyad", "Adres", "Vatandaşlık", "Doğum T.", "İşe Giriş T.", "Görev"]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(columnsm):
        label_m = Label(table_frame_m, text=col_name, padx=5, pady=5, relief="ridge")
        label_m.grid(row=0, column=col_index, sticky="nsew")

    # Verileri veritabanından çekme
    cursor.execute("SELECT * FROM murettebat")
    rowsm = cursor.fetchall()

    # Verileri ekleme
    for row_index, row_data in enumerate(rowsm, start=1):
        for col_index, col_data in enumerate(row_data):
            label_m = Label(table_frame_m, text=col_data, padx=10, pady=5, relief="ridge")
            label_m.grid(row=row_index, column=col_index, sticky="nsew")

def gemi_ozellikleri_goster(seri_numarasi):

    # Seri numarasına göre gemi özelliklerini sorgula
    cursor.execute("SELECT * FROM gemiler WHERE seri_no = ?", (seri_numarasi,))
    gemi = cursor.fetchone()

    cursor.execute("SELECT gemi_turu FROM gemiler WHERE seri_no = ?", (seri_numarasi,))
    gemi_tur = cursor.fetchone()
    print(gemi_tur)

    cursor.execute("SELECT * FROM {} WHERE seri_no = ?".format(gemi_tur[0]), (seri_numarasi,))
    gemi2 = cursor.fetchone()

    if gemi:
        # Tek satırlık tabloyu oluştur
        table_frame = LabelFrame(gemiler_p, text="Gemi Özellikleri")
        table_frame.grid(row=7, column=2, sticky="n", padx=0, pady=(0,10))

        # Başlıklar
        columns = ["Seri No", "Ad", "Ağırlık", "Yapım Yılı", "Gemi Türü"]

        # Başlıkları ekleme
        for col_index, col_name in enumerate(columns):
            label = Label(table_frame, text=col_name, padx=10, pady=5, relief="ridge")
            label.grid(row=0, column=col_index, sticky="nsew")

        # Verileri ekleme
        for col_index, col_data in enumerate(gemi):
            label = Label(table_frame, text=col_data, padx=10, pady=5, relief="ridge")
            label.grid(row=1, column=col_index, sticky="nsew")
    else:
        messagebox.showerror("Hata", "Belirtilen Id sahip gemi bulunamadı.")

    # Tek satırlık tabloyu oluştur
    table_frame2 = LabelFrame(gemiler_p, text="Gemi Özellikleri2")
    table_frame2.grid(row=8, column=2, sticky="n", padx=0, pady=(10,10))

    # Başlıklar
    cursor.execute("PRAGMA table_info({})".format(gemi_tur[0]))
    columns2 = cursor.fetchall()
    sutunlar = [col[1] for col in columns2]

    # Başlıkları ekleme
    for col_index, col_name in enumerate(sutunlar):
        label2 = Label(table_frame2, text=col_name, padx=10, pady=5, relief="ridge")
        label2.grid(row=0, column=col_index, sticky="nsew")

    # Verileri ekleme
    for col_index, col_data in enumerate(gemi2):
        label2 = Label(table_frame2, text=col_data, padx=10, pady=5, relief="ridge")
        label2.grid(row=1, column=col_index, sticky="nsew")

    ozellikler = ["seri_no", "ad", "agirlik", "yapim_yili", "gemi_turu"]
    ozellikler2=["seri_no", "ad", "agirlik", "yapim_yili", "gemi_turu"]
    for s in sutunlar:
        ozellikler.append(s)

    # Combobox oluştur
    degisiklik_combobox2 = Combobox(gemiler_p, values=ozellikler)
    degisiklik_combobox2.grid(row=10, column=2, sticky="n")

    g_degis2 = Entry(gemiler_p, width=20)
    g_degis2.grid(row=11, column=2, padx=15, pady=20, sticky="n")

    tablo = ""

    def combobox_secildi(event):
        global degisiklik
        degisiklik = degisiklik_combobox2.get()
        print("Seçilen değer:", degisiklik)

    degisiklik_combobox2.bind("<<ComboboxSelected>>", combobox_secildi)


    gemi_db = Button(gemiler_p, text="Gemi Değiştir", font=("Times New Roman", 12), bg="#A5C0D0",
                         padx=20, pady=5, command=lambda: Gemi.gemi_degistir(seri_numarasi, degisiklik_combobox2.get(),
                                                                             g_degis2.get(), ozellikler2, sutunlar, gemi_tur[0]))
    gemi_db.grid(row=12, column=2, padx=10, pady=20)


penc.columnconfigure(0, weight=100)
penc.columnconfigure(1, weight=300)
penc.columnconfigure(2, weight=100)

penc.rowconfigure(0, weight=30)
penc.rowconfigure(1, weight=700)

baslik = Label(penc, text="Gezgin Gemi \n Company", bg="#06141A", fg="#E5ECFF", font=("Times New Roman", 40))
baslik.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

yenileme_tusu = Button(penc, text="Yenile", font=("Times New Roman", 10), bg="#5f92b0", padx=20, pady=5,
                             command=lambda: gemi_tablolar())
yenileme_tusu.grid(row=0, column=0, padx=2, pady=5, sticky="nw")

label_frame = Frame(penc, bg="#0D1B1E")
label_frame.grid(row=1, column=1)

# Butonların eşit boyutlarda karelerden oluşması için uniform boyut kullanıyoruz
uniform_buton_boyut = 5

buton0 = Button(label_frame, text="Gemiler", font=("Times New Roman", 20), bg="#A5C0D0", padx=60, pady=10,
                width=uniform_buton_boyut, height=uniform_buton_boyut, command=lambda: Gemi_Pencereleri.gemiler_pencere())
buton0.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

buton1 = Button(label_frame, text="Kaptanlar", font=("Times New Roman", 20), bg="#A5C0D0", padx=60, pady=10,
                width=uniform_buton_boyut, height=uniform_buton_boyut, command=lambda: Kaptanlar.kaptanlar_pencere())
buton1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

buton2 = Button(label_frame, text="Seferler", font=("Times New Roman", 20), bg="#A5C0D0", padx=60, pady=10,
                width=uniform_buton_boyut, height=uniform_buton_boyut, command=lambda: Seferler.seferler_pencere())
buton2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

buton3 = Button(label_frame, text="Limanlar", font=("Times New Roman", 20), bg="#A5C0D0", padx=20, pady=10,
                width=uniform_buton_boyut, height=uniform_buton_boyut, command=lambda: Limanlar.limanlar_pencere())
buton3.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

buton4 = Button(label_frame, text="Mürettebat", font=("Times New Roman", 20), bg="#A5C0D0", padx=20, pady=10,
                width=uniform_buton_boyut, height=uniform_buton_boyut, command=lambda: Murettebatlar.murettebat_pencere())
buton4.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

buton5 = Button(label_frame, text="Exit", font=("Times New Roman", 20), bg="#5f92b0", fg="white",
                padx=20, pady=10, width=uniform_buton_boyut, height=uniform_buton_boyut, command=penc.destroy)
buton5.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

gemiler_tablosu_olusturma()
diger_tablolar_olusturma()
penc.mainloop()
