---
title: Barkod Okuyucu Entegrasyonu
description: El terminallerinin ERP stok modülüne bağlanması için yapılandırma rehberi.
---

# Barkod Okuyucu Entegrasyonu

Depo el terminalleri, ERP stok modülüne yerel ağ üzerinden bir REST servisi ile bağlanır. Bu döküman terminal tarafında yapılması gereken yapılandırmayı anlatır.

## Bağlantı Yapılandırması

Her el terminaline aşağıdaki gibi bir yapılandırma dosyası yüklenir:

```json
{
  "warehouse_id": "IST-01",
  "endpoint": "https://erp.local/api/stock/scan",
  "scan_mode": "batch",
  "sync_interval_seconds": 15,
  "offline_queue_limit": 500
}
```

`scan_mode` alanı `batch` veya `realtime` değerini alabilir. Depo yoğunken `batch` modu tercih edilir çünkü ağ trafiğini azaltır; ancak stok görünürlüğü `sync_interval_seconds` kadar gecikmeli olur.

## Çevrimdışı Kuyruk

Terminal ağ bağlantısını kaybettiğinde okutulan barkodlar `offline_queue_limit` değerine kadar yerel olarak biriktirilir. Bağlantı geri geldiğinde kuyruk otomatik olarak boşaltılır ve sunucuya sırayla iletilir. Kuyruk limiti dolarsa terminal ekranında uyarı gösterilir ve yeni okutma işlemi engellenir.

## Hatalı Barkod Okuma

Sistemde tanımlı olmayan bir barkod okutulduğunda terminal, işlemi yerel kuyruğa almaz ve kullanıcıya anında "Tanımsız Ürün" uyarısı gösterir. Bu davranış, tanımsız barkodların sessizce kuyrukta birikip senkronizasyon sırasında toplu hata üretmesini engellemek içindir.

## Firmware Güncellemeleri

Terminal firmware güncellemeleri, depo kapalıyken merkezi bir yönetim konsolundan uzaktan gönderilir. Güncelleme sırasında terminal çevrimdışı kuyruğu korunur ve güncelleme sonrası otomatik olarak senkronize edilir.
