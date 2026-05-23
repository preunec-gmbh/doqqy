# Sıkça Sorulan Sorular | PayTR

# Sıkça Sorulan Sorular

* * *

#### Genel Sorular

Genel SorularMağaza API bilgilerine nereden ulaşabilirim?

[PayTR Mağaza Paneli > Destek & Kurulum >](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfasından ulaşabilirsiniz. 

Genel Sorular Hangi dil seçenekleri var? 

Ödeme ekranında yer alan dil seçenekleri Türkçe ve İngilizce şeklindedir. Ek bir dil seçeneği bulunmamaktadır. 

Genel SorularÖdeme sayfasında “İŞLEMİ TEST MODUNDA YAPIYORSUNUZ.” Uyarısı alıyorum. Ne yapmalıyım?

Mağazanız test modunda olduğu için ilgili uyarı mesajını almaktasınız. Canlı moda geçmeden önce test işlemi yapmanız gerekmektedir. 

Genel SorularBİLDİRİM URL EKSİK / HATALI uyarısı alıyorum. Ne yapmalıyım?

Entegrasyonunuz henüz tamamlanmamıştır. Hazır bir E-Ticaret modülü kullanıyorsanız; [ PayTR Mağaza Paneli > Ayarlar ](https://www.paytr.com/magaza/ayarlar) sayfasında bulunan "Bildirim URL" başlığı altından "Değiştir" linkine tıklayarak ilgili modül / hazır site için tanımlanan butonlar yardımı ile Bildirim URL'inizi belirleyebilirsiniz. Eğer özel bir yazılım kullanıyorsanız; Entegrasyon dokümanının 2. ADIM'ında anlatılan Bildirim URL kısmını hazırlamanız gerekmektedir. 

Genel SorularLokalde çalışırken Bildirim URL’e nasıl yanıt alabilirim?

Lokalde çalışırken Bildirim URL'inize yanıt almak istiyorsanız, lokal IP adresinizi dışarıdan erişime açmanız gerekmektedir. Devamında Bildirim URL olarak IP adresiniz ile birlikte, dosya yolunu gösterecek şekilde tanımlayabilirsiniz. 

Genel SorularTest işlemini neden panelimde göremiyorum?

Yapılan test işlemini [ Mağaza Paneli > İşlem & Döküm > İşlemler ](https://www.paytr.com/magaza/islemler) sekmesinden, test siparişini yapmış olduğunuz email adresi ile arama işlemi yaparak görüntüleyebilirsiniz 

Genel SorularÖdeme işlemi sonrası ilgili işlem durumu “Devam Ediyor” olarak gözüküyor. Ne yapmalıyım?

Belirlemiş olduğunuz Bildirim URL’den OK yanıtı alamayan işlemler bildirim sürecini tamamlamadığı için durumu “Devam ediyor” olarak görünür. İşlemlerin bildirim URL üzerinden OK yanıtı dönülerek bildirim sürecinin tamamlanması gerekmektedir. Entegrasyon dokümanı 2.Adımı incelemeniz gerekmektedir. 

Genel SorularCanlı moda nasıl geçiş yapabilirim?

Test işlemini gerçekleştirdikten sonra [ PayTR Mağaza Paneli > Destek & Kurulum > Canlı Mod ](https://www.paytr.com/magaza/canli-mod) sayfasından canlı moda geçiş yapabilirsiniz. 

Genel SorularPayTR Görsellerine nasıl ulaşabilirim?

PayTR görsellerine [ link ](https://dev.paytr.com/sikca-sorulan-sorular/PayTR_Gorselleri.zip) üzerinden ulaşabilirsiniz. 

#### iFrame API

iFrame APIiFrame API ödeme çözümünde peşin fiyatına taksit ayarı nasıl yapabilirim?

[PayTR Mağaza Paneli > Yönetim & Ayarlar > Taksit ayarları ](https://www.paytr.com/magaza/pft-ayar) sayfası Peşin Fiyatına Taksit Ayarları bölümünden gerekli ayarları yapabilirsiniz. 

iFrame APITaksit tablosu için token bilgisine nasıl ulaşabilirim?

[PayTR Mağaza Paneli > Yönetim & Ayarlar > Taksit](https://www.paytr.com/magaza/pft-ayar) sayfasından ulaşabilirsiniz. 

#### Direkt API

Direkt APIDirekt API ödeme çözümünde taksit ayarları nasıl yapılmaktadır?

Bu çözümde peşin fiyatına taksit işlemleri, taksit oranlarının ayarlanması ve taksit kısıtlama gibi işlemlerin, kendi yazılımınızda veya eticaret alt yapı sağlayıcınızın sunduğu yönetim panelinde yapılmalıdır. 

#### Link API

Link APILinkle ödeme nasıl alabilirim?

Linkle ödeme alabilmeniz için mağazanıza yetki tanımlanması gerekmektedir. [PayTR Mağaza Paneli > Destek](https://www.paytr.com/magaza/destek) sayfası üzerinden talebinizi iletebilirsiniz. 

#### WordPress

WordPress- WoocommerceKurulum Modülüne nereden ulaşabilirim?

[ PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri)sayfası üzerinden web sitenizde kullanmış olduğunuz modüle uygun kurulum dosyasına ulaşabilirsiniz. 

WordPress- WoocommerceWooCommerce için taksit seçeneklerini ürün detay sayfasına nasıl ekleyebilirim?

[ PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfası üzerinde yer alan WooCommerce Taksit Tablosu modülünü kurarak ekleyebilirsiniz. 

#### OpenCart

OpenCartKurulum Modülüne nereden ulaşabilirim?

[ PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfası üzerinden web sitenizde kullanmış olduğunuz modüle uygun kurulum dosyasına ulaşabilirsiniz. 

OpenCart"PAYTR IFRAME failed. reason:payment_amount değeri en az 100 olmalıdır. gönderilen:0" şeklinde hata alıyorum.

Ürün fiyatını 1 TL üzeri işlem deneyerek işlem yapmanız gerekmektedir. 1 TL altı işlem yapılamamaktadır. 

OpenCartSitemizde bulunan ürün sayfalarına taksit seçeneği nasıl eklenir?

[ PayTR Mağaza Paneli > Taksit Ayarları ](https://www.paytr.com/magaza/pft-ayar) sekmesinden sunulan taksit tablosu kodundaki "Urun-Fiyati" alanına, ürün sayfanızda bulunan ve ürünlerin tutarını gösteren kod blogundan gelen veriyi eklemeli, her sayfa yüklendiğinde ilgili tutarın kodun içerisinde güncellemesini sağlamalısınız. 

#### Magento

MagentoKurulum Modülüne nereden ulaşabilirim?

[ PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfası üzerinden web sitenizde kullanmış olduğunuz modüle uygun kurulum dosyasına ulaşabilirsiniz. 

MagentoMagento Modülü aktifleştirirken vendor name hatasını nasıl çözebilirim?

İlgili alan değeri olarak "Paytr_Payment" kullanılabilir. Bu işlemlerin ardından komut satırından aşağıdaki komutlar sırasıyla çalıştırılması gerekmektedir. -php bin/magento module:enable Paytr_Payment --clear-static-content 

MagentoMagento Composer ile yükleme yaparken paket bulunamadı hatasını nasıl çözebilirim?

İlgili sorunu çözmek için Magento sunucusuna bağlanılması gerekmektedir. 

#### Mağaza Bildirimleri

Mağaza BildirimleriMağaza Bildirimleri sayfasında neden işlemler görüyorum?

![](https://dev.paytr.com/sikca-sorulan-sorular/images/images1.png) Mağazanız üzerinde gerçekleşen "Başarılı" veya "Başarısız" işlemler içerisinde bildirim süreci tamamlanamamış olanlar, **PayTR Mağaza Paneli > İşlemler > Mağaza Bildirimleri **sayfasında yer almaktadır. Başarılı gerçekleşen işlemlerinizden bildirim süreci tamamlanamayan olması durumunda, **PayTR Mağaza Paneli > Ana Sayfa** üzerinde uyarı gösterilmektedir.  
İşlemlerin bu alanda bulunma sebebine ait detayı, Hata Detayı; Detayı Göster alanından öğrenebilirsiniz. Bildirim Durumu; Bildirim Durdu olan işlemleriniz için bildirimin tamamlanmasına engel olan hatanın düzeltilmesi halinde, sayfa üzerinde bulunan Duran Bildirimleri Yeniden Başlat alanını kullanabilir ve yaptığınız düzenlemenin sonucu gözlemleyebilirsiniz. İlgili işlemlerin, Mağaza Bildirimleri sayfasından kaybolması halinde bildirim sürecinin başarılı şekilde tamamlandığını varsayabilirsiniz. **PayTR Mağaza Paneli > İşlemler** sayfası üzerinden işlemlerinizi takip edebilirsiniz. Hata detayı ve çözümü hakkında altyapı sağlayıcınızdan veya yazılımcınızdan destek talep edebilirsiniz. 