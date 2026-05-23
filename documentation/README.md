# documentation/

İnsanlar için belgeler. Yeni gelen bir geliştirici buradan başlasın; ajanlar/`memory-bank/` ise iç bağlamı tutar.

| Belge | Kime | Ne anlatır |
|---|---|---|
| [MIMARI.md](MIMARI.md) | "Bu sistem nasıl çalışıyor?" sorusu olan herkes | Pipeline akışı, modül-modül rol, veri modeli, LanceDB şeması |
| [KULLANIM.md](KULLANIM.md) | Sistemi çalıştırmak isteyen kullanıcı | Kurulum, CLI komutları, tipik akışlar, sık karşılaşılan sorunlar |
| [GELISTIRME.md](GELISTIRME.md) | Yeni format/parser eklemek isteyen geliştirici | Genişletme noktaları, kod kuralları |

Hızlı başlangıç için [README.md](../README.md) kök dizinde.

## Bu klasör vs. `memory-bank/`

| | `documentation/` | `memory-bank/` |
|---|---|---|
| **Hedef kitle** | İnsanlar | AI ajanlar (Claude, Cline, vb.) |
| **Stil** | Açıklayıcı, örnekli, FAQ'lı | Sıkıştırılmış karar metni, gerekçeli |
| **İçerik** | Kullanım + mimari + genişletme | "Şu kararı neden verdik", "şu konuda ne yaptık" |
| **Güncelleme** | Sistem davranışı değişince | Her oturumda |
| **Stabilite** | Stabil — değişiklikler önemli | Akışkan |
