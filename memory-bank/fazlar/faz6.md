# Faz 6: CLI UX İyileştirmesi ve Progress Barlar (Rich)

## Hedef
Kullanıcı araçla (özellikle CLI üzerinden) etkileşimde bulunurken arka planda çalışan uzun süreçlerin durumunu görsel ve profesyonel bir şekilde görebilmelidir. Geri bildirim eksikliği (örn. "süreç dondu mu?" endişesi), terminal tabanlı programlar (RAG/ingest sistemleri gibi büyük verileri işlerken) için istenmeyen bir durumdur.

`rich` kullanılarak `doqqy ingest` ve `doqqy embed` komutlarına modern progress barlar, spinner'lar eklenecek ve terminal arayüz standardı artırılacaktır.

## Temel Bileşenler & Beklenen Özellikler
1. **`rich` Kütüphanesi:** Çekirdek Python bağımlılıklarına dahil edilecek (`pyproject.toml`).
2. **`doqqy ingest` Sinyalleri:**
    - Parse edilen ve işlenen belge sayısını/durumunu bar olarak gösterme.
    - Büyük bir PDF (docling) işlenirken "animasyonlu spinner" eşliğinde kullanıcının işlemin sürdüğünü anlayabilmesini sağlama.
3. **`doqqy chunk` ve `doqqy embed` Sinyalleri:**
    - Binlerce chunk vektörize edilirken "Batch 1/X işleniyor..." gibi bilgileri içeren progress barlar konulması.
    - İşlemler başarıyla/hatayla sonlandığında renkli, yapılandırılmış terminal çıktıları (Panel vb.) verilmesi.

## Neden `rich`?
Python terminal ekosisteminde de-facto standart olması, kullanımı çok kolay bir progress ve log arayüzü sunması. Projede hali hazırda kullanılan Typer (CLI altyapısı) ile de doğal bir entegrasyonu vardır (Typer, logları Rich üzerinden renklendirilebilir).

## Görevler
- [x] `pyproject.toml` veya paket yöneticisine `rich`'in bağımlılık olarak eklenmesi.
- [x] `src/doqqy/cli.py` içerisinde `rich.progress.Progress`, `rich.console.Console` adaptasyonu yapılması.
- [x] Mevcut `ingest` ve `embed` pipeline'ındaki `tqdm` ve `print` çıktılarının veya sade döngülerin yerine `rich.progress` entegrasyonu yapılması.
- [x] Windows terminalinde `utf-8` ve `rich_markup_mode` konfigürasyonlarının yeni düzende bozulmadığından (sorun çıkartmadığından) emin olunması.

## Ek Kararlar / Implementasyon Detayları
- Dataclass sıralamaları (required field ve default field konumu) kontrol edildi ve TypeError ortadan kaldırıldı.
- Typer'ın eski standart print() methodları Console ve Panel class'ları ile zenginleştirilerek tüm çıktı ve hatalar formatlandı.
- Hız kaybı olmadan CLI düzeyinde premium bir RAG pipeline deneyimi elde edildi.

---
**Bağlam Notu:** Bu aşama, `doqqy` komut satırı arayüzünün sistem çapında (`pipx` ile vs.) küresel bir UI modülü gibi pürüzsüz çalışmasını amaçlayan polish (cilalama) katmanıdır.
