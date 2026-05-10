from models.icerik import Yemek, Icecek

class Siparis:
    def __init__(self):
        self.__urunler = [] # Kapsülleme: Dışarıdan doğrudan müdahale edilemez 

    def urun_ekle(self, urun, adet):
        try:
            # Savunmacı Programlama: Hatalı giriş kontrolü [cite: 11, 46]
            if adet <= 0:
                raise ValueError("Ürün adedi 0'dan büyük olmalıdır!")
            
            self.__urunler.append({"urun": urun, "adet": adet})
            print(f"Eklendi: {adet} adet {urun.ad}")
            
        except ValueError as e:
            print(f"Hata oluştu: {e}") # Kullanıcıya anlamlı hata mesajı [cite: 47]

    def toplam_tutar_hesapla(self):
        toplam = 0
        for kalem in self.__urunler:
            toplam += kalem["urun"].fiyat * kalem["adet"]
        return toplam

    def fis_yazdir(self):
        print("\n--- RESTORAN SİPARİŞ FİŞİ ---")
        for kalem in self.__urunler:
            print(f"{kalem['urun'].detaylari_getir()} x {kalem['adet']}")
        print(f"TOPLAM: {self.toplam_tutar_hesapla()} TL")
        print("----------------------------")