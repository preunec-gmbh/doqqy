# Prestashop Açık Kaynaklı Altyapı | PayTR

# Prestashop Açık Kaynaklı Altyapı

![](/images/8/a/e/a/b/8aeab10801fee2c3a11661cf2c0217de6852bd0e-vertical-logo-2015.png)

**ÖNEMLİ! Kurulum işlemine başlamadan önce, sisteminizde yüklü bir PayTR Ödeme Modülü varsa mutlaka kaldırılmalıdır. Aksi takdirde modül doğru şekilde çalışmayabilir.**

**Modül Kurulum Adımları**

  1. Modülün Yüklenmesi;


  * İndirdiğiniz paytr_prestashop_iframe_api_8x.zip dosyasını, PrestaShop admin panelinde yer alan “Modül Yükle” seçeneği üzerinden seçerek otomatik yükleme işlemini gerçekleştirebilirsiniz.

  * Eğer bu yöntemle yükleme yapamıyorsanız:

    * İndirdiğiniz .zip dosyasını çıkarın.
    * Sunucunuzda bulunan public_html/modules yoluna gidip paytrcheckoutisimli bir klasör oluşturun.
    * Zip’ten çıkarmış olduğunuz dosyaları paytrcheckoutisimli klasöre kopyalayın.
  * PrestaShop admin paneline giriş yapın



  2. Modülün Kurulum;


  * 1.7.X ve sürümler için;

    * Menüden Modül Kataloğu altından PayTR olarak arama yaparak modülü bulun ve yükleme işlemini gerçekleştirin.
    * Yükleme işlemi tamamlandıktan sonra Yapılandır Butonuna tıklayarak modül sayfasına ulaşabilir API Entegrasyon Bilgilerini girerek kurulumu tamamlayabilirsiniz.
    * Eğer Yapılandır Butonu görünmez ise aşağıdaki adımları takip edebilirsiniz. o Menüden Modüller başlığı altından Modül Manager sayfasına ulaşın. o Listelenmiş Modüller içerisinde Diğer başlığı altında PayTR Sanal POS modülünü bulun. o Yapılandır diyerek ilgili ayarları tamamlayın.
  * 1.6.1.x sürümleri için;

    * Menüden Modüller başlığı altından PayTR olarak arama yaparak veya Ödemeler ve Ağ Geçitlerine tıklayarak PayTR Sanal POS modülünü bulabilirsiniz.
    * Yükleme işlemi tamamlandıktan sonra Yapılandır Butonuna tıklayarak modül ayar sayfasına ulaşabilirsiniz. BİLGİ: Modül için gereken API Entegrasyon Bilgilerine https://www.paytr.com/magaza adresine ulaşarak Bilgi menüsü altında bulabilirsiniz.
  * 8.x ve Üzeri Sürümler İçin;

    * Admin panelinde sol menüden “Modül Kataloğu” bölümüne gidin.
    * Arama çubuğuna “PayTR” yazarak modülü bulun ve “Yükle” butonuna tıklayın.
    * Yükleme tamamlandıktan sonra “Yapılandır” butonuna tıklayarak modül ayar sayfasına geçin. API entegrasyon bilgilerini girerek kurulumu tamamlayın.
    * Not: Eğer “Yapılandır” butonu görünmüyorsa:
    * Menüden “Modüller” > “Modül Yöneticisi” (Module Manager) sayfasına gidin.
    * Listelenen modüller arasında “Diğer” başlığı altında “PayTR Sanal POS” modülünü bulun.
    * “Yapılandır” seçeneğine tıklayarak ayarları tamamlayın.



BİLGİ: Modül için gerekli API entegrasyon bilgilerine, https://www.paytr.com/magaza adresinden giriş yaparak “Bilgi” menüsü altında ulaşabilirsiniz.

  * **Bildirim adresinin yapılandırması;**
    * PayTR Mağaza Paneli’ne (https://www.paytr.com/magaza) giriş yapın.
    * Sol menüden "Destek&Kurulum -> Ayarlar" sekmesine tıklayın.
    * “Bildirim URL Ayarı” bölümünde yer alan “Belirle” bağlantısına tıklayın.
    * Açılan alana aşağıdaki URL’yi, url adresinizin başını sitenizin adresine göre düzenleyerek ekleyin: /index.php?fc=module&module=paytr&controller=notification
    * “Kaydet” butonuna tıklayarak ayarları kaydedin.



**\- BİLDİRİM URL HAKKINDA ÖNEMLİ BİLGİLENDİRME:** Eğer sitenizde SSL var ise, Protokol’ü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS seçimi yapmayın. Sitenizde daha sonradan SSL kurulumu yaptırırsanız, bu alana tekrar gelerek Protokolü HTTPS olarak değiştirerek kaydedin. (Bildirim URL hakkında daha fazla bilgi için, entegrasyon dokümanının 2.ADIM’ını inceleyebilirsiniz)

**\- ENTEGRASYONUN HAKKINDA ÖNEMLİ BİLGİLENDİRME** : Bildirim URL tanımı yapıldıktan sonra birkaç test ödemesi gerçekleştirerek, Paytr Mağaza Paneli > İşlemler altında Başarılı ibaresini gördükten sonra lütfen Paytr Mağaza Paneli > Destek bölümünden canlı moda geçmek için bize bilgi verin. Eğer Devam Ediyor bilgisi görüyorsanız, işlemin detayına girerek bildirim hatalarını görebilir, gerekli kontrolleri ve düzenlemeyi yapabilirsiniz.

  * SEO URL YAPILANDIRMASI: Yönlendirmelerin doğru çalışması için sitenizde SEO URL yapısının aşağıdaki görsele uygun olması gerekmektedir.



![](/user/pages/16.moduller/02.prestashop/asasa.jpg)

PrestaShop 1.6.x ve 1.7.x modülünü aşağıdan indirebilirsiniz. Ayrıca PrestaShop iFrame API Taksit Modülü kullanmak isterseniz, versiyonunuza uygun modülü indirerek ürün sayfasında taksit tablosunun görünmesini sağlayabilirsiniz.

[**PrestaShop 8x versiyonları için iFrame API**](/moduller/prestashop/paytr_prestashop_iframe_8x.zip)

[**PrestaShop 1.6.x ve 1.7.x versiyonları için iFrame API**](/moduller/prestashop/paytr_prestashop_iframe_16_17.zip)

[**PrestaShop iFrame API 1.6.x Taksit Tablosu**](/moduller/prestashop/paytr_prestashop_taksit_16.zip) \- (Kurulum dokümanı dosya içerisindedir)

[**PrestaShop iFrame API 1.7.x Taksit Tablosu**](/moduller/prestashop/paytr_prestashop_taksit_17.zip) \- (Kurulum dokümanı dosya içerisindedir)

[**PrestaShop iFrame API 8.x Taksit Tablosu**](/moduller/prestashop/paytr_prestashop_taksit_8.zip) \- (Kurulum dokümanı dosya içerisindedir)

[**PrestaShop iFrame API 9.x Taksit Tablosu**](/moduller/prestashop/paytr_prestashop_taksit_9.zip) \- (Kurulum dokümanı dosya içerisindedir)
