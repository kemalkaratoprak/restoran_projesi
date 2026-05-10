from models.icerik import Yemek, Icecek
from services.siparis_sistemi import Siparis

def ana_dongu():
    
    kebap = Yemek("Adana Kebap", 250, 450)
    ayran = Icecek("Yayık Ayranı", 40, True)
    
    
    yeni_siparis = Siparis()
    
    print("--- Restoran Sistemine Hoş Geldiniz ---")
    
    
    yeni_siparis.urun_ekle(kebap, 2)
    yeni_siparis.urun_ekle(ayran, -1) # Bu hata vermeli ama sistemi çökertmemeli
    yeni_siparis.urun_ekle(ayran, 3)
    
   
    yeni_siparis.fis_yazdir()

if __name__ == "__main__":
    ana_dongu()