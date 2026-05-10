from .menu import MenuItem

class Food(MenuItem):
    def __init__(self, name, price, calories):
        super().__init__(name, price)
        self.calories = calories

    def get_details(self):
        # burada ana sınıfın metodunu özelleşiriyorum
        base_details = super().get_details()
        return f"{base_details} - {self.calories} kcal"

class Drink(MenuItem):
    def __init__(self, name, price, is_cold=True):
        super().__init__(name, price)
        self.is_cold = is_cold

    def get_details(self):
        
        temp = "Soğuk" if self.is_cold else "Sıcak"
        base_details = super().get_details()
        return f"{base_details} ({temp})"