# Teknik Yığın ve Mimari Şartnamesi

**Versiyon:** 4.0.0 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel

---

## 1. GENEL BAKIŞ

B2B ERP Entegre Portalı — Next.js tabanlı, çift veritabanı mimarili, multi-tenant white-label web uygulaması.

---

## 2. TEMEL TEKNOLOJİLER

| Katman | Teknoloji | Versiyon | Notlar |
|--------|-----------|----------|--------|
| Framework | Next.js | 16.1.6 | App Router, SSR, API Routes |
| UI Kütüphanesi | React | 19.2.4 | — |
| Dil | TypeScript | 5.9.3 | Strict mode — `any` kullanımı yasak |
| Stil | Tailwind CSS | 4.1.8 | Utility-first, CSS variables ile tema |
| Bileşen Kütüphanesi | shadcn/ui | Güncel | Radix UI tabanlı, özelleştirilebilir |
| İkonlar | Lucide React | 0.510.0 | Hafif, tutarlı ikon seti |
| Runtime | Node.js | LTS | Hem yerel hem VPS ortamları |
| Paket Yöneticisi | pnpm | — | Hızlı ve disk dostu |

---

## 3. VERİTABANI VE ORM

### 3.1 Web Uygulama Veritabanı (PostgreSQL)

| Özellik | Teknoloji | Detay |
|---------|-----------|-------|
| Motor | PostgreSQL 16+ | Yerel: Docker, Production: VPS |
| ORM | Prisma | 7.4.2 |
| Adapter | @prisma/adapter-pg | pg 8.x üzerinden |
| Tablolar | `web_*` öneki | web_login, web_auth_log, web_cart, web_cart_item, web_payment, web_images |

### 3.2 ERP Veritabanı (SQL Server)

| Özellik | Teknoloji | Detay |
|---------|-----------|-------|
| Motor | Microsoft SQL Server | Şirket içi ERP sunucusu |
| Kütüphane | mssql | 12.2.0 |
| Erişim | **Salt Okunur** | SELECT, stored procedure çağrısı; doğrudan yazma yasak |
| Yazma | Stored Procedure | `Ekle_Siparis`, `Ekle_Siparis_Detay` — sipariş oluşturma için |
| Bağlantı | Read-only kullanıcı | IP kısıtlı, şifreli |

### 3.3 Veri Erişim Stratejisi

- **Senkronizasyon yok:** Stok, cari, fiyat — SQL Server'dan anlık okunur
- **PostgreSQL:** Yalnızca web'e özgü veriler (oturum, sepet, ödeme, görsel meta)
- **ERP'ye yazma:** Yalnızca stored procedure üzerinden (sipariş oluşturma)

---

## 4. KİMLİK DOĞRULAMA

| Bileşen | Teknoloji | Detay |
|---------|-----------|-------|
| Token üretimi | `jose` + `jsonwebtoken` | JWT, 24 saat ömür |
| Token doğrulama | `src/proxy.ts` | Next.js middleware — SSR ve API koruması |
| Şifre hashleme | `bcryptjs` | — |
| Cookie | HttpOnly, Secure, SameSite=Strict | XSS ve CSRF koruması |
| Rate limiting | Bellek içi IP tablosu | 5 deneme / 15 dakika |

---

## 5. DURUM YÖNETİMİ VE VERİ ÇEKME

| Konu | Teknoloji | Detay |
|------|-----------|-------|
| Server state | TanStack Query | v5 — API cache, refetch, stale-time |
| Form yönetimi | React Hook Form + Zod | Form validasyonu için Zod şemaları |
| Global state | React Context / props | Zustand kullanılmıyor |

---

## 6. ÖDEMEve ENTEGRASYONLAR

| Entegrasyon | Kütüphane / Yöntem | Detay |
|-------------|-------------------|-------|
| Ödeme | PayTR iFrame API | HMAC-SHA256 token, callback doğrulama |
| PayTR yardımcıları | `src/lib/paytr.ts` | `generatePaytrToken`, `verifyCallbackHash`, `buildUserBasket` |

---

## 7. MULTI-TENANT KONFİGÜRASYON

| Bileşen | Konum | Detay |
|---------|-------|-------|
| Config arayüzü | `src/config/types.ts` | `TenantConfig` TypeScript interface |
| Tenant seçici | `src/config/tenant.ts` | `TENANT_ID` env → tenant dosyası yükler |
| Tenant dosyaları | `src/config/tenants/` | `{tenantId}.ts` — her müşteri için ayrı |
| Client injection | `src/proxy.ts` | `window.__TENANT_CONFIG__` SSR'da enjekte |

Config kapsamı: tema, lokasyon ID'leri, proje ID'si, collation, KDV oranı, kritik stok eşiği, ödeme yöntemi ID'leri, feature flag'leri, dil/para birimi ayarları.

---

## 8. TEST

| Araç | Versiyon | Kapsam |
|------|----------|--------|
| Vitest | 4.x | Birim testleri, servis testleri |

---

## 9. PROJE YAPISI

```
src/
├── app/                  # Next.js App Router sayfaları ve API route'ları
│   ├── admin/            # Admin sayfaları
│   ├── dashboard/        # Müşteri sayfaları
│   └── api/              # API endpoint'leri
├── config/               # Multi-tenant konfigürasyon sistemi
│   ├── types.ts          # TenantConfig interface
│   ├── tenant.ts         # getTenantConfig() + Proxy
│   └── tenants/          # Tenant dosyaları (erim.ts, ...)
├── features/             # Domain bazlı özellik modülleri
│   ├── auth/             # Kimlik doğrulama servisleri
│   ├── cari/             # Cari yönetimi
│   ├── stok/             # Stok/ürün modülü
│   ├── siparis/          # Sipariş görüntüleme
│   ├── sepet/            # Sepet ve sipariş oluşturma + PayTR
│   └── hareketler/       # Finansal hareketler
├── lib/                  # Paylaşılan yardımcı kütüphaneler
│   ├── paytr.ts          # PayTR entegrasyon yardımcıları
│   └── ...
├── core/                 # Paylaşılan altyapı (db, utils, types)
├── components/           # Paylaşılan UI bileşenleri
│   └── ui/               # shadcn/ui bileşenleri
└── proxy.ts              # Next.js middleware — JWT + tenant config injection
```

---

## 10. GÜVENLİK STANDARTLARİ

| Alan | Standart |
|------|---------|
| Ortam değişkenleri | `.env` — koda asla yazılmaz, client'a gönderilmez |
| SQL injection | Prisma ORM (PostgreSQL); parametreli sorgu (SQL Server) |
| XSS | Next.js varsayılan escape; `dangerouslySetInnerHTML` yasak |
| CSRF | SameSite=Strict cookie |
| Kart bilgisi | PayTR iFrame — sunucuya gelmez |
| Rate limiting | Login endpoint brute-force koruması |
| ERP erişimi | Read-only kullanıcı, IP whitelist, sıfır yazma yetkisi |

---

## 11. KODLAMA STANDARTLARI

- Fonksiyonel bileşenler ve servisler
- API response tipleri `features/*/types/` klasörlerinde tanımlı
- Hata yönetimi: `try-catch` — kullanıcıya teknik detay gösterilmez
- İsimlendirme: Bileşenler `PascalCase`, utility'ler `camelCase`, API route'lar `kebab-case`
- Tüm PostgreSQL sorguları Prisma ile; SQL Server için parametreli `mssql` sorguları

---

## 12. BAĞIMLILIK LİSTESİ (BAŞLICALAR)

| Paket | Versiyon |
|-------|---------|
| next | 16.1.6 |
| react | 19.2.4 |
| typescript | 5.9.3 |
| tailwindcss | 4.1.8 |
| @prisma/client | 7.4.2 |
| @prisma/adapter-pg | 7.4.2 |
| mssql | 12.2.0 |
| jose | 5.10.0 |
| jsonwebtoken | 9.0.2 |
| bcryptjs | 3.0.2 |
| @tanstack/react-query | 5.75.5 |
| react-hook-form | 7.56.3 |
| zod | 3.24.4 |
| lucide-react | 0.510.0 |
| vitest | 4.0.0 |
