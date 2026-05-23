# SİPARİŞ GEREKSİNİMLERİ (SİSTEM DURUMU)

**Versiyon:** 1.1 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel Sistem Yapısı

---

## 1. GENEL BAKIŞ

Sipariş modülü iki işlevi kapsar:
1. **Sipariş Görüntüleme:** ERP SQL Server'dan salt okunur listeleme ve detay
2. **Sipariş Oluşturma:** Sepet tamamlandığında stored procedure'ler aracılığıyla ERP'ye yazma

**ERP Okuma:** `SIPARIS`, `SIPARIS_DETAY`, `FIS`, `FIS_DETAY` tabloları — salt SELECT.  
**ERP Yazma:** Yalnızca `Ekle_Siparis` ve `Ekle_Siparis_Detay` stored procedure'leri üzerinden.

---

## 2. KULLANICI ROLLERİ

| Rol | Görüntüleyebilecekleri | Oluşturabilecekleri |
|-----|----------------------|---------------------|
| `ADMIN` | Tüm carilerin siparişleri | Müşteri adına sipariş (cariId parametresiyle) |
| `CUSTOMER` | Yalnızca kendi siparişleri | Kendi adına sipariş |

---

## 3. SİPARİŞ LİSTELEME

**Dosya:** `src/features/siparis/services/siparisService.ts` → `getSiparisList()`  
**Route:** `GET /api/siparis`  
**URL:** Admin → `/admin/siparis` | Müşteri → `/dashboard/siparis`

### Gösterilen Sütunlar

| Sütun | Kaynak |
|-------|--------|
| Sipariş No | `SIPARIS.BELGENO` |
| Sipariş Tarihi | `SIPARIS.SIPARIS_TARIHI` |
| Durum | `SIPARIS.ONAYLI` + `SIPARIS.FIS` |
| Toplam Tutar | `SIPARIS.GENELTOPLAM` (KDV dahil) |
| Fatura No | `FIS.BELGENO` (varsa) |
| Cari Ad | Admin'e gösterilir, müşteriye gizlenir |

### Durum Mapping

| `ONAYLI` | `FIS` | Durum | Badge |
|----------|-------|-------|-------|
| 0 | NULL | ERP_GONDERILDI | Sarı |
| 1 | NULL | ERP_GONDERILDI | Mavi |
| herhangi | DOLU | FATURALANDI | Yeşil |

### Filtreler

| Filtre | Kullanıcı | Açıklama |
|--------|-----------|----------|
| Tarih aralığı | Admin + Müşteri | Başlangıç-bitiş tarihi |
| Durum | Admin + Müşteri | ERP_GONDERILDI / FATURALANDI |
| Cari seçimi | Sadece Admin | Dropdown |
| Varsayılan aralık | Her ikisi | Son 90 gün |

**Sipariş türü filtresi:** `tenantConfig.orders.receivedType` (Erim: `SIPARIS_TURU = 2`)

### Sayfalama

- 25 kayıt/sayfa
- Sıralama: sipariş tarihine göre azalan (en yeni önce)

---

## 4. SİPARİŞ DETAY SAYFASI

**Dosya:** `src/features/siparis/services/siparisService.ts` → `getSiparisById()`  
**Route:** `GET /api/siparis/[id]`

### Gösterilen Bölümler

**Bölüm 1: Başlık**
Sipariş No, durum badge, sipariş tarihi, termin tarihi, vade tarihi.

**Bölüm 2: Müşteri Bilgileri**
Cari adı, cari kodu, teslimat adresi.

**Bölüm 3: Kalemler (Tablo)**
Ürün kodu, ürün adı, miktar, birim, birim fiyat, KDV, toplam.

**Bölüm 4: Finansal Özet**
Satır toplamı, KDV toplamı, iskonto, genel toplam.

**Bölüm 5: Fatura Bilgisi (Varsa)**
Fatura no, fatura tarihi, fatura türü.

### Güvenlik

- Müşteri: `SIPARIS.CARI = token.cariId` kontrolü — başka cari siparişine erişemez.
- Yetkisiz erişim: HTTP 403.

---

## 5. SİPARİŞ OLUŞTURMA

**Dosya:** `src/features/sepet/services/siparisService.ts` → `createSiparis()`  
**Route:** `POST /api/sepetim/siparis-olustur`

### Akış

1. Stok kontrolü: `AS_STOK_MIKTAR_GENEL` — tüm sepet kalemleri için
2. Fiyat çekme: `STOK.SON_ALIS_FIYAT × CARPAN` (birim dönüşümü ile)
3. Limit kontrolü: `(CARI_BAKIYELER.BAKIYE + sepatToplamı) ≤ CARI.RISK`
4. Barkod çekme: `STOK_BARKOD` tablosundan her kalem için
5. Sipariş no üretme: PostgreSQL sequence — `SPRS-YYYY-NNNNN` formatı
6. `[dbo].[Ekle_Siparis]` stored procedure çağrısı:
   - `@LOKASYON`: `tenantConfig.stock.locationId[0]`
   - `@PROJE`: `tenantConfig.stock.projectId[0]`
   - `@CARI_ADR`: Seçilen adres ID'si
7. `[dbo].[Ekle_Siparis_Detay]` stored procedure çağrısı (her kalem için)
8. Sipariş başarılı: `AKTIF = 1` ve `SIPARIS_OZEL_KOD_1 = odemeYontemiId` güncellenmesi
9. `web_cart.status = CONVERTED` olarak işaretlenir

### Sipariş Sonrası

- Sepet kartları korunur (referans için)
- Kullanıcıya sipariş no gösterilir
- PayTR ödemesinde callback sonrası ERP sipariş no'su alınır

### Hata Durumu

- ERP bağlantı hatası veya prosedür hatası → sepet korunur, "Tekrar Dene" gösterilir
- Stok bitik → stok hatası, sipariş oluşturulmaz
- Limit aşımı → limit uyarısı, işlem durur

---

## 6. SİPARİŞ VE ÖDEME İLİŞKİSİ

PayTR ödemeli sipariş akışı:
1. Sepet → `/api/odeme/basalt` → PayTR token alınır → `web_payment` oluşturulur (status=pending)
2. Müşteri PayTR iframe'de ödeme yapar
3. PayTR `/api/odeme/callback`'i çağırır → hash doğrulaması → `createSiparis()` → `web_payment.durum = success`
4. Başarısız ödeme → `web_payment.durum = failed`

Ödeme yöntemi ERP'de `SIPARIS_OZEL_KOD_1` alanına kaydedilir: `tenantConfig.paymentMethods.krediKartiId`.

---

## 7. API ENDPOINT'LERİ

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/siparis` | Login | Sipariş listesi (cariId filtresi otomatik) |
| GET | `/api/siparis/[id]` | Login | Sipariş detayı |
| GET | `/api/siparis/[id]/odeme` | Login | Siparişe bağlı ödeme bilgisi |
| POST | `/api/sepetim/siparis-olustur` | Login | Sepetten sipariş oluştur |

---

## 8. VERİTABANI TABLO REFERANSI

### ERP (Okuma)

| Tablo | Amaç |
|-------|------|
| `SIPARIS` | Sipariş başlık — `CARI`, `BELGENO`, `ONAYLI`, `FIS`, `GENELTOPLAM` |
| `SIPARIS_DETAY` | Sipariş kalemleri — `STOK`, `MIKTAR`, `FIYAT`, `TUTAR`, `KDV_TOPTAN` |
| `SIPARIS_TURU` | Sipariş türü tanımları |
| `FIS` | Fatura başlık |
| `FIS_DETAY` | Fatura kalemleri |
| `STOK_BARKOD` | Barkod bilgisi (sipariş oluştururken) |

### ERP (Yazma — Yalnızca Stored Procedure)

| Prosedür | Açıklama |
|----------|----------|
| `[dbo].[Ekle_Siparis]` | Sipariş başlık kaydı + SEQUENS_VER çağrısı |
| `[dbo].[Ekle_Siparis_Detay]` | Sipariş kalemi + otomatik toplam güncelleme |

### PostgreSQL

| Tablo | Amaç |
|-------|------|
| `web_cart` | Sipariş sonrası CONVERTED olarak işaretlenir |
| `web_payment` | Ödeme kaydı — `siparisId` callback sonrası dolar |
