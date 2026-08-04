---
title: e-Fatura GİB Entegrasyonu
description: Nova Ticaret A.Ş. ERP sisteminin Gelir İdaresi Başkanlığı e-Fatura servisine entegrasyonu için teknik rehber.
---

# e-Fatura GİB Entegrasyonu

Bu döküman, Nova Ticaret A.Ş. ERP sisteminin Gelir İdaresi Başkanlığı (GİB) e-Fatura servisine nasıl bağlandığını, hangi XML şemasının kullanıldığını ve entegrasyon sırasında karşılaşılan hataların nasıl çözüldüğünü anlatır.

## Giriş

e-Fatura entegrasyonu, ERP sisteminde kesilen her satış faturasının UBL-TR 1.2 formatında bir XML belgesine dönüştürülüp GİB'in özel entegratör servisine iletilmesi esasına dayanır. Entegrasyon iki bileşenden oluşur: dönüştürme motoru ve ileti kuyruğu.

## GİB Entegrasyonu Mimarisi

### Dönüştürme Motoru

Fatura kesildiği anda ERP, fatura satırlarını ve başlık bilgilerini alıp UBL-TR şemasına uygun bir XML üretir. Bu XML, imzalama servisine gönderilmeden önce yerel olarak şema doğrulamasından geçer.

### İleti Kuyruğu

Doğrulanan XML belgeleri bir ileti kuyruğuna yazılır. Kuyruk, GİB servisinin yoğun olduğu saatlerde (özellikle ayın son iş günü) belgeleri sıraya alarak zaman aşımı hatalarını azaltır.

## XML Şema Örneği

Aşağıda basitleştirilmiş bir UBL-TR fatura XML örneği verilmiştir:

```xml
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:ID>NOVA2026000123</cbc:ID>
  <cbc:IssueDate>2026-08-03</cbc:IssueDate>
  <cbc:InvoiceTypeCode>SATIS</cbc:InvoiceTypeCode>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cac:PartyName>
        <cbc:Name>Nova Ticaret A.Ş.</cbc:Name>
      </cac:PartyName>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity>10</cbc:InvoicedQuantity>
    <cac:Item>
      <cbc:Name>Endüstriyel Vida Seti</cbc:Name>
    </cac:Item>
  </cac:InvoiceLine>
</Invoice>
```

Bu şemadaki `cbc:ID` alanı, faturanın GİB nezdindeki benzersiz kimliğidir ve ERP tarafında `invoice_uuid` alanıyla eşleştirilir.

## Hata Kodları

Entegrasyon sırasında GİB servisinden dönebilecek hata kodları dört ana kategoride toplanır.

### Şema Doğrulama Hataları

#### E-1001: Eksik Zorunlu Alan

Fatura başlığında `cbc:IssueDate` veya `cbc:ID` alanlarından biri boşsa bu hata döner. Çözüm: ERP tarafındaki fatura numaralandırma servisinin çalışır durumda olduğu kontrol edilir.

#### E-1002: Geçersiz Vergi Kimlik Numarası

Alıcı firmanın vergi kimlik numarası 10 haneli değilse bu hata alınır. Çözüm: müşteri kartındaki VKN alanı düzeltilip fatura yeniden oluşturulur.

### Bağlantı Hataları

#### E-2001: Zaman Aşımı

GİB servisi 30 saniye içinde yanıt vermezse ileti kuyruğu isteği otomatik olarak 3 kez tekrar dener. Üçüncü denemede de başarısız olursa fatura "İletilemedi" statüsünde işaretlenir ve muhasebe ekibine bildirim gönderilir.

#### E-2002: Sertifika Süresi Dolmuş

ERP'nin GİB'e bağlanmak için kullandığı mali mühür sertifikasının süresi dolduğunda bu hata alınır. Sertifika yenileme süreci BT ekibi tarafından yürütülür ve genellikle 2 iş günü sürer.

## Test Ortamı

Canlıya geçmeden önce her entegrasyon GİB'in test (pilot) ortamında doğrulanmalıdır. Test ortamında üretilen faturalar gerçek mali değeri taşımaz ve otomatik olarak 24 saat sonra sistemden temizlenir.

## Canlıya Geçiş Kontrol Listesi

Canlıya geçiş öncesi aşağıdaki maddelerin tamamlanmış olması gerekir:

- Mali mühür sertifikasının canlı ortam için tanımlanmış olması
- Test ortamında en az 50 faturanın hatasız iletilmiş olması
- İleti kuyruğu izleme panelinin BT ekibine tanımlanmış olması
- Hata kodları için otomatik bildirim kurallarının aktif edilmiş olması

Bu kontrol listesindeki maddelerden herhangi biri eksikse canlıya geçiş ertelenir.
