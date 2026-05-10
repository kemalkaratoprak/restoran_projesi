import pytest
from models.icerik import Yemek, Icecek
from services.siparis_sistemi import Siparis

def test_yemek_olusturma():
    # Yemek sınıfı doğru verilerle oluşuyor mu?
    kebap = Yemek("Kebap", 200, 500)
    assert kebap.ad == "Kebap"
    assert kebap.fiyat == 200

def test_siparis_toplam_hesaplama():
    # Sipariş toplam tutarı doğru hesaplıyor mu?
    siparis = Siparis()
    yemek = Yemek("Pizza", 100, 800)
    siparis.urun_ekle(yemek, 2)
    assert siparis.toplam_tutar_hesapla() == 200

def test_hatali_adet_ekleme():
    # Negatif adet eklendiğinde sistem boş kalmalı 
    siparis = Siparis()
    icecek = Icecek("Su", 10)
    siparis.urun_ekle(icecek, -5)
    assert siparis.toplam_tutar_hesapla() == 0

def test_icecek_sicaklik_kontrolu():
    su = Icecek("Su", 10, soguk_mu=True)
    assert "Soğuk" in su.detaylari_getir()

def test_yemek_detay_kontrolu():
    pizza = Yemek("Pizza", 150, 800)
    assert "800 kcal" in pizza.detaylari_getir()

def test_coklu_urun_hesaplama():
    siparis = Siparis()
    siparis.urun_ekle(Yemek("A", 100, 100), 1)
    siparis.urun_ekle(Icecek("B", 50), 2)
    assert siparis.toplam_tutar_hesapla() == 200

def test_kapsulleme_fiyat_degismez():
    # Private değişkene dışarıdan müdahale edilse bile    
    urun = Yemek("Test", 50, 100)
    urun.__fiyat = 100 
    assert urun.fiyat == 50

def test_bos_siparis_tutari():
    siparis = Siparis()
    assert siparis.toplam_tutar_hesapla() == 0

def test_farkli_icecek_tipi():
    cay = Icecek("Çay", 20, soguk_mu=False)
    assert "Sıcak" in cay.detaylari_getir()

def test_urun_ad_dogrulama():
    urun = Yemek("Corba", 40, 200)
    assert urun.ad == "Corba"