# Direkt API Entegrasyon Süreçleri ve Canlı Moda Geçiş | PayTR

# Direkt API Entegrasyon Süreçleri ve Canlı Moda Geçiş

**1- PayTR Sanal POS ve Direkt API Ödeme Çözümü Başvurusunun Yapılması**

<https://www.paytr.com/uye-isyeri-olun> adresinden Direkt API Ödeme çözümü kullanımı için başvuru sürecini başlatabilirsiniz.

**2- Entegrasyon Dokümanları & Örnek Kodlar**

PayTR Mağaza Paneli > Destek & Kurulum > Developer Portal sayfası üzerinde bulunan menüde yer alan [Direkt API Entegrasyonu](https://dev.paytr.com/direkt-api) başlığı altında; 1.ADIM ve 2.ADIM’a ait entegrasyon dokümanları ve birden fazla yazılım dili için geliştirilmiş, entegrasyon kod örnekleri bulunmaktadır. İlgili dokümanları yazılımcınız veya altyapı sağlayıcınız ile paylaşabilirsiniz.

**3- Entegrasyon Sırasında Kullanılacak Mağaza API Bilgilerine Ulaşılması**

Entegrasyon aşamasında kullanmanız gereken:

**\- Mağaza No** (merchant_id), 

**\- Mağaza Parola** (merchant_key), 

**\- Mağaza Gizli Anahtar** (merchant_salt),

değerlerine PayTR Mağaza Paneli > Destek & Kurulum > [ Entegrasyon Bilgileri ](https://www.paytr.com/magaza/entegrasyon-bilgileri) sayfasındaki API Entegrasyon Bilgileri başlığı altından erişebilirsiniz.

**4- Test İşlemi Sırasında Kullanılacak Test Kart Bilgilerine Ulaşılması**

Test işleminiz sırasında kullanacağınız Test Kart Bilgilerine PayTR Mağaza Paneli > Destek & Kurulum > Developer Portal sayfası üzerinde bulunan menüde yer alan [Direkt API Test Kart Bilgileri](https://dev.paytr.com/direkt-api/test-kart-bilgileri) başlığı altından ulaşabilirsiniz.

**5- Test İşleminin Gerçekleştirilmesi**

Entegrasyonun 1. ve 2. adımlarının tamamlanmasının ardından, web siteniz veya uygulamanız üzerinde hazırladığınız ödeme sayfanızı ziyaret etmeniz ve test ödemesi gerçekleştirmeniz gerekmektedir. Test ödeme işlemi esnasında, PayTR’ın sizlere sunmuş olduğu test kart bilgileri kullanılması gerekmektedir. (Bknz 4) 

Hazırlamış olduğunuz ödeme sayfanıza temin ettiğiniz test kart bilgilerini girerek, formun PayTR adresine POST edilmesini sağlayın. Entegrasyonda herhangi bir sorununuz yoksa eğer, karşınıza gelecek PayTR 3D Secure test sayfasındaki Gönder butonuna tıklayarak test ödeme işlemini tamamlayın.

**6- Test Ödeme Tahsilatının Kontrolü**

Gerçekleştirmiş olduğunuz test işlemlerine PayTR Mağaza Paneli > İşlem & Rapor > [İşlemler](https://www.paytr.com/magaza/islemler) sayfası üzerinden, işlem sırasında iletmiş olduğunuz mail adresi ile arama yaparak ulaşabilirsiniz.

**7- Canlı Moda Geçiş Talebi**

Test işleminizin başarılı olarak sonuçlanmasının ardından, PayTR Mağaza Paneli > Destek & Kurulum > [Canlı Mod](https://www.paytr.com/magaza/canli-mod) sayfasından **Evet, Entegrasyonu Tamamladım** butonuna tıklayarak yapmış olduğunuz test işlemlerinin kontrolünü başlatabilirsiniz. Test akışının başarılı şekilde sonuçlanması ardından **Canlı Moda Geçiş Talebi Gönder** butonuna tıklayarak canlı moda geçiş talebi gönderebilirsiniz. 

**8- Canlı Moda Geçiş Bilgilendirmesi**

Test işlemleriniz ve talebiniz, 7/24 destek sağlayan birimlerimizce kontrol edilir. Yapılan kontrolün ardından, mağazanızın canlı moda geçişi için herhangi bir sorun bulunmaması durumunda işlem tamamlanır ve sistemde kayıtlı cep telefonu numaranıza SMS, kayıtlı e-posta adresine ise yazılı olarak bildirimi yapılır. Alacağınız bildirimin ardından gerçek ödeme tahsilatına başlayabilirsiniz.
