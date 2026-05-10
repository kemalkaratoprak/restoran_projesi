import customtkinter as ctk
import json
import os
from models.icerik import Yemek, Icecek
from services.siparis_sistemi import Siparis

class ModernRestoranApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Restoran Projesi v3.0")
        self.geometry("1000x600")
        
        # VERİ YÜKLEME (Kalıcılık)
        self.dosya_yolu = "menu_verisi.json"
        self.menu_listesi = self.veriyi_yukle()
        
        # MASA MANTIĞI
        self.masalar = {f"Masa {i}": Siparis() for i in range(1, 6)}
        self.aktif_masa = "Masa 1"

        # ARAYÜZ TASARIMI
        self.grid_columnconfigure(1, weight=1)
        
        # SOL PANEL: Masa ve Ürün Seçimi
        self.sol_panel = ctk.CTkFrame(self, width=250)
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sol_panel, text="Masalar", font=("Arial", 16, "bold")).pack(pady=5)
        self.masa_secimi = ctk.CTkOptionMenu(self.sol_panel, values=list(self.masalar.keys()), command=self.masa_degistir)
        self.masa_secimi.pack(pady=10)

        ctk.CTkLabel(self.sol_panel, text="Menü", font=("Arial", 16, "bold")).pack(pady=5)
        self.urun_secimi = ctk.CTkOptionMenu(self.sol_panel, values=[u.ad for u in self.menu_listesi])
        self.urun_secimi.pack(pady=10)
        
        ctk.CTkButton(self.sol_panel, text="Siparişe Ekle", command=self.siparis_ekle_aksiyon).pack(pady=10)

        # SAĞ PANEL: Fiş ve Menü Düzenleme
        self.sag_panel = ctk.CTkFrame(self)
        self.sag_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.fis_ekrani = ctk.CTkTextbox(self.sag_panel, width=400, height=300)
        self.fis_ekrani.pack(pady=10, padx=10, fill="x")
        
        # Menü Düzenleme Alanı
        self.duzenle_frame = ctk.CTkFrame(self.sag_panel)
        self.duzenle_frame.pack(pady=10, fill="x", padx=10)
        self.yeni_ad = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Yeni Ürün Adı")
        self.yeni_ad.pack(side="left", padx=5)
        self.yeni_fiyat = ctk.CTkEntry(self.duzenle_frame, placeholder_text="Fiyat")
        self.yeni_fiyat.pack(side="left", padx=5)
        ctk.CTkButton(self.duzenle_frame, text="Menüye Kaydet", command=self.menuye_yeni_ekle).pack(side="left", padx=5)

    def veriyi_yukle(self):
        # Program açıldığında dosyadan oku
        if os.path.exists(self.dosya_yolu):
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                veriler = json.load(f)
                return [Yemek(v["ad"], v["fiyat"], 0) for v in veriler]
        return [Yemek("Varsayılan Kebap", 200, 0)] # Dosya yoksa varsayılan

    def veriyi_kaydet(self):
        # Her değişiklikte dosyaya yaz (Kalıcılık)
        veriler = [{"ad": u.ad, "fiyat": u.fiyat} for u in self.menu_listesi]
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veriler, f, ensure_ascii=False, indent=4)

    def menuye_yeni_ekle(self):
        ad = self.yeni_ad.get()
        fiyat = float(self.yeni_fiyat.get())
        self.menu_listesi.append(Yemek(ad, fiyat, 0))
        self.veriyi_kaydet()
        self.urun_secimi.configure(values=[u.ad for u in self.menu_listesi])

    def masa_degistir(self, secilen_masa):
        self.aktif_masa = secilen_masa
        self.fis_guncelle()

    def siparis_ekle_aksiyon(self):
        secilen_ad = self.urun_secimi.get()
        urun = next(u for u in self.menu_listesi if u.ad == secilen_ad)
        self.masalar[self.aktif_masa].urun_ekle(urun, 1)
        self.fis_guncelle()

    def fis_guncelle(self):
        self.fis_ekrani.delete("1.0", "end")
        self.fis_ekrani.insert("end", f"--- {self.aktif_masa} SİPARİŞ DETAYI ---\n")
        siparis = self.masalar[self.aktif_masa]
        # Sipariş detaylarını buraya yazdırıyoruz...
        self.fis_ekrani.insert("end", f"\nToplam: {siparis.toplam_tutar_hesapla()} TL")

if __name__ == "__main__":
    app = ModernRestoranApp()
    app.mainloop()