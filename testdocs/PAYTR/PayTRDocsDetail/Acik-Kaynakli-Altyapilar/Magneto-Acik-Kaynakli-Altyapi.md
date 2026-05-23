# Magneto Açık Kaynaklı Altyapı | PayTR

# Magneto Açık Kaynaklı Altyapı

![](/user/pages/16.moduller/05.magento/mgn.png)

**Modül kurulumu için yapılması gerekenler;**

Kurulum Not: Bu kurulum Magento 2.3.x ve 2.4.x versiyonlarını kapsamaktadır.

Eklentiyi composer aracılığıyla kurabilirsiniz.

  1. composer require paytr/magento2-payment
  2. bin/magento module:enable Paytr_Payment --clear-static-content
  3. bin/magento setup:upgrade
  4. php bin/magento setup:di:compile 



NOT: Bu dokümanda yer alan görseller Magento sürümünüze göre değişiklik gösterebilir.  


**Ayarların Yapılması**

  1. Magento yönetici paneline giriş yaptıktan sonra sırasıyla; a. Mağazalar/Ayarlar/Satış/Ödeme Yöntemleri sayfasına ilerleyin. b. PayTR Sanal POS ayarlarına tıklayın.
  2. Bildirim URL Adresi: Bu alanda yazan adresi kopyalayarak https://www.paytr.com/magaza/ayarlar sayfasında yer alan ilgili alana yapıştırın.
  3. Ödeme Alanı Başlığı: Ödeme metotları listesinde müşterinizin göreceği başlıktır.
  4. Merchant ID, Merchant Key ve Merchant Salt değerlerini, https://www.paytr.com/magaza/bilgi sayfasından kopyalayarak ilgili alanlara yapıştırın.
  5. Hata Ayıklama: Ödeme ekranında alacağınız hataları ekranda görüntüleyebilirsiniz.
  6. Test modu: Mağazanız canlıya geçmeye hazır ise kapatabilirsiniz. Test modu ve canlıya alma işlemleri için https://www.paytr.com/magaza/canli-mod sayfasında yer alan yönergeleri izleyiniz.
  7. Ödeme Yöntemi Sırası: Sıralamayı değiştirerek, müşterilerinizin ödeme yöntemini hangi sırada görüntüleyeceğini seçebilirsiniz.
  8. PayTR Logosu Gösterilsin mi: Ödeme yöntemi alanında PayTR logosunu gösterilip, gösterilmeyeceğini seçebilirsiniz.
  9. Taksit Ayarları: Maksimum taksit sayısını seçmenizi sağlar. Ürün Kategorilerine göre taksit seçenekleri düzenlenebilir.
  10. Taksit Tablosu Gösterilsin mi: Ürün detay sayfasında taksit tablosunun gösterilip, gösterilmeyeceğini seçebilirsiniz.
  11. Tüm Taksit Seçenekleri Taksit Tablosunda Gösterilsin mi: Taksit tablosunun tamamını veya özet olarak gösterilmesini seçebilirsiniz.
  12. Taksit Tablosu Token: Taksit tablosunun gösterilmesi için gereken token’i https://www.paytr.com/magaza/pft-ayar sayfasından kopyalayabilirsiniz.



![m1](/user/pages/16.moduller/05.magento/m1.png)

**Bildirim URL’in Ayarlanması** PayTR Mağaza Paneline giriş yapın, Destek & Kurulum menüsünden Ayarlar bağlantısına tıklayarak ayarlar sayfasına ulaşın. Bildirim URL Ayarı (Callback URL) bölümünde bulunan Değiştir butonuna tıklayın. Açılan ilgili bölümde Magento 2 seçeneğini seçin ve Kaydet butonuna basarak değişiklikleri kaydedin. Eğer sitenizde SSL varsa, Protokol seçeneğinden https:// seçeneğini seçin. Eğer SSL sertifikanız yoksa, http:// seçeneğini seçin. Daha sonradan SSL kurulumu yaparsanız buradaki Protokol’ü https:// olarak güncelleyin

![m2](/user/pages/16.moduller/05.magento/m2.png)

**Kullanmaya Başlama**

Sepetenize ürün ekleyerek ödeme sayfasına kadar ilerleyin. Ardından PayTR ödeme yöntemini seçip devam edin.

![m3](/user/pages/16.moduller/05.magento/m3.png)

Ödeme sayfasına geldiğinizde yukarıdaki ekran ile karşılaşırsınız. Eğer PayTR Mağazanız Canlı durumdaysa yukarıdaki ekran yerine Canlı Mod ekranını göreceksiniz. Test modu ekranı ile karşılaşırsanız, Canlı Moda geçmeden önce 1 veya 2 kere test işlemi yapmanız gerekmektedir. Bu bölüme kadar olan tüm adımları eksiksiz tamamladıktan sonra ödeme almaya başlayabilirsiniz.

**PayTR Havale/EFT Modülü**

Eklentiyi composer aracılığıyla kurabilirsiniz.

  1. composer require paytr/magento2-banktransfer
  2. bin/magento module:enable Paytr_Transfer --clear-static-content
  3. bin/magento setup:upgrade
  4. php bin/magento setup:di:compile 



**Ayarların Yapılması**

  1. Magento yönetici paneline giriş yaptıktan sonra sırasıyla; a. Mağazalar/Ayarlar/Satış/Ödeme Yöntemleri sayfasına ilerleyin. b. PayTR Bank Transfer ayarlarına tıklayın.
  2. Bildirim URL Adresi: Bu alanda yazan adresi kopyalayarak https://www.paytr.com/magaza/ayarlar sayfasında yer alan ilgili alana yapıştırın.
  3. Ödeme Alanı Başlığı: Ödeme metotları listesinde müşterinizin göreceği başlıktır.
  4. Merchant ID, Merchant Key ve Merchant Salt değerlerini, https://www.paytr.com/magaza/entegrasyon-bilgileri sayfasından kopyalayarak ilgili alanlara yapıştırın.
  5. Hata Ayıklama: Ödeme ekranında alacağınız hataları ekranda görüntüleyebilirsiniz.
  6. Test modu: Mağazanız canlıya geçmeye hazır ise kapatabilirsiniz. Test modu ve canlıya alma işlemleri için https://www.paytr.com/magaza/canli-mod sayfasında yer alan yönergeleri izleyiniz.
  7. Ödeme Yöntemi Sırası: Sıralamayı değiştirerek, müşterilerinizin ödeme yöntemini hangi sırada görüntüleyeceğini seçebilirsiniz.
  8. PayTR Logosu Gösterilsin mi: Ödeme yöntemi alanında PayTR logosunu gösterilip, gösterilmeyeceğini seçebilirsiniz.



**Bildirim URL’in Ayarlanması** PayTR Mağaza Paneline giriş yapın, Destek & Kurulum menüsünden Ayarlar bağlantısına tıklayarak ayarlar sayfasına ulaşın. Bildirim URL Ayarı (Callback URL) bölümünde bulunan Değiştir butonuna tıklayın. Açılan ilgili bölümde Magento 2 seçeneğini seçin ve Kaydet butonuna basarak değişiklikleri kaydedin. Eğer sitenizde SSL varsa, Protokol seçeneğinden https:// seçeneğini seçin. Eğer SSL sertifikanız yoksa, http:// seçeneğini seçin. Daha sonradan SSL kurulumu yaparsanız buradaki Protokol’ü https:// olarak güncelleyin.

**Kullanmaya Başlama**

Sepetenize ürün ekleyerek ödeme sayfasına kadar ilerleyin. Ardından PayTR ödeme yöntemini seçip devam edin. Ödeme sayfasına geldiğinizde Test modu ekranı ile karşılaşırsanız, Canlı Moda geçmeden önce 1 veya 2 kere test işlemi yapmanız gerekmektedir.

Bu bölüme kadar olan tüm adımları eksiksiz tamamladıktan sonra ödeme almaya başlayabilirsiniz.

[**Magento iFrame API Ödeme Modülü**](https://github.com/paytr/magento2-payment/archive/refs/tags/1.2.9.zip)

[**Magento iFrame API Havale/EFT Modülü**](https://github.com/paytr/magento2-banktransfer/archive/refs/tags/1.2.1.zip)
