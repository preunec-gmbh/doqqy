# STOK YÖNETİMİ GEREKSİNİMLERİ (SİSTEM DURUMU)

**Versiyon:** 1.1 | **Son Güncelleme:** 2026-05-20 | **Durum:** Güncel Sistem Yapısı

---

## 1. GENEL BAKIŞ

Stok (ürün) yönetim modülü. SQL Server'daki stok verileri salt okunur; görseller PostgreSQL'deki `web_images` tablosunda tutulur ve CDN URL'leri üzerinden sunulur.

**ERP Yazma:** Stok verisine yazma yoktur. Sipariş oluşturma için stored procedure'ler kullanılır.

---

## 2. ÜRÜN LİSTELEME

**Dosya:** `src/features/stok/services/stokService.ts` → `getStokList()`  
**Route:** `GET /api/stok`

### Kart Başına Gösterilen Bilgiler

| Alan | Kaynak | Açıklama |
|------|--------|----------|
| Görsel | `web_images` → CDN URL | `sira = 0` önizleme; yoksa placeholder |
| KOD | `STOK.KOD` | — |
| AD | `STOK.AD` | — |
| KATEGORİ | `STOK_GRUP.AD` | — |
| FİYAT | `STOK.SON_ALIS_FIYAT × birimCarpan` | KDV hariç, varsayılan birim |
| BİRİM | `STOK_STOK_BIRIM.AD` (VARSAYILAN=1) | — |
| STOK DURUMU | `AS_STOK_MIKTAR_GENEL` SUM | `VAR` / `KRITIK` / `YOK` badge |

**Müşteri:** Fiyat detayı (maliyet, kâr marjı) gizlenir; yalnızca KDV hariç nihai fiyat gösterilir.  
**Admin:** Tüm fiyat detayları görünür.

### Stok Durumu Hesaplaması

```
toplamMiktar = SUM(AS_STOK_MIKTAR_GENEL.MIKTAR) WHERE LOKASYON IN tenantConfig.stock.locationId
kritikEsik   = STOK_SEVIYE.MIN (yoksa tenantConfig.stock.defaultCriticalLevel)

Durum:
  toplamMiktar <= 0           → YOK (kırmızı)
  toplamMiktar <= kritikEsik  → KRITIK (sarı)
  toplamMiktar > kritikEsik   → VAR (yeşil)
```

### Arama ve Filtreleme

- **Arama:** `STOK.AD` — `LIKE` ile kısmi eşleşme, tenant collation kullanılır
- **Kategori:** `STOK_GRUP` hiyerarşisi (CTE ile max 3 seviye) — alt kategoriler dahil
- **Stok durumu filtresi:** `VAR` / `KRITIK` / `YOK` — müşteri yalnızca `VAR` ve `KRITIK` görebilir
- **Aktif filtre:** Müşteri daima `AKTIF=1`; admin tüm ürünleri görebilir

### Sayfalama ve Performans

- Sayfa başına 25 kayıt
- Liste sayfasında tam stok miktarı hesaplanmaz; `EXISTS` subquery ile `stokVar` (boolean) döner
- Görseller batch olarak PostgreSQL'den (`web_images`) çekilir — N+1 önlemi

---

## 3. ÜRÜN DETAY SAYFASI

**Route:** `GET /api/stok/[kod]`

### Bölüm 1: Temel Bilgiler

`KOD`, `AD`, kategori hiyerarşik yolu, opsiyonel görsel galerisi.

### Bölüm 2: Fiyat ve Birim Seçimi

- **Birim Seçici (Dropdown):** `STOK_STOK_BIRIM` tablosundan ürüne ait tüm birimler
- Birim değiştiğinde fiyat ve stok miktarı otomatik yenilenir:
  ```
  Fiyat = SON_ALIS_FIYAT × CARPAN   (KDV hariç)
  ```
- **Döviz Fiyat (Faz-11):** Eğer `STOK.SON_DOVIZ` ≠ `tenantConfig.locale.baseCurrencyId` ise döviz kuru çekilip TRY'ye çevrilir
- **KDV:** ERP'den dinamik çekilir; gelmezse `tenantConfig.tax.defaultVatRate` kullanılır

### Bölüm 3: Stok Bilgisi

- `toplamMiktar` ve stok durumu badge
- Kritik eşik gösterimi

### Bölüm 4: Sepete Ekleme (Müşteri ve Admin)

- Miktar input, birim seçici, toplam fiyat önizlemesi
- `KRITIK` veya `YOK` stokta "Sepete Ekle" butonu pasif

---

## 4. GÖRSEL YÖNETİMİ

**Dosya:** `src/features/stok/services/stokService.ts`  
**Model:** `web_images` (PostgreSQL)

### Görsel Servisi

1. **PostgreSQL'de kayıt var:** `imageName` CDN URL'i olarak `next/image` ile render edilir
2. **PostgreSQL'de kayıt yok:** `next.config.ts`'de tanımlı harici CDN URL'lerine fallback (`erimelektronik.com` vb.)
3. **Hiç görsel yok:** Placeholder görüntü

### Admin Görsel Yönetimi

- **Bileşen:** `src/features/stok/components/ResimYonetimi.tsx`
- Admin ürün detay sayfasında görsel yükleyebilir, silebilir, sırayı düzenleyebilir
- `sira = 0` olan görsel önizleme/varsayılan görseli olarak kullanılır
- **Route:** `POST /api/uploads`, `GET /api/stok/resimler`

---

## 5. SEPETE EKLEME AKIŞI

**Bileşen:** `src/features/stok/components/SepeteEkleModal.tsx`

1. "Sepete Ekle" butonuna tıklanır → modal/popup açılır
2. Miktar input + birim dropdown
3. Stok kontrolü: `tenantConfig.stock.locationId` üzerinden anlık `AS_STOK_MIKTAR_GENEL` sorgusu
4. Fiyat önizlemesi anlık güncellenir
5. Onaylanırsa `POST /api/sepetim/ekle` çağrılır

**Kural:** Stok miktarı ≤ 0 veya ≤ kritikEsik ise buton pasif — müşteri ekleyemez.

---

## 6. ERİŞİM KONTROLÜ

| Rol | Görüntüleyebileceği Ürünler | Fiyat Detayı |
|-----|-----------------------------|--------------|
| `ADMIN` | Tüm ürünler (AKTIF + pasif) | Tam (maliyet, kâr) |
| `CUSTOMER` | Sadece AKTIF=1, STOK > 0 veya KRITIK | Yalnızca son fiyat |
| Giriş yapmamış | Hiçbiri (login'e yönlendirilir) | — |

---

## 7. HATA YÖNETİMİ

| Durum | Kullanıcı Mesajı |
|-------|-----------------|
| ERP bağlantı hatası | "Sistem hatası, lütfen tekrar deneyin" |
| Stok bilgisi yüklenemedi | "Stok bilgisi alınamadı" |
| Görsel yüklenemedi | Placeholder gösterilir |
| Yetkisiz erişim | 403 Forbidden |

---

## 8. VERİTABANI TABLO REFERANSI

### ERP (Read-Only)

| Tablo | Kritik Alanlar |
|-------|----------------|
| `STOK` | `ID`, `KOD`, `AD`, `STOK_GRUP`, `SON_ALIS_FIYAT`, `AKTIF`, `SON_DOVIZ` |
| `STOK_GRUP` | `ID`, `USTID`, `AD`, `AKTIF` |
| `STOK_STOK_BIRIM` | `ID`, `STOK`, `STOK_BIRIM`, `CARPAN`, `VARSAYILAN` |
| `STOK_BIRIM` | `ID`, `AD` |
| `AS_STOK_MIKTAR_GENEL` | `STOK`, `LOKASYON`, `MIKTAR` |
| `STOK_SEVIYE` | `STOK`, `LOKASYON`, `MIN`, `MAX` |
| `STOK_BARKOD` | `STOK`, `BARKOD` (sipariş oluştururken kullanılır) |

### PostgreSQL

| Tablo | Kritik Alanlar |
|-------|----------------|
| `web_images` | `id`, `stockNo`, `imageName`, `sira` |

---

## 9. NOTLAR

- **Kâr marjı hesabı:** `tenantConfig.stock.marginField` alanından okunur (Erim: `STOK_OZEL_KOD_1`). Müşteriye gösterilmez.
- **Depo filtresi:** `tenantConfig.stock.locationId` — tek ID, çoklu ID listesi veya `"all"`.
- **Kritik stok eşiği:** `STOK_SEVIYE.MIN` önceliklidir; yoksa `tenantConfig.stock.defaultCriticalLevel`.
- **Varsayılan birim:** `STOK_STOK_BIRIM.VARSAYILAN = 1` olan birim; yoksa `tenantConfig.stock.defaultUnit`.
