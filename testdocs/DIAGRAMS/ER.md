# Entity-Relationship Diyagramı

Bu diyagram yalnızca **PostgreSQL (web_*)** tablolarını gösterir. SQL Server (ERP) tabloları dışsal kaynak olup bu diyagramda yer almaz; bağlantılar uygulama düzeyinde sağlanır.

---

## Mermaid ER Diyagramı

```mermaid
erDiagram
    WebLogin {
        string id PK "cuid"
        string cariKod "nullable - CARI.KOD ile eşleşir"
        string email UK
        string passwordHash "nullable - bcrypt"
        UserRole role "ADMIN | CUSTOMER"
        boolean isActive
        datetime lastLoginAt "nullable"
        datetime createdAt
        datetime updatedAt
    }

    WebAuthLog {
        string id PK "cuid"
        string email
        string cariKod "nullable"
        UserRole role "nullable"
        boolean success
        string reason "nullable"
        string ipAddress "nullable"
        string userAgent "nullable"
        datetime createdAt
    }

    WebCart {
        string id PK "uuid"
        string userId "web_login.id (app-level)"
        string cariKod "nullable"
        string status "ACTIVE|CONVERTED|ABANDONED"
        datetime createdAt
        datetime updatedAt
    }

    WebCartItem {
        string id PK "uuid"
        string cartId FK
        bigint stokId "STOK.ID (app-level)"
        string stokKod
        string stokAd
        decimal miktar "18,3"
        bigint birimId "STOK_BIRIM.ID (app-level)"
        string birimAd
        decimal birimCarpan "18,8"
        decimal kdvHaricFiyat "18,2 - sabitlenir"
        decimal kdvDahilFiyat "18,2 - sabitlenir"
        decimal kdvOrani "18,2"
        decimal kdvTutari "18,2"
        datetime createdAt
        datetime updatedAt
    }

    WebImage {
        int id PK "autoincrement"
        string stockNo "STOK.KOD ile eşleşir"
        string imageName
        string resimAciklamasi "nullable"
        int sira "0=varsayılan"
        datetime createdAt
        datetime updatedAt
    }

    WebPayment {
        int id PK "autoincrement"
        string merchantOid UK "WEB/COD prefix"
        string paytrRefNo "nullable"
        string userId "web_login.id (app-level)"
        int cariId "CARI.ID (app-level)"
        int siparisId "nullable - SIPARIS.ID"
        decimal odemeTutari "18,2"
        decimal tahsilTutari "nullable 18,2"
        string paraBirimi "TL"
        int adresId "nullable"
        string aciklama "nullable"
        string durum "pending|success|failed|success_no_order"
        string islemTipi "SEPET|CARI_ODEME"
        string cariAd "nullable"
        string odemeYontemi "nullable card|eft"
        string hataKodu "nullable"
        string hataMesaji "nullable"
        datetime tamamlanmaZamani "nullable"
        datetime createdAt
        datetime updatedAt
    }

    WebCart ||--o{ WebCartItem : "items"
```

---

## SQL Server (ERP) Tabloları — Referans

Aşağıdaki tablolar SQL Server'da bulunur ve PostgreSQL'e yazılmaz. Uygulama bu tablolardan sadece okur; sipariş oluştururken stored procedure'ler aracılığıyla yazar.

| Tablo | Açıklama | Erişim |
|-------|----------|--------|
| `CARI` | Müşteri kayıtları | Read-only |
| `CARI_BAKIYELER` | Müşteri bakiyeleri (multi-currency) | Read-only |
| `CARI_ADRES` | Müşteri adresleri | Read-only |
| `STOK` | Ürün master | Read-only |
| `STOK_GRUP` | Ürün kategorileri (hiyerarşik) | Read-only |
| `STOK_STOK_BIRIM` | Ürün-birim ilişkisi | Read-only |
| `STOK_BIRIM` | Birim tanımları | Read-only |
| `AS_STOK_MIKTAR_GENEL` | Stok miktarları | Read-only |
| `SIPARIS` | Sipariş başlık | Read via proc |
| `SIPARIS_DETAY` | Sipariş kalemleri | Read via proc |
| `FIS` | Fatura başlık | Read-only |
| `FIS_DETAY` | Fatura kalemleri | Read-only |
| `FINANS` | Finansal hareketler | Read-only |
| `KART_ADLARI` | Muhasebe kart isimleri | Read-only |

---

## Uygulama Düzeyinde Bağlantılar

PostgreSQL ↔ SQL Server bağlantıları DB-level FK olmadan uygulama kodu ile sağlanır:

```
WebLogin.cariKod  ──► CARI.KOD
WebCart.userId    ──► WebLogin.id
WebCartItem.stokId ──► STOK.ID
WebCartItem.birimId ──► STOK_BIRIM.ID
WebPayment.userId ──► WebLogin.id
WebPayment.cariId ──► CARI.ID
WebPayment.siparisId ──► SIPARIS.ID (callback sonrası)
WebImage.stockNo  ──► STOK.KOD
```
