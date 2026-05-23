# Sequence Diyagramları

**Versiyon:** 1.0.0 | **Son Güncelleme:** 2026-05-20

---

## 1. Login Akışı (Cari — Hibrit Kimlik Doğrulama)

```mermaid
sequenceDiagram
    actor Müşteri
    participant Browser
    participant proxy.ts as Next.js Middleware (proxy.ts)
    participant LoginAPI as POST /api/auth/login
    participant PostgreSQL
    participant SQLServer as SQL Server (ERP)

    Müşteri->>Browser: Kullanıcı adı + şifre girer
    Browser->>LoginAPI: POST /api/auth/login {username, password}

    LoginAPI->>LoginAPI: Rate limit kontrolü (IP, 5/15dk)
    alt Limit aşıldı
        LoginAPI-->>Browser: 429 Too Many Requests
    end

    LoginAPI->>PostgreSQL: web_login WHERE username = ?
    alt Kayıt bulunamadı
        LoginAPI-->>Browser: 401 Unauthorized
    end

    PostgreSQL-->>LoginAPI: {hashedPassword, role, cariId, isActive}

    alt Kayıt var ama aktif değil
        LoginAPI-->>Browser: 403 Hesap pasif
    end

    LoginAPI->>LoginAPI: bcrypt.compare(password, hashedPassword)

    alt bcrypt başarısız — ADMIN kullanıcısı ise
        LoginAPI-->>Browser: 401 Unauthorized
    else bcrypt başarısız — CUSTOMER + ilk giriş olabilir
        LoginAPI->>SQLServer: ERP fallback (LAST_5_DIGITS veya STATIC)
        SQLServer-->>LoginAPI: Eşleşme sonucu
        alt ERP fallback başarılı
            LoginAPI->>PostgreSQL: Yeni bcrypt hash kaydet
        else ERP fallback başarısız
            LoginAPI-->>Browser: 401 Unauthorized
        end
    end

    LoginAPI->>LoginAPI: JWT üret (cariId, role, 24h)
    LoginAPI->>PostgreSQL: web_auth_log kaydı ekle
    LoginAPI-->>Browser: Set-Cookie: token=JWT (HttpOnly, Secure)
    Browser->>Browser: Rol bazlı yönlendirme
    note over Browser: ADMIN → /admin/dashboard\nCUSTOMER → /dashboard
```

---

## 2. Sepet → Sipariş Oluşturma Akışı (Havale/EFT veya Kapıda Ödeme)

```mermaid
sequenceDiagram
    actor Müşteri
    participant Browser
    participant SepetAPI as Sepet API
    participant OdemeAPI as POST /api/sepetim/siparis-olustur
    participant PostgreSQL
    participant SQLServer as SQL Server (ERP)

    Müşteri->>Browser: Ürün detayına gider, sepete ekle
    Browser->>SepetAPI: POST /api/sepetim/ekle {stokId, miktar, birimId}
    SepetAPI->>SQLServer: Stok miktarı kontrol (AS_STOK_MIKTAR_GENEL)
    SepetAPI->>SQLServer: Fiyat çek (STOK.SON_ALIS_FIYAT × CARPAN)
    SepetAPI->>PostgreSQL: web_cart_item kaydet (kdvHaricFiyat, kdvDahilFiyat sabitlenir)
    SepetAPI-->>Browser: Sepet güncellendi

    Müşteri->>Browser: Sepetim → Adres seçimi
    Browser->>SepetAPI: GET /api/sepetim/adresler
    SepetAPI->>SQLServer: CARI_ADRES sorgula
    SepetAPI-->>Browser: Adres listesi

    Müşteri->>Browser: Ödeme yöntemi seç (Havale/EFT veya Kapıda)
    Browser->>SepetAPI: POST /api/sepetim/limit-kontrol
    SepetAPI->>SQLServer: CARI_BAKIYELER.BAKIYE + sepetToplam ≤ CARI.RISK
    alt Limit aşımı
        SepetAPI-->>Browser: Uyarı göster
        Browser->>Müşteri: Limit aşımı uyarısı
    end

    Müşteri->>Browser: "Sipariş Ver" butonuna tıkla
    Browser->>OdemeAPI: POST /api/sepetim/siparis-olustur {adresId, odemeYontemiId}

    OdemeAPI->>SQLServer: Stok tekrar kontrol
    OdemeAPI->>SQLServer: Fiyat tekrar çek
    OdemeAPI->>SQLServer: Barkod çek (STOK_BARKOD)
    OdemeAPI->>PostgreSQL: Sipariş no üret (SPRS-YYYY-NNNNN)

    OdemeAPI->>SQLServer: EXEC Ekle_Siparis (@LOKASYON, @PROJE, @CARI_ADR, ...)
    SQLServer-->>OdemeAPI: BELGENO (ERP sipariş no)

    loop Her sepet kalemi için
        OdemeAPI->>SQLServer: EXEC Ekle_Siparis_Detay (...)
    end

    OdemeAPI->>SQLServer: SIPARIS_OZEL_KOD_1 = odemeYontemiId güncelle
    OdemeAPI->>PostgreSQL: web_cart.status = CONVERTED
    OdemeAPI-->>Browser: {siparisNo: "SPRS-2026-00001"}
    Browser->>Müşteri: Başarı sayfası /dashboard/sepetim/basarili
```

---

## 3. PayTR Kredi Kartı Ödeme Callback Akışı

```mermaid
sequenceDiagram
    actor Müşteri
    participant Browser
    participant BasaltAPI as POST /api/odeme/basalt
    participant PayTR
    participant CallbackAPI as POST /api/odeme/callback
    participant PostgreSQL
    participant SQLServer as SQL Server (ERP)

    Müşteri->>Browser: Ödeme sayfasında "Kredi Kartıyla Öde" tıkla
    Browser->>BasaltAPI: POST /api/odeme/basalt {hedefCariId?}

    BasaltAPI->>PostgreSQL: Aktif sepet + kalemleri çek
    BasaltAPI->>SQLServer: Stok + fiyat doğrula
    BasaltAPI->>BasaltAPI: buildUserBasket() — KDV dahil fiyatlar
    BasaltAPI->>BasaltAPI: generateMerchantOid() → WEB2026NNNNN
    BasaltAPI->>BasaltAPI: generatePaytrToken() — HMAC-SHA256

    BasaltAPI->>PayTR: POST token isteği (20s timeout)
    PayTR-->>BasaltAPI: {token: "iframeToken"}

    BasaltAPI->>PostgreSQL: web_payment kaydet (status=pending, merchantOid)
    BasaltAPI-->>Browser: {iframeToken, merchantOid}

    Browser->>Browser: PayTR iFrame göster
    Müşteri->>PayTR: Kart bilgisi girer (doğrudan PayTR'ye)
    PayTR->>PayTR: Ödeme işlemi

    alt Ödeme başarılı
        PayTR->>CallbackAPI: POST /api/odeme/callback {merchantOid, status=success, ...}
    else Ödeme başarısız
        PayTR->>CallbackAPI: POST /api/odeme/callback {merchantOid, status=failed, ...}
    end

    CallbackAPI->>CallbackAPI: verifyCallbackHash() — timing-safe HMAC-SHA256
    alt Hash uyuşmazlığı
        CallbackAPI-->>PayTR: Hata (loglanır, reddedilir)
    end

    CallbackAPI->>PostgreSQL: Idempotency kontrolü — aynı merchantOid işlendi mi?
    alt Zaten işlendi
        CallbackAPI-->>PayTR: "OK" (tekrar işleme)
    end

    alt WEB prefix + ödeme başarılı
        CallbackAPI->>SQLServer: EXEC Ekle_Siparis (...)
        loop Her kalem
            CallbackAPI->>SQLServer: EXEC Ekle_Siparis_Detay (...)
        end
        CallbackAPI->>PostgreSQL: web_cart.status = CONVERTED
        CallbackAPI->>PostgreSQL: web_payment.durum = success, siparisId güncelle
    else WEB prefix + sipariş oluşturma hatası
        CallbackAPI->>PostgreSQL: web_payment.durum = success_no_order
    else WEB prefix + ödeme başarısız
        CallbackAPI->>PostgreSQL: web_payment.durum = failed
    else COD prefix (cari ödeme) + başarılı
        CallbackAPI->>PostgreSQL: web_payment.durum = success (sipariş oluşturulmaz)
    end

    CallbackAPI-->>PayTR: "OK"

    Browser->>BasaltAPI: Ödeme durumu polling (PayTR OK/FAIL URL tetikler)
    Browser->>Müşteri: Başarı → /dashboard/sepetim/basarili?oid=WEB2026NNNNN
```
