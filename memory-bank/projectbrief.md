# Proje Brifi

## Proje Adı
**doqqy** (geçici çalışma adı) — Yerel Doküman Bilgi Sistemi.

## Temel Problem
Elimizde ~500 sayfa, klasörlere dağılmış doküman var (md, pdf, docx karışık). Geliştirme sırasında ihtiyaç oldukça doğru bölümlere hızlıca ulaşabilmek istiyoruz. Dokümanın tek seferde okunup anlaşılması mümkün değil; "kervan yolda düzülür" mantığıyla çalışacağız ama bunun için **neyin nerede olduğunu** ve **hangi bölümün hangiyle ilgili olduğunu** sistemin bilmesi gerekiyor.

## Ana Hedefler
1. **Harita:** Tüm korpusun gezilebilir bir indeksi çıkarılsın. Hangi konunun nerede olduğunu görsel olarak görelim.
2. **Hızlı arama:** Doğal dilli sorgu ile alakalı bölümlere saniyeler içinde ulaşalım.
3. **İlişkili bölümler:** Bir bölümle bağlantılı diğer dokümanları/bölümleri sistem otomatik yüzeye çıkarsın.

## Kapsam

### Dahil (MVP)
- `md`, `pdf`, `docx` ingest (her birine ayrı pipeline).
- Header-aware chunking.
- Hibrit semantik + lexical arama (bge-m3 hybrid mode).
- Cross-encoder reranking.
- Section-bazlı statik harita (LLM ile üretilir, `topics.yaml` + `INDEX.md` çıktıları).
- Obsidian uyumlu vault çıktısı (`[[wiki-link]]`'lerle).
- CLI sorgu arayüzü.

### Hariç (Şimdilik)
- Inkremental update — her seferinde tam rebuild.
- Görsel / şema / diyagram işleme — placeholder bırakılır, kullanıcı PDF'i açıp bakar.
- LLM ile cevap sentezi — sorguya ham chunk dönülür, kullanıcı orijinal metni okur.
- MCP server entegrasyonu — sistem stabilleştikten sonra eklenecek.
- Web arayüz — Obsidian + CLI yeter.

## Başarı Kriterleri
- 500 sayfalık korpus 1-2 saatte tamamen indekslenmiş olmalı (tek seferlik).
- "JWT refresh nasıl çalışıyor?" tarzı bir sorguya top-5'te doğru bölüm gelmeli (<1 saniye).
- Obsidian'da graph view ile doküman ilişkileri görülebilmeli.
- Tek bir bölümden ilgili olduğu diğer bölümlere `[[wiki-link]]` ile gidilebilmeli.

## Kısıtlar
- **OS:** Windows 10, PowerShell ortamı.
- **Dil:** Python 3.11+ ekosistemi.
- **Privacy:** Kısıt yok, ama embedding ve reranking yine de local çalışsın (ücretsiz + hızlı).
- **Bütçe:** Harita üretiminde önce ücretsiz LLM denenir (Gemini 2.5 Pro free tier). Kalite yetmezse ücretli Claude Opus 4.7'ye geçilir.

## Bu Belgenin Rolü
Tüm diğer memory bank dosyaları bu brifin üzerine inşa edilir. Kapsam ve hedefler değişirse **önce burası güncellenir**, sonra alt belgeler buna uyum sağlar.
