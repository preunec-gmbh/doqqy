# Perfex CRM Açık Kaynaklı Altyapı | PayTR

# Perfex CRM Açık Kaynaklı Altyapı

![](/images/f/c/7/9/2/fc7926cf0557baa85388c71be44a168a0fa5f6a4-logo.png)

Dökümanda kullanılan görseller ve içerikler Perfex CRM versiyonuna göre değişiklik gösterebilir.

**Kurulum**

  1. PayTR Github hesabından ya da link üzerinden dosyaları zip olarak indirin.
  2. Perfex CRM’in kurulu olduğu ana dizine gidin ve modules klasörüne paytr_gateway isimli bir klasör oluşturun.
  3. Zip dosyasından çıkan dosyaları bu klasöre kopyalayın.
  4. Perfex CRM Yönetici paneline giriş yaparak Modüller menüsüne tıklayın.
  5. PayTR Virtual Pos iFrame API modülünü aktif yapın.



**Modül Ayarları**

**Ayarlar / Ödeme Geçitleri** menüsüne ilerleyin. Üst menüde yer alan PayTR Virtual Pos iFrame API sekmesine tıklayın. Ardından ayarları aşağıda yer alan görseldeki gibi güncelleyin.

  1. **Merchant ID** , **Merchant Key** ve **Merchant Salt** değerlerini, https://www.paytr.com/magaza/entegrasyon-bilgileri sayfasından kopyalayarak ilgili alanlara yapıştırın.
  2. PayTR Mağaza Paneli > Destek & Kurulum > Ayarlar sayfasına gidin (https://www.paytr.com/magaza/ayarlar). Ardından Bildirim URL ayarını kendi site adresinize göre güncelleyin. (**paytr_gateway/checkout_module/notify**). Örneğin https://siteadresiniz.com/paytr_gateway/checkout_module/notify



![1](/user/pages/16.moduller/10.perfex-crm/1.PNG)

**Kullanmaya Başlama**

  1. Yeni bir fatura oluşturun. Ardından müşteri hesabına giriş yaparak faturayı ödeme ekranına gelin.



![2](/user/pages/16.moduller/10.perfex-crm/2.PNG)

  2. Şimdi Öde butonuna basarak ilerleyin. Ardından ödeme işlemini gerçekleştirin.



![3](/user/pages/16.moduller/10.perfex-crm/3.PNG)

  3. Tüm işlemlerin ardından faturanız ödendi olarak görüntülenecektir.



![4](/user/pages/16.moduller/10.perfex-crm/4.PNG)

**Hatalar ve Hataların Takibi**

  1. Hata takibi için PayTR Mağaza Paneli’ni kullanabilirsiniz. Sipariş numarası veya e-posta adresi ile siparişe ulaşabilir ve detayları görüntüleyebilirsiniz.
  2. Perfex CRM Yönetici panelinde yer alan **Uygulamalar / Etkinlik Kayıtları** alanından logları kullanabilirsiniz



Perfex CRM iFrame API Ödeme Modülünü [**indirmek için tıklayın.**](/moduller/perfex-crm/perfexcrm-payment-main.zip)
