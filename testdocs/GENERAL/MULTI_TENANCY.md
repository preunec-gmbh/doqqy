# Multi-Tenant Konfigürasyon Sistemi

Bu sistem, aynı kod tabanının farklı müşterilere (tenant'lara) özelleştirilebilir şekilde sunulmasını sağlar. Her tenant kendi marka kimliği, veritabanı ayarları, ödeme yöntemleri ve iş kurallarıyla yapılandırılır.

---

## Nasıl Çalışır

```
TENANT_ID (env)
      │
      ▼
src/config/tenant.ts  →  getTenantConfig()
      │
      ├── Server-side: process.env.TENANT_ID → configs[tenantId]
      └── Client-side: window.__TENANT_CONFIG__ (layout.tsx'te enjekte edilir)
```

### Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `src/config/types.ts` | `TenantConfig` arayüzü — tüm alanların şeması |
| `src/config/tenant.ts` | `getTenantConfig()` ve `tenantConfig` proxy nesnesi |
| `src/config/tenants/erim.ts` | Erim Elektronik konfigürasyonu |
| `src/config/tenants/slay.ts` | Slay konfigürasyonu |
| `src/config/tenants/template_tenant.ts` | Yeni tenant için boş şablon |

---

## TenantConfig Arayüzü

### `company` — Şirket Bilgileri

```ts
company: {
  name: string;         // Sidebar ve başlıklarda kullanılır
  logo: string;         // Sidebar logo URL/Path (/logos/erim-logo.png)
  loginImage: string;   // Giriş sayfası görseli
  loginSubtitle: string;// Giriş sayfası alt başlığı
  support: {
    phone: string;      // Destek telefonu
    whatsapp: string;   // WhatsApp linki
  };
}
```

### `metadata` — SEO ve Favicon

```ts
metadata: {
  title: string;        // Tarayıcı sekme başlığı
  description: string;  // Meta description
  icons: {
    icon: string;       // favicon.ico
    svg: string;        // favicon.svg (modern tarayıcılar)
    png96: string;      // 96x96 PNG (Android/PWA)
    apple: string;      // Apple Touch Icon
  };
  manifest: string;     // site.webmanifest yolu
}
```

### `locale` — Bölgesel Ayarlar

```ts
locale: {
  defaultCurrency: string;  // "TRY" — SQL sorgularında ve UI formatlarında
  baseCurrencyId: number;   // 1 — veritabanındaki ana para birimi ID'si
  currencySymbol: string;   // "₺" — UI gösterimi için
}
```

### `theme` — Görsel Tema

```ts
theme: {
  colors: {
    primary: string;         // Ana marka rengi (#2563eb)
    primaryHover: string;    // Hover rengi (#1d4ed8)
    cart?: {
      badge: string;
      button: string;
      buttonHover: string;
      summaryText: string;
    };
  };
  fontFamily: string;        // "var(--font-sans)" veya "'Inter', sans-serif"
  radius: string;            // "0.5rem"
}
```

### `db` — Veritabanı Collation

```ts
db: {
  collations: {
    search: string;   // "Turkish_CI_AI" — arama sorguları için
    strict: string;   // "Latin1_General_CS_AS" — şifre doğrulama için
  }
}
```

### `auth` — Kimlik Doğrulama Stratejisi

```ts
auth: {
  fallbackStrategy: "STATIC" | "LAST_5_DIGITS";
  staticPassword?: string;  // strategy "STATIC" ise zorunlu
}
```

İlk girişte müşterinin şifresi yoksa:
- `LAST_5_DIGITS`: Kimlik/Vergi no son 5 hanesi kullanılır
- `STATIC`: Belirlenen sabit şifre kullanılır (örn: `"12345"`)

### `tax` — Vergi Ayarları

```ts
tax: {
  defaultVatRate: number;  // 20 — ERP'den oran gelmezse fallback KDV (%)
}
```

### `stock` — Stok ve Depo Ayarları

```ts
stock: {
  locationId: number | number[] | "all";
  // number: tek depo (75919)
  // number[]: birden fazla depo, toplamı göster ([75919, 2398996])
  // "all": tüm depoları topla
  // Sipariş oluştururken ilk ID kullanılır.

  projectId: number | number[] | "all";
  // Proje filtresi — sipariş oluştururken ilk ID kullanılır

  defaultCriticalLevel: number;  // Kritik stok eşiği (ürün bazlı yoksa)
  marginField: string;           // "STOK_OZEL_KOD_1" — kâr marjı alanı
  defaultUnit: {
    name: string;      // "Adet"
    id: number;        // 0
    multiplier: number; // 1
  };
}
```

### `orders` — Sipariş Ayarları

```ts
orders: {
  receivedType: number;           // 2 — "Alınan Sipariş" belge türü kodu
  defaultInvoiceTypeName: string; // "Satış Faturası" — fallback fatura türü adı
}
```

### `transactions` — Finansal Hareketler

```ts
transactions: {
  filterTypes: Array<{
    id: number;
    label: string;
    isInvoice?: boolean;  // true ise "Detay" butonu aktif
  }>;
}
```

Örnek (Erim):
```ts
filterTypes: [
  { id: 47, label: "Satış Faturası", isInvoice: true },
  { id: 48, label: "Satıştan İade Faturası", isInvoice: true },
  { id: 1, label: "Nakit Tahsilat" },
  // ...
]
```

### `paymentMethods` — Ödeme Yöntemleri

```ts
paymentMethods: {
  eftHavaleId: number;    // 30 — ERP'deki havale ödeme tipi ID'si
  krediKartiId: number;   // 48 — kredi kartı ödeme tipi ID'si
  kapidaOdemeId: number;  // 10 — kapıda ödeme tipi ID'si
  digerId: number;        // 97
  bankInfo: {
    bankName: string;
    iban: string;
    accountHolder: string;
    accountType: string;
  };
  paytr: {
    fallbackPhone: string;    // PayTR telefon fallback'i
    addressSepet: string;     // Sepetli sipariş açıklaması
    addressCari: string;      // Cari ödeme açıklaması
    currencyMap: Record<string, string>;  // {"TRY": "TL"}
  };
  timeoutMinutes: number;   // 30 — PayTR oturumu zaman aşımı
}
```

### `features` — Özellik Flag'leri

```ts
features: {
  enableDirectDebtPayment: boolean;
  // true → Müşteri, sepetsiz doğrudan borç ödeyebilir
  // false → /cari-odeme menüleri gizlenir
}
```

### `currencies` — Para Birimi Tanımları

```ts
currencies: Record<string, {
  symbol: string;  // "₺", "$", "€"
  label: string;   // "TL", "USD", "EUR"
  icon: string;    // Lucide icon adı: "TurkishLira"
}>;
```

---

## Yeni Tenant Ekleme

1. `src/config/tenants/template_tenant.ts` dosyasını kopyalayın:
   ```
   src/config/tenants/yeni_firma.ts
   ```

2. Tüm alanları doldurun (`TenantConfig` arayüzüne uygun).

3. `src/config/tenant.ts` dosyasındaki `configs` objesine ekleyin:
   ```ts
   import { yeniFirmaConfig } from "./tenants/yeni_firma";

   const configs = {
     erim: erimConfig,
     slay: slayConfig,
     yeni_firma: yeniFirmaConfig,  // ← buraya ekle
   };
   ```

4. `.env` dosyasında `TENANT_ID=yeni_firma` olarak ayarlayın.

5. Yeni tenant'a özgü logo ve favicon dosyalarını `public/logos/` ve `public/favicons/yeni_firma/` klasörlerine ekleyin.

---

## Client-Side Konfigürasyon Enjeksiyonu

Konfigürasyon `src/app/layout.tsx` içinde `window.__TENANT_CONFIG__` olarak enjekte edilir. Client component'leri `getTenantConfig()` çağırarak server-side ve client-side'da tutarlı yapılandırmaya erişir.

```ts
// Her iki ortamda da aynı şekilde kullanılır:
import { tenantConfig } from "@/config/tenant";

const sirketAdi = tenantConfig.company.name;
const lokasyonId = tenantConfig.stock.locationId;
```

---

## Mevcut Tenant'lar

| `TENANT_ID` | Şirket | Durum |
|------------|--------|-------|
| `erim` | Erim Elektronik | Aktif (production) |
| `slay` | Slay | Yapılandırılmış |
| `template_tenant` | — | Boş şablon |
