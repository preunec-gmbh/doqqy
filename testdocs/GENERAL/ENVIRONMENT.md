# Ortam Değişkenleri Kılavuzu (.env)

Bu dosya `.env` / `.env.example` içindeki tüm değişkenleri açıklar. Yeni bir sunucuya veya tenant'a kurulum yaparken bu kılavuzu referans alın.

---

## Zorunlu Değişkenler

### `TENANT_ID`
```
TENANT_ID=erim
```
Aktif tenant kimliği. `src/config/tenants/` klasöründeki dosya adıyla eşleşmelidir.

| Geçerli Değerler | Açıklama |
|-----------------|----------|
| `erim` | Erim Elektronik konfigürasyonu |
| `slay` | Slay konfigürasyonu |
| `template_tenant` | Boş şablon (yeni tenant oluşturulmadan önce) |

**Eksikse:** `template_tenant` konfigürasyonu kullanılır.

---

### `DATABASE_URL`
```
DATABASE_URL="postgresql://user:password@host:port/dbname"
```
PostgreSQL bağlantı URL'i. Prisma ORM bu değişkeni kullanır.

**Format:** `postgresql://[kullanıcı]:[şifre]@[host]:[port]/[veritabanı_adı]`

**Örnekler:**
- Yerel Docker: `postgresql://postgres:postgres@localhost:5432/b2b_dev`
- Hostinger VPS: `postgresql://b2buser:GüçlüŞifre@localhost:5432/b2b_prod`

---

### `SQLSERVER_SERVER`
```
SQLSERVER_SERVER=192.168.1.100
```
SQL Server sunucu adresi (IP veya hostname). Named instance için: `SERVER\INSTANCE`.

---

### `SQLSERVER_PORT`
```
SQLSERVER_PORT=1433
```
SQL Server port numarası. Varsayılan: `1433`.

---

### `SQLSERVER_DATABASE`
```
SQLSERVER_DATABASE=ERIM2025
```
ERP veritabanı adı. **Bu alan boş bırakılamaz** — eksikse uygulama hata fırlatır (fallback yoktur).

---

### `SQLSERVER_USER`
```
SQLSERVER_USER=b2b_readonly
```
SQL Server kullanıcı adı. Bu kullanıcının yalnızca SELECT yetkisi olmalıdır.

---

### `SQLSERVER_PASSWORD`
```
SQLSERVER_PASSWORD=
```
SQL Server kullanıcı şifresi.

---

### `JWT_SECRET`
```
JWT_SECRET=en-az-32-karakter-uzun-rastgele-string
```
JWT token imzalama anahtarı. En az 32 karakter, rastgele üretilmiş olmalıdır.

**Üretmek için:**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

---

### `NODE_ENV`
```
NODE_ENV=production
```
Uygulama ortamı.

| Değer | Açıklama |
|-------|----------|
| `production` | Canlı ortam — güvenlik ayarları tam aktif |
| `development` | Geliştirme — mock fallback'ler devreye girebilir |

---

### `NEXT_PUBLIC_SITE_URL`
```
NEXT_PUBLIC_SITE_URL=https://b2b.erimelektronik.com
```
Sitenin tam URL'i. PayTR callback URL'lerinde, CDN yapılandırmasında ve Next.js Image Optimization'da kullanılır. Sondaki `/` olmamalıdır.

---

## PayTR Değişkenleri (Faz-9 Ödeme Entegrasyonu)

### `PAYTR_MERCHANT_ID`
```
PAYTR_MERCHANT_ID=123456
```
PayTR mağaza kimliği. **PayTR Panel → Destek & Kurulum → Entegrasyon Bilgileri** sayfasından alınır.

### `PAYTR_MERCHANT_KEY`
```
PAYTR_MERCHANT_KEY=abc123xyz
```
PayTR API anahtarı. Gizli tutulmalı, asla frontend'e gönderilmemeli.

### `PAYTR_MERCHANT_SALT`
```
PAYTR_MERCHANT_SALT=salt123
```
Hash hesaplamada kullanılan tuz değeri. Gizli tutulmalı.

### `PAYTR_TEST_MODE`
```
PAYTR_TEST_MODE=1
```
| Değer | Açıklama |
|-------|----------|
| `1` | Sandbox (test) modu — gerçek para çekilmez |
| `0` | Canlı mod — **production'a geçmeden önce mutlaka `0` yapılmalı** |

### `PAYTR_CALLBACK_URL`
```
PAYTR_CALLBACK_URL=https://b2b.erimelektronik.com/api/odeme/callback
```
PayTR'nin ödeme sonucunu POST atacağı endpoint. **PayTR panelindan da aynı URL tanımlanmalıdır.** HTTPS zorunludur.

### `PAYTR_OK_URL`
```
PAYTR_OK_URL=https://b2b.erimelektronik.com/dashboard/sepetim/basarili
```
Başarılı ödeme sonrası müşterinin yönlendirileceği sayfa.

### `PAYTR_FAIL_URL`
```
PAYTR_FAIL_URL=https://b2b.erimelektronik.com/dashboard/sepetim/odeme
```
Başarısız ödeme sonrası müşterinin yönlendirileceği sayfa.

---

## Geliştirme Ortamı Notları

1. `.env.example` dosyasını kopyalayarak `.env` oluşturun: `cp .env.example .env`
2. `SQLSERVER_DATABASE` her zaman doldurulmalıdır — boş bırakılırsa uygulama hata fırlatır.
3. `JWT_SECRET` production'da güçlü bir değer olmalıdır.
4. `PAYTR_TEST_MODE=1` ile başlayın, canlıya geçişte `0` yapın.
5. `.env` dosyasını asla git'e commit etmeyin (`.gitignore`'da yer almalıdır).
