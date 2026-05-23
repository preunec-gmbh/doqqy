# Ürün Gereksinim Dokümanı (PRD) — Güncel Sistem Durumu

**Proje:** B2B ERP Entegre Portali  
**Versiyon:** 4.0.0 | **Son Güncelleme:** 2026-05-20 | **Durum:** Aktif Geliştirme

---

## 1. PROJE TANIMI

**Problem:** Şirketin ERP sistemi yalnızca masaüstü uygulama veya şirket içi ağ üzerinden erişilebilir. Müşteriler stok, fiyat ve bakiye bilgileri için satış temsilcilerine bağımlı.

**Çözüm:** İki veritabanı katmanlı modern web portali:
- **SQL Server (ERP):** Ana veri kaynağı — stok, cari, fiyat, sipariş; anlık okunur, senkronizasyon yok
- **PostgreSQL (Web):** Web'e özgü veriler — giriş, sepet, ödeme kayıtları

**Mimari:** Multi-tenant white-label sistem. `TENANT_ID` env değişkeni ile farklı şirketlere aynı kod tabanından özelleştirilmiş portal sunulabilir.

---

## 2. KULLANICI ROLLERİ

| Rol | Açıklama | Ana Sayfası |
|-----|----------|-------------|
| `ADMIN` | Sistem yöneticisi | `/admin/dashboard` |
| `CUSTOMER` | ERP müşterisi (Cari) | `/dashboard` |

---

## 3. TAMAMLANAN FAZLAR

### Faz 1 — Temel Altyapı ve Login ✅
- PostgreSQL kurulumu, Prisma şeması
- JWT kimlik doğrulama middleware (`src/proxy.ts`)
- Admin login: PostgreSQL bcrypt
- Cari login: Hibrit (PostgreSQL bcrypt + ERP SQL Server fallback)
- Rate limiting (IP bazlı, 5 deneme/15dk)
- Rol bazlı yönlendirme (`/admin`, `/dashboard`)
- Denetim kayıtları (`web_auth_log`)

### Faz 2 — Cari Yönetimi ✅
- Admin: Cari listeleme, arama, sayfalama
- Admin: Cari detay (temel bilgi, bakiye, adres, son siparişler)
- Admin: Şifre sıfırlama, aktif/pasif toggle
- Müşteri: Profil sayfası (salt okunur)
- Bakiye: Multi-currency `CARI_BAKIYELER` sorgusu

### Faz 3 — Stok Yönetimi ✅
- Ürün listeleme: Kart formatı, sayfalama, arama, kategori filtresi
- Ürün detay: Birim seçici, fiyat, stok durumu
- Stok durumu: VAR / KRİTİK / YOK (tenant konfigürasyonlu eşik)
- Görsel yönetimi: `web_images` (PostgreSQL) + CDN fallback
- Admin: Görsel yükleme/silme/sıralama

### Faz 4 — Finansal Hareketler (Hareketler) ✅
- Müşteri ve admin: Hareket listeleme (tarih, tür filtresi)
- Bakiye özeti kartı
- Hareket detayı (fatura kalemleri)
- PDF ve Excel export (`/api/hareketler/export/`)

### Faz 5 — Sipariş Görüntüleme ✅
- Admin ve müşteri: Sipariş listeleme (durum, tarih, cari filtresi)
- Sipariş detayı (kalemler, finansal özet, fatura bilgisi)
- Durum mapping: `ONAYLI` + `FIS` alanları

### Faz 6 — Ayarlar ve Kullanıcı Yönetimi ✅
- Admin: Kullanıcı listesi ve yönetimi
- Döviz kuru ayarları

### Faz 7 — Sepet ve Sipariş Oluşturma ✅
- Sepet CRUD (`web_cart` + `web_cart_item`)
- Fiyatlar sepete ekleme anında sabitlenir
- Adres seçimi, ödeme yöntemi seçimi
- Stored procedure ile ERP'ye sipariş yazma (`Ekle_Siparis`, `Ekle_Siparis_Detay`)
- Limit kontrolü
- Başarı sayfası

### Faz 8 — Görsel Yönetimi ✅
- Admin: Ürün görseli yükleme (PostgreSQL `web_images`)
- CDN URL + PostgreSQL hibrit görsel servisi

### Faz 9 — Kredi Kartı Ödeme (PayTR iFrame) ✅
- PayTR iFrame API entegrasyonu
- Ödeme başlatma: HMAC-SHA256 token
- Callback: Hash doğrulama, idempotency, sipariş oluşturma
- `web_payment` kayıt yönetimi
- Fiyat kontrol endpoint'i

### Faz 10 — Alışverişsiz Borç Ödeme (Cari Ödeme) ✅
- Sipariş oluşturmaksızın cari borç ödeme
- Feature flag: `tenantConfig.features.enableDirectDebtPayment`
- `COD` prefix'li merchantOid akışı

### Faz 11 — Dövizli Fiyatlandırma ✅
- Ürün döviz fiyat desteği
- Kur çekimi ve TRY çeviri

### Faz 1 (Config) — Multi-Tenant Konfigürasyon Şeması 🔄 (Devam Ediyor)
- `src/config/` klasörü: `TenantConfig` arayüzü, tenant dosyaları, proxy nesnesi
- 21 hardcoded nokta tespit edildi (bkz. `docs/PHASES/ip1/faz-1-config-schema.md`)
- Tamamlanan konfigürasyonlar: lokasyon ID, proje ID, collation, KDV fallback, kritik stok eşiği, marjin alanı, fallback stratejisi, ödeme yöntemi ID'leri, tema, metadata

---

## 4. MİMARİ ÖZET

```
Kullanıcı Browser
     │
     ▼
Next.js 16 (App Router, SSR)
     │
     ├── /admin/**  → ADMIN rolü gerektirir
     ├── /dashboard/**  → CUSTOMER rolü gerektirir
     └── /api/**  → Auth middleware → Handler
           │
           ├── Prisma (PostgreSQL)
           │   web_login, web_cart, web_payment, web_images
           │
           └── mssql (SQL Server — Read-only)
               CARI, STOK, SIPARIS, FIS, FINANS, ...
               Stored Proc: Ekle_Siparis, Ekle_Siparis_Detay
```

---

## 5. TEKNİK STACK ÖZETI

| Katman | Teknoloji |
|--------|-----------|
| Framework | Next.js 16, React 19, TypeScript 5 |
| Stil | Tailwind CSS 4, shadcn/ui |
| State | TanStack Query v5, React Hook Form + Zod |
| PostgreSQL | Prisma 7, @prisma/adapter-pg |
| SQL Server | mssql 12 |
| Auth | JWT (jose + jsonwebtoken), bcryptjs |
| Ödeme | PayTR iFrame API |
| Test | Vitest 4 |

---

## 6. GÜVENLİK PRENSİPLERİ

- JWT token: HttpOnly, Secure, SameSite=Strict cookie — 24 saat
- Rate limiting: Login endpoint'inde IP bazlı brute-force koruması
- ERP: Dedicated read-only SQL Server kullanıcısı, IP whitelist
- Şifreler: bcrypt hash, plain text saklanmaz
- PayTR: HMAC-SHA256 doğrulama, kart bilgisi sunucuya gelmez
- Hata mesajları: Kullanıcıya teknik detay gösterilmez

---

## 7. DETAYLI GEREKSİNİM DOKÜMANLARI

| Modül | Doküman |
|-------|---------|
| Login & Auth | [LOGIN_REQUIREMENTS.md](LOGIN_REQUIREMENTS.md) |
| Cari Yönetimi | [CARI_REQUIREMENTS.md](CARI_REQUIREMENTS.md) |
| Stok Yönetimi | [STOK_REQUIREMENTS.md](STOK_REQUIREMENTS.md) |
| Sipariş | [SIPARIS_REQUIREMENTS.md](SIPARIS_REQUIREMENTS.md) |
| Sepet | [SEPETIM_REQUIREMENTS.md](SEPETIM_REQUIREMENTS.md) |
| PayTR Ödeme | [PAYTR_REQUIREMENTS.md](PAYTR_REQUIREMENTS.md) |
