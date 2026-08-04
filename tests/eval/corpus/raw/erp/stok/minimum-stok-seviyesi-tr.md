---
title: Minimum Stok Seviyesi ve Yeniden Sipariş Noktası
description: Ürün kategorilerine göre tanımlanan minimum stok seviyeleri ve otomatik sipariş tetikleme kuralları.
---

# Minimum Stok Seviyesi ve Yeniden Sipariş Noktası

ERP sistemi, her stok kalemi için bir minimum seviye ve yeniden sipariş noktası (ROP) tutar. Stok bu seviyenin altına düştüğünde satın alma birimine otomatik bildirim gönderilir.

## Kategoriye Göre Varsayılan Seviyeler

| Kategori | Minimum Seviye | Yeniden Sipariş Noktası | Ortalama Tedarik Süresi |
|----------|-----------------|--------------------------|---------------------------|
| Hızlı tüketim ürünleri | 200 adet | 350 adet | 3 gün |
| Endüstriyel yedek parça | 15 adet | 30 adet | 21 gün |
| Mevsimsel ürünler | 0 adet | 100 adet | 45 gün |
| İthal elektronik | 10 adet | 25 adet | 60 gün |

## Otomatik Sipariş Tetikleme

Bir kalemin mevcut stoku yeniden sipariş noktasının altına düştüğünde sistem, tanımlı tedarikçiye otomatik bir taslak satın alma siparişi oluşturur. Bu taslak, satın alma uzmanı tarafından onaylanmadan tedarikçiye iletilmez.

## Mevsimsel Ürünler İstisnası

Mevsimsel ürünlerde minimum seviye kasıtlı olarak sıfır tutulur; sezon dışında stok bulundurulmaz. Sezon başlangıcından 45 gün önce planlama ekibi bu ürünler için manuel bir başlangıç siparişi oluşturur.

## Seviye Güncelleme

Minimum seviye ve ROP değerleri, geçmiş 12 aylık satış verisine göre her çeyrekte otomatik olarak yeniden hesaplanır. Planlama ekibi, hesaplanan yeni değerleri onaylamadan sistem eski değerleri kullanmaya devam eder.
