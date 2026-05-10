class MenuItem:
    def __init__(self, name, price):
        self.__name = name    #Private değişken kullanıyorum
        self.__price = price  #Private değişken kullanıyorum

    def get_details(self):
        return f"{self.__name}: {self.__price} TL"

    @property
    def price(self):
        return self.__price