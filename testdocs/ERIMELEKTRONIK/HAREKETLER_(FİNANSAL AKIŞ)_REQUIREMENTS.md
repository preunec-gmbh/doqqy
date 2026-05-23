HAREKETLER (FİNANSAL AKIŞ) GEREKSİNİMLERİ (MVP)
Versiyon: 1.2 | Tarih: 2026-03-07 | Durum: Onaylandı
1. GENEL BAKIŞ
Bu doküman, B2B ERP Entegre E-Ticaret Portalı'nın MVP versiyonu için Hareketler modülünü tanımlar. Sistem, mevcut ERP veritabanındaki finans tablolarını okuma amaçlı kullanır, hiçbir yazma işlemi yapılmaz.
Önemli Kural: MVP aşamasında ERP veritabanına (SQL Server) hiçbir yazma işlemi yapılmayacaktır. Tüm hareket verileri salt okunur şekilde ERP'den anlık çekilir.
2. KARAR VERİLEN YAKLAŞIMLAR (MVP)
Konu
	
Karar
Hareket Verisi Kaynağı
	
ERP'deki FINANS ve FINANS_DETAY tablolarından okunur
Bakiye Gösterimi
	
CARI_BAKIYELER tablosundan anlık çekilir
İşlem Tipi
	
FINANS_ISLEM_TURU tablosundan Türkçe ad mapping yapılır
Fatura Bağlantısı
	
FIS tablosundan BELGENO gösterilir
Detay Sayfası
	
Ayrı sayfa (/hareketler/:id), modal değil
ERP Yazma Politikası
	
Sıfır yazma işlemi (salt okunur erişim)
3. KULLANICI ROLLERİ VE YETKİLER
3.1. Admin (Yönetici)

    Yetkiler: Tüm carilerin hareket işlemlerini görüntüleyebilir
    Filtreleme: Cari bazlı filtreleme yapabilir
    Kısıtlamalar: Hareket oluşturamaz, düzenleyemez, silemez

3.2. Müşteri (Cari)

    Yetkiler: Sadece kendi hareket işlemlerini görüntüleyebilir
    Filtreleme: Kendi işlemleri arasında tarih filtrelemesi yapabilir
    Kısıtlamalar: Başka carilerin hareketlerini göremez

4. HAREKETLER LİSTELEME SAYFASI
4.1. Görüntülenecek Sütunlar
Sütun
	
Açıklama
	
Kaynak
Belge No
	
Hareket belge numarası
	
FINANS.BELGENO
İşlem Tarihi
	
Finansal işlem tarihi
	
FINANS.ISLEM_TARIHI
İşlem Tipi
	
Hareket türü (Türkçe)
	
FINANS_ISLEM_TURU.AD
Tutar
	
İşlem tutarı (TRY)
	
FINANS_DETAY.TUTAR
Yön
	
Borç/Alacak badge
	
KART_BORCLU/KART_ALACAKLI
Fatura No
	
İlgili fatura numarası
	
FIS.BELGENO
Detay
	
Detay sayfasına link
	
Buton
4.2. Üst Özet Kartı (Bakiye)
Hareket listesi sayfasının en üstünde cari bakiyesi gösterilir.
Bakiye Renk Kodları:

    🔴 Kırmızı: Pozitif bakiye (Cari bize borçlu)
    🟢 Yeşil: Negatif bakiye (Biz cariye borçluyuz)
    ⚪ Gri: Sıfır bakiye (Hesap dengede)

4.3. Arama ve Filtreleme
Müşteri İçin:

    Tarih Aralığı: Başlangıç - Bitiş tarihi seçimi
    İşlem Tipi: Dropdown ile filtre
    Varsayılan: Son 30 gün

Admin İçin:

    Tüm müşteri filtreleri +
    Cari Seçimi: Dropdown ile cari seçimi

5. HAREKET DETAY SAYFASI
5.1. Sayfa Yapısı
URL: /dashboard/hareketler/:id (Müşteri) | /admin/hareketler/:id (Admin)
Önemli: Detay bilgileri modal değil, ayrı sayfada gösterilir.
5.2. Görüntülenecek Bilgiler
Başlık Bilgileri:

    Belge No
    İşlem Tarihi
    İşlem Tipi
    Cari Ünvanı

Tutar Bilgileri:

    Ana Tutar
    KDV Tutarı
    Toplam Tutar
    Döviz Bilgisi (varsa)

Hareket Yönü:

    Borçlu Kart (KART_ADLARI.AD)
    Alacaklı Kart (KART_ADLARI.AD)

Ek Bilgiler:

    Vade Tarihi
    İlgili Fatura No
    Açıklama
    Personel (varsa)

5.3. Geri Dönüş

    Sol üstte "← Hareketlere Dön" butonu
    Önceki sayfaya yönlendirir

6. API ENDPOINT TANIMLARI
6.1. GET /api/hareketler (Hareket Listesi)
Yetki: Login olmuş kullanıcı (Admin veya Customer)
Query Parametreleri:
Parametre
	
Tip
	
Varsayılan
	
Açıklama
baslangic
	
date
	
30 gün önce
	
Başlangıç tarihi
bitis
	
date
	
Bugün
	
Bitiş tarihi
cariId
	
number
	
null
	
Sadece Admin: Cari ID filtresi
islemTipi
	
number
	
null
	
İşlem tipi filtresi
page
	
number
	
1
	
Sayfa numarası
limit
	
number
	
25
	
Sayfa başına kayıt
Response Format:

json
1
2
3
4
5
6
7

6.2. GET /api/hareketler/:id (Hareket Detay)
Yetki: Login olmuş kullanıcı
Parametre: Hareket ID'si
Response Format:

json
1
2
3
4
5
6
7
8
9
10

7. GÜVENLİK VE ERİŞİM KURALLARI
7.1. Role-Based Access Control
Middleware Kontrolü:

    /dashboard/hareketler → CUSTOMER role kontrolü
    /admin/hareketler → ADMIN role kontrolü

API Seviyesinde Kontrol:

    Müşteri cariId parametresi gönderse bile kendi cariKod'u kullanılır
    Admin cariId parametresi ile istediği cari'yi filtreleyebilir

7.2. SQL Injection Koruması

    Tüm sorgular parametreli olmalı
    Raw SQL kullanımı minimize edilmeli

7.3. Hata Yönetimi
Hata Durumu
	
Kullanıcı Mesajı
	
Sistem Logu
ERP bağlantı hatası
	
"Hareket bilgileri alınamadı"
	
erp_connection_failed
Yetkisiz erişim
	
"Bu işlem için yetkiniz yok"
	
unauthorized_access
Geçersiz tarih aralığı
	
"Geçersiz tarih aralığı"
	
invalid_date_range
8. TEST SENARYOLARI (KABUL KRİTERLERİ)
ID
	
Senaryo
	
Beklenen Sonuç
TC-01
	
Müşteri kendi hareketlerini görür
	
Sadece kendi işlemleri listelenir
TC-02
	
Admin tüm hareketleri görür
	
Tüm carilerin işlemleri listelenir
TC-03
	
Admin cari bazlı filtreleme
	
Sadece seçili cari işlemleri gösterilir
TC-04
	
Tarih aralığı filtreleme
	
Sadece seçili tarih aralığı gösterilir
TC-05
	
İşlem tipi filtreleme
	
Sadece seçili işlem tipi gösterilir
TC-06
	
Güncel bakiye gösterimi
	
Üst kartta anlık bakiye gösterilir
TC-07
	
Bakiye renk kodlaması
	
Pozitif=Kırmızı, Negatif=Yeşil
TC-08
	
Müşteri başka cari erişimi
	
Filtre override edilir, kendi verisi gösterilir
TC-09
	
ERP bağlantı hatası
	
500 hata + kullanıcı mesajı
TC-10
	
Sayfalama
	
26-50. kayıtlar listelenir
TC-11
	
Login olmayan erişim
	
/login sayfasına yönlendirilir
TC-12
	
Detay sayfası açılışı
	
Ayrı sayfada detaylar gösterilir
TC-13
	
Detay sayfası geri dönüş
	
"Hareketlere Dön" butonu çalışır
9. BİLİNEN RİSKLER VE MVP SINIRLARI
9.1. Kabul Edilen Riskler
Risk
	
Açıklama
	
MVP Çözümü
	
Phase 2
AD ile Bakiye Eşleştirme
	
CARI_BAKIYELER'de FK yok
	
MVP'de kabul edildi
	
ERP'den doğru FK istenecek
Anlık Sorgu Performansı
	
Her sayfada ERP sorgusu
	
Cache yok, anlık
	
TanStack Query cache
Çoklu Döviz
	
Farklı DOVIZ_AD'ler
	
Sadece TRY toplanır
	
Döviz çevrimi
FIS Bağlantısı
	
FIS.BELGENO gösteriliyor
	
Sadece numara
	
Fatura detay sayfası
9.2. MVP Dışı Bırakılanlar

    Hareket oluşturma/düzenleme (ERP sorumluluğunda)
    Ödeme yöntemi detaylı gösterimi
    Döviz bazlı bakiye gösterimi
    Excel/PDF export özelliği
    Gelişmiş filtreler (tutar aralığı, vade tarihi)
    Hareket eşleştirme (hangi fatura ödendi)
    Çek/Senet detaylı yönetimi

10. VERİTABANI TABLO REFERANSLARI
10.1. ERP Tarafı (Read-Only)
Tablo
	
Amaç
	
Kritik Alanlar
	
JOIN Şartı
FINANS
	
Hareket başlık
	
ID, BELGENO, TARIH
	
FINANS_DETAY.FINANS = FINANS.ID
FINANS_DETAY
	
Hareket satır
	
ID, TUTAR, KART_BORCLU
	
KART_BORCLU = CARI.ID
FINANS_ISLEM_TURU
	
İşlem tipi
	
ID, AD
	
FINANS_DETAY.FINANS_ISLEM_TURU = ID
FIS
	
Fatura bilgisi
	
ID, BELGENO
	
FINANS.FIS = FIS.ID
CARI_BAKIYELER
	
Güncel bakiye
	
AD, BAKIYE
	
AD = CARI.AD
KART_ADLARI
	
Kart isimleri
	
ID, AD
	
KART_BORCLU = KART_ADLARI.ID
10.2. PostgreSQL Tarafı
Hareket modülünde PostgreSQL kullanılmaz. Tüm veriler ERP'den anlık okunur.
11. NOTLAR VE AÇIKLAMALAR
11.1. Bakiye Hesaplama Mantığı

1
2
3

MVP: Sadece DOVIZ_AD = 'TRY' kayıtları toplanır.
11.2. Hareket Yönü Hesaplama

1
2

11.3. Tarih Formatı

    API Request: ISO 8601 (2026-03-01T00:00:00.000Z)
    UI Gösterim: GG.AA.YYYY (06.03.2026)
    SQL Server: DATETIME (2026-03-06 14:30:00.000)

12. FAZ PLANLAMASI
Faz
	
Özellik
	
Durum
Faz-5
	
Hareketler Görüntüleme
	
✅ Mevcut
Faz-6
	
Sipariş Görüntüleme
	
⏳ Sonraki
Faz-7
	
Sepetim + Sipariş Oluşturma
	
⏳ Sonraki
Faz-8
	
Yapıkredi + Ödeme
	
⏳ Sonraki
Bu doküman MVP kapsamını tanımlar. Değişiklikler versiyon takibi ile yapılacaktır.
Onaylayan: Proje Yöneticisi | Tarih: 2026-03-07
Versiyon 1.2.0 Değişiklikleri:

    Detay sayfası modal değil, ayrı sayfa olarak değiştirildi
    Gereksiz detaylar temizlendi, önceki doküman formatına uygun hale getirildi
    Test senaryoları sadeleştirildi