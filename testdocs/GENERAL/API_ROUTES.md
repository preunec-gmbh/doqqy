# API Endpoint Referansı

**Versiyon:** 1.0.0 | **Son Güncelleme:** 2026-05-20

Tüm endpoint'ler `/api/` önekiyle başlar. Auth kolonu: `Public` = auth gerekmez, `Login` = JWT token gerekir, `Admin` = ADMIN rolü zorunludur.

---

## Kimlik Doğrulama

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| POST | `/api/auth/login` | Public | Giriş (rate limit: 5/15dk IP bazlı) |
| DELETE | `/api/auth/logout` | Login | Çıkış — auth cookie temizlenir |

---

## Admin

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/admin/dashboard/ozet` | Admin | Dashboard özeti: aktif müşteri sayısı, bekleyen sipariş, son auth logları |
| GET | `/api/admin/kullanicilar` | Admin | Tüm web kullanıcılarını listele (`web_login`) |
| POST | `/api/admin/kullanicilar` | Admin | Yeni kullanıcı oluştur (ADMIN veya CUSTOMER) |
| PATCH | `/api/admin/kullanicilar/[id]` | Admin | Kullanıcı güncelle: email, şifre, aktif/pasif, rol |
| DELETE | `/api/admin/kullanicilar/[id]` | Admin | Kullanıcı sil (kendini silemez) |
| GET | `/api/admin/ayarlar/doviz-kur` | Admin | Güncel döviz kurlarını getir (`DOVIZ_KUR` tablosu) |

---

## Cari (Müşteri Yönetimi)

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/cari` | Admin | Tüm carileri listele — arama, sayfalama (SQL Server) |
| GET | `/api/cari/me` | Login | Giriş yapan müşterinin kendi profili |
| GET | `/api/cari/[kod]` | Login | Cari detayı — admin tümünü görür, müşteri yalnızca kendisini |
| PATCH | `/api/cari/[kod]/status` | Admin | Web erişimini aktif/pasif yap |
| POST | `/api/cari/[kod]/password` | Admin | Cari şifresi sıfırla |
| GET | `/api/musteri/firma-adi` | Login | Giriş yapan müşterinin `CARI.AD` alanı |
| GET | `/api/musteri/arama` | Admin | Admin ödeme formu için müşteri arama |
| GET | `/api/musteri/dashboard/ozet` | Login | Müşteri dashboard özeti: bakiye, limit, son sipariş |

---

## Stok (Ürün Kataloğu)

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/stok` | Login | Ürün listesi — arama, kategori, stok durumu filtresi, sayfalama |
| GET | `/api/stok/[kod]` | Login | Ürün detayı — birimler, toplam stok, kritik eşik |
| GET | `/api/stok/kategoriler` | Login | Kategori hiyerarşisi (CTE ile maks 3 seviye) |
| GET | `/api/stok/kur` | Login | Güncel döviz kurları (10 dakika önbellek) |
| GET | `/api/stok/[kod]/resimler` | Public | Ürün görselleri listesi |
| POST | `/api/stok/[kod]/resimler` | Admin | Ürün görseli yükle |
| PATCH | `/api/stok/[kod]/resimler/[id]` | Admin | Görsel sıra/açıklama güncelle |
| DELETE | `/api/stok/[kod]/resimler/[id]` | Admin | Görsel sil |

---

## Finansal Hareketler

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/hareketler` | Login | Hareket listesi — tarih/tür filtresi; admin tümünü, müşteri kendisini görür |
| GET | `/api/hareketler/[id]` | Login | Hareket detayı (fatura kalemleri dahil) |
| GET | `/api/hareketler/bakiye` | Login | Müşterinin TRY bakiyesi (`CARI_BAKIYELER`) |
| GET | `/api/hareketler/export/excel` | Admin | Hareketleri Excel olarak dışa aktar |
| GET | `/api/hareketler/export/pdf` | Admin | Hareketleri PDF olarak dışa aktar |

---

## Sepet

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/sepetim` | Login | Aktif sepet içeriği + tahmini fiyatlar |
| GET | `/api/sepetim/count` | Login | Sepet ürün sayısı (badge için — hafif) |
| POST | `/api/sepetim/ekle` | Login | Sepete ürün ekle (fiyat sepete sabitlenir) |
| PUT | `/api/sepetim/guncelle` | Login | Sepet kalemi miktar/birim güncelle |
| DELETE | `/api/sepetim/sil` | Login | Sepetten ürün sil |
| DELETE | `/api/sepetim/bosalt` | Login | Tüm sepeti boşalt |
| GET | `/api/sepetim/adresler` | Login | Teslimat adresleri — admin `?cariId` ile filtreleyebilir |
| GET | `/api/sepetim/odeme-yontemleri` | Login | Kullanılabilir ödeme yöntemleri |
| POST | `/api/sepetim/limit-kontrol` | Login | Kredi limiti kontrolü (bakiye + sepet toplamı ≤ risk limiti) |
| POST | `/api/sepetim/stok-kontrol` | Login | Checkout öncesi gerçek zamanlı stok doğrulama |
| POST | `/api/sepetim/siparis-olustur` | Login | ERP'ye sipariş yaz (havale/kapıda ödeme); admin `hedefCariId` kullanabilir |

---

## Siparişler

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/siparis` | Login | Sipariş listesi — tarih/durum filtresi; admin tümünü görür |
| GET | `/api/siparis/[id]` | Login | Sipariş detayı — admin tümünü, müşteri yalnızca kendisini görür |
| GET | `/api/siparis/[id]/odeme` | Admin | Siparişe bağlı ödeme kaydı (`web_payment`) |

---

## Ödeme (PayTR)

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| POST | `/api/odeme/basalt` | Login | Sepet ödemesi için PayTR iFrame token al |
| POST | `/api/odeme/cari-basalt` | Login | Sipariş olmadan cari borç ödemesi için PayTR token al (`enableDirectDebtPayment`) |
| POST | `/api/odeme/callback` | **Public** | PayTR webhook — HMAC-SHA256 doğrulama, idempotent |
| GET | `/api/odeme/sonuc` | Public | PayTR iFrame içindeki yönlendirme sayfası |
| GET | `/api/odeme/durum` | Login | Callback sonrası ödeme durumu ve sipariş numarası sorgula |
| POST | `/api/odeme/fiyat-kontrol` | Login | Ödeme başlatmadan önce sepet fiyatlarının geçerliliğini kontrol et |
| GET | `/api/odeme/cari-gecmis` | Login | Müşteri ödeme geçmişi (sipariş olmaksızın) |
| GET | `/api/odeme/durum-ozet` | Admin | Admin dashboard için bekleyen ödeme özeti |

---

## Dosya Yükleme ve Genel

| Method | Path | Auth | Açıklama |
|--------|------|------|----------|
| GET | `/api/uploads/[...path]` | Public | Yüklenen dosyaları sun (WebP görseller, cache header'lı) |
| GET | `/api/firma-info` | Public | Şirket iletişim bilgileri (ad, adres, tel, email, web, IBAN) |
| GET | `/api/health` | Public | SQL Server ve PostgreSQL bağlantı testi |

---

## Özet

| Auth Seviyesi | Endpoint Sayısı |
|---------------|----------------|
| Public | 6 |
| Login (tüm roller) | 32 |
| Admin only | 14 |
| **Toplam** | **52** |

---

## Notlar

- **Admin olarak müşteri adına işlem:** `hedefCariId` query/body parametresi kabul eden endpoint'ler admin için müşteri adına çalışır (`/api/sepetim/*`, `/api/odeme/basalt`, vb.)
- **`/api/odeme/callback`:** PayTR sunucusundan gelen POST isteklerini karşılar. Auth middleware dışındadır; güvenlik HMAC-SHA256 hash doğrulaması ile sağlanır.
- **Hareketler export:** Yalnızca admin endpoint'i; müşteri kendi hareketlerini UI üzerinden görebilir ancak doğrudan export yapamaz.
