# Faz 2 — Hibrit Arama + Rerank Implementation Notları

Bu belge Faz 2'nin planını ve implementation notlarını içerir.

## 1. Durum Özeti

**🟢 Faz 2 TAMAM — Hibrit arama + reranker çalışıyor (2026-05-28).**

Faz 1'de dense-only arama çalışıyor. Faz 2'nin amacı:
- bge-m3'ün sparse vektörünü de kullanarak lexical eşleşmeyi eklemek
- Dense + sparse skorlarını RRF ile birleştirmek
- `bge-reranker-v2-m3` ile top-50 → top-5 daraltmak

## 2. Neden Gerekli?

Faz 1'de gözlemlenen sorun: dense-only retrieval bazı sorgularda doğru dosyayı ilk sıraya getiremiyor.

Örnek: "PayTR odeme akisi" sorgusunda SEQUENCE.md tam karşılık olmasına rağmen PRISMA.md daha yüksek skor aldı.

İki problemi var:
1. **Lexical boşluk:** "JWT_REFRESH_SECRET" gibi tam eşleme gerektiren sorgularda dense vektör yetersiz. Sparse vektör bunu çözer.
2. **Ranking kalitesi:** İlk retrieval'da gürültü fazla. Reranker, sorgu ile chunk'ı birlikte görüp gerçek alakayı ölçer.

## 3. Yapılacaklar

### 3.1 Sparse Vektör Ekleme (`embed.py`)

- [x] `encode()` çağrısında `return_sparse=True` ekle
- [x] LanceDB schema'ya `sparse_vector` kolonu ekle (JSON string formatı: `{"token_id": weight}`)
- [x] Mevcut `store.lance` tablosunu yeni schema ile yeniden oluştur (tam rebuild)
- [x] `docq embed` komutu sonunda kaç sparse token üretildiğini log'a yaz

### 3.2 Hybrid Query (`query.py`)

- [x] Dense arama: top-50 getir
- [x] Sparse arama: top-50 getir (manuel python-side dot product — LanceDB FTS yerine)
- [x] **Reciprocal Rank Fusion (RRF):** iki listeyi birleştir (k=60)
- [x] RRF sonrası top-50 → reranker'a gönder

### 3.3 Reranker (`rerank.py` — yeni modül)

- [x] `transformers.AutoModelForSequenceClassification` ile yükle (`lru_cache`)
- [x] `(query, chunk_content)` çiftleri batch_size=4 ile skorlan
- [x] Sigmoid normalize → 0-1 arası skor → top-5 döndür
- [x] İlk indirme ~2.27 GB (tek seferlik, HuggingFace cache)

### 3.4 CLI Güncellemesi (`cli.py`)

- [x] `docq query` komutuna `--no-rerank` flag'i ekle (debug için)
- [x] Çıktıda hangi aşamanın skoru olduğunu göster: `dense_rank`, `sparse_rank`, `rrf_score`, `rerank_score`

### 3.5 LanceDB Sparse Desteği

- [x] LanceDB sparse native desteği yetersiz → **manuel python-side dot product** seçildi
- [x] Sparse çıktı JSON string olarak saklanıyor, sorgu sırasında `json.loads()` ile geri alınıyor

## 4. Pipeline Değişikliği

**Faz 1 (mevcut):**
```
query → dense embed → cosine top-5 → sonuç
```

**Faz 2 (hedef):**
```
query → dense embed → cosine top-50 ─┐
                                      ├─ RRF → top-50 → reranker → top-5
query → sparse embed → sparse top-50 ─┘
```

## 5. Dosya Değişiklikleri

| Dosya | Değişiklik |
|---|---|
| `src/docq/embed.py` | `return_sparse=True`, LanceDB schema güncelleme |
| `src/docq/query.py` | Sparse retrieval + RRF fonksiyonu |
| `src/docq/rerank.py` | Yeni modül — `bge-reranker-v2-m3` |
| `src/docq/cli.py` | `--no-rerank` flag, çıktıda aşama skorları |
| `pyproject.toml` | Gerekirse yeni bağımlılık yok (FlagEmbedding reranker'ı zaten içeriyor) |

## 6. Test Planı

1. `docq embed` ile sparse vektörler de yazıldı mı kontrol et (`docq info` güncellenir)
2. `docq query "JWT_REFRESH_SECRET"` — tam eşleşme gerektiren sorgu, sparse olmadan çok kötüydü
3. `docq query "PayTR odeme akisi"` — önceki problemi çözdü mü?
4. `docq query "..." --no-rerank` vs normal — reranker fark yaratıyor mu?
5. 15-20 soru ile recall@5 hesapla (Faz 2 eval seti)

## 7. Riskler

| Risk | Olasılık | Çözüm |
|---|---|---|
| LanceDB sparse desteği yetersiz | Orta | Manuel python-side hesaplama |
| Reranker bellek sorunu (CPU) | Düşük | batch_size=4 ile çalıştır |
| RRF k parametresi ayarı | Düşük | k=60 literatür standardı, test ile fine-tune |
| FlagEmbedding sparse çıktısı formatı değişmiş | Düşük | Sürüm sabitlenmiş (1.4.0) |

## 9. Bugün Öğrenilenler (2026-05-28)

### FlagEmbedding 1.4.0 + bge-reranker-v2-m3 Uyumsuzluğu
`FlagReranker` ve `FlagLLMReranker` her ikisi de `XLMRobertaTokenizer.prepare_for_model` hatası verdi. Bilinen bir bug. **Çözüm:** FlagEmbedding tamamen bypass edildi, `transformers.AutoModelForSequenceClassification` ile direkt implement edildi. Skor sigmoid ile 0-1 normalize edildi.

### max_length=8192 RAM Sorunu
Embed sırasında makine 28 GB RAM kullandı (boşta 12 GB). Sebep: `max_length=8192` her batch için 8192 tokenlik attention matrisi ayırıyor, chunk 200 token olsa bile. `max_length=1024` + `EMBEDDING_BATCH_SIZE=4` ile ~5-6 GB'a indi. RAG kalitesine etkisi yok — vektör matematiği değişmiyor.

### section_path Numpy Array Hatası
LanceDB'den gelen `section_path` kolonu numpy array olarak dönüyor. `or []` operatörü bunu patlatıyor (`ValueError: truth value of array`). **Çözüm:** `_safe_section_path()` yardımcı fonksiyonu eklendi, her iki sonuç dalında kullanılıyor.

### Reranker Gerçek Model Boyutu
Dokümanlarda ~1.1 GB yazıyordu, gerçekte **2.27 GB** indirdi. HuggingFace symlink Windows'ta çalışmıyor, duplicate saklıyor — disk kullanımı 2x olabilir.

### Sparse Arama LanceDB FTS ile Uyumsuz
bge-m3 sparse çıktısı BM25 terimi değil, model vocab token ID'si. LanceDB FTS bunları index'leyemiyor. **Seçilen yol:** JSON serialize + python-side dot product. 50-100 chunk için milisaniye düzeyinde, performans yeterli.

## 10. Test Sonuçları (2026-05-28)

**Sorgu: "PayTR odeme akisi"**
- [2]. SEQUENCE.md dense'de yok, sparse rank=11 ile yakalandı → reranker 0.938 verdi. Faz 1'deki sorun çözüldü.
- Reranker RRF sıralamasını önemli ölçüde düzeltti: RRF'de 1. olan chunk reranker sonrası 3.'ye düştü.

**Sorgu: "JWT_REFRESH_SECRET"**
- ENVIRONMENT.md hem dense hem sparse rank=1 — mükemmel lexical eşleşme.
- Login akışı chunk'ı (JWT içeriyor ama alakasız) reranker tarafından 0.030'a düşürüldü. Gürültü temizlendi.

**Faz 3 — Harita Üretimi (Seçenek D):**
- Per-file LLM çağrısı (Gemini 2.5 Pro) → summary + concepts + explicit/thematic ilişkiler
- Embedding cosine → `might_be_related`
- `topics.yaml` + `INDEX.md` üretimi
