# Ürün Bağlamı

## Bu Sistem Neden Var?

Elimizde 500 sayfalık dağınık bir doküman korpusu var. Geliştirme yaparken iki temel problem yaşıyoruz:

1. **Bilişsel yük:** 500 sayfa tek seferde okunmaz, okunsa da akılda kalmaz. Önce bütüne hakim olmadan parçaya dalmak verimsiz.
2. **Erişim:** "Auth flow'u nerede anlatıyordu?" gibi sorularda manuel arama dakikalar alıyor, çoğu zaman kaybolup gidiliyor.

Bu sistemin felsefesi: **Önce zihinsel bir harita oluştur, sonra ihtiyaç anında detaya in.**

## Çözmek İstediğimiz Problemler

### 1. Genel Yapıyı Kavrama
Dokümanlar hakkında zihinsel bir harita oluşturmak. Hangi konunun hangi dosyada/bölümde olduğunu, hangi konunun hangiyle ilgili olduğunu bir bakışta görmek.

### 2. İhtiyaç Anında Erişim
Geliştirirken bir konu çıkınca o konunun anlatıldığı bölüme saniyeler içinde ulaşmak. Manuel arama, dosya gezme, Ctrl+F çekiştirme — hepsi yok.

### 3. İlişkileri Görebilme
Bir bölümü okuduğumda onunla bağlantılı diğer bölümleri kolayca bulmak. "Bu konuyu derinleştirmek istersem nereye bakarım?" sorusunun cevabı sistem tarafından önceden hesaplanmış olmalı.

## Nasıl Çalışmalı

İki katmanlı yapı:

### Katman 1: Harita (Statik, Tek Seferlik)
- Dokümanların tamamı **section seviyesinde** özetlenmiş.
- Konu kümeleri çıkarılmış (Auth, API, Deployment vb.).
- Section'lar arası çapraz referanslar üretilmiş.
- Çıktı: gezilebilir `INDEX.md` + makine-okur `topics.yaml` + Obsidian graph view.

### Katman 2: Sorgu (Dinamik, Sürekli)
- Doğal dilli sorgu → top-5 ilgili bölüm.
- Sonuç: **ham chunk** + kaynak (dosya, bölüm, sayfa) + ilgili diğer bölüm referansları.
- **LLM cevap sentezi YAPILMAZ** — kullanıcı orijinal metni okur.

## Kullanıcı Deneyimi Hedefleri

### Keşif Modu
Obsidian vault'unu aç → `INDEX.md`'den başla → graph view ile dolaş. Genel yapıya hakim ol.

### Hedefli Arama Modu
`doqqy query "..."` ile CLI'dan sor → top-5 sonucu oku → gerekirse Obsidian'dan o dosyaya atla → orijinal bağlamı gör.

### Performans
- Sorgu sonucu **<1 saniye** gelmeli.
- Sorgu zamanında internet bağımlılığı YOK (embedding/rerank local).

### Şeffaflık (Kritik)
Sentez yok; kullanıcı her zaman orijinal metni görür. "LLM yorumladı" katmanı eklenmez. Bu bilinçli bir tasarım kararı.

## Karar Gerekçesi: Neden LLM Sentezi Yok?

Kullanıcı dokümanı **anlamak** istiyor, "özet" değil. Sentezlenmiş cevap kolaycıdır ama:
- Orijinal metnin bağlamını, üslubunu ve etrafındaki detayları kaybeder.
- "LLM ne anladı?" değil, "doküman ne diyor?" sorusu önemli.
- Her sorguda LLM çağrısı = sürekli maliyet ve gecikme.
- Ham chunk = ücretsiz, anlık, şeffaf.

Geliştirici dokümantasyonu için ham chunk daha doğru.

## Karar Gerekçesi: Neden Section Bazlı Harita?

Dosya bazlı özet "ne hakkında" bilgisi verir ama "**nereye git**" demez. 30 sayfalık bir dosyanın özetini bilmek, içindeki 15 farklı konudan hangisinde olduğunu söylemez. Section bazlı (her `##` / `###` için ayrı özet + ilişkiler) granülariteyi doğru noktaya koyar — kullanıcıya "şu paragraf grubunu oku" diyebilir.

## Karar Gerekçesi: Neden Görseller İşlenmez?

MVP'yi karmaşık tutmamak için. Görseller (mimari diyagram, sequence diagram vs.) PDF'lerde önemli ama vision LLM ile caption üretmek extra pipeline + extra LLM maliyeti demek. İlk versiyonda placeholder bırakılır, kullanıcı PDF'i açıp bakar. İhtiyaç netleşince sonradan eklenir.
