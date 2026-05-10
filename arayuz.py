import customtkinter as ctk
import json
import os
from tkinter import messagebox
from models.icerik import Yemek, Icecek
from services.siparis_sistemi import Siparis

# Görünüm Ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernRestoranApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Restoran Yönetim Sistemi v3.0")
        self.geometry("1100x700")
        
        # VERİ YÜKLEME (Kalıcılık)
        self.dosya_yolu = "menu_verisi.json"
        self.menu_listesi = self.veriyi_yukle()
        
        # MASA MANTIĞI
        self.masalar = {f"Masa {i}": Siparis() for i in range(1, 11)}
        self.aktif_masa = "Masa 1"

        # GRID DÜZENİ
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- SOL PANEL: SİPARİŞ VE MASA YÖNETİMİ ---
        self.sol_panel = ctk.CTkFrame(self, width=300)
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sol_panel, text="MASA SEÇİMİ", font=("Arial", 16, "bold")).pack(pady=(20,5))
        self.masa_secimi = ctk.CTkOptionMenu(self.sol_panel, values=list(self.masalar.keys()), command=self.masa_degistir)
        self.masa_secimi.pack(pady=10)

        ctk.CTkLabel(self.sol_panel, text="MENÜDEN EKLE", font=("Arial", 16, "bold")).pack(pady=(20,5))
        self.urun_secimi = ctk.CTkOptionMenu(self.sol_panel, values=[u.ad for u in self.menu_listesi])
        self.urun_secimi.pack(pady=10)
        
        ctk.CTkButton(self.sol_panel, text="Siparişe Ekle (+1)", fg_color="green", hover_color="#006400",
                      command=self.siparis_ekle_aksiyon).pack(pady=20)

        # --- SAĞ PANEL: FİŞ VE YÖNETİM ---
        self.sag_panel = ctk.CTkFrame(self)
        self.sag_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Fiş Ekranı
        self.fis_ekrani = ctk.CTkTextbox(self.sag_panel, font=("Consolas", 13), width=500)
        self.fis_ekrani.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Menü Düzenleme Çerçevesi
        self.yonetim_frame = ctk.CTkLabel(self.sag_panel, text="MENÜ YÖNETİMİ", font=("Arial", 14, "bold"))
        self.yonetim_frame.pack(pady=(10,0))
        
        self.duzenle_frame = ctk.CTkFrame(self.sag_panel)
        self.duzenle_frame.pack(pady=10, fill="x", padx=10)
        
        self.yeni_ad = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Ürün Adı", width=150)
        self.yeni_ad.pack(side="left", padx=5, pady=10)
        
        self.yeni_fiyat = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Fiyat", width=100)
        self.yeni_fiyat.pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(self.duzenle_frame, text="Kaydet / Güncelle", command=self.menuye_yeni_ekle).pack(side="left", padx=5)
        ctk.CTkButton(self.duzenle_frame, text="Seçiliyi Menüden Sil", fg_color="red", hover_color="#8B0000",
                      command=self.menuden_sil).pack(side="left", padx=5)

        self.fis_guncelle()

    # --- VERİ YÖNETİMİ METOTLARI ---
    def veriyi_yukle(self):
        if os.path.exists(self.dosya_yolu):
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    veriler = json.load(f)
                    # Basitlik adına tüm verileri Yemek olarak yüklüyoruz, 
                    # istersen "tip" alanı ekleyip Icecek/Yemek ayırabilirsin.
                    return [Yemek(v["ad"], v["fiyat"], v.get("kalori", 0)) for v in veriler]
            except:
                return [Yemek("Adana Kebap", 250, 450), Icecek("Ayran", 40, True)]
        return [Yemek("Adana Kebap", 250, 450), Icecek("Ayran", 40, True)]

    def veriyi_kaydet(self):
        veriler = [{"ad": u.ad, "fiyat": u.fiyat} for u in self.menu_listesi]
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veriler, f, ensure_ascii=False, indent=4)

    # --- MENÜ İŞLEMLERİ ---
    def menuye_yeni_ekle(self):
        ad = self.yeni_ad.get()
        fiyat_str = self.yeni_fiyat.get()
        
        if not ad or not fiyat_str:
            messagebox.showwarning("Hata", "Lütfen ad ve fiyat girin!")
            return

        try:
            fiyat = float(fiyat_str)
            # Eğer ürün zaten varsa fiyatını güncelle
            mevcut = next((u for u in self.menu_listesi if u.ad.lower() == ad.lower()), None)
            
            if mevcut:
                # Kapsülleme nedeniyle fiyatı menu.py'deki mantığa göre güncelliyoruz
                # (Eğer setter yazmadıysan burada yeni nesne oluşturmak en temizidir)
                self.menu_listesi.remove(mevcut)
                
            self.menu_listesi.append(Yemek(ad, fiyat, 0))
            self.veriyi_kaydet()
            self.menu_arayuz_guncelle()
            messagebox.showinfo("Başarılı", f"{ad} menüye işlendi.")
        except ValueError:
            messagebox.showerror("Hata", "Fiyat sayısal bir değer olmalıdır!")

    def menuden_sil(self):
        secilen_ad = self.urun_secimi.get()
        self.menu_listesi = [u for u in self.menu_listesi if u.ad != secilen_ad]
        self.veriyi_kaydet()
        self.menu_arayuz_guncelle()
        messagebox.showinfo("Bilgi", f"{secilen_ad} menüden silindi.")

    def menu_arayuz_guncelle(self):
        yeni_liste = [u.ad for u in self.menu_listesi]
        self.urun_secimi.configure(values=yeni_liste)
        if yeni_liste:
            self.urun_secimi.set(yeni_liste[0])

    # --- SİPARİŞ İŞLEMLERİ ---
    def masa_degistir(self, secilen_masa):
        self.aktif_masa = secilen_masa
        self.fis_guncelle()

    def siparis_ekle_aksiyon(self):
        secilen_ad = self.urun_secimi.get()
        urun = next((u for u in self.menu_listesi if u.ad == secilen_ad), None)
        if urun:
            self.masalar[self.aktif_masa].urun_ekle(urun, 1)
            self.fis_guncelle()

    def fis_guncelle(self):
        self.fis_ekrani.delete("1.0", "end")
        self.fis_ekrani.insert("end", f"{'='*40}\n")
        self.fis_ekrani.insert("end", f"          {self.aktif_masa.upper()} FİŞ DETAYI\n")
        self.fis_ekrani.insert("end", f"{'='*40}\n\n")
        
        siparis = self.masalar[self.aktif_masa]
        
        # icerik.py polimorfizmini kullanıyoruz
        # Not: Private listeye erişim için _Siparis__urunler ismini kullanıyoruz (Naming Mangling)
        items = getattr(siparis, f"_{siparis.__class__.__name__}__urunler", [])
        
        if not items:
            self.fis_ekrani.insert("end", "\n         Henüz sipariş yok...\n")
        else:
            for kalem in items:
                urun = kalem["urun"]
                adet = kalem["adet"]
                detay = urun.detaylari_getir() # icerik.py'deki polimorfik detay
                ara_toplam = urun.fiyat * adet
                
                self.fis_ekrani.insert("end", f"> {detay}\n")
                self.fis_ekrani.insert("end", f"  Adet: {adet} | Tutar: {ara_toplam} TL\n")
                self.fis_ekrani.insert("end", f"{'-'*40}\n")
            
        toplam = siparis.toplam_tutar_hesapla()
        self.fis_ekrani.insert("end", f"\n{'='*40}\n")
        self.fis_ekrani.insert("end", f" GENEL TOPLAM: {toplam} TL\n")
        self.fis_ekrani.insert("end", f"{'='*40}")

if __name__ == "__main__":
    app = ModernRestoranApp()
    app.mainloop()