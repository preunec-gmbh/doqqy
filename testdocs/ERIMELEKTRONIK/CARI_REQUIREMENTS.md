# CARİ YÖNETİMİ GEREKSİNİMLERİ (SİSTEM DURUMU)

**Versiyon:** 1.1 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel Sistem Yapısı

---

## 1. GENEL BAKIŞ

Cari (müşteri) yönetim modülü. ERP SQL Server'daki `CARI` ve ilgili tablolar salt okunur kullanılır; şifre ve erişim bilgileri PostgreSQL'de tutulur.

**Temel Kural:** ERP veritabanına yazma işlemi yapılmaz. Tek istisna: stored procedure'ler aracılığıyla sipariş oluşturma (sepet modülü).

---

## 2. VERİ KAYNAKLARI

| Kaynak | Kullanım |
|--------|----------|
| `CARI` (SQL Server) | Müşteri temel bilgileri, risk limiti, aktiflik |
| `CARI_BAKIYELER` (SQL Server) | Güncel bakiye (multi-currency, TRY önce sıralı) |
| `CARI_ADRES` (SQL Server) | Müşteri adresleri |
| `SIPARIS` (SQL Server) | Son siparişler özeti |
| `web_login` (PostgreSQL) | Web giriş bilgisi — `passwordHash`, `isActive`, `lastLoginAt` |

---

## 3. ADMIN — CARİ LİSTELEME

**Dosya:** `src/features/cari/services/cariService.ts` → `getCariList()`  
**Route:** `GET /api/cari`

### Gösterilen Sütunlar

| Sütun | Kaynak | Açıklama |
|-------|--------|----------|
| `KOD` | CARI.KOD | Cari kodu |
| `AD` | CARI.AD | Cari unvanı |
| `EMAIL` | CARI.EMAIL | E-posta |
| `RISK` | CARI.RISK | Kredi limiti (TRY) |
| `WEB ERİŞİM` | web_login.isActive | Yeşil/Kırmızı badge |
| `SON GİRİŞ` | web_login.lastLoginAt | Son giriş tarihi |

### Arama ve Filtreleme

- **Arama:** Sadece `CARI.AD` alanında `LIKE` (büyük/küçük harf duyarsız — tenant collation'ı kullanılır)
- **Aktif Filtre:** "Sadece Aktifleri Göster" toggle — `web_login.isActive` üzerinden filtreleme
- **Sıralama:** `AD` veya `RISK` alanına göre ASC/DESC

### Sayfalama

- Sayfa başına 25 kayıt (varsayılan)
- Cari listede bakiye gösterilmez (N+1 önlemek için); detay sayfasında çekilir

---

## 4. ADMIN — CARİ DETAY SAYFASI

**Dosya:** `src/features/cari/services/cariService.ts` → `getCariByKod()`

### Bölüm 1: Temel Bilgiler (Salt Okunur)

`KOD`, `AD`, `EMAIL`, `TELEFON`, `CEP TELEFONU`, `VERGI_NUMARASI`, `KIMLIK_NO`, `CARI_GRUP`, aktiflik badge.

### Bölüm 2: Finansal Bilgiler

- **RISK (Limit):** `CARI.RISK` (TRY)
- **BAKIYE:** `bakiyeService.getBakiyeInfo()` → `CARI_BAKIYELER` tablosundan TRY bakiyesi + multi-currency kalemler
  - Pozitif: Cari bize borçlu
  - Negatif: Biz cariye borçluyuz
  - `bakiyeHata = true` ise bakiye çekilemedi uyarısı

### Bölüm 3: Varsayılan Adres

`CARI_ADRES` tablosundan `VARSAYILAN = 1` olan kayıt: başlık, açık adres, il/ilçe, posta kodu, yetkili, telefon.

### Bölüm 4: Son 5 Sipariş

`SIPARIS` tablosundan cari ID ile filtrelenmiş son 5 kayıt: sipariş no, tarih, toplam tutar, durum.

### Bölüm 5: Web Erişim Yönetimi

- **Şifre Sıfırla:** Admin yeni şifre girer → bcrypt ile hash'lenir → `web_login.passwordHash` güncellenir. Bir sonraki girişte ERP fallback atlanır, yalnızca bu hash kullanılır.
- **Durum Değiştir:** `web_login.isActive` toggle. Pasif yapılırsa müşteri giriş yapamaz.
- **Not:** Şifre değişikliğinde müşteriye otomatik bildirim gönderilmez; admin manuel iletir.

---

## 5. CARİ (MÜŞTERİ) — PROFİL SAYFASI

**Route:** `/dashboard/profil`

Salt okunur profil bilgileri: ad, email, telefon, risk limiti, bakiye, varsayılan adres, son siparişler.

---

## 6. LİMİT KONTROLÜ

**Dosya:** `src/features/sepet/services/siparisService.ts` → `limitKontrol()`

Formül:
```
(CARI_BAKIYELER.BAKIYE + Sepet Toplamı) <= CARI.RISK
```

- Limit aşılırsa sipariş tamamlanamaz, uyarı gösterilir.
- `features.enableDirectDebtPayment = true` ise müşteriye borç ödeme sayfası seçeneği sunulur.

---

## 7. GÜVENLİK

- **Müşteri:** Yalnızca kendi verisine erişebilir. API endpoint'lerinde `cariKod === token.cariKod` kontrolü yapılır.
- **Admin:** Tüm carilere erişebilir.
- Yetkisiz erişim: HTTP 403 Forbidden.
- ERP bağlantısı: Read-only kullanıcı, IP kısıtlamalı.

---

## 8. HATA YÖNETİMİ

| Durum | Kullanıcı Mesajı |
|-------|-----------------|
| ERP bağlantı hatası | "Sistem hatası, lütfen tekrar deneyin" |
| Bakiye sorgu hatası | "Bakiye bilgisi alınamadı" — liste yine gösterilir |
| Yetkisiz erişim | "Bu işlem için yetkiniz yok" (403) |
| Şifre değiştirme hatası | "Şifre güncellenemedi" |

---

## 9. VERİTABANI TABLO REFERANSI

### ERP (Read-Only)

| Tablo | Kritik Alanlar |
|-------|----------------|
| `CARI` | `ID`, `KOD`, `AD`, `EMAIL`, `RISK`, `AKTIF`, `VERGI_NUMARASI`, `KIMLIK_NO`, `TELEFON`, `CEPNO` |
| `CARI_BAKIYELER` | `CARI_KOD`, `DOVIZ_AD`, `BAKIYE` |
| `CARI_ADRES` | `ID`, `CARI`, `AD`, `ADRES`, `VARSAYILAN`, `TELEFON`, `ILILCE` |
| `SIPARIS` | `ID`, `BELGENO`, `CARI`, `SIPARIS_TARIHI`, `GENELTOPLAM`, `ONAYLI`, `FIS` |

### PostgreSQL

| Tablo | Kritik Alanlar |
|-------|----------------|
| `web_login` | `id`, `cariKod`, `email`, `passwordHash`, `role`, `isActive`, `lastLoginAt` |
| `web_auth_log` | `id`, `email`, `cariKod`, `success`, `reason`, `ipAddress`, `createdAt` |

---

## 10. NOTLAR

- **Bakiye sıralama:** `bakiyeService` TRY bakiyesini önce sıralar (ORDER BY CASE WHEN DOVIZ_AD = 'TRY' THEN 0).
- **Email eşleşmesi:** PostgreSQL tarafında case-sensitive, SQL Server tarafında tenant collation'ına göre.
- **Negatif bakiye:** `bakiyeHata` flag'i ayrıca döner — bakiye verisi çekilemedi ama liste gösterilebilir.
