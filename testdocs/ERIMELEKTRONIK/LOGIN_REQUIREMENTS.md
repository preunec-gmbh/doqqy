# LOGIN VE KİMLİK DOĞRULAMA GEREKSİNİMLERİ (SİSTEM DURUMU)

**Versiyon:** 1.2 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel Sistem Yapısı

---

## 1. GENEL BAKIŞ

B2B ERP Entegre Portali'nın giriş ve yetkilendirme sistemini tanımlar. İki kullanıcı rolü mevcuttur: **Admin** ve **Cari (Müşteri)**. Her iki rol de e-posta + şifre ile giriş yapar; aynı `LoginForm` bileşeni kullanılır.

**Kapsam Dışı:** "Beni Hatırla", "Şifremi Unuttum", e-posta ile doğrulama.

---

## 2. KULLANICI ROLLERİ

| Rol | Açıklama | Giriş Yöntemi | Yönlendirme |
|-----|----------|---------------|-------------|
| `ADMIN` | Sistem yöneticisi | E-posta + bcrypt (PostgreSQL) | `/admin/dashboard` |
| `CUSTOMER` | ERP müşterisi | Hibrit: PostgreSQL bcrypt + ERP SQL Server fallback | `/dashboard` |

---

## 3. LOGIN ARAYÜZÜ (UI)

- Hem `/login` (müşteri) hem `/admin/login` (admin) ortak `LoginForm` bileşenini kullanır.
- Form üzerinde "Müşteri" / "Yönetici" sekme geçişi (pill style) bulunur.
- Rotaya göre `defaultRole` parametresi atanır.
- Oturum süresi dolduğunda (`?expired=1`) "Oturum süreniz doldu" uyarısı gösterilir.
- Hatalar form üzerinde kırmızı alert kutusu ile gösterilir; spesifik neden gizlenir.

---

## 4. ADMIN LOGIN AKIŞI

**Dosya:** `src/features/auth/services/adminAuthService.ts`

1. Kullanıcı e-posta + şifre girer, rol "Yönetici" seçer.
2. `POST /api/auth/login` çağrılır.
3. PostgreSQL `web_login` tablosunda `email` ve `role = ADMIN` kontrolü yapılır.
4. `isActive = false` ise reddedilir.
5. `bcrypt.compare` ile şifre doğrulanır.
6. Başarılı ise JWT token üretilir (payload: `{ sub: adminId, role: "ADMIN" }`), `auth_token` HttpOnly cookie'ye yazılır.
7. `/admin/dashboard`'a yönlendirilir.

**Not:** Geliştirme ortamında (`DATABASE_URL` tanımsız ise) `.env` üzerindeki `ADMIN_EMAIL` ve `ADMIN_PASSWORD` ile mock giriş fallback'i aktif olur.

---

## 5. CARİ (MÜŞTERİ) LOGIN AKIŞI — HİBRİT YETKİLENDİRME

**Dosya:** `src/features/auth/services/cariAuthService.ts`

### Aşama 1: PostgreSQL Kontrolü
1. `email` ile `web_login` tablosunda kullanıcı aranır.
2. `isActive = false` ise giriş derhal reddedilir.
3. Kayıtta `passwordHash` mevcutsa → `bcrypt.compare` ile doğrulanır. Başarılı ise giriş onaylanır.

### Aşama 2: ERP SQL Server Fallback (Varsayılan Şifre)
Yalnızca `web_login`'de kayıt yoksa veya `passwordHash = null` ise devreye girer.

1. SQL Server `CARI` tablosundan `email` ile kullanıcı aranır.
2. `AKTIF = 0` ise reddedilir.
3. Fallback şifre `tenantConfig.auth.fallbackStrategy` konfigürasyonundan belirlenir:
   - `LAST_5_DIGITS`: `KIMLIK_NO` son 5 hane; boşsa `VERGI_NUMARASI` son 5 hane.
   - `STATIC`: `tenantConfig.auth.staticPassword` değeri.
4. İkisi de boş veya eşleşmezse kimlik bilgisi eksik/yanlış hatası.

### Başarılı Giriş Sonrası
- `provisionCariLogin` servisi çağrılır: `web_login` tablosunda kayıt yoksa **otomatik oluşturulur** veya `lastLoginAt` güncellenir.
- JWT token üretilir (payload: `{ sub: cariKod, role: "CUSTOMER", cariKod, cariId }`).
- `/dashboard`'a yönlendirilir.

---

## 6. GÜVENLİK

### 6.1. Rate Limiting
**Dosya:** `src/core/utils/rateLimiter.ts`

- IP bazlı in-memory sayaç.
- **Eşik:** Aynı IP'den 5 başarısız deneme / 15 dakika penceresi.
- Eşik aşılırsa: HTTP 429 + "Çok fazla deneme yaptınız, lütfen X dakika sonra tekrar deneyin."
- Başarılı girişte IP sayacı sıfırlanır.
- **Kısıt:** Sunucu yeniden başlarsa sayaç sıfırlanır (in-memory MVP).

### 6.2. Hata Yönetimi — Jenerik Mesajlar

| Durum | Kullanıcıya Gösterilen Mesaj |
|-------|------------------------------|
| Email bulunamadı / Şifre yanlış | "E-posta veya kimlik bilgileri hatalı." |
| Cari/admin pasif | "Hesabınız pasif, lütfen yönetici ile iletişime geçin." |
| Kimlik bilgisi eksik (ERP fallback) | "Kimlik bilgileriniz eksik, lütfen yönetici ile iletişime geçin." |
| Sistem/DB hatası | "Sistem hatası, lütfen daha sonra tekrar deneyin." |
| Rate limit aşımı | "Çok fazla deneme yaptınız, lütfen X dakika sonra tekrar deneyin." |

### 6.3. Denetim Kayıtları (Audit Log)
Tüm giriş denemeleri `web_auth_log` tablosuna kaydedilir:
- `email`, `cariKod`, `role`, `success`, `reason`, `ipAddress`, `userAgent`, `createdAt`

### 6.4. JWT
- **Kütüphane:** `jose` + `jsonwebtoken`
- **Süre:** 24 saat.
- **Cookie:** `auth_token` — `HttpOnly`, `Secure`, `SameSite=Strict`.
- Süre dolduğunda middleware sayfa yüklemelerini `?expired=1` ile login'e yönlendirir.
- `JWTExpired` hatası ayrıca yakalanır ve oturum timeout mesajı tetiklenir.

---

## 7. MIDDLEWARE (ROTA KORUMA)

**Dosya:** `src/proxy.ts`

- `/admin/**` rotaları: `ADMIN` rolü gerektirir.
- `/dashboard/**` rotaları: `CUSTOMER` veya `ADMIN` rolü gerektirir.
- `/api/cari/**`, `/api/stok/**`, `/api/siparis/**` vb. API rotaları korunur.
- `/api/odeme/callback` **PUBLIC** bırakılır (PayTR webhook).
- JWT payload aşağıdaki header'lara enjekte edilir:
  - `x-user-id`, `x-user-role`, `x-user-carikod`, `x-user-cariid`

---

## 8. TEST SENARYOLARI

| Test ID | Senaryo | Beklenen Sonuç |
|---------|---------|----------------|
| TC-AUTH-01 | Admin doğru bilgilerle giriş | 200, JWT cookie |
| TC-AUTH-02 | Admin yanlış şifre | 401, jenerik hata |
| TC-AUTH-03 | Cari (PostgreSQL) doğru bilgilerle giriş | 200, JWT cookie |
| TC-AUTH-04 | Cari (ERP fallback) yanlış son-5-hane | 401, jenerik hata |
| TC-AUTH-05 | Pasif cari girişi | 401, hesap pasif mesajı |
| TC-AUTH-06 | 6. başarısız denemede rate limit | 429, dakika uyarısı |
| TC-AUTH-07 | Zod validasyonu — hatalı email formatı | 400 |
| TC-AUTH-08 | KIMLIK_NO ve VERGI_NUMARASI boş cari | 401, kimlik eksik mesajı |

**Test dosyası:** `src/__tests__/login.route.test.ts`

---

## 9. VERİTABANI REFERANSI

| Tablo | Tür | Açıklama |
|-------|-----|----------|
| `web_login` | PostgreSQL | Portal kullanıcıları — `email`, `passwordHash`, `role`, `isActive` |
| `web_auth_log` | PostgreSQL | Tüm giriş denemeleri |
| `CARI` | SQL Server (Read-only) | ERP müşteri kaydı — `EMAIL`, `KIMLIK_NO`, `VERGI_NUMARASI`, `AKTIF` |
