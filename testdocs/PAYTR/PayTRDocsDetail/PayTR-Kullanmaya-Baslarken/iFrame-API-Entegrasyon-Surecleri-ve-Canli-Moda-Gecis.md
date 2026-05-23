# iFrame API Entegrasyon Süreçleri ve Canlı Moda Geçiş | PayTR

# iFrame API Entegrasyon Süreçleri ve Canlı Moda Geçiş

# 

**1- PayTR Sanal POS ve iFrame API Ödeme Çözümü Başvurusunun Yapılması**

<https://www.paytr.com/uye-isyeri-olun> adresinden iFrame API Ödeme çözümü kullanımı için başvuru sürecini başlatabilirsiniz.

**2- Entegrasyon Dokümanları & Örnek Kodlar**

PayTR Mağaza Paneli > Destek & Kurulum > Developer Portal sayfası üzerinde bulunan menüde yer alan [iFrame API Entegrasyonu](https://dev.paytr.com/iframe-api) başlığı altında 1.ADIM ve 2.ADIM’a ait entegrasyon dokümanları ve birden fazla yazılım dili için geliştirilmiş, entegrasyon kod örnekleri bulunmaktadır. İlgili dokümanları yazılımcınız veya altyapı sağlayıcınız ile paylaşabilirsiniz.

**3- Entegrasyon Sırasında Kullanılacak Mağaza API Bilgilerine Ulaşılması**

Entegrasyon aşamasında kullanmanız gereken:

**\- Mağaza No** (merchant_id), 

**\- Mağaza Parola** (merchant_key), 

**\- Mağaza Gizli Anahtar** (merchant_salt),

değerlerine PayTR Mağaza Paneli > Destek & Kurulum > [ Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfasındaki API Entegrasyon Bilgileri başlığı altından erişebilirsiniz.

**4- Test İşlemi Sırasında Kullanılacak Test Kart Bilgilerine Ulaşılması**

iFrame API Ödeme çözümünün başarılı şekilde entegre edilmesi sonucunda PayTR tarafından hazırlanan ortak ödeme ekranı sunulmaktadır. Test işleminiz sırasında kullanmanız gereken test kart bilgileri, ödeme sayfası üzerinde ön tanımlı olarak yer almaktadır. Bu sebeple, test kart bilgisinin tarafınızdan değiştirilmesine veya girilmesine ihtiyaç bulunmamaktadır.

**5- Test İşleminin Gerçekleştirilmesi**

Entegrasyonun 1. ve 2. adımlarının tamamlanmasının ardından, web siteniz veya uygulamanız üzerinde hazırladığınız ödeme sayfanızı ziyaret etmeniz ve test ödemesi gerçekleştirmeniz gerekmektedir. Ulaşmış olduğunuz ödeme sayfasına ön tanımlı olarak gelen test kart bilgileri sayesinde Ödeme Yap butonuna tıklamanız, ödeme akışını başlatmanız için yeterlidir. Entegrasyonda herhangi bir sorununuz yoksa, karşınıza gelecek PayTR 3D Secure test sayfasındaki Gönder butonuna tıklayarak test ödeme işlemini tamamlayabilirsiniz.

**6- Test Ödeme Tahsilatının Kontrolü**

Gerçekleştirmiş olduğunuz test işlemlerine PayTR Mağaza Paneli > İşlem & Rapor > [İşlemler](https://www.paytr.com/magaza/islemler) sayfası üzerinden, işlem esnasında iletmiş olduğunuz e-posta adresi ile arama yaparak ulaşabilirsiniz.

**7- Ödeme ve iFrame Sayfası Ayarlarının Yapılması**

**Mağaza API Bilgileri**

Entegrasyon aşamasında kullanmanız gereken API Entegrasyon Bilgilerinize PayTR Mağaza Paneli > Destek & Kurulum > [ Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfasından erişebilirsiniz. 

**Sayfa Renk Düzenlemesi**

PayTR Mağaza Paneli > Destek & Kurulum > [Ayarlar](https://www.paytr.com/magaza/ayarlar) sayfasından ödeme sayfanızın renk düzenlemesini ayarlayabilirsiniz. 

**Taksit Tablosu Token**

PayTR Mağaza Paneli > Yönetim & Ayarlar > [Taksit Ayarları](https://www.paytr.com/magaza/pft-ayar) sayfasından taksit tablosu ile ilgili kodlara erişebilir ve web sitenize taksit tablosu yerleştirebilirsiniz.

**Peşin Fiyatına Taksit Ayarları**

PayTR Mağaza Paneli > Yönetim & Ayarlar > [Taksit Ayarları](https://www.paytr.com/magaza/pft-ayar) sayfasından Peşin Fiyatına taksit alanından; müşterilerinize Peşin Fiyatına Taksit imkanı sunmak istemeniz durumunda gerekli ayarları yapabilirsiniz.

**8- Canlı Moda Geçiş Talebi**

Test işleminizin başarılı olarak sonuçlanmasının ardından, PayTR Mağaza Paneli > Destek & Kurulum > [Canlı Mod](https://www.paytr.com/magaza/canli-mod) sayfasından **Evet, Entegrasyonu Tamamladım** butonuna tıklayarak yapmış olduğunuz test işlemlerinin kontrolünü başlatabilirsiniz. Test akışının başarılı şekilde sonuçlanması ardından **Canlı Moda Geçiş Talebi Gönder** butonuna tıklayarak canlı moda geçiş talebi gönderebilirsiniz. 

**9- Canlı Moda Geçiş Bilgilendirmesi**

Test işlemleriniz ve talebiniz, 7/24 destek sağlayan birimlerimizce kontrol edilir. Yapılan kontrolün ardından, mağazanızın canlı moda geçişi için herhangi bir sorun bulunmaması durumunda işlem tamamlanır ve sistemde kayıtlı cep telefonu numaranıza SMS, kayıtlı e-posta adresine ise yazılı olarak bildirimi yapılır. Alacağınız bildirimin ardından gerçek ödeme tahsilatına başlayabilirsiniz.
