# PostgreSQL Veritabanı Şeması (Prisma)

**ORM:** Prisma 7.4.2 | **Adapter:** @prisma/adapter-pg (PrismaPg) | **Veritabanı:** PostgreSQL 16+

Bu veritabanı yalnızca web portala özgü verileri tutar. ERP ana verileri (stok, cari, sipariş) SQL Server'dan anlık okunur ve buraya yazılmaz.

---

## Enum'lar

### `UserRole` → `user_role`

| Değer | Açıklama |
|-------|----------|
| `ADMIN` | Yönetici — tüm cari ve sipariş verilerini görebilir |
| `CUSTOMER` | Müşteri (Cari) — yalnızca kendi verilerini görür |

---

## Modeller

### `WebLogin` → `web_login`

Portal kullanıcıları. Admin veya Cari olabilir.

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | `String` (cuid) | ✓ PK | Uygulama içi ID |
| `cariKod` | `String?` | — | SQL Server CARI.KOD ile eşleşme (sadece CUSTOMER) |
| `email` | `String` | ✓ UNIQUE | Giriş e-postası |
| `passwordHash` | `String?` | — | bcrypt hash; null ise ERP fallback kullanılır |
| `role` | `UserRole` | ✓ default=CUSTOMER | Rol |
| `isActive` | `Boolean` | ✓ default=true | Hesap aktif mi |
| `lastLoginAt` | `DateTime?` | — | Son başarılı giriş zamanı |
| `createdAt` | `DateTime` | ✓ auto | Oluşturma zamanı |
| `updatedAt` | `DateTime` | ✓ auto | Son güncelleme |

---

### `WebAuthLog` → `web_auth_log`

Tüm giriş denemeleri (başarılı + başarısız). Güvenlik denetimi için.

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | `String` (cuid) | ✓ PK | — |
| `email` | `String` | ✓ | Deneme yapılan e-posta |
| `cariKod` | `String?` | — | Cari kodu (başarılı ise dolar) |
| `role` | `UserRole?` | — | Hangi rol için denendi |
| `success` | `Boolean` | ✓ | Giriş başarılı mı |
| `reason` | `String?` | — | Başarısız ise neden |
| `ipAddress` | `String?` | — | İstemci IP |
| `userAgent` | `String?` | — | Tarayıcı/istemci bilgisi |
| `createdAt` | `DateTime` | ✓ auto | Deneme zamanı |

---

### `WebCart` → `web_cart`

Sepet başlık tablosu. Her aktif kullanıcının en fazla 1 `ACTIVE` sepeti olabilir.

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | `String` (UUID) | ✓ PK | — |
| `userId` | `String` | ✓ | `web_login.id` referansı |
| `cariKod` | `String?` | — | SQL Server CARI.KOD (opsiyonel) |
| `status` | `String` | ✓ default="ACTIVE" | `ACTIVE` \| `CONVERTED` \| `ABANDONED` |
| `createdAt` | `DateTime` | ✓ auto | — |
| `updatedAt` | `DateTime` | ✓ auto | — |

**İlişki:** `items → WebCartItem[]`

---

### `WebCartItem` → `web_cart_item`

Sepet ürün satırları. Fiyatlar sepete ekleme anında anlık sabitlenir.

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | `String` (UUID) | ✓ PK | — |
| `cartId` | `String` (UUID) | ✓ FK | `web_cart.id` |
| `stokId` | `BigInt` | ✓ | SQL Server STOK.ID |
| `stokKod` | `String` | ✓ | STOK.KOD |
| `stokAd` | `String` | ✓ | Ürün adı (anlık snapshot) |
| `miktar` | `Decimal(18,3)` | ✓ | Sipariş miktarı |
| `birimId` | `BigInt` | ✓ | STOK_BIRIM.ID |
| `birimAd` | `String` | ✓ | Birim adı (örn: Adet) |
| `birimCarpan` | `Decimal(18,8)` | ✓ | Birim çarpanı |
| `kdvHaricFiyat` | `Decimal(18,2)` | ✓ default=0 | Eklenme anındaki KDV hariç birim fiyat |
| `kdvDahilFiyat` | `Decimal(18,2)` | ✓ default=0 | Eklenme anındaki KDV dahil birim fiyat |
| `kdvOrani` | `Decimal(18,2)` | ✓ default=20 | KDV oranı (%) |
| `kdvTutari` | `Decimal(18,2)` | ✓ default=0 | KDV tutarı |
| `createdAt` | `DateTime` | ✓ auto | — |
| `updatedAt` | `DateTime` | ✓ auto | — |

**İlişki:** `cart → WebCart` (cascade ile silinir)

---

### `WebImage` → `web_images`

Admin'in yüklediği ürün görselleri. `stockNo` → SQL Server STOK.KOD ile uygulama düzeyinde eşleşir (DB FK yok).

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | `Int` (autoincrement) | ✓ PK | — |
| `stockNo` | `String(150)` | ✓ | STOK.KOD ile eşleşen ürün kodu |
| `imageName` | `String(500)` | ✓ | Dosya adı / CDN path |
| `resimAciklamasi` | `String(255)?` | — | Opsiyonel açıklama |
| `sira` | `Int` | ✓ default=0 | 0 = varsayılan/önizleme görseli |
| `createdAt` | `DateTime` | ✓ auto | — |
| `updatedAt` | `DateTime` | ✓ auto | — |

**Kısıtlar:** `UNIQUE(stockNo, imageName)` | **İndeksler:** `stockNo`, `(stockNo, sira)`

---

### `WebPayment` → `web_payment`

Ödeme kayıtları. PayTR iFrame entegrasyonu için.

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | `Int` (autoincrement) | ✓ PK | — |
| `merchantOid` | `String(64)` | ✓ UNIQUE | PayTR sipariş no (`WEB{YYYY}{NNNNN}` veya `COD{...}`) |
| `paytrRefNo` | `String(100)?` | — | PayTR'nin döndürdüğü referans no |
| `userId` | `String(50)` | ✓ | `web_login.id` |
| `cariId` | `Int` | ✓ | SQL Server CARI.ID |
| `siparisId` | `Int?` | — | ERP SIPARIS.ID (başarılı callback sonrası dolar) |
| `odemeTutari` | `Decimal(18,2)` | ✓ | Gönderilen tutar |
| `tahsilTutari` | `Decimal(18,2)?` | — | PayTR'den gelen gerçekleşen tutar |
| `paraBirimi` | `String(10)` | ✓ default="TL" | — |
| `adresId` | `Int?` | — | CARI_ADRES.ID |
| `aciklama` | `String(500)?` | — | — |
| `durum` | `String(20)` | ✓ default="pending" | `pending` \| `success` \| `failed` \| `success_no_order` |
| `islemTipi` | `String(20)` | ✓ default="SEPET" | `SEPET` (sepetli) \| `CARI_ODEME` (siparişsiz borç ödeme) |
| `cariAd` | `String(250)?` | — | Cari adı snapshot |
| `odemeYontemi` | `String(20)?` | — | `card` \| `eft` |
| `hataKodu` | `String(10)?` | — | PayTR hata kodu |
| `hataMesaji` | `String(500)?` | — | Hata açıklaması |
| `tamamlanmaZamani` | `DateTime?` | — | Callback başarıyla işlendiği zaman |
| `createdAt` | `DateTime` | ✓ auto | — |
| `updatedAt` | `DateTime` | ✓ auto | — |

**İndeksler:** `cariId`, `merchantOid`, `durum`, `islemTipi`

---

## İlişki Özeti

```
WebCart ──< WebCartItem   (one-to-many, FK: cartId)
```

`WebLogin`, `WebAuthLog`, `WebImage`, `WebPayment` bağımsız tablolar — SQL Server kayıtlarıyla uygulama düzeyinde ilişkilendirilir, DB-level FK yoktur.

---

## Notlar

- Tüm PostgreSQL tabloları `web_` önekiyle başlar; SQL Server tablolarından ayırt etmek içindir.
- `WebCartItem` fiyat alanları ekleme anında sabitlenir; fiyat güncellemesi için `/api/odeme/fiyat-kontrol` endpoint'i kullanılır.
- `WebPayment.durum = "success_no_order"` → Ödeme başarılı ama sipariş oluşturma başarısız oldu; manuel müdahale gerekir.
- Prisma adapter olarak `@prisma/adapter-pg` (PrismaPg) kullanılır; `DATABASE_URL` env değişkeninden bağlantı alır.
