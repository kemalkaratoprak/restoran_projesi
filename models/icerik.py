from .menu import MenuElemani

class Yemek(MenuElemani):
    def __init__(self, ad, fiyat, kalori):
        super().__init__(ad, fiyat)
        self.kalori = kalori

    def detaylari_getir(self):
        temel_detay = super().detaylari_getir()
        return f"{temel_detay} - {self.kalori} kcal"

class Icecek(MenuElemani):
    def __init__(self, ad, fiyat, soguk_mu=True):
        super().__init__(ad, fiyat)
        self.soguk_mu = soguk_mu

    def detaylari_getir(self):
        sicaklik = "Soğuk" if self.soguk_mu else "Sıcak"
        temel_detay = super().detaylari_getir()
        return f"{temel_detay} ({sicaklik})"