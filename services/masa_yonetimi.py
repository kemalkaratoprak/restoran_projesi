from .siparis_sistemi import Siparis

class RestoranYonetimi:
    def __init__(self, masa_sayisi):
        # Her masa için boş bir sipariş listesi oluşturur
        self.masalar = {f"Masa {i}": Siparis() for i in range(1, masa_sayisi + 1)}

    def masaya_siparis_ekle(self, masa_adi, urun, adet):
        try:
            if masa_adi not in self.masalar:
                raise KeyError(f"{masa_adi} bulunamadı!")
            self.masalar[masa_adi].urun_ekle(urun, adet)
        except Exception as e:
            print(f"Sistem Hatası: {e}")
            