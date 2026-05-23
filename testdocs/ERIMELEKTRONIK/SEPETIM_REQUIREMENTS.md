# SEPETİM GEREKSİNİMLERİ (SİSTEM DURUMU)

**Versiyon:** 1.1 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel Sistem Yapısı

---

## 1. GENEL BAKIŞ

Sepet modülü. Sepet verileri PostgreSQL'de tutulur; sipariş oluştururken ERP stored procedure'leri çağrılır. Ödeme entegrasyonu PayTR iFrame API üzerindendir.

---

## 2. VERİ YAKLAŞIMI

| Konu | Uygulanan Karar |
|------|----------------|
| Sepet veri saklama | PostgreSQL (`web_cart` + `web_cart_item`) |
| Fiyat sabitlendi mi? | **Evet** — fiyatlar sepete ekleme anında `web_cart_item`'a yazılır |
| Fiyat kontrolü | Ödeme başlatmadan önce `/api/odeme/fiyat-kontrol` ile doğrulanır |
| Stok rezervasyonu | Yok — sipariş oluştururken anlık kontrol |
| Sipariş numarası | Web: `SPRS-YYYY-NNNNN` (PostgreSQL sequence), ERP: `BELGENO` (prosedür üretir) |
| Ödeme yöntemi | PayTR iFrame API (kredi kartı) + havale/EFT + diğer |
| Sepet ömrü | 30 gün işlem görmeyen → `ABANDONED` |

---

## 3. KULLANICI ROLLERİ

| Rol | Yetki |
|-----|-------|
| `CUSTOMER` | Kendi sepetini oluşturur, görür, düzenler, siparişe geçer |
| `ADMIN` | `hetefCariId` parametresiyle müşteri adına tüm akışı yönetir |

---

## 4. SEPET OPERASYONLARI

**Dosya:** `src/features/sepet/services/sepetService.ts`

### Sepet Oluşturma / Getirme

`getOrCreateCart(userId)` — kullanıcının `ACTIVE` sepeti yoksa yeni oluşturur.

### Ürün Ekleme (`/api/sepetim/ekle`)

1. Stok kontrolü: `AS_STOK_MIKTAR_GENEL` — anlık
2. Fiyat çekme: `STOK.SON_ALIS_FIYAT × CARPAN` + KDV hesaplaması
3. Aynı stokId + birimId varsa miktarı artırır; yoksa yeni satır ekler
4. Fiyat bilgileri (kdvHaricFiyat, kdvDahilFiyat, kdvOrani, kdvTutari) `web_cart_item`'a sabit olarak yazılır

### Ürün Güncelleme (`/api/sepetim/guncelle`)

Miktar veya birim güncellemesi. Birim değişince yeni KDV hesaplanır ve `web_cart_item`'a yazılır.

### Ürün Silme / Sepeti Boşaltma

`/api/sepetim/sil` | `/api/sepetim/bosalt`

---

## 5. SEPET SAYFASI

**URL:** Müşteri → `/dashboard/sepetim` | Admin → `/admin/sepetim`

- Ürünler listesi: stokAd, stokKod, miktar, birimAd, KDV hariç fiyat, toplam
- KDV hariç alt toplam, KDV toplamı, genel toplam
- Miktar artır/azalt, ürün sil, sepeti boşalt butonları
- "Siparişe Geç" butonu

---

## 6. ADRES SEÇİMİ

**URL:** `/dashboard/sepetim/adres`

- `CARI_ADRES` tablosundan müşteri adresleri çekilir
- `VARSAYILAN = 1` olan adres otomatik seçili
- Kart formatında adres listesi
- Seçilen adres ID'si (`CARI_ADRES.ID`) sipariş oluşturulurken kullanılır

---

## 7. ÖDEME YÖNTEMİ SEÇİMİ

**URL:** `/dashboard/sepetim/odeme`  
**Route:** `GET /api/sepetim/odeme-yontemleri`

Ödeme yöntemleri tenant konfigürasyonundan belirlenir:

| Yöntem | ID (Erim) | Akış |
|--------|-----------|------|
| Kredi Kartı | 48 | PayTR iFrame → callback |
| EFT/Havale | 30 | Bilgi gösterimi → admin onayı |
| Kapıda Ödeme | 10 | Direkt sipariş oluşturma |
| Diğer | 97 | Direkt sipariş oluşturma |

**Limit kontrolü bu aşamada yapılır:**
```
(CARI_BAKIYELER.BAKIYE + sepatToplamı) ≤ CARI.RISK
```
Limit aşılırsa uyarı gösterilir; kredi kartı ödeme tamamlandıktan sonra sipariş oluşturulur (limit kontrol bypass — zaten ödendi).

---

## 8. KREDİ KARTI ÖDEMESİ (PayTR iFrame)

**Dosyalar:**  
- `src/features/sepet/components/PaytrIframe.tsx`  
- `src/app/api/odeme/basalt/route.ts`

1. `/api/odeme/basalt` çağrılır → `web_payment` `pending` statüsünde oluşturulur
2. PayTR'ye token isteği gönderilir (`HMAC-SHA256` imzalı)
3. `iframeToken` ile PayTR iframe gösterilir — kart bilgileri PayTR'ye gider, sunucumuza gelmez
4. Ödeme tamamlanınca PayTR `/api/odeme/callback` (PUBLIC) endpoint'ine POST atar
5. Callback: hash doğrulama → idempotency → `createSiparis()` → `web_cart = CONVERTED` → `web_payment.durum = success`
6. Müşteri `/dashboard/sepetim/basarili` sayfasına yönlendirilir

### Fiyat Kontrolü

`/api/odeme/fiyat-kontrol` — ödeme başlatmadan önce sepetteki sabit fiyatların hâlâ geçerli olup olmadığını kontrol eder. Fark varsa kullanıcıya uyarı gösterilir.

---

## 9. DİĞER ÖDEME YÖNTEMLERİ (Direkt Sipariş)

**Route:** `POST /api/sepetim/siparis-olustur`

Kredi kartı dışı yöntemler (havale, kapıda ödeme, diğer) için:
1. Stok + fiyat kontrolü
2. Limit kontrolü
3. `createSiparis()` çağrısı
4. `web_cart = CONVERTED`
5. Başarı sayfasına yönlendirilir

---

## 10. BAŞARI SAYFASI

**URL:** `/dashboard/sepetim/basarili?oid=[merchantOid]`

- Sipariş numarası (`SPRS-YYYY-NNNNN` formatı)
- Sipariş özeti
- "Siparişlerime Git" ve "Alışverişe Devam Et" butonları

---

## 11. SEPET YAŞAM DÖNGÜSÜ

```
ACTIVE → CONVERTED  (sipariş başarılı)
ACTIVE → ABANDONED  (30 gün işlem yok)
```

---

## 12. İŞ KURALLARI

| Kural | Açıklama |
|-------|----------|
| BR-SEP-01 | Kritik stok altındaki ürünler sepete eklenemez |
| BR-SEP-02 | Stokta olmayan ürünler sepete eklenemez |
| BR-SEP-03 | Ekleme anında fiyatlar sabitlenir ve web_cart_item'a yazılır |
| BR-SEP-04 | Ödeme başlatmadan önce fiyat-kontrol endpoint'i çağrılır |
| BR-SEP-05 | Sipariş oluştururken stok tekrar kontrol edilir |
| BR-SEP-06 | PayTR callback başarılı ise sipariş oluşturulur |
| BR-SEP-07 | Aynı merchantOid için çift callback idempotent işlenir |
| BR-SEP-08 | Sipariş başarısız ise sepet CONVERTED yapılmaz, kullanıcı "Tekrar Dene" görür |
| BR-SEP-09 | Admin müşteri adına `hedefCariId` parametresiyle işlem yapabilir |

---

## 13. API ENDPOINT'LERİ

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/sepetim` | Login | Aktif sepeti getir |
| GET | `/api/sepetim/count` | Login | Sepet ürün sayısı |
| POST | `/api/sepetim/ekle` | Login | Ürün ekle |
| PATCH | `/api/sepetim/guncelle` | Login | Miktar/birim güncelle |
| DELETE | `/api/sepetim/sil` | Login | Ürün sil |
| DELETE | `/api/sepetim/bosalt` | Login | Sepeti boşalt |
| GET | `/api/sepetim/adresler` | Login | Cari adresleri |
| GET | `/api/sepetim/odeme-yontemleri` | Login | Ödeme yöntemleri |
| POST | `/api/sepetim/limit-kontrol` | Login | Limit kontrolü |
| POST | `/api/sepetim/stok-kontrol` | Login | Stok kontrolü |
| POST | `/api/sepetim/siparis-olustur` | Login | Direkt sipariş oluştur |
| POST | `/api/odeme/basalt` | Login | PayTR token başlat |
| GET | `/api/odeme/fiyat-kontrol` | Login | Fiyat doğrulama |
| POST | `/api/odeme/callback` | PUBLIC | PayTR webhook |
| GET | `/api/odeme/durum` | Login | Ödeme durumu sorgula |

---

## 14. VERİTABANI TABLO REFERANSI

### PostgreSQL

| Tablo | Amaç |
|-------|------|
| `web_cart` | Sepet başlık — `status` yönetimi |
| `web_cart_item` | Sepet kalemleri — sabitlenmiş fiyatlar dahil |
| `web_payment` | Ödeme kaydı |

### ERP (Okuma)

| Tablo | Amaç |
|-------|------|
| `AS_STOK_MIKTAR_GENEL` | Stok miktarı sorgusu |
| `CARI_BAKIYELER` | Limit kontrolü |
| `CARI_ADRES` | Adres listesi |
| `STOK` | Fiyat bilgisi |
| `STOK_BARKOD` | Sipariş oluştururken barkod |

### ERP (Yazma — Stored Procedure)

| Prosedür | Açıklama |
|----------|----------|
| `[dbo].[Ekle_Siparis]` | Sipariş başlık |
| `[dbo].[Ekle_Siparis_Detay]` | Sipariş kalemleri |
