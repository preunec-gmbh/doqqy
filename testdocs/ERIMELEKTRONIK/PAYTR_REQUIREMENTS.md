# ÖDEME MODÜLÜ — PAYTR ENTEGRASYONU (SİSTEM DURUMU)

**Versiyon:** 1.1 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel Sistem Yapısı

---

## 1. GENEL BAKIŞ

Ödeme entegrasyonu PayTR iFrame API ile gerçekleştirilmiştir. Tüm ödeme kayıtları PostgreSQL `web_payment` tablosunda tutulur.

**Önemli Kural:** Ödeme durumu ne olursa olsun, ERP `SIPARIS.ONAYLI` alanı backend tarafından değiştirilmez — bu alan ERP masaüstü uygulaması tarafından yönetilir.

---

## 2. ÖDEME YÖNTEMLERİ

| Yöntem | İşlem Tipi | Akış |
|--------|-----------|------|
| Kredi Kartı / Banka Kartı | `SEPET` veya `CARI_ODEME` | PayTR iFrame → callback → sipariş |
| EFT/Havale | — | Banka bilgisi gösterilir, admin onayı beklenir |
| Kapıda Ödeme / Diğer | — | Direkt sipariş oluşturulur, ödeme manuel |

---

## 3. KREDİ KARTI ÖDEME AKIŞI — SEPET (`SEPET`)

### 3.1. Ödeme Başlatma

**Route:** `POST /api/odeme/basalt`  
**Dosya:** `src/app/api/odeme/basalt/route.ts`

1. JWT doğrulama (Admin → `hedefCariId` parametresi, Müşteri → kendi cariId'si)
2. Aktif sepet + kalemler çekilir; fiyatlar ve stok durumu yeniden kontrol edilir
3. `buildUserBasket()` ile PayTR user_basket JSON'ı oluşturulur (KDV dahil fiyatlar)
4. `generateMerchantOid()` → `WEB{YYYY}{NNNNN}` formatında benzersiz sipariş no
5. `generatePaytrToken()` → HMAC-SHA256 ile hash hesabı
6. PayTR token API'ye POST (20s timeout)
7. `web_payment` tablosuna `durum = pending` ile kayıt oluşturulur
8. `iframeToken` + `merchantOid` döner

### 3.2. Callback İşleme

**Route:** `POST /api/odeme/callback` — **PUBLIC** (auth middleware dışı)  
**Dosya:** `src/app/api/odeme/callback/route.ts`

1. `verifyCallbackHash()` → timing-safe HMAC-SHA256 karşılaştırma
2. Hash uyuşmazsa: istek reddedilir, loglanır
3. Idempotency: Aynı `merchantOid` için daha önce işlem yapıldıysa yeniden işlenmez
4. **Prefix bazlı yönlendirme:**
   - `WEB` prefix → `handleSepetOdemeCallback()` → `createSiparis()` → sepet CONVERTED
   - `COD` prefix → `handleCariOdemeCallback()` → sipariş oluşturulmaz, sadece ödeme loglanır
5. Başarılı: `web_payment.durum = success`, `siparisId` güncellenir
6. Başarısız veya sipariş hatası: `web_payment.durum = failed` veya `success_no_order`
7. **Yanıt: Yalnızca `OK` string'i** — JSON, whitespace veya HTML eklenmez

**Kritik:** `ODEME_YONTEMI_KART = tenantConfig.paymentMethods.krediKartiId` sipariş OZEL_KOD_1'e yazılır.

### 3.3. PayTR Yardımcı Fonksiyonlar

**Dosya:** `src/lib/paytr.ts`

| Fonksiyon | Açıklama |
|-----------|----------|
| `generatePaytrToken()` | HMAC-SHA256 — parametre sırası PayTR dokümantasyonuna göre |
| `verifyCallbackHash()` | Callback doğrulama |
| `generateMerchantOid()` | `WEB{YYYY}{NNNNN}` formatı |
| `buildUserBasket()` | Base64-JSON sepet formatı |
| `toPaytrAmount()` | `34.56` → `3456` dönüşümü |
| `fromPaytrAmount()` | `3456` → `34.56` dönüşümü |
| `getPaytrConfig()` | Merchant ID/KEY/SALT env'den alır |
| `getPaytrTestMode()` | `PAYTR_TEST_MODE` env'den — `"1"` veya `"0"` |

---

## 4. DOĞRUDAN BORÇ ÖDEME AKIŞI — `CARI_ODEME` (Faz-10)

**Özellik aktif/pasif:** `tenantConfig.features.enableDirectDebtPayment`  
**Route:** `POST /api/odeme/cari-basalt`

Sipariş oluşturmaksızın müşterinin mevcut borcunu kapatması için:
1. Cari bakiyesi gösterilir
2. Müşteri ödemek istediği tutarı girer
3. `merchantOid` = `COD{...}` prefix ile üretilir
4. PayTR iFrame ile ödeme yapılır
5. Callback `COD` prefix'ini algılar → sipariş oluşturulmaz → `web_payment.durum = success`
6. Admin ERP'de manuel tahsilat fişi keser

**Bu özellik `enableDirectDebtPayment = false` ise:** Menüler gizlenir, endpoint hata döner.

---

## 5. ÖDEME GEÇMİŞİ

**Route:** `GET /api/odeme/cari-gecmis`

- Kullanıcının kendi ödeme kayıtları (`web_payment`)
- Tarih aralığı ve durum filtresi
- Admin tüm ödemeleri görebilir; müşteri yalnızca kendisini

---

## 6. GÜVENLİK

| Önlem | Açıklama |
|-------|----------|
| HMAC-SHA256 | Token ve callback imzalama |
| Timing-safe compare | Hash karşılaştırmasında zamanlama saldırısı önlemi |
| PUBLIC callback | Auth middleware dışı — PayTR'den gelen POST'lar için |
| Idempotency | Aynı merchantOid için çift işlem yapılmaz |
| Kart bilgisi | Sunucuya gelmez — PayTR iFrame'de işlenir |
| SSL zorunlu | Tüm PayTR istekleri HTTPS üzerinden |
| Env değişkenleri | `PAYTR_MERCHANT_KEY`, `PAYTR_MERCHANT_SALT` asla client'a gönderilmez |

---

## 7. HATA YÖNETİMİ

**Dosya:** `src/features/sepet/types/odeme.ts` → `PAYTR_HATA_MESAJLARI`

PayTR hata kodları kullanıcı dostu mesajlara dönüştürülür. Teknik hata kodları kullanıcıya gösterilmez.

**`success_no_order` durumu:** Ödeme başarılı ama sipariş oluştururken hata → `web_payment.durum = success_no_order` — manuel müdahale gerektirir.

---

## 8. ORTAM DEĞİŞKENLERİ

Detay için [ENVIRONMENT.md](ENVIRONMENT.md)'e bakınız.

```
PAYTR_MERCHANT_ID=
PAYTR_MERCHANT_KEY=
PAYTR_MERCHANT_SALT=
PAYTR_TEST_MODE=1    # production'da 0 olmalı
PAYTR_CALLBACK_URL=https://domain.com/api/odeme/callback
PAYTR_OK_URL=https://domain.com/dashboard/sepetim/basarili
PAYTR_FAIL_URL=https://domain.com/dashboard/sepetim/odeme
```

---

## 9. TEST STRATEJİSİ

- Test kart bilgileri: `docs/PAYTR/PayTRDocsDetail/` klasöründeki test kart dokümantasyonu
- `PAYTR_TEST_MODE=1` ile sandbox testleri
- Canlıya geçiş: `PAYTR_TEST_MODE=0` + PayTR panelinden mağaza onayı

---

## 10. VERİTABANI TABLO REFERANSI

### PostgreSQL

| Tablo | Amaç |
|-------|------|
| `web_payment` | Ödeme kayıtları — `merchantOid`, `durum`, `islemTipi`, `siparisId` |

### ERP (Yazma — Yalnızca Başarılı Callback Sonrası)

Callback başarılı ise `createSiparis()` çağrılır (bkz. [SIPARIS_REQUIREMENTS.md](SIPARIS_REQUIREMENTS.md)).

---

## 11. PAYTR DOKÜMAN REFERANSLARI

Detaylı PayTR API dokümantasyonu için bkz. `docs/PAYTR/` klasörü:
- `docs/PAYTR/paytr_dokumanlari.md` — genel bakış
- `docs/PAYTR/PayTRIFrameAPI/` — iFrame entegrasyon adımları
- `docs/PAYTR/PayTRDocsDetail/` — detaylı API dokümantasyonu (85+ dosya)
