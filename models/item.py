class MenuItem:
    def __init__(self, name, price):
        self.__name = name    # Kapsülleme: Private değişken [cite: 42]
        self.__price = price  # Kapsülleme: Private değişken [cite: 42]

    def get_details(self):
        return f"{self.__name}: {self.__price} TL"

    @property
    def price(self):
        return self.__price