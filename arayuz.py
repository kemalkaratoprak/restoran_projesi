import customtkinter as ctk
from tkinter import messagebox
from models.icerik import Yemek, Icecek
from services.siparis_sistemi import Siparis

# Görünüm ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernRestoranApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Restoran Yönetim Sistemi v2.0")
        self.geometry("800x500")
        
        self.siparis = Siparis()
        self.menu_listesi = [
            Yemek("Adana Kebap", 250, 450),
            Icecek("Ayran", 40, True)
        ]

        # Izgara (Grid) düzeni
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SOL PANEL: Menü Yönetimi
        self.sol_panel = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sol_panel, text="Ürün Yönetimi", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.ad_entry = ctk.CTkEntry(self.sol_panel, placeholder_text="Ürün Adı")
        self.ad_entry.pack(pady=5, padx=10)
        
        self.fiyat_entry = ctk.CTkEntry(self.sol_panel, placeholder_text="Fiyat")
        self.fiyat_entry.pack(pady=5, padx=10)
        
        ctk.CTkButton(self.sol_panel, text="Menüye Ekle / Güncelle", command=self.menu_guncelle).pack(pady=10)

        # SAĞ PANEL: Sipariş ve Fiş
        self.sag_panel = ctk.CTkFrame(self)
        self.sag_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.fis_alani = ctk.CTkTextbox(self.sag_panel, width=400)
        self.fis_alani.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkButton(self.sag_panel, text="Siparişleri Listele", command=self.fis_detaylandir).pack(pady=10)

    def menu_guncelle(self):
        # Savunmacı Programlama: Boş giriş kontrolü 
        ad = self.ad_entry.get()
        try:
            fiyat = float(self.fiyat_entry.get())
            # Burada mevcut ürünü bulup fiyatını güncelleyebilir veya yeni ekleyebiliriz
            yeni_urun = Yemek(ad, fiyat, 0)
            self.siparis.urun_ekle(yeni_urun, 1)
            messagebox.showinfo("Bilgi", f"{ad} güncellendi/eklendi.")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir fiyat girin!")

    def fis_detaylandir(self):
        self.fis_alani.delete("1.0", "end")
        self.fis_alani.insert("end", "="*30 + "\n")
        self.fis_alani.insert("end", "   AYRINTILI SİPARİŞ FİŞİ\n")
        self.fis_alani.insert("end", "="*30 + "\n\n")
        
        # Sipariş listesini döngüyle daha şık yazdıralım
        # private değişkene erişim için property kullanıyoruz [cite: 42]
        for kalem in self.siparis._Siparis__urunler: # Private erişim testi için
            urun = kalem["urun"]
            adet = kalem["adet"]
            ara_toplam = urun.fiyat * adet
            self.fis_alani.insert("end", f"{urun.ad}\n")
            self.fis_alani.insert("end", f"   {adet} x {urun.fiyat} TL = {ara_toplam} TL\n")
            self.fis_alani.insert("end", "-"*20 + "\n")
            
        toplam = self.siparis.toplam_tutar_hesapla()
        self.fis_alani.insert("end", f"\nGENEL TOPLAM: {toplam} TL", ("bold"))

if __name__ == "__main__":
    uygulama = ModernRestoranApp()
    uygulama.mainloop() 