---
title: KDV Hesaplama Rehberi
description: Nova Ticaret A.Ş. ERP sisteminde ürün kategorilerine göre KDV oranlarının uygulanması.
---

# KDV Hesaplama Rehberi

ERP sistemi, satış faturası oluşturulurken ürün kategorisine göre otomatik KDV oranı ataması yapar. Bu döküman uygulanan oranları ve istisnai durumları açıklar.

## Kategori Bazlı Oranlar

Aşağıdaki tablo, sistemde tanımlı ürün kategorileri ile uygulanan KDV oranlarını gösterir:

| Ürün Kategorisi | KDV Oranı | Not |
|------------------|-----------|-----|
| Temel gıda maddeleri | %1 | Ekmek, un, bakliyat |
| Kitap ve süreli yayın | %1 | Elektronik kitaplar dahil |
| Tekstil ve hazır giyim | %10 | - |
| Elektronik eşya | %20 | Beyaz eşya dahil |
| Danışmanlık hizmetleri | %20 | Hizmet faturaları |
| İhracat kalemleri | %0 | Gümrük çıkış belgesi zorunlu |

## Otomatik Atama Mantığı

ERP sisteminde her stok kartı bir "vergi grubu" alanına sahiptir. Fatura satırı oluşturulurken bu alan okunur ve yukarıdaki tablo baz alınarak oran otomatik uygulanır. Kullanıcı oranı manuel değiştiremez; değişiklik yalnızca stok kartı üzerinden yapılabilir.

## İstisnai Durumlar

İhracat faturalarında KDV oranı sıfır olarak uygulanır ancak gümrük çıkış belgesinin sisteme yüklenmesi zorunludur. Belge yüklenmeden fatura "onay bekliyor" statüsünde kalır ve muhasebeleştirilemez.

## Hatalı Oran Bildirimi

Bir stok kalemi için yanlış vergi grubu atandığı tespit edilirse, düzeltme talebi ERP üzerinden muhasebe müdürlüğüne iletilir. Geçmişe dönük kesilmiş faturalarda oran düzeltmesi yapılmaz; yalnızca yeni kesilecek faturalara yansıtılır.
