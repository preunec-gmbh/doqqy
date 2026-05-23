# WHMCS Açık Kaynaklı Altyapı | PayTR

# WHMCS Açık Kaynaklı Altyapı

## ![](/images/8/a/6/7/0/8a670c86a7b103b460fbf909d938920bca6bf1e0-whmcs-logo.png)

**Kurulum**

  * İndirdiğiniz zip dosyasını ayıklayın. İçerisinden çıkan dosyaları kopyalayarak **modules/gateways** klasörüne ilerleyin ve yapıştırın.  

  * Whmcs yönetim paneline giriş yaparak sırasıyla; -**Kurulum > Ödeme Ayarları > Ödeme Yöntemleri** sayfasına ilerleyin.  

  * **All Payment Gateways** butonuna tıklayarak, gelen sayfada **PayTR Virtual Pos iFrame API** eklentisini bulun.  




![1](/user/pages/16.moduller/08.whmcs/1.PNG)

-Modül bu sayfada görüntüleniyor ise sorunsuz bir şekilde kurulum yapılmıştır.  


**Ayarların Yapılması** Aşağıda yer alan görsele göre ayarları yapabilirsiniz. Gerekli API bilgilerinize PayTR Mağaza Paneli > Destek & Kurulum > Bilgi sayfasından ulaşabilirsiniz.

![2](/user/pages/16.moduller/08.whmcs/2.PNG)

**Bildirim URL (Callback URL) Ayarlarının Yapılması** ● PayTR Mağaza Paneline giriş yaparak Ayarlar sayfasına ilerleyin. ● Bildirim URL alanına site adresinizi yazarak alan adınızın sonunda yer alacak şekilde **“modules/gateways/callback/paytr.php”** değerini ekleyin

![3](/user/pages/16.moduller/08.whmcs/3.PNG)

**İade İşlemlerinin Yapılması** PayTR Virtual Pos iFrame API eklentisi ve WHMCS altyapısı ile ödemelerinizi iade edebilirsiniz. Siparişinizin altında yer alan iade et veya iptal ve iade et butonlarına basıldığında iade işlemlerinizi gerçekleştirebilirsiniz. İade işlemlerini PayTR Mağaza Paneli üzerinden takip edebilirsiniz.

[**PayTR iFrame WHMCS Ödeme Modülü**](https://marketplace.whmcs.com/product/5924-paytr-virtual-pos-iframe-api)

WHMCS iFrame API Ödeme Modülü Kurulum Dökümanı [**indirmek için tıklayın.**](/moduller/whmcs/Whmcs_7.x_-_8.x_Kullanım_Kılavuzu.zip)
