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
        self.title("Restoran Yönetim Sistemi v4.0 Final")
        self.geometry("1200x750")
        
        # VERİ YÜKLEME (Kalıcılık)
        self.dosya_yolu = "menu_verisi.json"
        self.menu_listesi = self.veriyi_yukle()
        
        # MASA MANTIĞI (10 Masa)
        self.masalar = {f"Masa {i}": Siparis() for i in range(1, 11)}
        self.aktif_masa = "Masa 1"

        # GRID DÜZENİ
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- SOL PANEL ---
        self.sol_panel = ctk.CTkFrame(self, width=300)
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sol_panel, text="MASA SEÇİMİ", font=("Arial", 16, "bold")).pack(pady=(20,5))
        self.masa_secimi = ctk.CTkOptionMenu(self.sol_panel, values=list(self.masalar.keys()), command=self.masa_degistir)
        self.masa_secimi.pack(pady=10)

        ctk.CTkLabel(self.sol_panel, text="SİPARİŞ EKLE", font=("Arial", 16, "bold")).pack(pady=(20,5))
        self.urun_secimi = ctk.CTkOptionMenu(self.sol_panel, values=[u.ad for u in self.menu_listesi])
        self.urun_secimi.pack(pady=10)
        
        ctk.CTkButton(self.sol_panel, text="Siparişe Ekle (+1)", fg_color="green", hover_color="#006400",
                      command=self.siparis_ekle_aksiyon).pack(pady=20)

        # --- SAĞ PANEL ---
        self.sag_panel = ctk.CTkFrame(self)
        self.sag_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.fis_ekrani = ctk.CTkTextbox(self.sag_panel, font=("Consolas", 13))
        self.fis_ekrani.pack(pady=10, padx=10, fill="both", expand=True)
        
        # --- YÖNETİM PANELİ (ALT) ---
        self.duzenle_frame = ctk.CTkFrame(self.sag_panel)
        self.duzenle_frame.pack(pady=10, fill="x", padx=10)
        
        # Giriş Alanları
        self.yeni_ad = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Ürün Adı", width=140)
        self.yeni_ad.pack(side="left", padx=5, pady=10)
        
        self.yeni_fiyat = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Fiyat", width=80)
        self.yeni_fiyat.pack(side="left", padx=5, pady=10)

        self.tur_secimi = ctk.CTkOptionMenu(self.duzenle_frame, values=["Yemek", "İçecek"], width=100)
        self.tur_secimi.pack(side="left", padx=5)

        self.detay_entry = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Kalori / Soğuk mu?(E/H)", width=150)
        self.detay_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(self.duzenle_frame, text="Kaydet", width=100, command=self.menuye_yeni_ekle).pack(side="left", padx=5)
        ctk.CTkButton(self.duzenle_frame, text="Sil", fg_color="red", width=60, command=self.menuden_sil).pack(side="left", padx=5)

        self.fis_guncelle()

    def veriyi_yukle(self):
        """JSON dosyasından ürünleri nesne olarak yükler."""
        if os.path.exists(self.dosya_yolu):
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    veriler = json.load(f)
                    yuklenenler = []
                    for v in veriler:
                        if v.get("tur") == "İçecek":
                            yuklenenler.append(Icecek(v["ad"], v["fiyat"], v.get("ozellik", True)))
                        else:
                            yuklenenler.append(Yemek(v["ad"], v["fiyat"], v.get("ozellik", 0)))
                    return yuklenenler
            except: pass
        return [Yemek("Adana Kebap", 250, 450), Icecek("Ayran", 40, True)]

    def veriyi_kaydet(self):
        """Mevcut menüyü tür bilgisiyle birlikte JSON'a yazar."""
        veriler = []
        for u in self.menu_listesi:
            tur = "İçecek" if isinstance(u, Icecek) else "Yemek"
            ozellik = u.soguk_mu if isinstance(u, Icecek) else u.kalori
            veriler.append({"ad": u.ad, "fiyat": u.fiyat, "tur": tur, "ozellik": ozellik})
            
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veriler, f, ensure_ascii=False, indent=4)

    def menuye_yeni_ekle(self):
        ad = self.yeni_ad.get()
        fiyat_s = self.yeni_fiyat.get()
        tur = self.tur_secimi.get()
        detay = self.detay_entry.get()

        if not ad or not fiyat_s:
            messagebox.showwarning("Hata", "Ad ve Fiyat zorunludur!")
            return

        try:
            fiyat = float(fiyat_s)
            # Eski kaydı temizle
            self.menu_listesi = [u for u in self.menu_listesi if u.ad.lower() != ad.lower()]
            
            if tur == "Yemek":
                yeni = Yemek(ad, fiyat, int(detay if detay.isdigit() else 0))
            else:
                yeni = Icecek(ad, fiyat, detay.lower() != "h")
                
            self.menu_listesi.append(yeni)
            self.veriyi_kaydet()
            self.menu_arayuz_guncelle()
            messagebox.showinfo("Başarılı", f"{ad} menüye kaydedildi.")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sayısal değerleri doğru girin!")

    def menuden_sil(self):
        secilen = self.urun_secimi.get()
        self.menu_listesi = [u for u in self.menu_listesi if u.ad != secilen]
        self.veriyi_kaydet()
        self.menu_arayuz_guncelle()

    def menu_arayuz_guncelle(self):
        liste = [u.ad for u in self.menu_listesi]
        self.urun_secimi.configure(values=liste)
        if liste: self.urun_secimi.set(liste[0])

    def masa_degistir(self, m):
        self.aktif_masa = m
        self.fis_guncelle()

    def siparis_ekle_aksiyon(self):
        ad = self.urun_secimi.get()
        urun = next((u for u in self.menu_listesi if u.ad == ad), None)
        if urun:
            self.masalar[self.aktif_masa].urun_ekle(urun, 1)
            self.fis_guncelle()

    def fis_guncelle(self):
        self.fis_ekrani.delete("1.0", "end")
        self.fis_ekrani.insert("end", f"{'='*50}\n")
        self.fis_ekrani.insert("end", f"            {self.aktif_masa.upper()} SİPARİŞ FİŞİ\n")
        self.fis_ekrani.insert("end", f"{'='*50}\n\n")
        
        siparis = self.masalar[self.aktif_masa]
        items = getattr(siparis, f"_{siparis.__class__.__name__}__urunler", [])
        
        for k in items:
            u, a = k["urun"], k["adet"]
            # icerik.py'deki detaylari_getir() sayesinde polimorfizm sağlanıyor
            self.fis_ekrani.insert("end", f"> {u.detaylari_getir()} x {a}\n")
            self.fis_ekrani.insert("end", f"  Tutar: {u.fiyat * a} TL\n")
            self.fis_ekrani.insert("end", f"{'-'*45}\n")
            
        self.fis_ekrani.insert("end", f"\nGENEL TOPLAM: {siparis.toplam_tutar_hesapla()} TL\n")
        self.fis_ekrani.insert("end", f"{'='*50}")

if __name__ == "__main__":
    ModernRestoranApp().mainloop()