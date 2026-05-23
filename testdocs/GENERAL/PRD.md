# Ürün Gereksinim Dokümanı — Genel Proje Özeti

**Versiyon:** 1.0.0 | **Son Güncelleme:** 2026-05-20 | **Durum:** Aktif Geliştirme

---

## 1. PROJE TANIMI

**Ürün:** B2B ERP Entegre Portali — şirketin ERP sistemine bağlı, müşterilere yönelik self-servis web portalı.

**Problem:** ERP sistemi yalnızca masaüstü uygulama veya şirket içi ağ üzerinden erişilebilir. Müşteriler stok durumu, fiyat, bakiye ve sipariş bilgileri için satış temsilcilerine bağımlıdır.

**Çözüm:** İki veritabanı katmanlı modern web portali:

| Katman | Teknoloji | Kullanım |
|--------|-----------|---------|
| Web DB | PostgreSQL (Prisma) | Oturum, sepet, ödeme kayıtları |
| ERP DB | SQL Server (mssql) | Stok, cari, sipariş, fiyat — salt okunur |

**Mimari:** Multi-tenant white-label sistem. `TENANT_ID` ortam değişkeni ile aynı kod tabanından farklı müşteri şirketlerine özelleştirilmiş portal sunulabilir.

---

## 2. HEDEF KİTLE

| Kullanıcı | Açıklama |
|-----------|----------|
| **Müşteri (Cari)** | ERP'de kayıtlı B2B alıcı. Stok görme, sipariş verme, ödeme yapma. |
| **Admin** | Sistem yöneticisi. Tüm carileri, siparişleri, ödeme geçmişini ve sistem ayarlarını yönetir. |

---

## 3. TEMEL ÖZELLİKLER

### Müşteri (CUSTOMER)
- Ürün kataloğu: arama, kategori filtresi, stok durumu, fiyat
- Sepet: ürün ekleme, birim seçimi, fiyat sabitleme
- Sipariş oluşturma: adres seçimi, ödeme yöntemi seçimi, limit kontrolü
- Sipariş geçmişi ve detayı
- Finansal hareketler (bakiye, fatura, tahsilat)
- Kredi kartı ödeme (PayTR iFrame)
- Doğrudan borç ödeme (kredi kartı ile, sipariş oluşturmadan)
- Profil sayfası

### Admin
- Tüm müşteri işlemlerini müşteri adına yapabilme
- Cari listeleme, detay, şifre sıfırlama, aktif/pasif toggle
- Sipariş ve hareket görüntüleme (tüm carilere)
- Ürün görsel yönetimi (yükleme, silme, sıralama)
- Ödeme geçmişi (tüm ödemeler)
- Döviz kuru ayarları

---

## 4. MİMARİ ÖZET

```
Tarayıcı
    │
    ▼
Next.js 16 (App Router, SSR)
    │
    ├── /admin/**       → ADMIN rolü zorunlu
    ├── /dashboard/**   → CUSTOMER rolü zorunlu
    └── /api/**         → JWT middleware → Handler
          │
          ├── Prisma → PostgreSQL
          │   web_login, web_auth_log, web_cart, web_cart_item,
          │   web_payment, web_images
          │
          └── mssql → SQL Server (ERP) — Salt Okunur
              STOK, CARI, SIPARIS, FIS, FINANS, ...
              Stored Proc: Ekle_Siparis, Ekle_Siparis_Detay
```

### Multi-Tenant Katmanı

```
TENANT_ID (env)
    │
    ▼
src/config/tenant.ts → getTenantConfig()
    │
    └── src/config/tenants/{tenantId}.ts → TenantConfig nesnesi
```

Her tenant için: tema, dil, para birimi, stok lokasyon ID'leri, proje ID'si, collation, KDV oranı, kritik stok eşiği, ödeme yöntemi ID'leri, feature flag'leri.

---

## 5. KİMLİK DOĞRULAMA

| Akış | Strateji |
|------|---------|
| Admin girişi | PostgreSQL `web_login` — bcrypt karşılaştırması |
| Cari girişi | PostgreSQL bcrypt → başarısız ise ERP SQL Server fallback |
| ERP fallback | `tenantConfig.auth.fallbackStrategy`: `LAST_5_DIGITS` veya `STATIC` |
| Token | JWT — HttpOnly, Secure, SameSite=Strict, 24 saat |
| Rate limiting | IP bazlı: 5 başarısız deneme / 15 dakika |

---

## 6. ÖDEME

| Yöntem | Akış |
|--------|------|
| Kredi/Banka Kartı | PayTR iFrame API — HMAC-SHA256, callback doğrulama |
| EFT/Havale | Banka bilgisi gösterilir, admin onayı beklenir |
| Kapıda Ödeme / Diğer | Direkt sipariş oluşturulur |
| Doğrudan Borç Ödeme | PayTR iFrame — sipariş oluşturulmaz (`enableDirectDebtPayment` feature flag) |

---

## 7. TAMAMLANAN FAZLAR

| Faz | Başlık | Durum |
|-----|--------|-------|
| 1 | Temel altyapı, JWT kimlik doğrulama, login | ✅ |
| 2 | Cari yönetimi (listeleme, detay, şifre, bakiye) | ✅ |
| 3 | Stok yönetimi (listeleme, detay, görsel, CDN) | ✅ |
| 4 | Finansal hareketler (listeleme, export) | ✅ |
| 5 | Sipariş görüntüleme | ✅ |
| 6 | Ayarlar ve kullanıcı yönetimi | ✅ |
| 7 | Sepet ve sipariş oluşturma (stored proc) | ✅ |
| 8 | Admin görsel yönetimi | ✅ |
| 9 | PayTR kredi kartı ödeme | ✅ |
| 10 | Doğrudan borç ödeme (cari ödeme) | ✅ |
| 11 | Dövizli fiyatlandırma | ✅ |
| ip1/faz-1 | Multi-tenant konfigürasyon şeması | 🔄 Devam |

---

## 8. GÜVENLİK ÖZETİ

- JWT: HttpOnly cookie, 24 saat, SameSite=Strict
- Şifreler: bcrypt — plain text saklanmaz
- ERP: read-only kullanıcı, IP whitelist
- PayTR: HMAC-SHA256, kart bilgisi sunucuya gelmez
- Rate limiting: brute-force koruması
- Hata mesajları: teknik detay kullanıcıya gösterilmez

---

## 9. DETAYLI DOKÜMANLAR

| Konu | Doküman |
|------|---------|
| Teknik yığın | [TECH_STACK.md](TECH_STACK.md) |
| UI/UX kılavuzu | [UI_UX_GUIDE.md](UI_UX_GUIDE.md) |
| Multi-tenant sistem | [MULTI_TENANCY.md](MULTI_TENANCY.md) |
| Ortam değişkenleri | [ENVIRONMENT.md](ENVIRONMENT.md) |
| API endpoint'leri | [API_ROUTES.md](API_ROUTES.md) |
| Veritabanı şeması | [../DATABASES/PRISMA.md](../DATABASES/PRISMA.md) |
| Tenant gereksinimleri | [../ERIMELEKTRONIK/PRD.md](../ERIMELEKTRONIK/PRD.md) |
