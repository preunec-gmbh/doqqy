# Faz 1: Tenant Konfigürasyon Şeması

Bu aşamada, her yeni tenant (müşteri) için dinamik hale getirilmesi gereken (şu an kod içerisine gömülü/hardcoded) bağımlı noktalar tespit edilmektedir.

**Son Güncelleme:** 2026-05-20

---

## Durum Özeti

| # | Başlık | Durum | TenantConfig Karşılığı |
|---|--------|-------|----------------------|
| 1 | Sidebar logo ve firma adı | ✅ Çözüldü | `company.name`, `company.logo` |
| 2 | Global metadata ve favicon | ✅ Çözüldü | `metadata.*` |
| 3 | Para birimi TRY zorlaması | ✅ Çözüldü | `locale.*`, `currencies` |
| 4 | Dashboard "Yakında" disabled alan | ❌ Bekliyor | Config dışı — UI temizlik |
| 5 | Veritabanı collation bağımlılıkları | ✅ Çözüldü | `db.collations.search`, `db.collations.strict` |
| 6 | Auth fallback şifre stratejisi | ✅ Çözüldü | `auth.fallbackStrategy`, `auth.staticPassword` |
| 7 | KDV %20 sabitlenmesi | ✅ Çözüldü | `tax.defaultVatRate` |
| 8 | Stok lokasyon ID | ✅ Çözüldü | `stock.locationId` |
| 9 | Kritik stok eşiği | ✅ Çözüldü | `stock.defaultCriticalLevel` |
| 10 | Varsayılan stok birimi | ✅ Çözüldü | `stock.defaultUnit` |
| 11 | Sipariş türü filtresi | ✅ Çözüldü | `orders.receivedType` |
| 12 | Varsayılan fatura türü adı | ✅ Çözüldü | `orders.defaultInvoiceTypeName` |
| 13 | Veritabanı adı fallback (ERIM2025COPY) | ❌ Bekliyor | Config dışı — servis kodlarında `|| "ERIM2025COPY"` kaldırılacak |
| 14 | CARI/KART join çelişkisi | 🔄 Ertelendi | Ayrı sprint — en son ele alınacak |
| 15 | Finans işlem türü ID | ✅ Çözüldü | `transactions.filterTypes[].isInvoice` |
| 16 | Sepet/stok kontrol lokasyon+proje | ✅ Çözüldü | `stock.locationId`, `stock.projectId` |
| 17 | Kâr marjı STOK_OZEL_KOD_1 | ✅ Çözüldü | `stock.marginField` |
| 18 | Ödeme yöntemi ID (kredi kartı) | ✅ Çözüldü | `paymentMethods.krediKartiId` |
| 19 | Cari ödeme feature flag | ✅ Çözüldü | `features.enableDirectDebtPayment` |
| 20 | Ödeme sabitleri + banka bilgisi | ✅ Çözüldü | `paymentMethods.*`, `paymentMethods.bankInfo` |
| 21 | Tema, renk ve font | ✅ Çözüldü | `theme.colors`, `theme.fontFamily`, `theme.radius` |

**18/21 çözüldü.** Bekleyen: #4 (UI temizlik), #13 (kod temizlik), #14 (ertelendi).

---

## Tespit Edilen Hardcoded (Bağımlı) Noktalar

### ✅ 1. Sidebar Bileşeni
- **Dosya Yolu:** `src/components/layout/Sidebar.tsx`
- **İlgili Satırlar:** ~91-94
- **Hardcoded Değer:** `alt="Erim Elektronik"` ve `src="/logo.png"`
- **Açıklama:** Sidebar içerisindeki logo resmi ve alt (alt text) etiketi statik olarak "Erim Elektronik" firmasına göre yazılmış. Yeni bir tenant açıldığında bu logo ve firma adının dinamik hale getirilmesi gerekmektedir.

### ✅ 2. Global Root Layout (Metadata & Favicon)
- **Dosya Yolu:** `src/app/layout.tsx`
- **İlgili Satırlar:** 12-24
- **Hardcoded Değerler:** 
  - `title: "Erim Elektronik"`
  - `description: "B2B ERP Web Portalı..."`
  - Favicon ve manifest yolları (`/favicon/favicon.ico`, `/favicon/site.webmanifest` vs.)
- **Açıklama:** Sitenin genel sekme başlığı (title), SEO açıklaması ve favicon ikonları "Erim Elektronik" firmasına göre statik (`export const metadata`) olarak tanımlanmış. Her tenant için bu değerlerin (`generateMetadata` fonksiyonu kullanılarak veya config'ten okunarak) dinamikleştirilmesi gerekmektedir.

### ✅ 3. Tüm Sistemde Para Birimi (TRY) ve Sembol (₺) Zorlaması
- **Dosya Yolları:** 
  - `src/features/cari/services/bakiyeService.ts` (Satır ~26-31)
  - `src/features/hareketler/services/hareketService.ts` (Satır ~114, bakiye sorgusu)
  - `src/app/dashboard/page.tsx` (Satır ~20-25)
  - `src/app/api/musteri/dashboard/ozet/route.ts`
  - `src/features/stok/components/StokCard.tsx` (Satır ~122)
  - `src/features/hareketler/components/HareketCard.tsx` (Satır ~14-20) ve diğer UI bileşenleri.
- **Hardcoded Kısıtlama:** Hem SQL sorgularında (`AND CB.DOVIZ_AD = 'TRY'`) hem de arayüz bileşenlerinde (`currency: "TRY"`, `₺` vb.) Türk Lirası koda sabit olarak gömülmüş.
- **Açıklama / Çözüm:** Sistemde bir firmanın TRY dışında bakiyesi olsa veya ürün fiyatlarını USD/EUR olarak göstermek istese bile bu yapı yüzünden mümkün olmuyor. Genelleştirme (Refactor) aşamasında **sistemin geriye kalan hiçbir yerinde statik "TRY" veya "₺" ibaresi bırakılmayacaktır**. Çözüm olarak; `tenantConfig` şemasına `defaultCurrency` ve `currencySymbol` ayarları eklenecek, hem SQL filtrelemeleri hem de tüm UI formatlamaları bu dinamik tenant ayarından veya API'den dönen döviz verisinden beslenecektir.

### ❌ 4. Dashboard "Yakında" (Disabled) Alanı
- **Dosya Yolu:** `src/app/dashboard/page.tsx`
- **İlgili Satırlar:** ~202
- **Hardcoded Durum:** "Yakında" yazısı içeren bir alan statik olarak pasif (disabled) bırakılmış.
- **Açıklama / Çözüm:** Projeyi genel bir B2B altyapısına çevirirken, bu tarz geçici kapatılmış statik alanlar tamamen silinecek veya ileride modül/feature-flag bazlı yönetilebilecek yapıya uygun hale getirilecektir.

### ✅ 5. Veritabanı Collation (Karakter Seti) Bağımlılıkları
- **Dosya Yolları:** 
  - `src/features/cari/services/cariService.ts`
  - `src/features/auth/services/cariAuthService.ts`
- **Hardcoded Kısıtlama:** SQL sorgularında `COLLATE Turkish_CI_AI` (arama toleransı için) ve `COLLATE Latin1_General_CS_AS` (şifre doğrulaması için) ifadeleri statik olarak yazılmış.
- **Açıklama / Çözüm:** Farklı ERP kurulumlarına sahip tenantlar farklı karakter setleri (collation) kullanıyor olabilir. Bu statik ifadeler yeni bir tenant'ta "Collation Conflict" hatasına yol açabilir. Çözüm olarak; `tenantConfig` şemasına `collations: { search: "...", strict: "..." }` şeklinde bir konfigürasyon objesi eklenecek ve SQL sorguları doğrudan bu dinamik değerleri kullanacaktır.

### ✅ 6. Kimlik Doğrulama Fallback (Varsayılan Şifre) İş Mantığı
- **Dosya Yolu:** `src/features/auth/services/cariAuthService.ts`
- **İlgili Satırlar:** ~125-133
- **Hardcoded Durum:** Müşterinin web şifresi henüz yoksa (ilk giriş ise), şifre olarak vergi/kimlik numarasının "son 5 hanesi" (`.slice(-5)`) kullanılacak şekilde koda statik bir iş kuralı (business rule) gömülmüş.
- **Açıklama / Çözüm:** Bu kural projeyi tek bir firmaya bağımlı kılmaktadır. Genelleştirme aşamasında konfigürasyona 2 farklı seçenek sunulacaktır: 1) "Son 5 Hane" (Vergi/Kimlik no son 5 hanesi), 2) "Sabit Şifre" (Tüm yeni kullanıcılar için tenant bazlı belirlenen sabit bir metin, örn: '123456'). Auth servisi config'teki bu tercihe göre davranacaktır.

### ✅ 7. Tüm Sistemde KDV Oranının (%20) Sabitlenmesi
- **Dosya Yolları:** 
  - `src/features/stok/types/stok.ts`
  - `src/features/sepet/services/fiyatService.ts`
  - `src/features/sepet/utils/sepetUtils.ts`
  - `src/app/api/odeme/basalt/route.ts`
- **Hardcoded Durum:** Sepet, sipariş hesaplamaları ve ödeme servislerinde KDV oranı varsayılan olarak sabit `%20` (`0.20` veya `20`) şeklinde koda gömülmüş.
- **Açıklama / Çözüm:** Gıda (%1), tekstil (%10) gibi farklı vergi dilimlerine sahip sektörlerde çalışan B2B firmaları (tenant'lar) için tüm ürünlerin vergisini %20 olarak hesaplamak ölümcül ticari hatalara (yanlış tahsilat) yol açar. Genelleştirme aşamasında öncelikli olarak ürünlerin gerçek KDV oranları ERP tablolarından (`STOK` veya `_STOK_STOK_BIRIM` vb.) çekilecektir. Eğer KDV oranı veritabanından çekilemezse / global bir varsayılan gerekiyorsa koddaki statik `%20` yerine `tenantConfig.defaultVatRate` ayarı kullanılacaktır. Eğer ERP'den oran çekilemiyorsa fallback olarak `tenantConfig` içerisinde tutulacak bir `defaultVatRate` (varsayılan KDV) parametresine başvurulacak şekilde yapı güncellenecektir.

### ✅ 8. Stok Lokasyon (Depo/Şube) ID'si
- **Dosya Yolu:** `src/features/stok/services/stokService.ts`
- **İlgili Satırlar:** ~57
- **Hardcoded Durum:** `const LOKASYON = 75919;` tanımlaması ile stok bakiye/miktar sorguları doğrudan Erim Elektronik'e ait spesifik bir depoya kilitlenmiş.
- **Açıklama / Çözüm:** ERP yazılımlarında (Logo, Mikro, ERP12 vs.) her şubenin veya deponun kimlik numarası farklıdır. Bir başka firmada bu depo kodu `1`, `0` veya tamamen alakasız bir değer olabilir. Bazen firmalar "Tüm depoların toplamını" da göstermek isteyebilir. Bu sorunu aşmak için lokasyon değeri koda yazılmayacak; `tenantConfig` JSON dosyasına `stockLocationId` (örn: `75919` veya tüm depolar için `null`) şeklinde dinamik bir özellik olarak eklenecektir.

### ✅ 9. Kritik Stok Eşiği (Varsayılan)
- **Dosya Yolu:** `src/core/constants/stok.ts`
- **Hardcoded Durum:** `export const DEFAULT_KRITIK_STOK_ESIGI = 1;` tanımlamasıyla ürünlerin kritik seviyeye inme eşiği sabit bir değişkene bağlanmış.
- **Açıklama / Çözüm:** Bir B2B firması için "Stokta son 1 adet" kalması kritik seviye (sarı renk/uyarı) kabul edilirken, büyük paletli satış yapan başka bir firmada bu eşik 100 veya 1000 olabilir. Bu sabiti projeden çıkarıp, tenant json (config) dosyasına `defaultCriticalStockLevel` parametresi olarak ekleyeceğiz. Böylece müşteri kendi kritik eşiğini kendisi belirleyebilecek.

### ✅ 10. Varsayılan Stok Birimi (Fallback Değerleri)
- **Dosya Yolu:** `src/features/stok/services/stokService.ts`
- **İlgili Satırlar:** ~108-110
- **Hardcoded Durum:** SQL sorgusundan bir ürünün birim bilgisi dönmezse koda sabit bir şekilde fallback olarak `varsayilanBirimAd: "Adet"`, `varsayilanBirimId: 0` ve `varsayilanCarpan: 1` atanmış.
- **Açıklama / Çözüm:** B2B şirketlerinde ana satış birimi her zaman "Adet" olmayabilir (Örn: "Kg", "Metre", "Kutu"). Ayrıca "Adet" kelimesi ERP'lerde `AD`, `ADET` veya `PCS` olarak geçebilir. Bu yüzden koddaki statik `"Adet"` ataması kaldırılarak genelleştirilecek; yerine `tenantConfig` içerisinde tutulacak olan `defaultUnitName` (Örn: "Adet"), `defaultUnitId` ve `defaultUnitMultiplier` değişkenlerinden okunması sağlanacaktır.

### ✅ 11. Sipariş Türü (Alınan Sipariş Kodu) Filtresi
- **Dosya Yolu:** `src/features/siparis/services/siparisService.ts`
- **İlgili Satırlar:** ~67
- **Hardcoded Durum:** Müşteri veya Admin fark etmeksizin tüm sipariş sorgularında `S.SIPARIS_TURU = 2` kısıtlaması SQL içerisine statik olarak yazılmış.
- **Açıklama / Çözüm:** Her ERP programında (veya her şirket veritabanında) "Alınan Sipariş" belge türünün kodu `2` olmayabilir. Bazen bu türler admin tarafından filtrelenmek de istenebilir. Projeyi genelleştirmek adına bu filtre koda gömülmeyecek, `tenantConfig` içerisine `orderTypes: { received: 2 }` (Alınan sipariş kodu) gibi bir yapı eklenecek ve sorgular bu ayara göre inşa edilecektir.

### ✅ 12. Varsayılan Fiş/Fatura Türü Adı (Fallback Metin)
- **Dosya Yolu:** `src/features/siparis/services/siparisService.ts`
- **İlgili Satırlar:** ~262
- **Hardcoded Durum:** Veritabanından fiş türü adı dönmediği durumlarda (`??`) fallback olarak `"Satış Faturası"` metni koda doğrudan yazılmış.
- **Açıklama / Çözüm:** Farklı bir dilde (Örn: İngilizce'de "Sales Invoice") veya farklı bir iş modelinde (Örn: "Teslimat Fişi", "Sipariş Fişi") bu kelimenin değişmesi gerekir. Koddaki bu statik metin kaldırılarak genelleştirme adımında `tenantConfig` şemasına `defaultInvoiceTypeName` değişkeni eklenecek ve bu metin oradan çekilecektir.

### ❌ 13. Veritabanı Adı Fallback (ERIM2025COPY)
- **Dosya Yolları:** Bütün servis ve API dosyaları (Örn: `siparisService.ts`, `hareketService.ts`, `cariService.ts` ve `route.ts` dosyaları).
- **Hardcoded Durum:** Kodun birçok yerinde `const DB = process.env.SQLSERVER_DATABASE || "ERIM2025COPY";` şeklinde bir kullanım mevcut. `.env` değişkeni eksikse sistem zorla "ERIM2025COPY" adlı Erim test veritabanına bağlanmaya çalışıyor.
- **Açıklama / Çözüm:** Bu çok tehlikeli bir fallback yöntemidir. Yeni bir tenant (müşteri) ayağa kaldırılırken `.env` dosyası eksik yapılandırılırsa, uygulama hata vermek yerine gidip başka bir firmanın (Erim Elektronik) veritabanına sorgu atabilir. Projedeki tüm `|| "ERIM2025COPY"` ibareleri tamamen silinecektir. Eğer `process.env.SQLSERVER_DATABASE` tanımsız ise sistemin fallback yapmak yerine doğrudan hata fırlatıp (Throw Error) durması sağlanacaktır.

### 🔄 14. CARI ve KART Eşleştirme (Join) Çelişkisi — Ertelendi
- **Dosya Yolu:** `src/features/hareketler/services/hareketService.ts`
- **İlgili Satırlar:** ~43, ~174-175, ~336
- **Hardcoded Durum:** Müşterinin finansal hareketlerini bulmak için `getKartId` sorgusunda `C.KOD = KA.KOD` (Cari Kodu ve Kart Kodu üzerinden) eşleştirme yapılırken, `getHareketList` sorgusunda `C_BC.ID = FD.KART_BORCLU` (Cari ID = Kart ID) eşleştirmesi yapılmış.
- **Açıklama / Çözüm:** Erim Elektronik veritabanında CARI tablosu ile KART_ADLARI tablosu tesadüfen aynı ID ile gidiyor olabilir. Fakat başka bir firmada CARI ID'si 12 iken KART ID'si 40 olursa sistem bozulur ve yanlış veriler gelir. Çözüm olarak; varsayımsal bir ara tablo aramak yerine, kodda zaten `getKartId` fonksiyonunda çalışır durumda olan `KART_ADLARI.KOD = CARI.KOD` eşleştirmesi tüm sql sorgularına (Örn: `ON C_BC.KOD = KA_B.KOD`) standart olarak uygulanacaktır. Böylece ID'ler tutmasa bile B2B sistemi kodu baz aldığı için tüm tenantlarda hatasız çalışacaktır.

### ✅ 15. Finans İşlem Türü (Satış Faturası) ID Kısıtlaması
- **Dosya Yolu:** `src/features/hareketler/components/HareketDetayContent.tsx`
- **İlgili Satırlar:** ~19
- **Hardcoded Durum:** Kodun içerisinde `const SATIS_FATURASI_TIP_IDS = new Set([47, 48]);` şeklinde Satış Faturası işlem tipleri doğrudan `47` ve `48` ID'lerine kilitlenmiş.
- **Açıklama / Çözüm:** ERP yazılımlarında `FINANS_ISLEM_TURU` tablosundaki "Satış Faturası" tipi her firmada farklı bir ID ile tutulabilir. Erim Elektronik'te 47 ve 48 iken başka bir firmada `1` veya `100` olabilir. Bu değerler statik kalırsa, yeni firmalarda sistem faturanın detaylarını göstermez (fatura olduğunu algılayamaz). Çözüm olarak; bu ID seti genelleştirme aşamasında `tenantConfig.transactionTypes.salesInvoiceIds` (Örn: `[47, 48]`) dizisine taşınarak dinamik bir yapıya kavuşturulacaktır. Bu da zaten linear notlarindaki tablolarda var. 

### ✅ 16. Sepet ve Stok Kontrol (Lokasyon ve Proje Sabitleri)
- **Dosya Yolları:** 
  - `src/features/sepet/services/siparisService.ts`
  - `src/features/sepet/services/stokKontrolService.ts`
- **Hardcoded Durum:** Kodun başında `const LOKASYON = 75919;` ve `const PROJE = 75916;` tanımlamaları statik olarak belirtilmiştir.
- **Açıklama / Çözüm:** Stok (Bakiye) daha önce 8. maddede genel olarak incelenmişti, ancak siparişin (sepetin) kaydı aşamasında ve sepet stok kontrolünde doğrudan bu iki spesifik ID kullanılıyor. Başka bir şirkette (tenant) sipariş açıldığında veritabanında 75916 ID'li bir proje bulunmayacağı için sipariş ekleme prosedürleri tamamen çökecektir. Şu anlık bu değerler `tenantConfig` üzerinden okunacak şekilde düzenlenecektir. İlerleyen fazlarda ise tüm lokasyonların ve projelerin veritabanından dinamik yönetildiği daha kapsamlı bir ERP modül yapısına geçilecektir.

### ✅ 17. Kâr Marjı İçin STOK_OZEL_KOD_1 Kullanımı (Business Rule)
- **Dosya Yolları:** 
  - `src/core/utils/fiyatHesaplama.ts`
  - `src/features/stok/services/stokService.ts`
  - `src/features/sepet/services/fiyatService.ts`
- **Hardcoded Durum:** Stok fiyatlarının kâr marjını hesaplamak için `STOK_OZEL_KOD_1` alanının KOD sütunu (Örn: "20" yazıyorsa %20 kâr) statik olarak kullanılmış.
- **Açıklama / Çözüm:** ERP programlarında `OZEL_KOD` alanları şirketlerin kendi ihtiyaçlarına göre (Renk, Marka, Reyon, Sezon vb.) serbestçe kullandıkları metin alanlarıdır. Erim Elektronik burayı "Kâr Marjı" tutmak için kullanmış olabilir. Ancak başka bir firma bu alanı "Marka" olarak kullanıp içine "SAMSUNG" yazdığında kod fiyat hesaplayamaz, ya da reyon numarası olarak "10" yazdığında sistem ürün fiyatına durduk yere %10 kâr ekleyip müşteriye yanlış fiyattan satar. Çözüm olarak; kâr marjının ERP'de hangi alandan okunacağı `tenantConfig.marginField` (Örn: `'STOK_OZEL_KOD_1'` veya `'STOK_OZEL_KOD_3'`) şeklinde konfigürasyon üzerinden dinamik olarak belirlenecektir.

### ✅ 18. Ödeme Yöntemi Kart ID'si (Kredi Kartı)
- **Dosya Yolu:** `src/app/api/odeme/callback/route.ts`
- **İlgili Satırlar:** ~33
- **Hardcoded Durum:** Kredi kartı ile yapılan tahsilatlarda siparişe yazılacak ödeme yöntemi ID'si `const ODEME_YONTEMI_KART = 48;` olarak statik yazılmış.
- **Açıklama / Çözüm:** B2B üzerinden kredi kartı ile sipariş atıldığında (PayTR vb. callback sonucunda), ERP tarafında siparişin "Kredi Kartı" ile ödendiğini belli etmek için `SIPARIS_OZEL_KOD_1` (veya ilgili ödeme alanı) bu ID ile güncellenmektedir. Başka bir tenant'ın veritabanında Kredi Kartı ödeme yönteminin ID'si (veya kodu) "48" değil, "1" veya "99" olabilir. Çözüm olarak; genelleştirme aşamasında kredi kartı vb. ödeme yöntemlerinin ERP eşleşmeleri `tenantConfig.paymentMethods.creditCardId` şeklinde bir yapıdan (veya arayüzden) dinamik çekilecektir.

### ✅ 19. Alışverişsiz Cari Ödeme (Feature Flag)
- **Dosya Yolu:** `src/app/api/odeme/callback/route.ts` (ve ilgili arayüz bileşenleri)
- **Hardcoded Durum:** Sipariş olmadan müşterinin doğrudan borç kapatmak için yaptığı "Cari Ödeme" işlemi yarı-otomatik çalışıp sadece `web_payment` tarafına log atacak şekilde kurgulanmış.
- **Açıklama / Çözüm:** Her B2B firması sipariş olmadan doğrudan tahsilat almayı tercih etmeyebilir veya manuel muhasebeleştirme sistemini kullanmak istemeyebilir. Bu bir müşteri (tenant) tercihidir. Genelleştirme aşamasında bu durum bir "Feature Flag" (özellik aç/kapat) anahtarına bağlanacaktır. Örn: `tenantConfig.features.enableDirectDebtPayment = true/false`. Eğer `false` ise, B2B panelinde "Cari Ödeme Yap" menüleri tamamen gizlenecektir.

### ✅ 20. Ödeme Sabitleri ve Banka (EFT/Havale) Bilgileri
- **Dosya Yolları:** 
  - `src/core/constants/odeme.ts`
  - `src/core/constants/stok.ts` (Kritik stok eşiği - 9. maddede de bahsedildi)
- **Hardcoded Durum:** `odeme.ts` dosyası içerisinde Erim Bilişim'e ait banka adı, IBAN numarası, hesap sahibi bilgileri statik olarak (`EFT_HESAP_BILGISI`) yazılmış. Ayrıca 18. maddedeki kredi kartına ek olarak `KAPIDA_ODEME = 10`, `EFT_HAVALE = 30` gibi tüm ERP ödeme yöntemi ID'leri koda gömülmüş.
- **Açıklama / Çözüm:** Bu durum B2B sisteminin başka bir şirkete açılmasının önündeki en büyük (ve ticari açıdan en tehlikeli) engellerdendir. Bir müşteri Havale/EFT yapmak istediğinde karşısına kendi tedarikçisinin değil, doğrudan Erim Bilişim'in IBAN'ı çıkacaktır. Çözüm olarak; bu constants dosyalarındaki tüm banka bilgileri, hesap sahipleri ve ödeme ID'leri (stok eşikleriyle birlikte) doğrudan `tenantConfig.bankAccounts` ve `tenantConfig.paymentMethods` yapısına taşınacaktır.

### ✅ 21. Tema, Renk ve Font Yönetimi (White-label UI)
- **Dosya Yolları:** 
  - `src/app/globals.css` (Tailwind değişkenleri)
  - `src/app/layout.tsx`
- **Hardcoded Durum:** Sistemin genelinde kullanılan ana renk (primary color), font ailesi ve arayüz yuvarlaklık (border-radius) değerleri Erim Elektronik'in marka kimliğine göre Tailwind içerisine statik olarak gömülmüş.
- **Açıklama / Çözüm:** Başka bir firmaya kurulum yapıldığında kodun içindeki tüm Tailwind renk class'larını bulup değiştirmek imkansızdır. Çözüm olarak; `tenantConfig.theme` içerisine `primaryColor` (Örn: #ef4444) ve `fontFamily` (Örn: Inter) tanımlanacak. Next.js uygulamasının `layout.tsx` dosyasında bu değerler dinamik CSS Variables (CSS Değişkenleri) olarak `:root` etiketine basılacak ve Tailwind doğrudan bu değişkenleri okuyacaktır. Böylece config değiştirildiği anda sitenin tüm rengi ve fontu saniyeler içinde o tenant'a özel hale gelecektir.


