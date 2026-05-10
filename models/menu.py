class MenuElemani:
    def __init__(self, ad, fiyat):
        self.__ad = ad    #Private değişken kullanıyorum
        self.__fiyat = fiyat  #Private değişken kullanıyorum

    def detaylari_getir(self):
        return f"{self.__ad}: {self.__fiyat} TL"

    @property
    def fiyat(self):
        return self.__fiyat

class MenuElemani:
    def __init__(self, ad, fiyat):
        self.__ad = ad        # Private 
        self.__fiyat = fiyat  # Private 

    @property
    def ad(self):             # Dışarıdan .ad diyerek okumamızı sağlıyor, ama değiştiremiyoruz
        return self.__ad

    @property
    def fiyat(self):
        return self.__fiyat

    def detaylari_getir(self):
        return f"{self.__ad}: {self.__fiyat} TL"