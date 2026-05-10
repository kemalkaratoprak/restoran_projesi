class MenuElemani:
    def __init__(self, ad, fiyat):
        self.__ad = ad    #Private değişken kullanıyorum
        self.__fiyat = fiyat  #Private değişken kullanıyorum

    def detaylari_getir(self):
        return f"{self.__ad}: {self.__fiyat} TL"

    @property
    def fiyat(self):
        return self.__fiyat