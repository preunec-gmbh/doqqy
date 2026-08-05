---
title: Fatura İptal Süreci
description: Nova Ticaret A.Ş. bünyesinde kesilmiş bir faturanın iptal edilmesi için izlenmesi gereken adımlar.
---

# Fatura İptal Süreci

Bu döküman, Nova Ticaret A.Ş. muhasebe biriminde kesilmiş bir satış faturasının nasıl iptal edileceğini anlatır.

## Ne Zaman Fatura İptal Edilir

Aşağıdaki durumlarda fatura iptali gündeme gelir:

- Müşteri siparişi son anda iptal ettiğinde
- Fatura üzerinde birim fiyat veya miktar hatası tespit edildiğinde
- Aynı sipariş için mükerrer fatura kesildiğinde

Faturanın iptal edilebilmesi için ilgili faturanın **e-Fatura GİB portalına henüz iletilmemiş** olması gerekir. İletilmiş faturalarda iptal yerine iade faturası (alacak dekontu) kesilir.

## İptal Adımları

### Talep Oluşturma

Muhasebe personeli, ERP sisteminde ilgili fatura kaydını açar ve "İptal Talebi Oluştur" butonuna basar. Talep formunda iptal gerekçesi zorunlu alan olarak doldurulmalıdır.

### Yetkilendirme

İptal talebi, fatura tutarına göre farklı onay mercilerine yönlendirilir:

- Tutar 5.000 TL'nin altındaysa: **Bölge Müdürü** onayı yeterlidir.
- Tutar 5.000 TL ve üzerindeyse: **Genel Müdür** onayı zorunludur.

Onay bekleyen talepler 48 saat içinde sonuçlandırılmazsa otomatik olarak muhasebe müdürüne eskale edilir.

### Sistem Kaydının Kapatılması

Onay verildikten sonra ERP sistemi faturayı "İptal Edildi" statüsüne çeker ve ilgili stok hareketlerini geri alır. Bu adım geri alınamaz.

## Yetkilendirme Matrisi

İptal yetkisi olan roller ve limitleri aşağıdaki gibidir:

| Rol | Onay Limiti | Süre |
|-----|-------------|------|
| Muhasebe Uzmanı | Onay yetkisi yok | - |
| Bölge Müdürü | 5.000 TL'ye kadar | 48 saat |
| Genel Müdür | Sınırsız | 72 saat |

## Sık Karşılaşılan Hatalar

Fatura zaten GİB'e iletilmişse sistem iptal butonunu devre dışı bırakır ve kullanıcıyı iade faturası sürecine yönlendirir. Bu davranış kasıtlıdır ve mevzuata uyum amacı taşır.
