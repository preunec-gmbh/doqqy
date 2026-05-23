# Wordpress Açık Kaynaklı Altyapı | PayTR

# Wordpress/WooCommerce Açık Kaynaklı Altyapı

![](/user/pages/16.moduller/03.wordpress/wcm.png)

**1\. Kurulum**

WordPress Yönetim Paneline giriş yaptıktan sonra;

  * **Eklentiler > Yeni Ekle** adımlarını takip edin.
  * **Arama** çubuğuna PayTR yazarak arama yapın.
  * Arama sonuçları içerisinden **PayTR Sanal POS WooCommerce – iFrame API** modülümüzü **Şimdi Kur** butonuna basarak kurulum işlemini tamamlayın.
  * Kurulum işlemi bittikten sonra **Etkinleştir** butonuna basarak modülü aktif edin.



**2\. Ayarların Yapılandırılması**

  * Kurulumu tamamladıktan sonra, **Eklentiler > Yüklü Eklentiler** adımlarını takip edin.
  * Listeden **PayTR Sanal POS WooCommerce - iFrame API** modülünün **Ayarlar** bağlantısına tıklayın. 
  * Açılan sayfada gerekli bilgileri doldurarak kaydedin.



**Mağaza No, Mağaza Parola ve Mağaza Gizli Anahtar** bilgilerinize https://www.paytr.com/magaza/bilgi adresinden ulaşabilirsiniz. Gerekli bilgileri ilgili alanlara doldurunuz.  


**Aktif/Devre Dışı:** Modülün aktif olmasını sağlar.  
**Başlık:** Ödeme metotları listesinde müşterinizin göreceği başlıktır.  
**Açıklama:** Ödeme metodu listesinde müşterinizin göreceği açıklamadır.  
**Logo:** Ödeme metodu listesinde PayTR logosunu göstermenizi sağlar.  
**Sipariş Durumu:** Başarılı ödemelerde ilgili siparişin alacağı Sipariş Durumunu seçebilirsiniz.  
**Vade Farkı:** Taksitli ödemelerde taksitten dolayı yansıyan vade farkını ilgili siparişe yansıtır.  
**Dil:** Ödeme sayfasının dilinizi ayarlamanıza yardımcı olur. Bu dil seçeneği ayrıca ödeme sayfası üzerinde de bulunur.  
**Taksit Ayarları:** Maksimum taksit sayısını seçmenizi sağlar. Ürün Kategorilerine göre taksit seçenekleri düzenlenebilir.  


**3\. Bildirim URL’in Ayarlanması**

PayTR Mağaza Paneline giriş yapın, menüden **Ayarlar** bağlantısına tıklayarak ayarlar sayfasına ulaşın. **Bildirim URL Ayarı (Callback URL)** bölümünde bulunan **Değiştir** butonuna tıklayın. Açılan ilgili bölümde **WooCommerce** seçeneğini seçin ve **Kaydet** butonuna basarak değişiklikleri kaydedin. Eğer sitenizde **SSL** varsa, Protokol seçeneğinden **https://** seçeneğini seçin. Eğer **SSL** sertifikanız yoksa, **http://** seçeneğini seçin. Daha sonradan **SSL** kurulumu yaparsanız buradaki **Protokol** ’ü **https://** olarak güncelleyin.

**4\. Kullanmaya Başlama** Sepetinize ürün ekleyerek ödeme sayfasına kadar ilerleyin.

![1](/user/pages/16.moduller/03.wordpress/1.PNG)

Ödeme sayfasına geldiğinizde yukarıdaki ekran ile karşılaşırsınız. Eğer PayTR Mağazanız Canlı durumdaysa yukarıdaki ekran yerine Canlı Mod ekranını göreceksiniz. Test modu ekranı ile karşılaşırsanız, Canlı Moda geçmeden önce 1 veya 2 kere test işlemi yapmanız gerekmektedir. Bu bölüme kadar olan tüm adımları eksiksiz tamamladıktan sonra ödeme almaya başlayabilirsiniz.

**5\. Sipariş Detayları**

**PayTR Sanal POS WooCommerce – iFrame API** modülü ile alınan siparişlerin **Özel Alanlar** bölümüne **paytr_order_id** parametresi eklenir. Bu parametre verisi **PayTR Mağaza Paneli > Satışlar** içerisindeki sipariş numarası ile aynıdır. Bu veriyi sadece yönetici görebilir.

![2](/user/pages/16.moduller/03.wordpress/2.PNG)

**Sipariş Notları** içerisine ödeme durumuna göre aşağıdaki gibi not eklenir.

![3](/user/pages/16.moduller/03.wordpress/3.PNG)

Siparişe Vade farkının yansıtılması aşağıdaki gibidir.

![4](/user/pages/16.moduller/03.wordpress/4.PNG)

**6\. İade Yapma**

Başarılı ödeme yapılmış siparişin detay sayfasından iade yapabilirsiniz. Bunun için;

![5](/user/pages/16.moduller/03.wordpress/5.PNG)

**Para İadesi** butonuna tıklayın. **İade Tutarı** alanına iade etmek istediğiniz miktarı girin. **PayTR Sanal POS** **WooCommerce – iFrame API ile iade et** butonuna basın. İşlem başarıyla tamamlandığında **Sipariş Notları** içerisine not düşecektir. Eğer **İade Tutarı** alanına veri girişi engellenmişse, ürün satırında bulunan **Toplam** ve **KDV** alanlarını kullanabilirsiniz. **İade gerekçesi PayTR Mağaza Paneline** yansıtılmaz. Sadece **Sipariş Notları** içerisine ek olarak eklenir. **Vade Farklı** ödemelerde, **lütfen vade farkını iade etmeyin.** Vade farkları sistem tarafından otomatik iade edilir. Modül ayarları içerisinde bulunan **Vade Farkı** seçeneği aktif değilse, yukarıdaki resimde bulunan **Vade Farkı** satırını görmezsiniz.

_**PayTR Mağaza Panelinden yapılan iadeler WooCommerce siparişine yansıtılmamaktadır.**_

**7\. Taksit Tablosu Modülü Yapılandırılması**

**1\. Kurulum** WordPress Yönetim Paneline giriş yaptıktan sonra;

  * Eklentiler> Yeni Ekle adımlarını takip edin.
  * Arama çubuğuna PayTR yazarak arama yapın.
  * Arama sonuçları içerisinden PayTR Taksit Tablosu WooCommerce modülümüzü Şimdi Kur butonuna basarak kurulum işlemini tamamlayın.
  * Kurulum işlemi bittikten sonra Etkinleştir butonuna basarak modülü aktif edin.



**2\. Ayarların Yapılandırılması**

  * Kurulumu tamamladıktan sonra, Eklentiler> Yüklü Eklentiler adımlarını takip edin.
  * Listeden PayTR Taksit Tablosu WooCommerce modülünün Ayarlar bağlantısına tıklayın.
  * Açılan sayfada gerekli bilgileri doldurarak kaydedin.



**Token** bilgisine https://www.paytr.com/magaza/pft-ayar adresinden ulaşabilirsiniz. Mağaza Numaranızı üst menüde bulunan Mağaza No: 000000 bölümünden alabilirsiniz. Gerekli bilgileri ilgili alanlara doldurunuz.  
**Ürün Sekme Başlığı** : Ürün Detay sayfasında bulunan sekmede görünecek başlıktır.  
**Maksimum Taksit Sayısı** : Taksit tablosunda maksimum kaç taksite kadar görüneceğini seçebilirsiniz.  
**Avantajlı Taksit** : Sadece PayTR Mağaza Panelinizden ayarladığınız avantajlı taksitleri gösterebilir veya Tüm Taksitler seçerek tüm taksit seçeneklerini gösterebilirsiniz.  
**Vergi Dahil** : Taksit tablosunun göstereceği ürün fiyatının KDV Dahil veya KDV Hariç olmasını seçebilirsiniz.  
**Sekme İçerik Başlığı** : Ürün Detay sayfasında bulunan sekmenin iç kısmında görünecek başlıktır. Boş bırakırsanız başlık görünmez.  


[**WooCommerce iFrame API Ödeme Modülü**](https://wordpress.org/plugins/paytr-sanal-pos-woocommerce-iframe-api/)

[**WooCommerce iFrame API Taksit Tablosu**](https://wordpress.org/plugins/paytr-taksit-tablosu-woocommerce/)

WooCommerce iFrame API Ödeme Modülü Kurulum Dökümanı [**indirmek için tıklayın.**](/moduller/wordpress/PayTR_Sanal_POS_WooCommerce_-_iFrame_API.zip)
