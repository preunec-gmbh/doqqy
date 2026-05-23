# PayTR Dokümantasyonu

Bu doküman, PayTR geliştirici portalındaki tüm sayfaların birleştirilmiş halidir.

# PayTR Geliştirici Merkezi


# PayTR Kullanmaya Başlarken

**PayTR Nedir?**  
PayTR Sanal POS ve Ödeme Çözümleri, web sitesi sahiplerinin en hızlı ve en kolay şekilde web sitelerinden güvenli online ödemeler almalarına imkan tanıyan bir servistir. Aidat ücreti bulunmayan PayTR, web sitelerine kolayca entegre edilerek çok kısa sürede kullanıma açılabilmektedir.

##  PayTR **hızlı** **güvenilir** **kolay**

**PayTR Nasıl Çalışır?**  
PayTR ile ödeme süreci aşağıdaki gibi işler:

Müşteri ürünün/hizmetin sergilendiği web sitesine ulaşır. Satın almak istediği ürünü/hizmeti belirler. Ödeme formunu sitede doldurur "veya" ortak ödeme sayfasına yönlenir. PayTR'a herhangi bir üyelik gerçekleştirmeden ödemesini tamamlar. Ödeme işlemi güvenlik alt yapısı tarafından doğrulanarak onaylanır. Web sitesine ödemenin güvenli ve başarılı olduğu bilgisi verilir. Ürün/hizmet web sitesi tarafından müşteriye sunulur.

**PayTR'ın Avantajları Nelerdir?**   
PayTR ödeme çözümlerini tercih etmeniz için birkaç neden:

Çalışma seçenekleri uygundur, aidat veya gizli ücretler yoktur. Entegrasyon süreci kolay ve hızlı işler, hazır modüller ve örnek kodlama sunulur. Ödeme güvenliği sağlanır; mağazalar ve müşterileri sahtecilikten korunur. Üye işyerleri "Ertesi İş Günü" ödeme alma avantajından faydalanır. Ödeme sayfasını sitenizin tasarımına göre özelleştirebilirsiniz. Mobil uyumlu ödeme sayfaları ile platform bağımsız ödeme alabilirsiniz.

![](/user/pages/01.home/aaa.png)

Teknik entegrasyon dokümanı; Pro API için açıklamalar, yönlendirmeler ve örnek kodlama içermektedir. 

__**Gelişmiş API (Pro API)**  


* * *

Tüm yazılım dilleriyle uyumlu bu çözümü kolayca entegre ederek, gömülü ödeme formu ile müşterilerinizin sitenizden ayrılmasına gerek kalmadan güvenli ödemeler almaya başlayın.  
  
__Tüm Yazılımlar İle Uyumlu  
__Kolay Entegrasyon, Hazır Kod Örnekleri  
__Hazır Modüller (OpenCart, Woocommerce, Prestashop, WHMCS, ve benzeri.)  
__PCI-DSS Uyumu Gerekli Değildir.

  


__**Kolay API (Basic API)**  


* * *

Tüm yazılım dilleriyle uyumlu bu çözümü kolayca entegre ederek, gömülü ödeme formu ile müşterilerinizin sitenizden ayrılmasına gerek kalmadan güvenli ödemeler almaya başlayın.  
  
__Entegrasyon Yok (Yazılım bilgisi gerekli değildir)  
__PCI-DSS Uyumu Gerekli Değildir  
__5 Dakikada Ödeme Almaya Başlayın  


  



---

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


---

# Linkle Ödeme Çözümü Entegrasyon Süreçleri ve Canlı Mod | PayTR


# Linkle Ödeme Çözümü Entegrasyon Süreçleri ve Canlı Moda Geçiş

**1- Linkle Ödeme Başvurusunun Yapılması**

<https://paytr.com/magaza/linkle-odeme-basvuru> adresinden Linkle Ödeme başvuru sürecini başlatabilirsiniz.

**2- Test Ödeme Linki Oluşturma**

Onaylanan başvurunuz sonrasında, PayTR Mağaza Paneli içerisinde bulunan Linkle Ödeme https://www.paytr.com/magaza/linkle-odeme sayfasına erişebilirsiniz. Linkle Ödeme sayfasında bulunan PayTR Ödeme Linki Oluştur butonu ile oluşturmak istediğiniz link türünü (Ürün/Hizmet veya Fatura/Cari) seçerek sürece devam edebilirsiniz.

**3- Ödeme Linki Ayarların Yapılması**

Link türü seçmenizin ardından açılan sayfada ilgili alanları alacağınız tahsilat doğrultusunda doldurun. Taksit seçeneklerini açmak istemeniz durumunda, Peşin Fiyatına Taksit ayarlaması yapabilirsiniz. 

**Peşin Fiyatına Taksit** ayarları açıklamaları şu şekildedir:

**Ayar Yok**

Bu seçeneği işaretlemeniz durumunda, seçmiş olduğunuz taksit sayıları belirlenen komisyon oranları çerçevesinde müşteriden tahsil edilecek ve herhangi bir Peşin Fiyatına Taksit koşulu uygulanmayacaktır.

**Mağaza Varsayılanı**

İlgili alanı seçmeniz durumunda PayTR Mağaza Paneli > Destek & Kurulum > [Taksit Ayarları](https://www.paytr.com/magaza/pft-ayar) sayfasında bulunan Peşin Fiyatına Taksit alanında tanımlı olan taksit ayalarınız, oluşturulan link üzerinde geçerli olacaktır.

**Özel Ayarlar**

İlgili alanı seçmeniz durumunda oluşturacağınız linkinize özel Peşin Fiyatına taksit ayarları yapabilirsiniz. Bu ayarlar sadece ilgili link üzerinde geçerli olacaktır.

**4- Ödeme Linkinin Gönderimi**

Oluşturmuş olduğunuz linkleri Ödeme Linkleriniz alanında görüntüleyebilirsiniz. 

E-Posta, SMS gönderimini sunulmuş olan hizmet çerçevesinde PayTR aracılığı ile iletebilirsiniz. Dilerseniz bağlantıyı kendi belirleyeceğiniz alanlara yerleştirebilir veya dilediğiniz şekilde paylaşabilirsiniz. Ayrıca QR Kod oluşturma seçeneği ile ödeme linkiniz için QR üretebilir ve dilediğiniz alanda kullanabilirsiniz.

**5- Test Ödeme Tahsilatına Başlama**

Oluşturmuş olduğunuz Ödeme Linki’ni tarayıcınızda açarak, PayTR tarafından sunulmuş ödeme sayfasına ulaşabilirsiniz. Ulaşılan sayfa üzerinden sunulan alanların eksiksiz olarak doldurulması sonrasında Ödeme Sayfasına Devam Et butonu ile ödeme adımına geçebilirsiniz.

**6- Test Ödeme Tahsilatının Tamamlanması**

Açılan ödeme sayfasına ön tanımlı olarak gelen Test kart bilgileri sayesinde Ödeme Yap butonuna tıklamanızın ardından PayTR’a ait Test 3D Secure sayfasında Gönder butonuna tıklayarak test ödeme işlemini sonuçlandırabilirsiniz.

**7- Test Ödeme Tahsilatının Kontrolü**

Test işleminizin başarılı olarak sonuçlanmasının ardından, PayTR Mağaza Paneli > Destek & Kurulum > [Canlı Mod](https://www.paytr.com/magaza/canli-mod) sayfasından **Evet, Entegrasyonu Tamamladım** butonuna tıklayarak yapmış olduğunuz test işlemlerinin kontrolünü başlatabilirsiniz. Test akışının başarılı şekilde sonuçlanması ardından **Canlı Moda Geçiş Talebi Gönder** butonuna tıklayarak canlı moda geçiş talebi gönderebilirsiniz. 

**8- Canlı Moda Geçiş Bilgilendirmesi**

Test işlemleriniz ve talebiniz, 7/24 destek sağlayan birimlerimizce kontrol edilir. Yapılan kontrolün ardından, mağazanızın canlı moda geçişi için herhangi bir sorun bulunmaması durumunda işlem tamamlanır ve sistemde kayıtlı cep telefonu numaranıza SMS, kayıtlı e-posta adresine ise yazılı olarak bildirimi yapılır. Alacağınız bildirimin ardından gerçek ödeme tahsilatına başlayabilirsiniz.


---

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


---

# iFrame API Entegrasyonu | PayTR


# iFrame API Entegrasyonu

**ENTEGRASYON HAKKINDA ÖNEMLİ ÖN BİLGİLENDİRME:** **Mağaza Bilgileri:**  
Entegrasyon için gerekli olan API entegrasyon bilgilerine Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri bölümünden ulaşabilirsiniz. (Bu bilgileri sadece Ana Kullanıcı ve Teknik kullanıcı görüntülüyebilir.)  
**Entegrasyon 2 Adımlıdır:**

  1. ADIM - PayTR'a arka planda (server-side) istek yapılarak iframe_token alınması ve alınan iframe_token ile iframe TAG’ı kullanılarak ödeme formunun açılması.  

  2. ADIM - PayTR sisteminin ödeme sonuçlarını bildireceği, sitenizin bildirim sayfasının (Bildirim URL) ayrı olarak hazırlanıp kodlanması.



Yardım talepleriniz için Mağaza panelindeki Destek Sayfasından mesajlarınızı göndermenizi rica ederiz.

Web siteniz veya uygulamanız üzerinde kullanabileceğiniz, PayTR görsellerini indirmek için [ tıklayın. ](https://dev.paytr.com/sikca-sorulan-sorular/PayTR_Gorselleri.zip)

iFrame API dokümanı ve tüm servisleri indirmek için [**tıklayın.**](/iframe-api/PayTR_IFrame_API.zip)


---

# iFrame API 1. Adım | PayTR


# iFrame API 1. Adım

1- iFrame Token istediğinde bulunabilmek için tabloda belirtilen bilgileri POST ile ilgili URL’e gönderin: https://www.paytr.com/odeme/api/get-token   
Bu istek arka planda (server-side) POST metodu ile gerçekleşir.

**POST REQUEST içeriğinde gönderilecek değerler:**   
  


Alan adı / tipi | Zorunlu | Token | Açıklama | Kısıtlar  
---|---|---|---|---  
merchant_id(string) | Evet | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası |   
user_ip (string) | Evet | Evet | Müşteri ip: İstek anında aldığınız müşteri ip numarası(Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | En fazla 39 karakter (ipv4)  
merchant_oid(string) | Evet | Evet | Mağaza sipariş no: Satış işlemi içinbelirlediğiniz benzersiz sipariş numarası.(Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | En fazla 64 karakter,Alfa numerik  
email (string) | Evet | Evet | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | En fazla 100 karakter  
payment_amount(integer) | Evet | Evet | Ödeme tutarı: Siparişe ait toplam ödeme tutarı.(Tutarı 100 ile çarparak göndermelisiniz) | Örn: 34.56 için 3456gönderilmelidir.(34.56 * 100 = 3456)  
currency(string) | Evet | Evet | Para birimi | TL(veya TRY), EUR, USD, GBP,RUB (Boş ise TL kabul edilir)  
user_basket(string) | Evet | Evet | Sepet içeriği: Müşterinin siparişindeki ürün/hizmet bilgilerini içermelidir | Nasıl bir yapıda olacağı ile ilgili olarak örnek kodlara bakmalısınız  
no_installment(int) | Evet | Evet | Taksit görüntülenmesin: Eğer 1 olarak gönderilirse taksit seçenekleri gösterilmez(Örn. cep telefonu için taksit yasağı vardır) | 0 veya 1  
max_installment(int) | Evet | Evet | En fazla taksit sayısı: Gösterilecek en fazlataksit sayısını belirler (Örn. kuyum harcamalarında en fazla 4 taksit uygulamasıvardır) | 0,2,3,4,5,6,7,8,9,10,11,12 Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur  
paytr_token(string) | Evet | Hayır | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız  
user_name(string) | Evet | Hayır | Müşteri adı ve soyadı: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız adı ve soyadı | En fazla 60 karakter  
user_address(string) | Evet | Hayır | Müşteri adresi: Müşterinin sipariş sırasında ilettiği adresi | En fazla 400 karakter  
user_phone(string) | Evet | Hayır | Müşteri telefon numarası: Müşterinin sipariş sırasında ilettiği telefon numarası | En fazla 20 karakter  
merchant_ok_url | Evet | Hayır | Müşterinin başarılı ödeme sonrası yönlendirileceği sayfa (Örn. Siparişlerim takip sayfası) | En fazla 400 karakter  
merchant_fail_url | Evet | Hayır | Müşterinin ödemesi sırasında beklenmeyen bir hatada yönlendirileceği sayfa | En fazla 400 karakter  
test_mode | Hayır | Evet | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | 0 veya 1  
debug_on (int) | Hayır | Hayır | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | 0 veya 1  
timeout_limit(int) | Hayır | Hayır | Sıfırdan farklı bir değer gönderilmesi durumunda, ödeme işlemi bu süre içerisinde tamamlanmalıdır. (Ödeme sırasındasisteminizde fiyat güncellemesi olmasıdurumuna karşı güvenlik amaçlı kullanabilirsiniz) | Dakika cinsinden(Gönderilmemesi durumunda 30 dakika olarak tanımlanır)  
lang(string) | Hayır | Hayır | Ödeme sürecinde sayfalarda kullanılacak dil | Türkçe için tr veya İngilizce içinen(Boş gönderilirse tr geçerli olur)  
  
  
  


* **iframe_token** isteğine verilen yanıt (RESPONSE) JSON formatındadır:
    
    
    - Başarılı yanıt örneği: (token içerir)
    {"status":"success","token":"28cc613c3d7633cfa4ed0956fdf901e05cf9d9cc0c2ef8db54fa"}
    
    
    - Başarısız yanıt örneğı:
    {"status":"failed","reason":"Zorunlu alan degeri gecersiz: merchant_id"}

Üye İşyeri, başarılı yanıt içerisinde gelen **iframe_token** ile iframe TAG’ı kullanarak ödeme formunu açar. Aşağıdaki HTML kod, gelen **iframe_token** değeri yerleştirilerek kullanılmalıdır. 
    
    
    <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
    <iframe src="https://www.paytr.com/odeme/guvenli/iframe_token" id="paytriframe" frameborder="0"
    scrolling="no" style="width: 100%;"></iframe>
    <script>iFrameResize({},'#paytriframe');</script>

Yukarıda anlatılan aşamaların tamamlanmasıyla birlikte, müşteri tarafından kullanılacak olan ödeme formu ekranda belirecektir. Ödeme işleminde müşterinin etkileşimde bulunacağı kısım entegrasyonda böylece tamamlanmış olur. _ANCAK; entegrasyonunuz henüz tamamlanmamıştır_ , 2. ADIM ödeme sonucunu (başarılı/başarısız) almanız ve siparişi onaylamanız / iptal etmeniz için gereklidir

**ÖNEMLİ UYARI:** PayTR ödeme alt yapısı asenkron olarak çalışmaktadır. Bu nedenle ödeme tamamlandığında müşteri merchant_ok_url'e yönlendirilirken, ödemenin kesin sonucu (Başarılı ya da Başarısız sonucu) Bildirim URL'ye POST ile gönderilmektedir. merchant_ok_url'e herhangi bir veri POST edilmemektedir, bu nedenle merchant_ok_url olarak belirttiğiniz sayfada sipariş onay/iptal gibi işlem yapmamalısınız. 

![](/user/pages/02.iframe-api/iframe-api-1-adim/odeme.png)

  * PHP
  * Python
  * .NET
  * NODEJS


    
    
    <!doctype html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Örnek Ödeme Sayfası</title>
    </head>
    <body>
    
    <div>
        <h1>Örnek Ödeme Sayfası</h1>
        <p>1. ADIM için örnek kodlar</p>
    </div>
    <br><br>
    
    <div style="width: 100%;margin: 0 auto;display: table;">
    
        <?php
    
        ## 1. ADIM için örnek kodlar ##
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        #
        ## Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
        $email = "XXXXXXXX";
        #
        ## Tahsil edilecek tutar.
        $payment_amount = ""; //9.99 için 9.99 * 100 = 999 gönderilmelidir.
        #
        ## Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
        $merchant_oid = "";
        #
        ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
        $user_name = "";
        #
        ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
        $user_address = "";
        #
        ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
        $user_phone = "";
        #
        ## Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
        ## !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
        ## !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
        $merchant_ok_url = "http://www.siteniz.com/odeme_basarili.php";
        #
        ## Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
        ## !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
        ## !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
        $merchant_fail_url = "http://www.siteniz.com/odeme_hata.php";
        #
        ## Müşterinin sepet/sipariş içeriği
        $user_basket = "";
        #
        /* ÖRNEK $user_basket oluşturma - Ürün adedine göre array'leri çoğaltabilirsiniz
        $user_basket = base64_encode(json_encode(array(
            array("Örnek ürün 1", "18.00", 1), // 1. ürün (Ürün Ad - Birim Fiyat - Adet )
            array("Örnek ürün 2", "33.25", 2), // 2. ürün (Ürün Ad - Birim Fiyat - Adet )
            array("Örnek ürün 3", "45.42", 1)  // 3. ürün (Ürün Ad - Birim Fiyat - Adet )
        )));
        */
        ############################################################################################
    
        ## Kullanıcının IP adresi
        if( isset( $_SERVER["HTTP_CLIENT_IP"] ) ) {
            $ip = $_SERVER["HTTP_CLIENT_IP"];
        } elseif( isset( $_SERVER["HTTP_X_FORWARDED_FOR"] ) ) {
            $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
        } else {
            $ip = $_SERVER["REMOTE_ADDR"];
        }
    
        ## !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
        ## buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
        $user_ip=$ip;
        ##
    
        ## İşlem zaman aşımı süresi - dakika cinsinden
        $timeout_limit = "30";
    
        ## Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
        $debug_on = 1;
    
        ## Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
        $test_mode = 0;
    
        $no_installment = 0; // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
    
        ## Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
        ## Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
        $max_installment = 0;
    
        $currency = "TL";
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $hash_str = $merchant_id .$user_ip .$merchant_oid .$email .$payment_amount .$user_basket.$no_installment.$max_installment.$currency.$test_mode;
        $paytr_token=base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
        $post_vals=array(
                'merchant_id'=>$merchant_id,
                'user_ip'=>$user_ip,
                'merchant_oid'=>$merchant_oid,
                'email'=>$email,
                'payment_amount'=>$payment_amount,
                'paytr_token'=>$paytr_token,
                'user_basket'=>$user_basket,
                'debug_on'=>$debug_on,
                'no_installment'=>$no_installment,
                'max_installment'=>$max_installment,
                'user_name'=>$user_name,
                'user_address'=>$user_address,
                'user_phone'=>$user_phone,
                'merchant_ok_url'=>$merchant_ok_url,
                'merchant_fail_url'=>$merchant_fail_url,
                'timeout_limit'=>$timeout_limit,
                'currency'=>$currency,
                'test_mode'=>$test_mode
            );
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/get-token");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    
         // XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
         // aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
         // curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR IFRAME connection error. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='success')
            $token=$result['token'];
        else
            die("PAYTR IFRAME failed. reason:".$result['reason']);
        #########################################################################
    
        ?>
    
        <!-- Ödeme formunun açılması için gereken HTML kodlar / Başlangıç -->
        <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
        <iframe src="https://www.paytr.com/odeme/guvenli/<?php echo $token;?>" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
        <script>iFrameResize({},'#paytriframe');</script>
        <!-- Ödeme formunun açılması için gereken HTML kodlar / Bitiş -->
    
    </div>
    
    <br><br>
    </body>
    </html>
    
    
    
    # Python 3.6+
    # 1. ADIM için örnek kodlar
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'YYYYYYYYYYYYYY'
    merchant_salt = b'ZZZZZZZZZZZZZZ'
    
    # Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
    email = 'XXXXXXXX'
    
    # Tahsil edilecek tutar.
    payment_amount = '' # 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    
    # Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    merchant_oid = ''
    
    # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
    user_name = ''
    
    # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
    user_address = ''
    
    # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
    user_phone = ''
    
    # Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    # !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    # !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
    merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php'
    
    # Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    # !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    # !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
    merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php'
    
    # Müşterinin sepet/sipariş içeriği
    user_basket = ''
    
    # ÖRNEK $user_basket oluşturma - Ürün adedine göre array'leri çoğaltabilirsiniz
    """
    user_basket = base64.b64encode(json.dumps([['Örnek ürün 1', '18.00', 1],
                   ['Örnek ürün 2', '33.25', 2],
                   ['Örnek ürün 3', '45.42', 1]]).encode())
    """
    
    # !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
    # buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
    user_ip = ''
    
    # İşlem zaman aşımı süresi - dakika cinsinden
    timeout_limit = '30'
    
    # Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    debug_on = '1'
    
    # Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    test_mode = '1'
    
    no_installment = '0' # Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
    
    # Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    # Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    max_installment = '0'
    
    currency = 'TL'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + user_basket.decode() + no_installment + max_installment + currency + test_mode
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': paytr_token,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['token'])
    
        """
        context = {
            'token': res['token']
        }
        """
    else:
        print(result.text)
    
    """
    # Ödeme formunun açılması için gereken HTML kodlar / Başlangıç #
    
    <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
    <iframe src="https://www.paytr.com/odeme/guvenli/{ token }" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
    <script>iFrameResize({},'#paytriframe');</script>
    
    # Ödeme formunun açılması için gereken HTML kodlar / Bitiş #
    """
    
    
    // 1. ADIM için örnek kodlar
    
    using Newtonsoft.Json.Linq; // Bu satırda hata alırsanız, site dosyalarınızın olduğu bölümde bin isimli bir klasör oluşturup içerisine Newtonsoft.Json.dll adlı DLL dosyasını kopyalayın.
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Linq;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    namespace WebApplication3
    {
        public partial class _Default : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
            //
            // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
            string merchant_id = "XXXXXX";
            string merchant_key = "YYYYYYYYYYYYYY";
            string merchant_salt = "ZZZZZZZZZZZZZZ";
            //
            // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
            string emailstr = "ZZZZZZZZZZZZZZ";
            //
            // Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
            int payment_amountstr = ;
            //
            // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
            string merchant_oid = "";
            //
            // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
            string user_namestr = "";
            //
            // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
            string user_addressstr = "";
            //
            // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
            string user_phonestr = "";
            //
            // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
            // !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
            // !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
            string merchant_ok_url = "http://www.siteniz.com/basarili";
            //
            // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
            // !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
            // !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
            string merchant_fail_url = "http://www.siteniz.com/basarisiz";
            //        
            // !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
            // buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
            string user_ip = Request.ServerVariables["HTTP_X_FORWARDED_FOR"];
            if (user_ip == "" || user_ip == null)
            {
                user_ip = Request.ServerVariables["REMOTE_ADDR"];
            }
            //
            // ÖRNEK user_basket oluşturma - Ürün adedine göre object'leri çoğaltabilirsiniz
            object[][] user_basket = {
                new object[] {"Örnek ürün 1", "18.00", 1}, // 1. ürün (Ürün Ad - Birim Fiyat - Adet)
                new object[] {"Örnek ürün 2", "33.25", 2}, // 2. ürün (Ürün Ad - Birim Fiyat - Adet)
                new object[] {"Örnek ürün 3", "45.42", 1}, // 3. ürün (Ürün Ad - Birim Fiyat - Adet)
                };
            /* ############################################################################################ */
    
            // İşlem zaman aşımı süresi - dakika cinsinden
            string timeout_limit = "30";
            //
            // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
            string debug_on = "1";
            //
            // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
            string test_mode = "1";
            //
            // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
            string no_installment = "0";
            //
            // Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
            // Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
            string max_installment = "0";
            //
            // Para birimi olarak TL, EUR, USD gönderilebilir. USD ve EUR kullanmak için kurumsal@paytr.com 
            // üzerinden bilgi almanız gerekmektedir. Boş gönderilirse TL geçerli olur.
            string currency = "TL";
            //
            // Türkçe için tr veya İngilizce için en gönderilebilir. Boş gönderilirse tr geçerli olur.
            string lang = "";
    
            // Gönderilecek veriler oluşturuluyor
            NameValueCollection data = new NameValueCollection();
            data["merchant_id"] = merchant_id;
            data["user_ip"] = user_ip;
            data["merchant_oid"] = merchant_oid;
            data["email"] = emailstr;
            data["payment_amount"] = payment_amountstr.ToString();
            //
            // Sepet içerği oluşturma fonksiyonu, değiştirilmeden kullanılabilir.
            JavaScriptSerializer ser = new JavaScriptSerializer();
            string user_basket_json = ser.Serialize(user_basket);
            string user_basketstr = Convert.ToBase64String(Encoding.UTF8.GetBytes(user_basket_json));
            data["user_basket"] = user_basketstr;
            //
            // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
            string Birlestir = string.Concat(merchant_id, user_ip, merchant_oid, emailstr, payment_amountstr.ToString(), user_basketstr, no_installment, max_installment, currency, test_mode, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            data["paytr_token"] = Convert.ToBase64String(b);
            //
            data["debug_on"] = debug_on;
            data["test_mode"] = test_mode;
            data["no_installment"] = no_installment;
            data["max_installment"] = max_installment;
            data["user_name"] = user_namestr;
            data["user_address"] = user_addressstr;
            data["user_phone"] = user_phonestr;
            data["merchant_ok_url"] = merchant_ok_url;
            data["merchant_fail_url"] = merchant_fail_url;
            data["timeout_limit"] = timeout_limit;
            data["currency"] = currency;
            data["lang"] = lang;
    
            using (WebClient client = new WebClient())
            {
                client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/get-token", "POST", data);
                string ResultAuthTicket = Encoding.UTF8.GetString(result);
                dynamic json = JValue.Parse(ResultAuthTicket);
    
                if (json.status == "success")
                { 
                    paytriframe.Attributes["src"] = "https://www.paytr.com/odeme/guvenli/" + json.token;
                    paytriframe.Visible = true;
                }
                else
                {
                    Response.Write("PAYTR IFRAME failed. reason:" + json.reason + "");
                }
            }
        }
    }
    
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'YYYYYYYYYYYYYY';
    var merchant_salt = 'ZZZZZZZZZZZZZZ';
    var basket = JSON.stringify([
        ['Örnek Ürün 1', '18.00', 1],
        ['Örnek Ürün 2', '33.25', 2],
        ['Örnek Ürün 3', '45.42', 1]
    ]);
    var user_basket = nodeBase64.encode(basket);
    var merchant_oid = "IN" + microtime.now(); // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    // Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    // Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    var max_installment = '0';
    var no_installment = '0'  // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın.
    var user_ip = '';
    var email = 'XXXXXXXX'; // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi.
    var payment_amount = 100; // Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    var currency = 'TL';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var user_name = ''; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
    var user_address = ''; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
    var user_phone = '05555555555'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
    
    // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php';
    // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php';
    var timeout_limit = 30; // İşlem zaman aşımı süresi - dakika cinsinden
    var debug_on = 1; // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    var lang = 'tr'; // Türkçe için tr veya İngilizce için en gönderilebilir. Boş gönderilirse tr geçerli olur.
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${user_basket}${no_installment}${max_installment}${currency}${test_mode}`;
    
        var paytr_token = hashSTR + merchant_salt;
    
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        var options = {
            method: 'POST',
            url: 'https://www.paytr.com/odeme/api/get-token',
            headers:
                { 'content-type': 'application/x-www-form-urlencoded' },
            formData: {
                merchant_id: merchant_id,
                merchant_key: merchant_key,
                merchant_salt: merchant_salt,
                email: email,
                payment_amount: payment_amount,
                merchant_oid: merchant_oid,
                user_name: user_name,
                user_address: user_address,
                user_phone: user_phone,
                merchant_ok_url: merchant_ok_url,
                merchant_fail_url: merchant_fail_url,
                user_basket: user_basket,
                user_ip: user_ip,
                timeout_limit: timeout_limit,
                debug_on: debug_on,
                test_mode: test_mode,
                lang: lang,
                no_installment: no_installment,
                max_installment: max_installment,
                currency: currency,
                paytr_token: token,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.render('layout', { iframetoken: res_data.token });
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
    
        // ÖNEMLİ UYARILAR!
        // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        var callback = req.body;
    
        // POST değerleri ile hash oluştur.
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        if (callback.status == 'success') {
            //basarili
        } else {
            //basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

  


iFrame API 1. Adım örnek kodları[**indirmek için tıklayın.**](/iframe-api/iframe-api-1-adim/PayTR iFrame API 1.ADIM.zip)


---

# iFrame API 2. Adım | PayTR


# iFrame API 2. Adım

iFrame ile açılan ödeme formunu kullanarak müşteriniz ödeme yaptığında, PayTR sistemi ödeme sonucunu yazılımınıza bildirmelidir ve yazılımınızdan bildirimin alındığına dair cevap almalıdır. Aksi halde, ödeme işlemi tamamlanmaz ve tarafınıza ödeme aktarılmaz.

PayTR sistemince ödeme sonuç bildiriminin yapılacağı sayfa (Bildirim URL) tarafınızca belirlenmeli ve Mağaza Paneli Destek & Kurulum alanındaki AYARLAR sayfasında tanımlanmalıdır.

Tanımlayacağınız Bildirim URL’ye POST metodu ile ödemenin sonucu (başarılı veya başarısız) her işlem için ayrı olarak gönderilir. Bu bildirime istinaden Bildirim URL’nizde yapacağınız kodlama ile yazılımınızda siparişi onaylamalı veya iptal etmelisiniz, ekrana OK basarak PayTR sistemine cevap vermelisiniz.

**PayTR sistemince Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**   


Alan Adı | Zorunlu | Token | Açıklama  
---|---|---|---  
merchant_oid | Evet | Evet | Mağaza sipariş no: Satış işlemi için belirlediğiniz ve 1. ADIM’da gönderdiğiniz sipariş numarası  
status | Evet | Evet | Ödeme işleminin sonucu (success veya failed)  
total_amount | Evet | Evet | Müşteriden tahsil edilen toplam tutar (100 ile çarpılmış hali gönderilir. 34.56 => 3456)(Not: Müşteri vade farklı taksit seçtiği vb. durumlarda, 1. ADIM’da gönderdiğiniz “payment_amount” değerinden daha yüksek olabilir)  
hash | Evet | Evet | PayTR sisteminden gönderilen değerlerin doğruluğunu kontrol etmeniz için güvenlik amaçlı oluşturulan hash değeri (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
failed_reason_code | Hayır | Evet | Ödemenin onaylanmaması durumunda gönderilir (Bkz: 2. Adım İçin Hata Kodları ve Açıklamaları Tablosu)  
failed_reason_msg | Hayır | Evet | Ödemenin neden onaylanmadığı mesajını içerir (Bkz: 2. Adım İçin Hata Kodları ve Açıklamaları Tablosu)  
test_mode | Hayır | Hayır | Mağazanız test modunda iken veya canlı modda yapılan test işlemlerde 1 olarak gönderilir  
payment_type | Evet | Evet | Ödeme şekli: Müşterinin hangi ödeme şekli ile ödemesini tamamladığını belirtir.'card' veya 'eft' değerlerini alır.  
currency | Evet | Hayır | Para birimi: Ödemenin hangi para birimi üzerinden yapıldığını belirtir. ‘TL’, ‘USD’,‘EUR’, ‘GBP’, ‘RUB’ değerlerinden birini alır  
payment_amount | Evet | Hayır | Sipariş tutarı: 1. ADIM’da gönderdiğiniz “payment_amount” değeridir.(100 ile çarpılmış hali gönderilir. 34.56 => 3456)  
  
**Bildirim URL’nize PayTR sistemince yapılacak isteğe dönülmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**
    
    
    Örnek (PHP): echo "OK";
    
    
    
    Örnek (.NET): Response.Write("OK");

**ÖNEMLİ UYARILAR:**

  1. Bildirim URL adresinize üye girişi ve benzeri erişim kısıtlaması yapılmamalıdır. Böylece PayTR sistemi bildirimleri kolayca iletebilecektir.

  2. Bildirim URL’nize gelecek bildirimlere döneceğiniz OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır.

  3. Bildirim URL’niz, müşterinizin ödeme sırasında ulaşacağı bir sayfa değildir, PayTR tarafından arka planda (server-side) ödeme sonucunu bildirmek için kullanılır. Bu nedenle, Bildirim URL’nizde kodlama yaparken oturum (SESSION) değerlerini kullanamazsınız. İşlemlerinizi Mağaza sipariş no (merchant_oid) kullanarak gerçekleştirmelisiniz.

  4. OK yanıtı alınmayan bildirimlerde, ilgili sipariş Mağaza Paneli'ndeki İşlemler sayfasında “Devam Ediyor” olarak görünecektir.

  5. PayTR sistemi, Bildirim URL’nizden OK cevabını istendiği şekilde almadığı durumda, bildirimin başarısız olduğunu varsayar. Ağ trafik sorunları, sitenizdeki anlık yoğunluklar ve benzeri nedenlerden dolayı aynı ödeme işlemi için birden fazla bildirim ulaşabilir. Bu nedenle, bildirimin birden fazla geldiği durumlarda, yalnızca ilk bildirim göz önünde bulundurulmalı, sonraki bildirimler için müşteriye tekrar ürün/hizmet sunulmamalıdır. Tekrarlayan bildirimlerde yalnızca OK yanıtı ile süreç sonlandırılmalıdır. Tekrarlayan bildirimlerin tespiti Mağaza sipariş no (merchant_oid) temel alınarak yapılmalıdır.

  6. Bildirimin PayTR sisteminden geldiğinden ve ulaşım esnasında değiştirilmediğinden emin olmak için, **POST içerisindeki hash** değeri ile tarafınızca **oluşturulacak hash** değerinin aynı olduğunu kontrol etmeniz, güvenlik açısından büyük önem arz etmektedir. Bu kontrolü yapmamanız durumunda maddi kayıplar ile karşılaşabilirsiniz.




**2\. Adım İçin Hata Kodları ve Açıklamaları**

failed_reason_code | failed_reason_msg | Açıklama  
---|---|---  
0 | DEĞİŞKEN (AÇIKLAMAYI OKUYUN) | Ödemenin neden onaylanmadığına ilişkin, detaylı hata mesajı (Örneğin: Kartın limiti / bakiyesi yetersiz).  
1 | Kimlik Doğrulama yapılmadı. Lütfen tekrar deneyin ve işlemi tamamlayın. | Müşteri, kimlik doğrulama adımında cep telefonu numarasını girmedi.  
2 | Kimlik Doğrulama başarısız. Lütfen tekrar deneyin ve şifreyi doğru girin. | Müşteri, cep telefonuna gelen şifreyi doğru girmedi.  
3 | Güvenlik kontrolü sonrası onay verilmedi veya kontrol yapılamadı. | Müşterinin işlemi PayTR tarafından güvenlik kontrolünden geçemedi veya kontrol yapılamadı.  
6 | Müşteri ödeme yapmaktan vazgeçti ve ödeme sayfasından ayrıldı. | Müşteri, kendisine tanınmış olan işlem süresinde (1.ADIM’da tanımlanan timeout_limit değeri) işlemini tamamlamadı veya müşteri ödeme sayfasını kapatarak işlemi sonlandırdı.  
8 | Bu karta taksit yapılamamaktadır. | Müşterinin kullanmakta olduğu kart ile seçmiş olduğu taksitli ödeme yöntemi kullanılamaz.  
9 | Bu kart ile işlem yetkisi bulunmamaktadır. | Müşterinin kullanmakta olduğu kart için mağazanızın işlem yetkisi bulunmuyor.  
10 | Bu işlemde 3D Secure kullanılmalıdır. | Müşteri, yapmış olduğu işlemde 3D Secure ile ödeme yapmalıdır.  
11 | Güvenlik uyarısı. İşlem yapan müşterinizi kontrol edin. | Müşterinin işleminde fraud tespiti bulunuyor. Güvenliğiniz için müşterinin işlemlerini kontrol edin.  
99 | İşlem başarısız: Teknik entegrasyon hatası. | Teknik entegrasyon hatası varsa dönülecektir. (debug_on değeri 0 ise)  
  
  
Yukarıdaki açıklamalara uygun olarak Bildirim URL’nizi hazırladıysanız, kontrol için bir adet test ödemesi gerçekleştirmelisiniz. Eğer yaptığınız test işlem PayTR Mağaza Paneli’nizdeki İşlemler sayfasında “Başarılı” olarak görünürse PayTR entegrasyonunuz tümüyle tamamlanmıştır.

Eğer işlemin durumu “Devam Ediyor” olarak görünüyorsa Bildirim URL’nizden “OK” yanıtı alınamıyor demektir. İşlemler sayfasında yaptığınız test işleminin satırında “Detay” linkine tıklayıp, Bildirim URL’nizden hangi yanıt geldiğini kontrol edin.

**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Destek & Kurulum > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ## 2. ADIM için örnek kodlar ##
    
        ## ÖNEMLİ UYARILAR ##
        ## 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        ## 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        ## veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        ## 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        ## siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        $post = $_POST;
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        ###########################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        #
        ## POST değerleri ile hash oluştur.
        $hash = base64_encode( hash_hmac('sha256', $post['merchant_oid'].$merchant_salt.$post['status'].$post['total_amount'], $merchant_key, true) );
        #
        ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ###########################################################################
    
        ## BURADA YAPILMASI GEREKENLER
        ## 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        ## 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
        /* Sipariş durum sorgulama örnek
           $durum = SQL
           if($durum == "onay" || $durum == "iptal"){
                echo "OK";
                exit;
            }
         */
    
        if( $post['status'] == 'success' ) { ## Ödeme Onaylandı
    
            ## BURADA YAPILMASI GEREKENLER
            ## 1) Siparişi onaylayın.
            ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            ## 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
            ## değişebilir. Güncel tutarı $post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
        } else { ## Ödemeye Onay Verilmedi
    
            ## BURADA YAPILMASI GEREKENLER
            ## 1) Siparişi iptal edin.
            ## 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
            ## $post['failed_reason_code'] - başarısız hata kodu
            ## $post['failed_reason_msg'] - başarısız hata mesajı
    
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir.
        echo "OK";
        exit;
    ?>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # 2. ADIM için örnek kodlar
    """
    ÖNEMLİ UYARILAR
    1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    """
    
    import base64
    import hashlib
    import hmac
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
    
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'YYYYYYYYYYYYYY'
        merchant_salt = 'ZZZZZZZZZZZZZZ'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # BURADA YAPILMASI GEREKENLER
        # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.
    
        if post['status'] == 'success':  # Ödeme Onaylandı
            """
            BURADA YAPILMASI GEREKENLER
            1) Siparişi onaylayın.
            2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
            Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
            """
            print(request)
        else:  # Ödemeye Onay Verilmedi
            """
            BURADA YAPILMASI GEREKENLER
            1) Siparişi iptal edin.
            2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
            post['failed_reason_code'] - başarısız hata kodu
            post['failed_reason_msg'] - başarısız hata mesajı
            """
            print(request)
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    
    // 2. ADIM için örnek kodlar
    
    // ÖNEMLİ UYARILAR!
    // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
    // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
    // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class bildirim_url_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYYYYYYYY";
        string merchant_salt    = "ZZZZZZZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string merchant_oid = Request.Form["merchant_oid"];
            string status = Request.Form["status"];
            string total_amount = Request.Form["total_amount"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(merchant_oid, merchant_salt, status, total_amount);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
                }
    
            //###########################################################################
    
            // BURADA YAPILMASI GEREKENLER
            // 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
            // 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
            if (status == "success") { //Ödeme Onaylandı
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER ONAY İŞLEMLERİDİR.
                // 1) Siparişi onaylayın.
                // 2) iframe çağırma adımında merchant_oid ve diğer bilgileri veri tabanınıza kayıp edip bu aşamada karşılaştırarak eğer var ise bilgieri çekebilir ve otomatik sipariş tamamlama işlemleri yaptırabilirsiniz.
                // 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapabilirsiniz. Bu işlemide yine iframe çağırma adımında merchant_oid bilgisini kayıt edip bu aşamada sorgulayarak verilere ulaşabilirsiniz.
                // 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
                // değişebilir. Güncel tutarı Request.Form['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
                } else { //Ödemeye Onay Verilmedi
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER
                // 1) Siparişi iptal edin.
                // 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
                // $post['failed_reason_code'] - başarısız hata kodu
                // $post['failed_reason_msg'] - başarısız hata mesajı
                }          
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'YYYYYYYYYYYYYY';
    var merchant_salt = 'ZZZZZZZZZZZZZZ';
    var basket = JSON.stringify([
        ['Örnek Ürün 1', '18.00', 1],
        ['Örnek Ürün 2', '33.25', 2],
        ['Örnek Ürün 3', '45.42', 1]
    ]);
    var user_basket = nodeBase64.encode(basket);
    var merchant_oid = "IN" + microtime.now(); // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    // Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    // Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    var max_installment = '0';
    var no_installment = '0'  // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın.
    var user_ip = '';
    var email = 'XXXXXXXX'; // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi.
    var payment_amount = 100; // Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    var currency = 'TL';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var user_name = ''; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
    var user_address = ''; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
    var user_phone = '05555555555'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
    
    // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php';
    // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php';
    var timeout_limit = 30; // İşlem zaman aşımı süresi - dakika cinsinden
    var debug_on = 1; // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    var lang = 'tr'; // Türkçe için tr veya İngilizce için en gönderilebilir. Boş gönderilirse tr geçerli olur.
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${user_basket}${no_installment}${max_installment}${currency}${test_mode}`;
    
        var paytr_token = hashSTR + merchant_salt;
    
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        var options = {
            method: 'POST',
            url: 'https://www.paytr.com/odeme/api/get-token',
            headers:
                { 'content-type': 'application/x-www-form-urlencoded' },
            formData: {
                merchant_id: merchant_id,
                merchant_key: merchant_key,
                merchant_salt: merchant_salt,
                email: email,
                payment_amount: payment_amount,
                merchant_oid: merchant_oid,
                user_name: user_name,
                user_address: user_address,
                user_phone: user_phone,
                merchant_ok_url: merchant_ok_url,
                merchant_fail_url: merchant_fail_url,
                user_basket: user_basket,
                user_ip: user_ip,
                timeout_limit: timeout_limit,
                debug_on: debug_on,
                test_mode: test_mode,
                lang: lang,
                no_installment: no_installment,
                max_installment: max_installment,
                currency: currency,
                paytr_token: token,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.render('layout', { iframetoken: res_data.token });
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
    
        // ÖNEMLİ UYARILAR!
        // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        var callback = req.body;
    
        // POST değerleri ile hash oluştur.
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        if (callback.status == 'success') {
            //basarili
        } else {
            //basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

iFrame API 2. Adım örnek kodları[**indirmek için tıklayın.**](/iframe-api/iframe-api-2-adim/PayTR iFrame API 2.ADIM.zip)


---

# Link API Entegrasyonu | PayTR


# Link API Entegrasyonu

Link API çözümü kullanma talebiniz, ilgili birimlerimizin onayından geçmesi halinde mağazanıza tanımlanmaktadır. Bu konu hakkında talebinizi reddetme veya onaylama hakkını PayTR kendinde saklı tutmaktadır.

**ENTEGRASYON HAKKINDA ÖNEMLİ ÖN BİLGİLENDİRME:** **Mağaza Bilgileri:**  
Entegrasyon için gerekli olan API entegrasyon bilgilerine Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri bölümünden ulaşabilirsiniz. (Bu bilgileri sadece Ana Kullanıcı ve Teknik kullanıcı görüntülüyebilir.)  


**Entegrasyon içerisinde 4 adet servis bulunmaktadır:**   
1- Link oluşturma. Bu [**linkten**](/link-api/link-api-create) gidebilirsiniz.  
2- Link silme. Bu [**linkten**](/link-api/link-api-delete) gidebilirsiniz.  
3- Link API Callback ( Opsiyonel ). Bu [**linkten**](/link-api/linkle-api-callback) gidebilirsiniz.  
4- Sms & Email( Opsiyonel ). Bu [**linkten**](/link-api/linkle-api-sms-and-email) gidebilirsiniz.  


Yardım talepleriniz için Mağaza panelindeki Destek Sayfasından mesajlarınızı göndermenizi rica ederiz.

Linkle ödeme dokümanını indirmek için [**tıklayın.**](/link-api/PayTR_Link_API.zip)


---

# Link API Callback Servisi | PayTR


# Link API Callback Servisi

Oluşturduğunuz ödeme linki üzerinden yalnızca başarılı bir ödeme yapıldığında, Create servisinde o link için göndermiş olduğunuz callbak_url’e işlem sonucu bildirilir.

BİLGİ: Eğer Create servisinde callbak_url belirlemediyseniz veya belirlemek istemiyorsanız, bu entegrasyonu yapmanız gerek yoktur.

DİKKAT: Bu servis yalnızca Create servisinde gönderdiğiniz linkin eğer varsa callback_url’ine istek atar. Mağaza Paneli içerisinde Bildirim URL kısmı ile hiçbir bağlantısı bulunmamaktadır.

**PayTR sistemince link için tanımladığınız Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**

Alan Adı | Açıklama  
---|---  
hash | PayTR sisteminden gönderilen değerlerin doğruluğunu kontrol etmeniz için güvenlik amaçlı oluşturulan hash değeri (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
merchant_oid | PayTR tarafından oluşturulan sipariş referans numarası.  
status | Başarılı ödeme sonucunda success değeri döner (Link API'de başarısız ödemeler için bildirim yapılmaz).  
total_amount | Müşteriden tahsil edilen toplam tutar. (100 ile çarpılmış hali gönderilir. 34.56 => 3456) (Not: Müşteri vade farklı taksit seçtiği vb. durumlarda, 1. ADIM’da gönderdiğiniz “payment_amount” değerinden daha yüksek olabilir)  
payment_amount | Sipariş tutarı: 1. ADIM’da gönderdiğiniz “payment_amount” değeridir. (100 ile çarpılmış hali gönderilir. 34.56 => 3456)  
payment_type | Müşterinin hangi ödeme şekli ile ödemesini tamamladığını belirtir. Örn. card, bex vb. değerleri alır.  
currency | Para birimi: Ödemenin hangi para birimi üzerinden yapıldığını belirtir. TL, USD, EUR, GBP, RUB değerlerinden birini alır.  
callback_id | Link oluşturmada (create) ilettiğiniz callbak_id bilgisi.  
merchant_id | PayTR mağaza numaranız.  
test_mode | Mağazanız test modunda iken veya canlı modda yapılan test işlemlerde 1 olarak gönderilir  
  
**Bildirim URL’nize PayTR sistemince yapılacak isteğe dönülmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**   

    
    
    Örnek (PHP): echo "OK";
    
    
    
    Örnek (.NET): Response.Write("OK");

**ÖNEMLİ UYARILAR:**

  1. Bildirim URL adresinize üye girişi ve benzeri erişim kısıtlaması yapılmamalıdır. Böylece PayTR sistemi bildirimleri kolayca iletebilecektir.

  2. Bildirim URL’nize gelecek bildirimlere döneceğiniz OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır.

  3. Bildirim URL’niz, müşterinizin ödeme sırasında ulaşacağı bir sayfa değildir, PayTR tarafından arka planda (server-side) ödeme sonucunu bildirmek için kullanılır. Bu nedenle, Bildirim URL’nizde kodlama yaparken oturum (SESSION) değerlerini kullanamazsınız. İşlemlerinizi Mağaza sipariş no (merchant_oid) kullanarak gerçekleştirmelisiniz.

  4. OK yanıtı alınmayan bildirimlerde, ilgili sipariş Mağaza Paneli'ndeki İşlemler sayfasında “Devam Ediyor” olarak görünecektir.

  5. PayTR sistemi, Bildirim URL’nizden OK cevabını istendiği şekilde almadığı durumda, bildirimin başarısız olduğunu varsayar. Ağ trafik sorunları, sitenizdeki anlık yoğunluklar ve benzeri nedenlerden dolayı aynı ödeme işlemi için birden fazla bildirim ulaşabilir. Bu nedenle, bildirimin birden fazla geldiği durumlarda, yalnızca ilk bildirim göz önünde bulundurulmalı, sonraki bildirimler için müşteriye tekrar ürün/hizmet sunulmamalıdır. Tekrarlayan bildirimlerde yalnızca OK yanıtı ile süreç sonlandırılmalıdır. Tekrarlayan bildirimlerin tespiti Mağaza sipariş no (merchant_oid) temel alınarak yapılmalıdır.

  6. Bildirimin PayTR sisteminden geldiğinden ve ulaşım esnasında değiştirilmediğinden emin olmak için, **POST içerisindeki hash** değeri ile tarafınızca **oluşturulacak hash** değerinin aynı olduğunu kontrol etmeniz, güvenlik açısından büyük önem arz etmektedir. Bu kontrolü yapmamanız durumunda maddi kayıplar ile karşılaşabilirsiniz.




Yukarıdaki açıklamalara uygun olarak Bildirim URL’nizi hazırladıysanız, kontrol için bir adet test ödemesi gerçekleştirmelisiniz. Eğer yaptığınız test işlem PayTR Mağaza Paneli’nizdeki İşlemler sayfasında “Başarılı” olarak görünürse PayTR entegrasyonunuz tümüyle tamamlanmıştır.

Eğer işlemin durumu “Devam Ediyor” olarak görünüyorsa Bildirim URL’nizden “OK” yanıtı alınamıyor demektir. İşlemler sayfasında yaptığınız test işleminin satırında “Detay” linkine tıklayıp, Bildirim URL’nizden hangi yanıt geldiğini kontrol edin.

**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Destek & Kurulum > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ############################# ÖDEME LİNKİ BİLDİRİM ÖRNEK KODLAR ############################
        #                                                                                          #
        $post = $_POST;
    
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'XXXXXXXXXXXXXXXX';
        $merchant_salt  = 'XXXXXXXXXXXXXXXX';
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
        #
        ## POST değerleri ile hash oluştur.
        $hash = base64_encode( hash_hmac('sha256', $post['callback_id'].$post['merchant_oid'].$merchant_salt.$post['status'].$post['total_amount'], $merchant_key, true) );
        #
        ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ############################################################################################
        #
        ## BURADA YAPILMASI GEREKENLER
        ## 1) Ödeme durumunu $post['callback_id'] değerini kullanarak veri tabanınızdan sorgulayın.
        ## 2) Eğer ödeme zaten daha önceden onaylandıysa (callback size ulaştıysa) sadece echo "OK"; exit; yaparak akışı sonlandırın.
        /* Ödeme durum sorgulama örnek
           $durum = SQL
           if($durum == "onay"){
                echo "OK";
                exit;
            }
         */
    
        if( $post['status'] == 'success' ) { ## Ödeme Onaylandı
            ## BURADA YAPILMASI GEREKENLER
            ## 1) Veri tabanınızda ödemeyi onaylayın.
            ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            ## 3) $post['total_amount'] müşterinin yaptığı ödemenin toplam tutarıdır. Muhasebe işlemlerinizde
            ## bu tutraı kullanmanız gerekmektedir.
        } else {
            ## Link API'de başarısız ödemeler için callback yapılmamaktadır.
            ## Dolayısıyla kod akışında buraya erişim olmayacaktır. Ancak ileride Link API'de yapılabilecek geliştirmeler
            ## için dilerseniz buraya bir handler yazabilirsiniz.
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir. OK yanıtını bu alandan kaldırmayın.
        echo "OK";
        exit;
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # ÖDEME LİNKİ BİLDİRİM ÖRNEK KODLAR
    
    import base64
    import hashlib
    import hmac
    import json
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'XXXXXXXXXXXXXXXX'
        merchant_salt = 'XXXXXXXXXXXXXXXX'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['callback_id'] + post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        """
        BURADA YAPILMASI GEREKENLER
        1) Ödeme durumunu post['callback_id'] değerini kullanarak veri tabanınızdan sorgulayın.
        2) Eğer ödeme zaten daha önceden onaylandıysa (callback size ulaştıysa) sadece 'OK' yaparak akışı sonlandırın.
        Ödeme durum sorgulama örnek
        durum = SQL
    
        if(durum == 'onay'){
             return HttpResponse(str('OK'))
        """
    
        if post['status'] == 'success':
            """
            BURADA YAPILMASI GEREKENLER
            1) Veri tabanınızda ödemeyi onaylayın.
            2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            3) post['total_amount'] müşterinin yaptığı ödemenin toplam tutarıdır. Muhasebe işlemlerinizde
            bu tutraı kullanmanız gerekmektedir.
            """
        else:
            """
            Link API'de başarısız ödemeler için callback yapılmamaktadır.
            Dolayısıyla kod akışında buraya erişim olmayacaktır. Ancak ileride Link API'de yapılabilecek geliştirmeler
            """
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class paytr_link_api_callback : System.Web.UI.Page
    {
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key = "XXXXXXXXXXXXXXXXXXXXXXXXXX";
        string merchant_salt = "YYYYYYYYYYYYYYYYYYYYYYYYY";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e)
        {
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string callback_id = Request.Form["callback_id"];
            string merchant_oid = Request.Form["merchant_oid"];
            string status = Request.Form["status"];
            string total_amount = Request.Form["total_amount"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(callback_id, merchant_oid, merchant_salt, status, total_amount);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token)
            {
                Response.Write("PAYTR notification failed: bad hash");
                return;
            }
    
            ////////////////////////////////////////////////////////////////////////////////////////////
            //
            //
            ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
            // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
            // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
            // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
            // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
            // [payment_amount]  => Ödeme tutarı.
            // [payment_type]    => Ödeme yöntemi.
            // [currency]        => Ödeme para birimi.
            // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
            // [merchant_id]     => PayTR mağaza numaranınz.
    
            // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
            ////////////////////////////////////////////////////////////////////////////////////////////
            //
    
            // BURADA YAPILMASI GEREKENLER
            // 1) Ödeme durumunu ['callback_id'] değerini kullanarak veri tabanınızdan sorgulayın.
            // 2) Eğer ödeme zaten daha önceden onaylandıysa (callback size ulaştıysa) sadece echo "OK"; exit; yaparak akışı sonlandırın.
    
            /* Ödeme durum sorgulama örnek
            status = SQL
            if(status == "confirm"){
                 Response.Write("OK");
            }
            */
    
            if (status == "success")
            { //Ödeme Onaylandı
    
                // BURADA YAPILMASI GEREKENLER ONAY İŞLEMLERİDİR.
                // 1) Veri tabanınızda ödemeyi onaylayın.
                // 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapabilirsiniz. Bu işlemide yine iframe çağırma adımında merchant_oid bilgisini kayıt edip bu aşamada sorgulayarak verilere ulaşabilirsiniz.
                // 3) ['total_amount'] müşterinin yaptığı ödemenin toplam tutarıdır. Muhasebe işlemlerinizde bu tutarı kullanmanız gerekmektedir.
            }
            else
            { //Ödemeye Onay Verilmedi
    
                // BURADA YAPILMASI GEREKENLER
                // 1) Link API'de başarısız ödemeler için callback yapılmamaktadır.
                // 2) Dolayısıyla kod akışında buraya erişim olmayacaktır. Ancak ileride Link API'de yapılabilecek geliştirmeler
                // için dilerseniz buraya bir handler yazabilirsiniz.
                // ['failed_reason_msg'] - başarısız hata mesajı
            }
            // Bildirimin alındığını PayTR sistemine bildir. OK yanıtını bu alandan kaldırmayın.
            Response.Write("OK");
        }
    }
    
    
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    var request = require('request');
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'AAAAAA';
    var merchant_key = 'XXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXX';
    
    app.get("/create", function (req, res) {
    
        var name = 'Örnek Ürün / Hizmet Adı';  // Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        var price = '1445'; // 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        var currency = 'TL';  //TL - USD - EUR - GBP gönderilebilir.
        var max_installment = '12'; // 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    
        //collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        //collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        //product ise min_count (satın alma adet alt limiti) gereklidir.
    
        var link_type = 'product';
        var lang = 'tr'; //tr veya en gönderilebilir.
        var required = name + price + currency + max_installment + link_type + lang;
        var email = '';
        var min_count = '';
        if (link_type == 'product') {
            min_count = '1';
            // Alt adet limiti.
            required += min_count;
        } else {
            (link_type == 'collection')
            email = 'test@example.com';
            // Ödeme yapan kullanıcının eposta adresi.
            required += email;
        }
    
        var max_count = '1';
    
        // Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
    
        var expiry_date = '2021-06-23 17:00:00';
    
        // Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
        // Örnek format: 2021-05-31 17:00:00
    
        //Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
        //http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
        //callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    
        var callback_link = '';
    
        // Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
        //callback_link gönderildiğinde bu alan zorunlu olmaktadır.
        var callback_id = '';
    
        var debug_on = '1'; //Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(required + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/create',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'name': name,
                'price': price,
                'currency': currency,
                'max_installment': max_installment,
                'link_type': link_type,
                'lang': lang,
                'min_count': min_count,
                'email': email,
                'expiry_date': expiry_date,
                'max_count': max_count,
                'callback_link': callback_link,
                'callback_id': callback_id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(body);
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.get("/delete", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/delete',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
                /* Başarılı yanıt içerik örneği
                [status]  => success
                */
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendsms", function (req, res) {
    
        var id = 'XXXX';  // Link ID - create metodunda dönülen değerdir.
        var cell_phone = '05555555555'; // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + cell_phone + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-sms',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'cell_phone': cell_phone,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendmail", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var email = ''; // Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + email + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-email',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'email': email,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        token = callback.id + callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(token).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
        // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
        // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
        // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
        // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
        // [payment_amount]  => Ödeme tutarı.
        // [payment_type]    => Ödeme yöntemi.
        // [currency]        => Ödeme para birimi.
        // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
        // [merchant_id]     => PayTR mağaza numaranınz.
    
        // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
        ////////////////////////////////////////////////////////////////////////////////////////////
    
        if (callback.status == 'success') {
    
            //basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Link API CallBack Servisi örnek kodlarını[**indirmek için tıklayın.**](/link-api/linkle-api-callback/PayTR Link API - Callback \(Optional\).zip)


---

# Link API Create ile Link API Oluşturma | PayTR


# Link API Create ile Link API Oluşturma

Create servisi ile Hizmet/Ürün veya Fatura/Cari tahsilatlarınız için ödeme linkleri oluşturabilirsiniz.

1- Aşağıdaki gönderilmesi zorunlu olan bilgiler iletildikten sonra bir token verisi üretilir.   
2- Oluşan token ve gönderilmesi zorunlu olan alanlarla birlikte https://www.paytr.com/odeme/api/link/create servisine istekte bulunulur.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
name (string) | Ürün veya hizmet adı | Evet | Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.  
price (string) | Ödeme tutarı | Evet | 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.) Esnek link için minimum ödeme tutarını temsil eder.  
currency (string) | Para birimi | Evet | TL, EUR, USD, GBP, RUB (Boş ise TL kabul edilir)  
max_installment (string) | En fazla taksit sayısı: Gösterilecek en fazla taksit sayısını belirler (Örn. kuyum harcamalarında en fazla 4 taksit uygulaması vardır) | Evet | 2 – 12 arası gönderilebilir. 1 gönderilirse bireysel kartlarla taksitli işlem yapılamaz.  
link_type(integer) | Link Tipi | Evet | Ürün hizmet satışı için: product Fatura/Cari tahsilat için: collection Esneklink için:flex  
lang(string) | Ödeme sürecinde sayfalarda kullanılacak dil | Evet | Türkçe için tr veya İngilizce için en (Boş gönderilirse tr geçerli olur)  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (integer) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
name (string) | Ürün veya hizmet adı | Evet | Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.  
user_name(string) | Esneklink ödeme yapan kişi ad-soyad bilgisi | Hayır  
price (string) | Ödeme tutarı | Evet | 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)  
flex_max_price | Esneklink için maksimum ödeme tutarı | Esneklink için Evet | -  
currency (string) | Para birimi | Evet | TL, EUR, USD, GBP, RUB (Boş ise TL kabul edilir)  
max_installment (string) | En fazla taksit sayısı: Gösterilecek en fazla taksit sayısını belirler (Örn. kuyum harcamalarında en fazla 4 taksit uygulaması vardır) | Evet | 2 – 12 arası gönderilebilir. 1 gönderilirse bireysel kartlarla taksitli işlem yapılamaz.  
lang(string) | Ödeme sürecinde sayfalarda kullanılacak dil | Evet | Türkçe için tr veya İngilizce için en (Boş gönderilirse tr geçerli olur)  
get_qr | QR kod oluşturabilmeniz için PNG formatında Base64 kodu döner. | Hayır | 1 veya 0 gönderilebilir. QR kod yanıtı alabilmek için 1 gönderilmelidir.  
link_type(integer) | Link Tipi | Evet | Ürün hizmet satışı için: product Fatura/Cari tahsilat için: collection  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir. | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız  
min_count (integer) | Alt adet limiti (Link tipi product ise zorunlu) | Hayır | En az 1 olabilir.  
email(string) | Eposta adresi (Link tipi collection ise zorunlu) | Hayır | En fazla 100 karakter  
max_count(integer) | Stok adedi (Yalnızca product tipinde kullanılabilir. Link'in stok adedini belirler ve gönderilmezse stok limiti uygulanmaz. Stok adedi kadar ödeme yapıldığında link pasif olur) | Hayır | En az 1 olabilir  
pft(integer) | Peşin Fiyatına Taksit ayarı (isteğe bağlı).Gönderilen en yüksek sayıya kadar olan tüm taksit seçenekleri Peşin Fiyatına Taksit olarak ayarlanır | Hayır | 2-12 arasındaki değerleri alabilir.DİKKAT: Peşin Fiyatına Taksit olarak belirlediğiniz taksit sayıları için yapılan tüm ödeme işlemlerinde, taksit komisyonları sizden kesilecektir.  
expiry_date | Linkin son kullanma tarihi | Hayır | Ödeme Link'inin son kullanma tarihi. Gönderilmezse, sürekli açık kalır. Örnek Format: “2021-05-31 17:00:00”  
callback_link | Ödeme sonucunun gönderileceği URL | Hayır | http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.  
callback_id | Bildirimde dönülecek ID (callback_link gönderildiğinde bu alanında gönderilmesi zorunludur.) | Hayır | Alfanumerik ve en fazla 64 karakter olabilir.  
debug_on | Hata mesajı (Entegrasyon ve test sürecinde hataları tespit etmek için 1 gönderin). | Hayır | 0 veya 1  
  
  
  


**2) DÖNEN DEĞERLER**

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
İstek sonucu | status (string) | success, error veya failed  
Benzersiz link tanımlayıcı | id (string) | Örnek: NB2Zlz3  
Link | status (string) | Örnek: https://www.paytr.com/link/NB2Zlz3  
İstek açıklaması (hata durumunda) | reason (string) | Örnek: Zorunlu alan degeri gecersiz veya gonderilmedi (Link API - create): price  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################## ÖDEME LİNKİ OLUŞTURMAK İÇİN ÖRNEK KODLAR ########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'AAAAAA';
        $merchant_key   = 'XXXXXXXXXXXXXXXX';
        $merchant_salt  = 'XXXXXXXXXXXXXXXX';
        #
    
        ## Gerekli Bilgiler
        #
        $name            = "Örnek Ürün / Hizmet Adı";
        # Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        #
        $price           = 1445;
        # 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        #
        $currency        = "TL";
        # TL - USD - EUR - GBP gönderilebilir.
        #
        $max_installment = "12";
        # 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
        #
        $link_type       = "product";
        # collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        # collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        # product ise min_count (satın alma adet alt limiti) gereklidir.
        #
        $lang            = "tr";
        # tr veya en gönderilebilir.
        $get_qr          = 1;
        # Opsiyoneldir 1 veya 0 gönderilebilir. 1 gönderildiğinde yanıt içerisinde
        # QR kod oluşturabilmeniz için PNG formatında Base64 kodu döner.
    
        $required        = $name.$price.$currency.$max_installment.$link_type.$lang;
    
        //Esneklink için gerekli token yöntemi
        // $required        = $name.$price.$currency.$max_installment.$link_type.$lang;
    
        if($link_type == "product"){
            $min_count     = "1";
            # Alt adet limiti.
            $required     .= $min_count;
        }elseif($link_type == "collection"){
            $email         = time()."@example.com";
            # Ödeme yapan kullanıcının eposta adresi.
            $required     .= $email;
        }
    
        ## Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
        #
        $expiry_date        = "2020-03-23 17:00:00";
        # Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
        # Örnek format: 2021-05-31 17:00:00
        #
        $max_count          = "1";
        # Yalnızca product modunda kullanılabilir.
        # Link'in stok adedini belirler. Gönderilmezse, stok limiti uygulanmaz.
        # Stok adedi kadar ödeme yapıldığında link pasif olur.
        #
        //$pft             = "0"; // OPSİYONEL
        # 2 - 12 arası gönderilebilir. Gönderilen en yüksek sayıya kadar olan tüm taksit seçenekleri
        # Peşin Fiyatına Taksit olarak ayarlanır.
        # DİKKAT: Peşin Fiyatına Taksit olarak belirlediğiniz taksit sayıları için yapılan tüm
        # ödeme işlemlerinde, taksit komisyonları sizden kesilecektir.
        #
        $callback_link      = "";
        # Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
        # http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
        # callback_id gönderildiğinde bu alan zorunlu olmaktadır.
        #
        $callback_id        = "";
        # Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
        # callback_link gönderildiğinde bu alan zorunlu olmaktadır.
    
        $debug_on           = 1;
        # Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
        #
        $paytr_token=base64_encode(hash_hmac('sha256', $required.$merchant_salt, $merchant_key, true));
        $post_vals=array(
            'merchant_id'       => $merchant_id,
            'name'              => $name,
            'price'             => $price,
            'currency'          => $currency,
            'max_installment'   => $max_installment,
            'link_type'         => $link_type,
            'lang'              => $lang,
            'min_count'         => $min_count,
            'email'             => $email,
            'expiry_date'       => $expiry_date,
            'max_count'         => $max_count,
            'callback_link'     => $callback_link,
            'callback_id'       => $callback_id,
            'debug_on'          => $debug_on,
            'get_qr'            => $get_qr,
            'paytr_token'       => $paytr_token,
            'user_name'         => $user_name,
            'flex_max_price'    => $flex_max_price
        );
        #
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/link/create");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR LINK CREATE API request timeout. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die($result['err_msg']);
        elseif($result['status']=='failed')
            print_r($result);
        else
            print_r($result);
    
    
    # Python 3.6+
    # Link API Create Servisi icin kullanılacak örnek kod yapısı.
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'AAAAAA'
    merchant_key = b'XXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXX'
    
    ## Gerekli Bilgiler
    name = 'Örnek Ürün / Hizmet Adı'
    # Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
    price           = '1445'
    # 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
    currency        = 'TL'
    # TL - USD - EUR - GBP gönderilebilir.
    max_installment = '12'
    # 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    link_type       = 'product'
    # collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
    # collection ise email (ödeme yapan tarafın eposta adresi olmalı).
    # product ise min_count (satın alma adet alt limiti) gereklidir.
    lang            = 'tr'
    # tr veya en gönderilebilir.
    get_qr          = 1
    # Opsiyoneldir 1 veya 0 gönderilebilir. 1 gönderildiğinde yanıt içerisinde
    # QR kod oluşturabilmeniz için PNG formatında Base64 kodu döner.
    email           =''
    min_count       =''
    
    required        = name + price + currency + max_installment + link_type + lang
    #Esneklink için gerekli token yöntemi
    # required        = name + price + currency + max_installment + link_type + lang;
    
    if link_type == 'product':
        min_count = '1'
        # Alt adet limiti.
        required+=min_count
    elif link_type == 'collection':
        email= random.randint(1, 9999999).__str__() + '@example.com'
        # Ödeme yapan kullanıcının eposta adresi.
        required+=email
    
    ## Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
    expiry_date= '2021-03-23 17:00:00'
    # Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
    # Örnek format: 2021-05-31 17:00:00
    max_count='1'
    # Yalnızca product modunda kullanılabilir.
    # Link'in stok adedini belirler. Gönderilmezse, stok limiti uygulanmaz.
    # Stok adedi kadar ödeme yapıldığında link pasif olur.
    #
    #pft='0'; // OPSİYONEL
    # 2 - 12 arası gönderilebilir. Gönderilen en yüksek sayıya kadar olan tüm taksit seçenekleri
    # Peşin Fiyatına Taksit olarak ayarlanır.
    # DİKKAT: Peşin Fiyatına Taksit olarak belirlediğiniz taksit sayıları için yapılan tüm
    # ödeme işlemlerinde, taksit komisyonları sizden kesilecektir.
    #
    callback_link =''
    # Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
    # http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
    # callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    callback_id=''
    # Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
    # callback_link gönderildiğinde bu alan zorunlu olmaktadır.
    debug_on=1
    # Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = required + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'name': name,
        'price': price,
        'currency': currency,
        'max_installment': max_installment,
        'link_type': link_type,
        'lang': lang,
        'min_count': min_count,
        'email': email,
        'expiry_date': expiry_date,
        'max_count': max_count,
        'callback_link': callback_link,
        'callback_id': callback_id,
        'debug_on': debug_on,
        'get_qr': get_qr,
        'paytr_token': paytr_token,
        'user_name' : user_name,
        'flex_max_price' : flex_max_price
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/link/create', params)
    res = json.loads(result.text)
    
    if res['status'] == 'error':
        print('Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print(result.text)
    else:
        print(result.text)
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using System.Web.Routing;
    namespace WebApplication1.Controllers
    {
        public class CreateController : Controller
        {
            public ActionResult List()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
    
                //    ## Gerekli Bilgiler
                string name = "Örnek Ürün / Hizmet Adı";
                // Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
    
                int price = 1445;
                // 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
    
                string max_installment = "12";
                // 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    
                string currency = "TL";
                //TL - USD - EUR - GBP gönderilebilir.
    
                string link_type = "product";
                //collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
                //collection ise email (ödeme yapan tarafın eposta adresi olmalı).
                //product ise min_count (satın alma adet alt limiti) gereklidir.
    
                string lang = "tr";
                //tr veya en gönderilebilir.
    
                get_qr          = '';
                // Opsiyoneldir 1 veya 0 gönderilebilir. 1 gönderildiğinde yanıt içerisinde
                // QR kod oluşturabilmeniz için PNG formatında Base64 kodu döner.
                ////////////////////////////////////////////////////////////////////////////////////////
                // Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
                string expiry_date = "2020-11-23 17:00:00";
                // Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
                // Örnek format: 2021-05-31 17:00:00
    
                string callback_id = "";
                // Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
                //callback_link gönderildiğinde bu alan zorunlu olmaktadır.
    
                string callback_link = "";
                //Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
                //http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
                //callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    
                string max_count = "";
                //Yalnızca product modunda kullanılabilir.
                //Link'in stok adedini belirler. Gönderilmezse, stok limiti uygulanmaz.
                //Stok adedi kadar ödeme yapıldığında link pasif olur.
    
                string pft = "";
                //2 - 12 arası gönderilebilir. Gönderilen en yüksek sayıya kadar olan tüm taksit seçenekleri
                //Peşin Fiyatına Taksit olarak ayarlanır.
                //DİKKAT: Peşin Fiyatına Taksit olarak belirlediğiniz taksit sayıları için yapılan tüm
                //ödeme işlemlerinde, taksit komisyonları sizden kesilecektir.
    
                string debug_on = "1";
                //Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
                ////////////////////////////////////////////////////////////////////////////////////////////
                ///
                string min_count = "";
                string email = "";
                string Birlestir = "";
    
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["name"] = name;
                data["price"] = price.ToString();
    
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                //Esneklink için gerekli token yöntemi
                 //required        = name,price,currency,max_installment,link_type,lang;
                if (link_type == "product")
                {
                   min_count = "1";
                Birlestir = string.Concat(name,price.ToString(),currency,max_installment,link_type,lang,min_count,merchant_salt);
                }
                else if (link_type == "collection")
                {
                   email = "test@mail.com";
                Birlestir = string.Concat(name,price.ToString(),currency,max_installment,link_type,lang,email,merchant_salt);
                }
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                data["currency"] = currency;
                data["max_installment"] = max_installment;
                data["link_type"] = link_type;
                data["lang"] = lang;
                data["get_qr"] = get_qr;
                data["min_count"] = min_count;
                data["email"] = email;
                data["expiry_date"] = expiry_date;
                data["callback_link"] = callback_link;
                data["callback_id"] = callback_id;
                data["debug_on"] = debug_on;
                data["paytr_token"] = paytr_token;
                data['user_name'] = $user_name,
                data['flex_max_price'] = $flex_max_price
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/link/create", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "error")
                    {
                        Response.Write("PAYTR LINK CREATE API request timeout. Error:" + json.err_msg + "");
                    }
                    else
                    {
                        Response.Write(json);
                       /* Başarılı yanıt içerik örneği
    
                         [status]  => success
                         [id]      => XXXXXX
                         [link]    => https://www.paytr.com/link/XXXXXX
                         */
                    }
                }
                return View();
            }
        }
    }
    
    
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    var request = require('request');
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'AAAAAA';
    var merchant_key = 'XXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXX';
    
    app.get("/create", function (req, res) {
    
        var name = 'Örnek Ürün / Hizmet Adı';  // Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        var price = '1445'; // 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        var currency = 'TL';  //TL - USD - EUR - GBP gönderilebilir.
        var max_installment = '12'; // 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    
        //collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        //collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        //product ise min_count (satın alma adet alt limiti) gereklidir.
    
        var link_type = 'product';
        var lang = 'tr'; //tr veya en gönderilebilir.
        var get_qr = ''; 
        // Opsiyoneldir 1 veya 0 gönderilebilir. 1 gönderildiğinde yanıt içerisinde
        // QR kod oluşturabilmeniz için PNG formatında Base64 kodu döner
        var required = name + price + currency + max_installment + link_type + lang;
        //Esneklink için gerekli token yöntemi
        //var required        = name + price + currency + max_installment + link_type + lang;
        var email = '';
        var min_count = '';
        if (link_type == 'product') {
            min_count = '1';
            // Alt adet limiti.
            required += min_count;
        } else {
            (link_type == 'collection')
            email = 'test@example.com';
            // Ödeme yapan kullanıcının eposta adresi.
            required += email;
        }
    
        var max_count = '1';
    
        // Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
    
        var expiry_date = '2021-06-23 17:00:00';
    
        // Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
        // Örnek format: 2021-05-31 17:00:00
    
        //$pft             = '0'; // OPSİYONEL
        // 2 - 12 arası gönderilebilir. Gönderilen en yüksek sayıya kadar olan tüm taksit seçenekleri
        // Peşin Fiyatına Taksit olarak ayarlanır.
        // DİKKAT:Peşin Fiyatına Taksit olarak belirlediğiniz taksit sayıları için yapılan tüm ödeme işlemlerinde, taksit komisyonları sizden kesilecektir.
        //
    
        //Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
        //http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
        //callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    
        var callback_link = '';
    
        // Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
        //callback_link gönderildiğinde bu alan zorunlu olmaktadır.
        var callback_id = '';
    
        var debug_on = '1'; //Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(required + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/create',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'name': name,
                'price': price,
                'currency': currency,
                'max_installment': max_installment,
                'link_type': link_type,
                'lang': lang,
                'get_qr': get_qr,
                'min_count': min_count,
                'email': email,
                'expiry_date': expiry_date,
                'max_count': max_count,
                'callback_link': callback_link,
                'callback_id': callback_id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
                'user_name' : $user_name,
                'flex_max_price' : $flex_max_price
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(body);
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.get("/delete", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/delete',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
                /* Başarılı yanıt içerik örneği
                [status]  => success
                */
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendsms", function (req, res) {
    
        var id = 'XXXX';  // Link ID - create metodunda dönülen değerdir.
        var cell_phone = '05555555555'; // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + cell_phone + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-sms',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'cell_phone': cell_phone,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendmail", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var email = ''; // Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + email + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-email',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'email': email,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        token = callback.id + callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(token).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
        // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
        // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
        // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
        // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
        // [payment_amount]  => Ödeme tutarı.
        // [payment_type]    => Ödeme yöntemi.
        // [currency]        => Ödeme para birimi.
        // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
        // [merchant_id]     => PayTR mağaza numaranınz.
    
        // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
        ////////////////////////////////////////////////////////////////////////////////////////////
    
        if (callback.status == 'success') {
    
            //basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Link API Create Servisi örnek kodlarını[**indirmek için tıklayın.**](/link-api/link-api-create/PayTR Link API - Create .zip)


---

# Link API Delete ile Ödeme Linklerini Silme | PayTR


# Link API Delete ile Ödeme Linklerini Silme

Delete servisi ile daha önce oluşturmuş olduğunuz ödeme linklerini silebilirsiniz.

1- Aşağıdaki gönderilmesi zorunlu olan bilgiler iletildikten sonra bir token verisi üretilir.   
2- Oluşan token ve gönderilmesi zorunlu olan alanlarla birlikte https://www.paytr.com/odeme/api/link/delete servisine istekte bulunulur.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
id (integer) | Link API Create metodundan dönülen değer | Evet  
merchant_id(integer) | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (integer) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
id (integer) | Link API Create metodundan dönülen değer(Toplu silme için "," ile ayrılarak maksimum 10 adet iletilebilir) | Evet | -  
debug_on(int) | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | Evet | 0 veya 1  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


**2) DÖNEN DEĞERLER**

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
İstek sonucu | status (string) | success, error veya failed  
İstek açıklaması (hata durumunda) | reason (string) | Örnek: Zorunlu alan degeri gecersiz veya gonderilmedi (Link API - create): price  
Toplu silme durumunda başarılı silinen linkler | success_deletes (array) | success_deletes => Array (0) => XXXX (1) => YYYY  
Toplu silme durumunda başarılı silinen linkler | failed_deletes (array) | failed_deletes => Array ( (0) => XXXX (1) => YYYY  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################### ÖDEME LİNKİNİ SİLMEK İÇİN ÖRNEK KODLAR #########################
    
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'AAAAAA';
        $merchant_key   = 'XXXXXXXXXXXXXXXX';
        $merchant_salt  = 'XXXXXXXXXXXXXXXX';
        #
    
        ## Gerekli Bilgiler
        #
        $id             = "YYYXXX";  //Toplu silme için XXXX,YYYY,ZZZZ şeklinde maksimum 10 adet olacak şekilde iletilebilir  // Link ID - create metodunda dönülen değerdir.
        $debug_on       = 1;           // Hataları ekrana basmak için kullanılır.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
        #
        $paytr_token=base64_encode(hash_hmac('sha256', $id.$merchant_id.$merchant_salt, $merchant_key, true));
        $post_vals=array(
            'merchant_id'       => $merchant_id,
            'id'                => $id,
            'debug_on'          => $debug_on,
            'paytr_token'       => $paytr_token
        );
        #
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/link/delete");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR LINK DELETE API request timeout. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die($result['err_msg']);
        elseif($result['status']=='failed')
            print_r($result);
        else
            print_r($result);
    
    
    # Python 3.6+
    # Link API Delete Servisi icin kullanılacak örnek kod yapısı.
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'AAAAAA'
    merchant_key = b'AAAAAA'
    merchant_salt = 'XXXXXXXXXXXXXXXX'
    
    # Gerekli Bilgiler
    id = 'YYYXXX' //Toplu silme için XXXX,YYYY,ZZZZ şeklinde maksimum 10 adet olacak şekilde iletilebilir 
    #Link ID - create metodunda dönülen değerdir.
    debug_on=1
    #Hataları ekrana basmak için kullanılır.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = id + merchant_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'id': id,
        'debug_on': debug_on,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/link/delete', params)
    res = json.loads(result.text)
    
    if res['status'] == 'error':
        print('Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print(result.text)
    else:
        print(result.text)
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using System.Web.Routing;
    namespace WebApplication1.Controllers
    {
        public class DeleteController : Controller
        {
            public ActionResult Delete()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA"; 
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
    
                // Gerekli Bilgiler
                string id = "YYYXXX"; // Link ID - create metodunda dönülen değerdir. //Toplu silme için XXXX,YYYY,ZZZZ şeklinde maksimum 10 adet olacak şekilde iletilebilir
                string debug_on = "1"; // Hataları ekrana basmak için kullanılır.
    
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(id,merchant_id, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["id"] = id;
                data["debug_on"] = debug_on;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/link/delete", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "error")
                    {
                        Response.Write("PAYTR LINK CREATE API request timeout. Error:" + json.err_msg + "");
                    }
                    else
                    {
                        Response.Write(json);
                        /* Başarılı yanıt içerik örneği
                        [status]  => success
                        */
                    }
                }
                return View();
            }
        }
    }
    
    
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    var request = require('request');
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'AAAAAA';
    var merchant_key = 'XXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXX';
    
    app.get("/delete", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir. //Toplu silme için XXXX,YYYY,ZZZZ şeklinde maksimum 10 adet olacak şekilde iletilebilir
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/delete',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
                /* Başarılı yanıt içerik örneği
                [status]  => success
                */
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    

Link API Delete Servisi örnek kodlarını[**indirmek için tıklayın.**](/link-api/link-api-delete/PayTR Link API - Delete.zip)


---

# Link API SMS ve Email | PayTR


# Link API SMS ve Email

**1-) SMS GÖNDERİMİ**

Bu servisi kullanarak belirttiğiniz cep telefonu numarasına oluşturmuş olduğunuz linkle ödeme sayfasına ait linkin gönderimini sağlayabilirsiniz. 

1- Aşağıdaki gönderilmesi zorunlu olan bilgiler iletildikten sonra bir token verisi üretilir.   
2- Oluşan token ve gönderilmesi zorunlu olan alanlarla birlikte https://www.paytr.com/odeme/api/link/send-sms servisine istekte bulunulur.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
id (integer) | Link API Create metodundan dönülen değer | Evet | -  
merchant_id(integer) | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
cell_phone(integer) | Linki göndermek istediğini telefon numarası | Evet | SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
id (integer) | Link API Create metodundan dönülen değer | Evet | -  
cell_phone(integer) | Linki göndermek istediğini telefon numarası | Evet | SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır  
debug_on(int) | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | Evet | 0 veya 1  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ###################### ÖDEME LİNKİNİ SMS İLE GÖNDERMEK İÇİN ÖRNEK KODLAR ###################
    
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'AAAAAA';
        $merchant_key   = 'XXXXXXXXXXXXXXXX';
        $merchant_salt  = 'XXXXXXXXXXXXXXXX';
        #
    
        ## Gerekli Bilgiler
        #
        $id             = "XXXYYY";         // Link ID - create metodunda dönülen değerdir.
        $cell_phone     = "05000000000";    // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
        $debug_on       = 1;                // Hataları ekrana basmak için kullanılır.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
        #
        $paytr_token=base64_encode(hash_hmac('sha256', $id.$merchant_id.$cell_phone.$merchant_salt, $merchant_key, true));
        $post_vals=array(
            'merchant_id'       => $merchant_id,
            'id'                => $id,
            'cell_phone'        => $cell_phone,
            'debug_on'          => $debug_on,
            'paytr_token'       => $paytr_token
        );
        #
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/link/send-sms");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR LINK SEND SMS API request timeout. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die($result['err_msg']);
        elseif($result['status']=='failed')
            print_r($result);
        else
            print_r($result);
    
    
    # Python 3.6+
    # Link API SMS Servisi icin kullanılacak örnek kod yapısı.
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'AAAAAA'
    merchant_key = b'XXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXX'
    
    #Gerekli Bilgiler
    id = 'XXXYYY'
    #Link ID - create metodunda dönülen değerdir.
    cell_phone= '05000000000'
    #SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
    debug_on=1
    #Hataları ekrana basmak için kullanılır.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = id + merchant_id + cell_phone + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'id': id,
        'cell_phone': cell_phone,
        'debug_on': debug_on,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/link/send-sms', params)
    res = json.loads(result.text)
    
    if res['status'] == 'error':
        print('Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print(result.text)
    else:
        print(result.text)
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using System.Web.Routing;
    namespace WebApplication1.Controllers
    {
        public class SmsController : Controller
        {
            public ActionResult Sms()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA"; 
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
    
                // Gerekli Bilgiler
                string id = "XXXYYY";  // Link ID - create metodunda dönülen değerdir.
                string cell_phone = "05000000000"; // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
                string debug_on = "1";    // Hataları ekrana basmak için kullanılır.
    
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(id, merchant_id,cell_phone, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["id"] = id;
                data["cell_phone"] = cell_phone;
                data["debug_on"] = debug_on;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/link/send-sms", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "error")
                    {
                        Response.Write("PAYTR LINK SEND SMS API request timeout. Error:" + json.err_msg + "");
                    }
                    else
                    {
                        Response.Write(json);
                        /* Başarılı yanıt içerik örneği
                        [status]  => success
                        */
                    }
                }
                return View();
            }
        }
    }
    
    
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    var request = require('request');
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'AAAAAA';
    var merchant_key = 'XXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXX';
    
    app.get("/create", function (req, res) {
    
        var name = 'Örnek Ürün / Hizmet Adı';  // Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        var price = '1445'; // 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        var currency = 'TL';  //TL - USD - EUR - GBP gönderilebilir.
        var max_installment = '12'; // 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    
        //collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        //collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        //product ise min_count (satın alma adet alt limiti) gereklidir.
    
        var link_type = 'product';
        var lang = 'tr'; //tr veya en gönderilebilir.
        var required = name + price + currency + max_installment + link_type + lang;
        var email = '';
        var min_count = '';
        if (link_type == 'product') {
            min_count = '1';
            // Alt adet limiti.
            required += min_count;
        } else {
            (link_type == 'collection')
            email = 'test@example.com';
            // Ödeme yapan kullanıcının eposta adresi.
            required += email;
        }
    
        var max_count = '1';
    
        // Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
    
        var expiry_date = '2021-06-23 17:00:00';
    
        // Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
        // Örnek format: 2021-05-31 17:00:00
    
        //Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
        //http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
        //callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    
        var callback_link = '';
    
        // Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
        //callback_link gönderildiğinde bu alan zorunlu olmaktadır.
        var callback_id = '';
    
        var debug_on = '1'; //Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(required + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/create',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'name': name,
                'price': price,
                'currency': currency,
                'max_installment': max_installment,
                'link_type': link_type,
                'lang': lang,
                'min_count': min_count,
                'email': email,
                'expiry_date': expiry_date,
                'max_count': max_count,
                'callback_link': callback_link,
                'callback_id': callback_id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(body);
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.get("/delete", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/delete',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
                /* Başarılı yanıt içerik örneği
                [status]  => success
                */
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendsms", function (req, res) {
    
        var id = 'XXXX';  // Link ID - create metodunda dönülen değerdir.
        var cell_phone = '05555555555'; // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + cell_phone + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-sms',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'cell_phone': cell_phone,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendmail", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var email = ''; // Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + email + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-email',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'email': email,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        token = callback.id + callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(token).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
        // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
        // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
        // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
        // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
        // [payment_amount]  => Ödeme tutarı.
        // [payment_type]    => Ödeme yöntemi.
        // [currency]        => Ödeme para birimi.
        // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
        // [merchant_id]     => PayTR mağaza numaranınz.
    
        // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
        ////////////////////////////////////////////////////////////////////////////////////////////
    
        if (callback.status == 'success') {
    
            //basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Link API SMS&EMAIL Servisi örnek kodlarını[**indirmek için tıklayın.**](/link-api/linkle-api-sms-and-email/PayTR Link API - Sms & Email \(Optional\).zip)

**2) EMAIL GONDERME**

Bu servisi kullanarak belirttiğiniz e-mail adresine oluşturmuş olduğunuz linkle ödeme sayfasına ait linkin gönderimini sağlayabilirsiniz. 

1- Aşağıdaki gönderilmesi zorunlu olan bilgiler iletildikten sonra bir token verisi üretilir.   
2- Oluşan token ve gönderilmesi zorunlu olan alanlarla birlikte https://www.paytr.com/odeme/api/link/send-sms servisine istekte bulunulur.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
id (integer) | Link API Create metodundan dönülen değer | Evet | -  
merchant_id(integer) | Ödeme tutarı | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası  
email(string) | Linki göndermek istediğini eposta bilgisi | Evet | En fazla 100 karakter  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
id (integer) | Link API Create metodundan dönülen değer | Evet | -  
email(string) | Linki göndermek istediğini eposta bilgisi | Evet | En fazla 100 karakter  
debug_on(int) | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | Evet | 0 veya 1  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        #################### ÖDEME LİNKİNİ EPOSTA İLE GÖNDERMEK İÇİN ÖRNEK KODLAR ##################
    
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'AAAAAA';
        $merchant_key   = 'XXXXXXXXXXXXXXXX';
        $merchant_salt  = 'XXXXXXXXXXXXXXXX';
        #
    
        ## Gerekli Bilgiler
        #
        $id             = "XXXYYY";         // Link ID - create metodunda dönülen değerdir.
        $email          = "test@mail.com";  // Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
        $debug_on       = 1;                // Hataları ekrana basmak için kullanılır.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
        #
        $paytr_token=base64_encode(hash_hmac('sha256', $id.$merchant_id.$email.$merchant_salt, $merchant_key, true));
        $post_vals=array(
            'merchant_id'       => $merchant_id,
            'id'                => $id,
            'email'             => $email,
            'debug_on'          => $debug_on,
            'paytr_token'       => $paytr_token
        );
        #
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/link/send-email");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR LINK SEND MAIL API request timeout. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die($result['err_msg']);
        elseif($result['status']=='failed')
            print_r($result);
        else
            print_r($result);
    
    
    # Python 3.6+
    # Link API EMAIL Servisi icin kullanılacak örnek kod yapısı.
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'AAAAAA'
    merchant_key = b'XXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXX'
    
    id = ''
    #Link ID - create metodunda dönülen değerdir.
    email = 'test@gmail.com'
    #Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
    debug_on=1
    #Hataları ekrana basmak için kullanılır.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = id + merchant_id + email + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'id': id,
        'email': email,
        'debug_on': debug_on,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/link/send-email', params)
    res = json.loads(result.text)
    
    if res['status'] == 'error':
        print('Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print(result.text)
    else:
        print(result.text)
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using System.Web.Routing;
    namespace WebApplication1.Controllers
    {
        public class MailController : Controller
        {
            public ActionResult Mail()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
    
                // Gerekli Bilgiler
                string id = "XXXYYY";  // Link ID - create metodunda dönülen değerdir.
                string email = "test@mail.com"; // Mail gönderilecek mail adresi değeridir. 
                string debug_on = "1";    // Hataları ekrana basmak için kullanılır.
    
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(id, merchant_id, email, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["id"] = id;
                data["email"] = email;
                data["debug_on"] = debug_on;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/link/send-email", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "error")
                    {
                        Response.Write("PAYTR LINK SEND MAIL API request timeout. Error:" + json.err_msg + "");
                    }
                    else
                    {
                        Response.Write(json);
                        /* Başarılı yanıt içerik örneği
                        [status]  => success
                        */
                    }
                }
                return View();
            }
        }
    }
    
    
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    var request = require('request');
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'AAAAAA';
    var merchant_key = 'XXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXX';
    
    app.get("/create", function (req, res) {
    
        var name = 'Örnek Ürün / Hizmet Adı';  // Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        var price = '1445'; // 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        var currency = 'TL';  //TL - USD - EUR - GBP gönderilebilir.
        var max_installment = '12'; // 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    
        //collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        //collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        //product ise min_count (satın alma adet alt limiti) gereklidir.
    
        var link_type = 'product';
        var lang = 'tr'; //tr veya en gönderilebilir.
        var required = name + price + currency + max_installment + link_type + lang;
        var email = '';
        var min_count = '';
        if (link_type == 'product') {
            min_count = '1';
            // Alt adet limiti.
            required += min_count;
        } else {
            (link_type == 'collection')
            email = 'test@example.com';
            // Ödeme yapan kullanıcının eposta adresi.
            required += email;
        }
    
        var max_count = '1';
    
        // Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
    
        var expiry_date = '2021-06-23 17:00:00';
    
        // Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
        // Örnek format: 2021-05-31 17:00:00
    
        //Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
        //http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
        //callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    
        var callback_link = '';
    
        // Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
        //callback_link gönderildiğinde bu alan zorunlu olmaktadır.
        var callback_id = '';
    
        var debug_on = '1'; //Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(required + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/create',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'name': name,
                'price': price,
                'currency': currency,
                'max_installment': max_installment,
                'link_type': link_type,
                'lang': lang,
                'min_count': min_count,
                'email': email,
                'expiry_date': expiry_date,
                'max_count': max_count,
                'callback_link': callback_link,
                'callback_id': callback_id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(body);
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.get("/delete", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/delete',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
                /* Başarılı yanıt içerik örneği
                [status]  => success
                */
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendsms", function (req, res) {
    
        var id = 'XXXX';  // Link ID - create metodunda dönülen değerdir.
        var cell_phone = '05555555555'; // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + cell_phone + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-sms',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'cell_phone': cell_phone,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendmail", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var email = ''; // Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + email + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-email',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'email': email,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        token = callback.id + callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(token).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
        // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
        // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
        // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
        // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
        // [payment_amount]  => Ödeme tutarı.
        // [payment_type]    => Ödeme yöntemi.
        // [currency]        => Ödeme para birimi.
        // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
        // [merchant_id]     => PayTR mağaza numaranınz.
    
        // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
        ////////////////////////////////////////////////////////////////////////////////////////////
    
        if (callback.status == 'success') {
    
            //basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Link API SMS&EMAIL Servisi örnek kodlarını[**indirmek için tıklayın.**](/link-api/linkle-api-sms-and-email/PayTR Link API - Sms & Email \(Optional\).zip)

**3) SERVİSTEN DÖNEN DEĞERLER**

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
İstek sonucu | status (string) | success, error veya failed  
İstek açıklaması (hata durumunda) | reason (string) | Örnek: Zorunlu alan degeri gecersiz veya gonderilmedi (Link API - create): price  
  
  



---

# Direkt API Entegrasyonu | PayTR


# Direkt API Entegrasyonu

Direkt API çözümünde, kullanılacak tüm servislerin kullanılacak yapıya entegre edilmesi ve test işlemlerinin sağlanması mağaza tarafından yapılmaktadır. Bu sebepten dolayı ödeme sayfasının çalışması, kullanılacak servislerin sağlıklı şekilde oluşturulması ve herhangi bir işlem kaybı yaşamamak adına, yazılım bilgisine sahip olunması gerekmektedir. Direkt API çözümünde, güvenlik olmak üzere tüm akış mağaza sahibinin kontrolünde ve sorumluluğundadır. Bu çözümde herhangi hazır bir yapı bulunmamaktadır. Direkt API çözümünü kullanma talebiniz, ilgili birimlerimizin onayından geçmesi halinde mağazanıza tanımlanmaktadır. Bu konu hakkında talebinizi reddetme veya onaylama hakkını PayTR kendinde saklı tutmaktadır.

**ENTEGRASYON HAKKINDA ÖNEMLİ ÖN BİLGİLENDİRME:**  
**Mağaza Bilgileri:** Entegrasyon için gerekli olan API entegrasyon bilgilerine Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri bölümünden ulaşabilirsiniz. (Bu bilgileri sadece Ana Kullanıcı ve Teknik kullanıcı görüntülüyebilir.)  
**Entegrasyon 2 Adımlıdır:**

  1. ADIM – Web sitenizde ödeme formunun hazırlanarak API tarafından ihtiyaç duyulan bilgilerin PayTR sistemlerine gönderilmesi.
  2. ADIM - PayTR sisteminin ödeme sonuçlarını bildireceği, sitenizin bildirim sayfasının(Bildirim URL) ayrı olarak hazırlanıp kodlanması.   
  




Yardım talepleriniz için Mağaza paneli Destek & Kurulum sayfasındaki Destek Sayfasından mesajlarınızı göndermenizi rica ederiz.

Web siteniz veya uygulamanız üzerinde kullanabileceğiniz, PayTR görsellerini indirmek için [ tıklayın. ](https://dev.paytr.com/sikca-sorulan-sorular/PayTR_Gorselleri.zip)

Direkt API dokümanı ve tüm servisleri indirmek için [**tıklayın.**](/direkt-api/PayTR_Direkt_API.zip)


---

# Direkt Kart Saklama API | PayTR


# 4.1 Direkt Kart Saklama API

Kart Saklama API servisi ile kullanıcılar kart saklama yapabilir ve kayıtlı kartlar aracılığıyla ödeme alabilirsiniz. Kayıtlı kart bilgileri PayTR'da saklanmaktadır. Ödeme işlemleriniz için istek tarafımıza gönderildikten sonra işleme alınmaktadır.

**KART SAKLAMA API**  
1- Yeni Kart Ekleme. Bu [**linkten**](/direkt-api/kart-saklama-api/yeni-kart-ekleme) gidebilirsiniz.  
2- Kayıtlı karttan ödeme. Bu [**linkten**](/direkt-api/kart-saklama-api/kayitli-karttan-odeme) gidebilirsiniz.  
3- Kayıtlı kart listesi. Bu [**linkten**](/direkt-api/kart-saklama-api/kayitli-kart-listesi) gidebilirsiniz.  
4- Kayıtlı kart silme. Bu [**linkten**](/direkt-api/kart-saklama-api/kayitli-kart-silme) gidebilirsiniz.  



---

# Taksit Oranları Sorgulama | PayTR


# 4.2 Taksit Oranları Sorgulama

Direkt API entegrasyonu yapılırken, taksit oranlarını çekmek için taksit oranları sorgulama API kullanılır. Oranlar günlük olarak değişebilir. Bu nedenle bu oranları günlük olarak taksit oranları sorgulama API aracılığıyla çekip, veritabanına kaydedebilir, güncelleyebilirsiniz. Bu oranları taksitli işlemlerde ürün fiyatına göre uygulayabilirsiniz. Aşağıda yer alan tablolarda result değişkeni içinde dönen değerler ayrıntılı olarak anlatılmıştır.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
request_id | İstek atılırken oluşturulacak random değer. | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Değişkenler | Açıklamalar | Zorunlu  
---|---|---  
merchant_id | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet  
request_id | En fazla 32 karakterden oluşan (string) istek ID'si. Yanıt içerisinde tekrar geri döner. | Evet  
paytr_token |  | Evet  
single_ratio | 1 veya 0 (Mağaza tek çekim oranı için 1 gönderilmelidir) | Hayır  
abroad_ratio | 1 veya 0 (Mağaza yurtdışı tek çekim oranı için 1 gönderilmelidir) | Hayır  
  
  


**Result değişkeni içinde dönen değerler:**

Değişkenler | Açıklamalar  
---|---  
status | Success olarak dönerse veritabanı işlemleri yapılır  
request_id | En fazla 32 karakterden oluşan (string) istek ID'si. Yanıtta geri döner  
err_msg | Hata mesajı döner (Örnek:"Zorunlu alan degeri gecersiz veya gonderilmedi:")  
max_inst_non_bus | Mağazanıza tanımlı maksimum taksit sayısı  
oranlar | Mağazanıza tanımlı taksit sayısının oranları kart tipine göre (axess, world, maximum, cardfinans, paraf, advantage, combo, bonus) array formatında döner  
  
  
Taksit sorgulama örnek kodları: Örnek kodlar içinde nasıl yapılacağı detaylı olarak anlatılmaktadır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
        $merchant_id='XXXXXX';
        $merchant_key='YYYYYYYYYYYYYY';
        $merchant_salt='ZZZZZZZZZZZZZZ';
        $request_id=time();
    
        $paytr_token=base64_encode(hash_hmac('sha256',$merchant_id.$request_id.$merchant_salt,$merchant_key,true));
    
        $post_vals=array(
            'merchant_id'=>$merchant_id,
            'request_id'=>$request_id,
            'paytr_token'=>$paytr_token
        );
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/taksit-oranlari");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
        {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
        $result=json_decode($result,1);
    
        if($result[status]=='success')
        {
            //VT işlemleri vs.
            print_r($result);
        }
        else //Örn. $result -> array('status'=>'error', "err_msg" => "Zorunlu alan degeri gecersiz veya gonderilmedi: "
        {
            echo $result[err_msg];
        }
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import time
    
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXX'
    merchant_key = b'XXX'
    merchant_salt = 'XXX'
    
    # Sorgu ID
    request_id = str(time.time())
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + request_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'request_id': request_id,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/taksit-oranlari', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        # VT işlemleri vs.
        print(res)
    else:
        """
        Örn.
        ['status']        - error
        ['err_no']        - 006
        ['err_msg']       - Zorunlu alan degeri gecersiz veya gonderilmedi: 
        """
        print(res)
    
    
    using Newtonsoft.Json.Linq; // Bu satırda hata alırsanız, site dosyalarınızın olduğu bölümde bin isimli bir klasör oluşturup içerisine Newtonsoft.Json.dll adlı DLL dosyasını kopyalayın.
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Linq;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class taksit_ornek : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
            //
            // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
            string merchant_id      = "XXXXXX";
            string merchant_key     = "YYYYYYYYYYYYYY";
            string merchant_salt    = "ZZZZZZZZZZZZZZ";
            //
            // İstek ID: İstekler için belirlediğiniz benzersiz numara
            string request_id       = "";
            //
            // Gönderilecek veriler oluşturuluyor
            NameValueCollection data = new NameValueCollection();
            data["merchant_id"] = merchant_id;
            data["request_id"] = request_id;
            //
            // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
            string Birlestir = string.Concat(merchant_id, request_id, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            data["paytr_token"] = Convert.ToBase64String(b);
            //
            using (WebClient client = new WebClient()) {
                client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                byte[] result = client.UploadValues("https://www.paytr.com/odeme/taksit-oranlari", "POST", data);
                string ResultAuthTicket = Encoding.UTF8.GetString(result);
                dynamic json = JValue.Parse(ResultAuthTicket);
    
                if (json.status == "success") {
                    //VT işlemleri vs.
                    Response.Write(json);
                }else{ //Örn. $result -> array('status'=>'error', "err_msg" => "Zorunlu alan degeri gecersiz veya gonderilmedi: ")
                    Response.Write(json.err_msg);
                }
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var microtime = require('microtime');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_id = 'XXXXXX';
    var merchant_key = 'YYYYYYYYYYYYYY';
    var merchant_salt = 'ZZZZZZZZZZZZZZ';
    
    var request_id = microtime.now(); // İstek ID: İstekler için belirlediğiniz benzersiz numara.
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + request_id + merchant_salt).digest('base64');
    
    app.get("/", function (req, res) {
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/taksit-oranlari',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'request_id': request_id,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send(response.body);
            // VT işlemleri
    
        } else {
            console.log(response.body);
            res.end(response.body);
            //Örn. $result -> array('status'=>'error', "err_msg" => "Zorunlu alan degeri gecersiz veya gonderilmedi: ")
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Taksit sorgulama örnek kodlarını[**indirmek için tıklayın.**](/direkt-api/taksit-sorgulama/PayTR Taksit Oranları Sorgulama Servisi.zip)


---

# BIN Sorgulama Servisi | PayTR


# 4.3 BIN Sorgulama Servisi

BIN sorgulama servisi ile bir BIN numarası gönderip kartın detaylı bilgilerine ulaşabilirsiniz.

1- Detayını sorgulamak istediğiniz kartın BIN numarasını (kart numarasının ilk 6 veya 8 hanesini) ve aşağıdaki tabloda belirtilen diğer bilgileri https://www.paytr.com/odeme/api/bin-detail adresine POST ile gönderin.   


**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
bin_number | BIN Numarası: Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın. | Evet | Maksimum 8 hane olacak şekilde.  
merchant_id | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Zorunlu | Açıklama  
---|---|---  
merchant_id(integer) | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası  
bin_number(string) | Evet | BIN Numarası: Kart numarasının ilk 6 veya 8 hanesi  
paytr_token(string) | Evet | Paytr Token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
  
  
2- Yaptığınız bu isteğe cevap JSON formatında döner.  
a. BIN Numarası tanmlı değilse (Örneğin bir yurtdışı kartı ise) status değeri “failed” olarak döner.  
b. Eğer BIN numarası tanımlı ise status değeri “success” olarak döner ve aşağıdaki tabloda bulunan bilgiler döner.  
c. Eğer sorguda bir hatanız varsa status değeri “error” döner. Bu durumda hata detayı için “err_msg” içeriğini kontrol etmelisiniz.   


Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.   


Alan adı / tipi | Değerler | Açıklama  
---|---|---  
status (string) | success, error veya failed | Status: Sorgulama sonucu  
cardType (string) | credit / debit | Kart Türü: Kartın tipi  
businessCard (string) | y / n | Şirket Kartı: Kartın şirket kartı olup olmadığı bilgisi  
bank (string) | Örnek: Yapı Kredi | Banka: Kartın bankası  
brand (string) | Örnek: axess, bonus,cardfinans, combo,world, paraf, advantage,maximum,saglamkart | Kart Program Ortaklığı İsmi: Kartın program ortaklığı ismi(Kart bir program ortaklığına dahil değil ise değer none olur. Bu durumda ilgili kart ile PayTR üzerinden taksitli işlem yapılamaz.)  
schema (string) | VISA, MASTERCARD, AMEX, TROY, OTHER | Kartın hangi şemaya ait olduğu. (Kartın hangi şemaya ait olduğu bilinmiyorsa OTHER döner.)  
bankCode (int) | Örnek: 0010 | Banka Kodu: Kart bankasının kodu  
allow_non3d (string) | Y(yes) ve N(no) | Non-3D işlem izni sonucu  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ## BIN sorgulama servisi için kullanılacak örnek kod ##
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXX';
        $merchant_salt  = 'XXXXXX';
        #
        ## Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
        $bin_number = "";
        #
        ############################################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $hash_str = $bin_number . $merchant_id . $merchant_salt;
        $paytr_token=base64_encode(hash_hmac('sha256', $hash_str, $merchant_key, true));
        $post_vals=array(
            'merchant_id'=>$merchant_id,
            'bin_number'=>$bin_number,
            'paytr_token'=>$paytr_token
        );
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/bin-detail");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR BIN detail request timeout. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die("PAYTR BIN detail request error. Error:".$result['err_msg']);
        elseif($result['status']=='failed')
            die("BIN tanımlı değil. (Örneğin bir yurtdışı kartı)");
        else
            print_r($result);
    
    ?>
    
    
    
    # Python 3.6+
    # BIN sorgulama servisi için kullanılacak örnek kod
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXX'
    merchant_key = b'XXX'
    merchant_salt = 'XXX'
    
    # Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
    bin_number = 'XXXXXX'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = bin_number + merchant_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'bin_number': bin_number,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/bin-detail', params)
    res = json.loads(result.text)
    
    if res['status'] == 'error':
        print('PAYTR BIN detail request error. Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print('BIN tanımlı değil. (Örneğin bir yurtdışı kartı)')
    else:
        print(result.text)
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    namespace WebApplication1.Controllers
    {
        public class HomeController : Controller
        {
            public ActionResult GetBinDetail()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "XXXXXX";
                string merchant_key = "XXXXXX";
                string merchant_salt = "XXXXXX";
                //
                // Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
                string bin_number = "";
                //
                // ###########################################################################
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(bin_number, merchant_id, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["bin_number"] = bin_number;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/bin-detail", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "success")
                    {
                        Response.Write(json);
                    }
                                else if (json.status == "failed")
                    {
                        Response.Write("BIN tanımlı değil. (Örneğin bir yurtdışı kartı)");
                    }
                                else if (json.status == "error")
                    {
                        Response.Write("PAYTR BIN detail request error. Error:" + json.err_msg + "");
                    }
                }
    
                return View();
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXX';
    var merchant_salt = 'XXXXXX';
    // Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
    var bin_number = 'XXXXXX';
    // Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. //
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(bin_number + merchant_id + merchant_salt).digest('base64');
    
    app.get("/", function (req, res) {
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/api/bin-detail',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'bin_number': bin_number,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send(response.body);
    
        } else {
            res.end(response.body);
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

  


BIN Sorgulama örnek kodları[**indirmek için tıklayın.**](/direkt-api/bin-sorgulama-servisi/PayTR_BIN_Sorgulama_Servisi.zip)


---

# Direkt API Entegrasyonu 1. Adım | PayTR


# Direkt API Entegrasyonu 1. Adım

Direkt API yöntemini kullanabilmeniz için ilgili birimlerimizden yetki almanız gerekmektedir. Eğer Direkt API yetkinizin açık olduğundan emin değilseniz. PayTR Mağaza Paneli > Destek & Kurulum -> Destek adımları üzerinden Direkt API yetkisi talep edebilir veya yetkinizin aktifliğinin kontrol edilmesini sağlayabilirsiniz. 

**ÖDEME FORMUNDAN BİLGİLERİN ALINARAK AKTARILMASI**

1) Müşteri, üye işyeri web sayfasında satın alma isteminde bulunur.

2) Üye işyeri bu istek doğrultusunda, Müşteriye ödeme seçeneklerini sunduğu sayfaya yönlendirir.

3) Müşterinin ödeme için bilgileri girmesi ve onaylaması sonrasında, Üye işyeri sayfası aşağıda belirlenmiş verileri aşağıdaki sırayla, PAYTR bilgisi dahilinde olan üye işyeri parolası ve üye işyeri gizli anahtarı ile önce sha256 algoritması ve HMAC(http://en.wikipedia.org/wiki/Hash-based_message_authentication_code) yöntemi ile şifreleyerek token oluşturur. Sonrasında token'ı base64 hale dönüştürür. 

4) Eğer müşteri taksitli işlem gerçekleştirecekse kartın hangi kart ailesine ait olduğunu öğrenebilmek için [**Binsorgu**](https://dev.paytr.com/direkt-api/bin-sorgulama-servisi) servisine istek yapılır. Binsorgu servisinden dönülen "brand" alanı yakalanarak ödeme isteğinde "card_type" parametresinde iletilir.

5) Eğer bir taksit tablosu gösterilmek istenirse veya işlemde taksitli vade farkı müşteriye yansıtılmak istenirse [**taksit-oranları**](https://dev.paytr.com/direkt-api/taksit-sorgulama) servisi üzerinden ilgili tüm taksit oranları çekilebilir.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası |  |   
user_ip (string) | Müşteri ip: İstek anında aldığınız müşteri ip numarası(Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | Evet | En fazla 39 karakter (ipv4)  
merchant_oid (string) | Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası.(Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | Evet | En fazla 64 karakter,Alfa numerik  
email (string) | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | Evet | En fazla 100 karakter  
payment_amount(integer) | Ödeme tutarı: Siparişe ait toplam ödeme tutarı | Evet | Ayraç olarak yalnızca nokta(.) gönderilmelidir  
payment_type(string) | Ödeme tipi | Evet | ('card')  
installment_count(int) | Taksit sayısı | Evet | 0, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12  
currency(string) | Para birimi | Hayır | TL, EUR, USD, GBP, RUB(Boş ise TL kabul edilir)  
test_mode | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | Hayır | 0 veya 1  
non_3d | Non 3D işlem yapabilmek için 1 gönderilebilir | Evet | 0 veya 1  
request_exp_date(int) | Sıfırdan farklı bir değer gönderilmesi durumunda,ödeme işlemi bu süre öncesinde tamamlanmalıdır.(Ödeme sırasında sisteminizde fiyat güncellemesi olması durumuna karşı güvenlik amaçlı kullanabilirsiniz) | Hayır | Timestamp  
  
  
4) Üye iş yeri, ürettiği token, token üretmek için kullandığı veriler ve token üretimi için gerekmeyen ancak ödeme işlemi için gerekli veriler ile birlikte https://www.paytr.com/odeme adresine POST metodu ile gönderir. (Önemli Uyarı: Üye iş yeri sayfasındaki form, kart bilgileri içerdiğinden sadece PayTR’a POST edilmelidir. Üye iş yerinin kendi sunucusuna POST kesinlikle yapılmamalıdır.)

**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet  
paytr_token (string) | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız  
user_ip (string) | Müşteri ip: İstek anında aldığınız müşteri ip numarası (Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | Evet | En fazla 39 karakter (ipv4)  
merchant_oid (string) | Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası. (Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | Evet | En fazla 64 karakter, Alfa numerik  
email (string) | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | Evet | En fazla 100 karakter  
payment_type(string) | Ödeme tipi | Evet | ('card')  
payment_amount (double), ondalık olarak nokta (.) ve noktadan sonra iki hane | Ödeme tutarı: Siparişe ait toplam ödeme tutarı | Evet | Örn: 100.99 veya 150 veya 1500.35  
installment_count(int) | Taksit sayısı | Evet | 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12  
card_type(string) | Kart tipi (Taksitli işlemlerde kullanmak üzere) | Hayır | advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart  
currency(string) | Para birimi | Hayır | TL, EUR, USD (Boş ise TL kabul edilir)  
client_lang(string) | Ödeme sürecinde kullanılacak dil | Hayır | Türkçe için tr veya İngilizce için en (Boş gönderilirse tr geçerli olur)  
test_mode | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | Hayır | 0 veya 1  
non_3d | Non 3D işlem yapabilmek için 1 gönderilebilir | Evet | 0 veya 1  
non3d_test_failed | Non 3D işlemde, başarısız işlem durumunu test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!) | Hayır | 0 veya 1  
cc_owner(string) | Kart sahibi | Evet | 50 karakter  
card_number(string) | Kart numarası | Evet | 16 karakter  
expiry_month(string) | Kart son kullanma tarihi(Ay) | Evet | 1, 2, 3, .. , 11, 12  
expiry_year(string) | Kart son kullanma tarihi(Yıl) | Evet | 25, 26, 27,…  
cvv(string) | Kart güvenlik kodu | Evet | 3 karakter  
merchant_ok_url(string) | Müşterinin başarılı ödeme sonrası yönledirileceği sayfa (Örn.Siparişlerim takip sayfası)(Uyarı: Müşteri bu sayfaya ulaştığında henüz sipariş onaylanmış olmaz) | Evet | En fazla 400 karakter Uyarı: Tam URL olmalıdır  
merchant_fail_url(string) | Müşterinin ödemesi sırasında beklenmeyen bir hatada yönlendirileceği sayfa | Evet | En fazla 400 karakter Uyarı: Tam URL olmalıdır  
user_name (string) | Müşteri adı ve soyadı: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız adı ve soyadı | Evet | En fazla 60 karakter  
user_address (string) | Müşteri adresi: Müşterinin sipariş sırasında ilettiği adresi | Evet | En fazla 400 karakter  
user_phone (string) | Müşteri telefon numarası: Müşterinin sipariş sırasında ilettiği telefon numarası | Evet | En fazla 20 karakter  
user_basket (string) | Sepet içeriği: Müşterinin siparişindeki ürün/hizmet bilgilerini içermelidir | Evet | JSON tipinde(Örnek kodları inceleyin)  
debug_on (int) | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | Hayır | 0 veya 1(Entegrasyon ve test sürecinde hataları tespit etmek için mutlaka 1  
sync_mode (int) | Sync Mode: Ödeme isteğinin gönderilmesi ardından işlem sonucuna göre başarılı veya başarısız sayfasına yönlendirme yapılmadan, JSON formatında olan yanıt direkt olarak istek sonucuna döner. Ek olarak; işleme ait detaylar tanımlı olan Bildirim URL adresine gönderilir. Sync mode sonucunda dönen status alanının alabileceği değerler “failed”, “wait_callback” ve “success” şeklindedir.Not: Bu işlem için mağazanızda Non3D yetkisinin açık olması gerekmektedir. | Hayır | 0 veya 1(İlgili yetkinin mağazaya tanımlanabilmesi için tarafımıza talep iletilmesi gerekmektedir. Birimlerimizin onayından geçmesi halinden yetki mağazaya tanımlanacaktır.)  
  
**SYNC MODE YANITLARI**

status | msg (Açıklama) | utoken, ctoken (Kart saklama yapıldıysa)  
---|---|---  
failed | “Henüz devam eden bir işleminiz bulunmaktadır, sonuçlandıktan sonra tekrar deneyebilirsiniz.” veya farklı bir hata mesajı. | Hayır  
wait_callback | Ödeme Kontrol Ediliyor, Bildirimi Bekleyin. | Evet  
success | Ödeme Başarılı. | Evet  
  
  


5) PAYTR sistemi, gönderilen bilgiler üzerinden kontrol ve doğrulamaları yapar ve ödeme sonucuna göre üye işyerinin vermiş olduğu merchant_ok_url veya merchant_fail_url adresine müşteriyi yönlendirir. Merchant_ok_url’e yönlenme durumunda POST içeriğinde herhangi bir veri gönderilmez. Merchant_fail_url’e yönlendirme durumunda POST içeriğinde fail_message alanında ödemenin neden başarısız olduğu bilgisi bulunur. Bu bilgi müşteriye doğrudan gösterilebilir şekilde formatlanmış bir mesajdır

6) Ödeme girişiminin sonucu, Üye işyeri web sitesindeki Bildirim URL’e(Callback URL), token, üye işyeri sipariş numarası ve ödeme durumu vb. bilgisinin post edilmesiyle üye işyerine bildirilir.

  


Yukarıda anlatılan aşamaların tamamlanmasıyla birlikte, ödeme işleminde müşterinin etkileşimde bulunacağı kısım entegrasyonda böylece tamamlanmış olur. ANCAK; entegrasyonunuz henüz tamamlanmamıştır, 2. ADIM ödeme sonucunu (başarılı/başarısız) almanız ve siparişi onaylamanız / iptal etmeniz için gereklidir. 

**ÖNEMLİ UYARI:** PayTR ödeme alt yapısı asenkron olarak çalışmaktadır. Bu nedenle ödeme tamamlandığında müşteri merchant_ok_url'e yönlendirilirken, ödemenin kesin sonucu (Başarılı ya da Başarısız sonucu) Bildirim URL'ye POST ile gönderilmektedir. merchant_ok_url'e herhangi bir veri POST edilmemektedir, bu nedenle merchant_ok_url olarak belirttiğiniz sayfada sipariş onay/iptal gibi işlem yapmamalısınız.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
        </head>
    
        <?php
    
            $merchant_id = 'MAGAZA_NO';
            $merchant_key = 'XXXXXXXXXXX';
            $merchant_salt = 'YYYYYYYYYYY';
    
            $merchant_ok_url="http://site-ismi/basarili";
            $merchant_fail_url="http://site-ismi/basarisiz";
    
            $user_basket = htmlentities(json_encode(array(
                array("Altis Renkli Deniz Yatağı - Mavi", "18.00", 1),
                array("Pharmasol Güneş Kremi 50+ Yetişkin & Bepanthol Cilt Bakım Kremi", "33,25", 2),
                array("Bestway Çocuklar İçin Plaj Seti Beach Set ÇANTADA DENİZ TOPU-BOT-KOLLUK", "45,42", 1)
            )));
    
            srand(time(null));
            $merchant_oid = rand();
    
            $test_mode="0";
    
            //3d'siz işlem
            $non_3d="0";
    
            //Ödeme süreci dil seçeneği tr veya en
            $client_lang = "tr";
    
            //non3d işlemde, başarısız işlemi test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!)
            $non3d_test_failed="0";
    
            if( isset( $_SERVER["HTTP_CLIENT_IP"] ) ) {
                $ip = $_SERVER["HTTP_CLIENT_IP"];
            } elseif( isset( $_SERVER["HTTP_X_FORWARDED_FOR"] ) ) {
                $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
            } else {
                $ip = $_SERVER["REMOTE_ADDR"];
            }
    
            $user_ip = $ip;
    
            $email = "testnon3d@paytr.com";
    
            // 100.99 TL ödeme
            $payment_amount = "100.99";
            $currency="TL";
            //
            $payment_type = "card";
    
    //      $card_type = "bonus";       // Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart
    //      $installment_count = "5";
    
            $post_url = "https://www.paytr.com/odeme";
    
            $hash_str = $merchant_id . $user_ip . $merchant_oid . $email . $payment_amount . $payment_type . $installment_count. $currency. $test_mode. $non_3d;
            $token = base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
        ?>
    
        <body>
            <form action="<?php echo $post_url;?>" method="post">
              Kart Sahibi Adı: <input type="text" name="cc_owner" value="TEST KARTI"><br>
              Kart Numarası: <input type="text" name="card_number" value="9792030394440796"><br>
              Kart Son Kullanma Ay: <input type="text" name="expiry_month" value="12" ><br>
              Kart Son Kullanma Yıl: <input type="text" name="expiry_year" value="99"><br>
              Kart Güvenlik Kodu: <input type="text" name="cvv" value="000"><br>
              <input type="hidden" name="merchant_id" value="<?php echo $merchant_id;?>">
              <input type="hidden" name="user_ip" value="<?php echo $user_ip;?>">
              <input type="hidden" name="merchant_oid" value="<?php echo $merchant_oid;?>">
              <input type="hidden" name="email" value="<?php echo $email;?>">
              <input type="hidden" name="payment_type" value="<?php echo $payment_type;?>">
              <input type="hidden" name="payment_amount" value="<?php echo $payment_amount;?>">
              <input type="hidden" name="currency" value="<?php echo $currency;?>">
              <input type="hidden" name="test_mode" value="<?php echo $test_mode;?>">
              <input type="hidden" name="non_3d" value="<?php echo $non_3d;?>">
              <input type="hidden" name="merchant_ok_url" value="<?php echo $merchant_ok_url;?>">
              <input type="hidden" name="merchant_fail_url" value="<?php echo $merchant_fail_url;?>">
              <input type="hidden" name="user_name" value="Paytr Test">
              <input type="hidden" name="user_address" value="test test test">
              <input type="hidden" name="user_phone" value="05555555555">
              <input type="hidden" name="user_basket" value="<?php echo $user_basket; ?>">
              <input type="hidden" name="debug_on" value="1">
              <input type="hidden" name="client_lang" value="<?php echo $client_lang; ?>">
              <input type="hidden" name="paytr_token" value="<?php echo $token; ?>">
              <input type="hidden" name="non3d_test_failed" value="<?php echo $non3d_test_failed; ?>">
              <input type="hidden" name="installment_count" value="<?php echo $installment_count; ?>">
              <input type="hidden" name="card_type" value="<?php echo $card_type; ?>">
              <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # Tek başına bir bütün değildir, home.html ile birlikte çalışmaktadır.
    # card_type, installment_count gibi kullanıcıya bağlı bilgiler alındıktan sonra paytr_token oluşturulması gerekmektedir.
    
    import base64
    import hashlib
    import hmac
    import html
    import json
    import random
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    def home(request):
        merchant_id = 'MAGAZA_NO'
        merchant_key = b'XXXXXXXXXXX'
        merchant_salt = b'YYYYYYYYYYY'
    
        merchant_ok_url = 'http://site-ismi/basarili'
        merchant_fail_url = 'http://site-ismi/basarisiz'
    
        user_basket = html.unescape(json.dumps([['Altis Renkli Deniz Yatağı - Mavi', '18.00', 1],
                                                ['Pharmaso Güneş Kremi 50+ Yetişkin & Bepanthol Cilt Bakım Kremi', '33,25',
                                                 2],
                                                ['Bestway Çocuklar İçin Plaj Seti Beach Set ÇANTADA DENİZ TOPU-BOT-KOLLUK',
                                                 '45,42', 1]]))
    
        merchant_oid = 'OS' + random.randint(1, 9999999).__str__()
        test_mode = '0'
        debug_on = '1'
    
        # 3d'siz işlem
        non_3d = '0'
    
        # Ödeme süreci dil seçeneği tr veya en
        client_lang = 'tr'
    
        # non3d işlemde, başarısız işlemi test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!)
        non3d_test_failed = '0'
        user_ip = ''
        email = 'testnon3d@paytr.com'
    
        # 100.99 TL ödeme
        payment_amount = "100.99"
        currency = 'TL'
        payment_type = 'card'
    
        user_name = 'Paytr Test'
        user_address = 'test test test'
        user_phone = '05555555555'
    
        # Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart
        card_type = 'bonus'
        installment_count = '5'
    
        hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + payment_type + installment_count + currency + test_mode + non_3d
        paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    
        context = {
            'merchant_id': merchant_id,
            'user_ip': user_ip,
            'merchant_oid': merchant_oid,
            'email': email,
            'payment_type': payment_type,
            'payment_amount': payment_amount,
            'currency': currency,
            'test_mode': test_mode,
            'non_3d': non_3d,
            'merchant_ok_url': merchant_ok_url,
            'merchant_fail_url': merchant_fail_url,
            'user_name': user_name,
            'user_address': user_address,
            'user_phone': user_phone,
            'user_basket': user_basket,
            'debug_on': debug_on,
            'client_lang': client_lang,
            'paytr_token': paytr_token.decode(),
            'non3d_test_failed': non3d_test_failed,
            'installment_count': installment_count,
            'card_type': card_type
        }
    
        return render(request, 'home.html', context)
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    namespace WebApplication1.Controllers
    {
        public class HomeController : Controller
        {
            public ActionResult Test()
            {
                ViewBag.Message = "Your test page.";
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "XXXXXX";
                string merchant_key = "XXXXXX";
                string merchant_salt = "XXXXXX";
                //
                // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
                string emailstr = "info@siteniz.com";
                //
                // Tahsil edilecek tutar.
                int payment_amountstr = 100.99;
                //
                // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
                string merchant_oid = "";
                //
                // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
                string user_namestr = "";
                //
                // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
                string user_addressstr = "";
                //
                // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
                string user_phonestr = "";
                //
                // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
                // !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
                // !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
                string merchant_ok_url = "http://siteniz.com/Success";
                //
                // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
                // !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
                // !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
                string merchant_fail_url = "http://siteniz.com/Failed";
                //        
                // !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
                // buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
                string user_ip = Request.ServerVariables["HTTP_X_FORWARDED_FOR"];
                if (user_ip == "" || user_ip == null){
                    user_ip = Request.ServerVariables["REMOTE_ADDR"];
                }
                //
                // ÖRNEK $user_basket oluşturma - Ürün adedine göre object'leri çoğaltabilirsiniz
                object[][] user_basket = {
                new object[] {"Örnek ürün 1", "18.00", 1}, // 1. ürün (Ürün Ad - Birim Fiyat - Adet)
                new object[] {"Örnek ürün 2", "33.25", 2}, // 2. ürün (Ürün Ad - Birim Fiyat - Adet)
                new object[] {"Örnek ürün 3", "45.42", 1}, // 3. ürün (Ürün Ad - Birim Fiyat - Adet)
                };
                /* ############################################################################################ */
                // Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart
                string card_type = "bonus";
                //
                // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
                string debug_on = "1";
                //
                // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
                string test_mode = "0";
                //
                // 3D'siz işlem
                string non_3d = "0";
                //
                // Non3d Test Failed
                string non3d_test_failed = "0";
                //
                // Taksit Sayısı
                string installment_count = "0";
                //
                // Ödeme türü
                string payment_type = "card";
                //
                // Post adresi
                string post_url = "https://www.paytr.com/odeme";
                //
                // Para birimi olarak TL, EUR, USD gönderilebilir. USD ve EUR kullanmak için kurumsal@paytr.com 
                // üzerinden bilgi almanız gerekmektedir. Boş gönderilirse TL geçerli olur.
                string currency = "TL";
                //
                //
                // Sepet içerği oluşturma fonksiyonu, değiştirilmeden kullanılabilir.
                JavaScriptSerializer ser = new JavaScriptSerializer();
                string user_basket_json = ser.Serialize(user_basket);
                //
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(merchant_id, user_ip, merchant_oid, emailstr, payment_amountstr.ToString(), payment_type, installment_count, currency, test_mode, non_3d, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                //
                ViewBag.MerchantId = merchant_id;
                ViewBag.UserIp = user_ip;
                ViewBag.MerchantOid = merchant_oid;
                ViewBag.Email = emailstr;
                ViewBag.PaymentType = payment_type;
                ViewBag.PaymentAmount = payment_amountstr.ToString();
                ViewBag.InstallmentCount = installment_count;
                ViewBag.Currency = currency;
                ViewBag.TestMode = test_mode;
                ViewBag.Non3d = non_3d;
                ViewBag.MerchantOkUrl = merchant_ok_url;
                ViewBag.MerchantFailUrl = merchant_fail_url;
                ViewBag.UserName = user_namestr;
                ViewBag.UserAddress = user_addressstr;
                ViewBag.UserPhone = user_phonestr;
                ViewBag.UserBasket = user_basket_json;
                ViewBag.Non3dTestFailed = non3d_test_failed;
                ViewBag.DebugOn = debug_on;
                ViewBag.CardType = card_type;
                ViewBag.PostUrl = post_url;
                ViewBag.PaytrToken = Convert.ToBase64String(b);
    
                return View();
            }
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var nodeBase64 = require('nodejs-base64-converter');
    var app = express();
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'MAGAZA_NO';
    var merchant_key = 'XXXXXXXXXXX';
    var merchant_salt = 'YYYYYYYYYYY';
    var basket = JSON.stringify([
        ['Örnek Ürün 1', '50.00', 1], // 1. ürün (Ürün Ad - Birim Fiyat - Adet)
        ['Örnek Ürün 2', '33.25', 2], // 2. ürün (Ürün Ad - Birim Fiyat - Adet)
        ['Örnek Ürün 3', '45.42', 1] // 3. ürün (Ürün Ad - Birim Fiyat - Adet)
    ]);
    var user_basket = basket;
    var merchant_oid = "IN" + microtime.now(); // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    var user_ip = '';
    var email = 'testnon3d@paytr.com'; // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi.
    var payment_amount = '100.99'; // Tahsil edilecek tutar.
    var currency = 'TL';
    var test_mode = '0';
    var user_name = 'PayTR Test';
    var user_address = 'test test test'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi.
    var user_phone = '05555555555';
    // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa. 
    // Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    // Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü ve sayfanın devamında bulunan /callback adımı).
    var merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php';
    // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php';
    var debug_on = 1;
    var client_lang = 'tr'; //Ödeme süreci dil seçeneği tr veya en.
    var payment_type = 'card'; // Ödeme türü
    var non_3d = '0'; //3d'siz işlem
    var card_type = '';  // Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart
    var installment_count = '0'; // Taksit Sayısı
    
    //non3d işlemde, başarısız işlemi test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!)
    var non3d_test_failed = '0';
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${payment_type}${installment_count}${currency}${test_mode}${non_3d}`;
        console.log('HASH STR' + hashSTR);
        var paytr_token = hashSTR + merchant_salt;
        console.log('PAYTR TOKEN' + paytr_token);
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        console.log('TOKEN' + token);
        context = {
            merchant_id,
            user_ip,
            merchant_oid,
            email,
            payment_type,
            payment_amount,
            currency,
            test_mode,
            non_3d,
            merchant_ok_url,
            merchant_fail_url,
            user_name,
            user_address,
            user_phone,
            user_basket,
            debug_on,
            client_lang,
            token,
            non3d_test_failed,
            installment_count,
            card_type,
        };
    
        res.render('index');
    
    });
    
    app.post("/callback", function (req, res) {
    
        // ÖNEMLİ UYARILAR!
        // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        if (callback.status == 'success') {
            // basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');  // Bildirimin alındığını PayTR sistemine bildir.  
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Direkt API 1. Adım örnek kodları[**indirmek için tıklayın.**](/direkt-api/direkt-api-1-adim/PayTR_Direkt__API_1.ADIM.zip)


---

# Direkt API Entegrasyonu 2. Adım | PayTR


# Direkt API Entegrasyonu 2. Adım

**ÖDEME SONUÇLARININ ALINMASI İÇİN BİLDİRİM URL’in HAZIRLANMASI**

**1\. ADIM** ’da ödeme formunu kullanarak müşteriniz ödeme yaptığında, PayTR sistemi ödeme sonucunu yazılımınıza bildirmelidir ve yazılımınızdan bildirimin alındığına dair cevap almalıdır. Aksi halde, ödeme işlemi tamamlanmaz ve tarafınıza ödeme aktarılmaz.

PayTR sistemince ödeme sonuç bildiriminin yapılacağı sayfa (Bildirim URL) tarafınızca belirlenmeli ve Mağaza Paneli Destek & Kurulum alanındaki AYARLAR sayfasında tanımlanmalıdır.

Tanımlayacağınız Bildirim URL’ye POST metodu ile ödemenin sonucu (başarılı veya başarısız) her işlem için ayrı olarak gönderilir. Bu bildirime istinaden Bildirim URL’nizde yapacağınız kodlama ile yazılımınızda siparişi onaylamalı veya iptal etmelisiniz, ekrana OK basarak PayTR sistemine cevap vermelisiniz.

**PayTR sistemince Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**

  


Alan adı | Zorunlu | Token | Açıklama  
---|---|---|---  
merchant_oid | Evet | Evet | Mağaza sipariş no: Satış işlemi için belirlediğiniz ve 1. ADIM’da gönderdiğiniz sipariş numarası  
status | Evet | Evet | Ödeme işleminin sonucu (success veya failed)  
total_amount | Evet | Evet | İşlem başarılı ise ödeme tutarı, işlem başarısız ise sıfır (0) döner.  
hash | Evet | Evet | PayTR sisteminden gönderilen değerlerin doğruluğunu kontrol etmeniz için güvenlik amaçlı oluşturulan hash değeri (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
failed_reason_code | Hayır | Evet | Ödemenin onaylanmaması durumunda gönderilir (Bkz: 2. Adım İçin Hata Kodları ve Açıklamaları Tablosu)  
failed_reason_msg | Hayır | Evet | Ödemenin neden onaylanmadığı mesajını içerir (Bkz: 2. Adım İçin Hata Kodları ve Açıklamaları Tablosu)  
test_mode | Evet | Evet | Mağazanız test modunda iken veya canlı modda yapılan test işlemlerde 1 olarak gönderilir.  
payment_type | Evet | Evet | Ödeme şekli: Müşterinin hangi ödeme şekli ile ödemesini tamamladığını belirtir. 'card' veya 'eft' değerlerini alır.  
currency | Evet | Hayır | Para birimi: Ödemenin hangi para birimi üzerinden yapıldığını belirtir. ‘TL’, ‘USD’, ‘EUR’, ‘GBP, ‘RUB’ değerlerinden birini alır.  
payment_amount | Evet | Hayır | Sipariş tutarı: 1. ADIM’da gönderdiğiniz “payment_amount” değeridir.(100 ile çarpılmış hali gönderilir. 34.56 => 3456)  
installment_count | Evet | Hayır | İşlemde yapılan taksit sayısı  
  
**Bildirim URL’nize PayTR sistemince yapılacak isteğe dönülmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**
    
    
    Örnek (PHP): echo "OK";
    
    
    Örnek (.NET): Response.Write("OK");
    

**ÖNEMLİ UYARILAR:**

  1. Bildirim URL adresinize üye girişi ve benzeri erişim kısıtlaması yapılmamalıdır. Böylece PayTR sistemi bildirimleri kolayca iletebilecektir.

  2. Bildirim URL’nize gelecek bildirimlere döneceğiniz OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır.

  3. Bildirim URL’niz, müşterinizin ödeme sırasında ulaşacağı bir sayfa değildir, PayTR tarafından arka planda (server-side) ödeme sonucunu bildirmek için kullanılır. Bu nedenle, Bildirim URL’nizde kodlama yaparken oturum (SESSION) değerlerini kullanamazsınız. İşlemlerinizi Mağaza sipariş no (merchant_oid) kullanarak gerçekleştirmelisiniz.

  4. OK yanıtı alınmayan bildirimlerde, ilgili sipariş Mağaza Paneli'ndeki İşlemler sayfasında “Devam Ediyor” olarak görünecektir.

  5. PayTR sistemi, Bildirim URL’nizden OK cevabını istendiği şekilde almadığı durumda, bildirimin başarısız olduğunu varsayar. Ağ trafik sorunları, sitenizdeki anlık yoğunluklar ve benzeri nedenlerden dolayı aynı ödeme işlemi için birden fazla bildirim ulaşabilir. Bu nedenle, bildirimin birden fazla geldiği durumlarda, yalnızca ilk bildirim göz önünde bulundurulmalı, sonraki bildirimler için müşteriye tekrar ürün/hizmet sunulmamalıdır. Tekrarlayan bildirimlerde yalnızca OK yanıtı ile süreç sonlandırılmalıdır. Tekrarlayan bildirimlerin tespiti Mağaza sipariş no (merchant_oid) temel alınarak yapılmalıdır.

  6. Bildirimin PayTR sisteminden geldiğinden ve ulaşım esnasında değiştirilmediğinden emin olmak için, POST içerisindeki hash değeri ile tarafınızca oluşturulacak hash değerinin aynı olduğunu kontrol etmeniz, güvenlik açısından büyük önem arz etmektedir. Bu kontrolü yapmamanız durumunda maddi kayıplar ile karşılaşabilirsiniz.




**2\. Adım İçin Hata Kodları ve Açıklamaları**

failed_reason_code | failed_reason_msg | Açıklama  
---|---|---  
0 | DEĞİŞKEN (AÇIKLAMAYI OKUYUN) | Ödemenin neden onaylanmadığına ilişkin,detaylı hata mesajı (Örneğin: Kartın limiti /bakiyesi yetersiz).  
1 | Kimlik Doğrulama yapılmadı. Lütfen tekrar deneyin ve işlemi tamamlayın. | Müşteri, kimlik doğrulama adımında cep telefonu numarasını girmedi.  
2 | Kimlik Doğrulama başarısız. Lütfen tekrar deneyin ve şifreyi doğru girin. | Müşteri, cep telefonuna gelen şifreyi doğru girmedi.  
3 | Güvenlik kontrolü sonrası onay verilmedi veya kontrol yapılamadı. | Müşterinin işlemi PayTR tarafından güvenlik kontrolünden geçemedi veya kontrol yapılamadı.  
6 | Müşteri ödeme yapmaktan vazgeçti ve ödeme sayfasından ayrıldı. | Müşteri, kendisine tanınmış olan işlem süresinde(1. ADIM’da tanımlanan request_exp_date değeri) işlemini tamamlamadı veya müşteri ödeme sayfasını kapatarak işlemi sonlandırdı.  
8 | Bu karta taksit yapılamamaktadır. | Müşterinin kullanmakta olduğu kart ile seçmiş olduğu taksitli ödeme yöntemi kullanılamaz.  
9 | Bu kart ile işlem yetkisi bulunmamaktadır. | Müşterinin kullanmakta olduğu kart için mağazanızın işlem yetkisi bulunmuyor.  
10 | Bu işlemde 3D Secure kullanılmalıdır. | Müşteri, yapmış olduğu işlemde 3D Secure ile ödeme yapmalıdır.  
11 | Güvenlik uyarısı. İşlem yapan müşterinizi kontrol edin. | Müşterinin işleminde fraud tespiti bulunuyor. Güvenliğiniz için müşterinin işlemlerini kontrol edin.  
99 | İşlem başarısız: Teknik entegrasyon hatası. | Teknik entegrasyon hatası varsa dönülecektir. (debug_on değeri 0 ise)  
  
  


Yukarıdaki açıklamalara uygun olarak Bildirim URL’nizi hazırladıysanız, kontrol için bir adet test ödemesi gerçekleştirmelisiniz. Eğer yaptığınız test işlem PayTR Mağaza Paneli’nizdeki İŞLEMLER sayfasında “Başarılı” olarak görünürse PayTR entegrasyonunuz tümüyle tamamlanmıştır.

Eğer işlemin durumu “Devam Ediyor” olarak görünüyorsa Bildirim URL’nizden “OK” yanıtı alınamıyor demektir. İŞLEMLER sayfasında yaptığınız test işleminin satırında “Detay” linkine tıklayıp, Bildirim URL’nizden hangi yanıt geldiğini kontrol edin.

**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Destek & Kurulum > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ## 2. ADIM için örnek kodlar ##
    
        ## ÖNEMLİ UYARILAR ##
        ## 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        ## 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        ## veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        ## 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        ## siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        $post = $_POST;
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        ###########################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        #
        ## POST değerleri ile hash oluştur.
        $hash = base64_encode( hash_hmac('sha256', $post['merchant_oid'].$merchant_salt.$post['status'].$post['total_amount'], $merchant_key, true) );
        #
        ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ###########################################################################
    
        ## BURADA YAPILMASI GEREKENLER
        ## 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        ## 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
        /* Sipariş durum sorgulama örnek
           $durum = SQL
           if($durum == "onay" || $durum == "iptal"){
                echo "OK";
                exit;
            }
         */
    
        if( $post['status'] == 'success' ) { ## Ödeme Onaylandı
    
            ## BURADA YAPILMASI GEREKENLER
            ## 1) Siparişi onaylayın.
            ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            ## 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
            ## değişebilir. Güncel tutarı $post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
        } else { ## Ödemeye Onay Verilmedi
    
            ## BURADA YAPILMASI GEREKENLER
            ## 1) Siparişi iptal edin.
            ## 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
            ## $post['failed_reason_code'] - başarısız hata kodu
            ## $post['failed_reason_msg'] - başarısız hata mesajı
    
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir.
        echo "OK";
        exit;
    ?>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # 2. ADIM için örnek kodlar
    """
    ÖNEMLİ UYARILAR
    1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    """
    
    import base64
    import hashlib
    import hmac
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
    
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'YYYYYYYYYYYYYY'
        merchant_salt = 'ZZZZZZZZZZZZZZ'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # BURADA YAPILMASI GEREKENLER
        # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.
    
        if post['status'] == 'success':  # Ödeme Onaylandı
            """
            BURADA YAPILMASI GEREKENLER
            1) Siparişi onaylayın.
            2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
            Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
            """
            print(request)
        else:  # Ödemeye Onay Verilmedi
            """
            BURADA YAPILMASI GEREKENLER
            1) Siparişi iptal edin.
            2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
            post['failed_reason_code'] - başarısız hata kodu
            post['failed_reason_msg'] - başarısız hata mesajı
            """
            print(request)// 2. ADIM için örnek kodlar
    
    
    
    // 2. ADIM için örnek kodlar
    
    // ÖNEMLİ UYARILAR!
    // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
    // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
    // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class bildirim_url_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYYYYYYYY";
        string merchant_salt    = "ZZZZZZZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string merchant_oid = Request.Form["merchant_oid"];
            string status = Request.Form["status"];
            string total_amount = Request.Form["total_amount"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(merchant_oid, merchant_salt, status, total_amount);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
                }
    
            //###########################################################################
    
            // BURADA YAPILMASI GEREKENLER
            // 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
            // 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
            if (status == "success") { //Ödeme Onaylandı
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER ONAY İŞLEMLERİDİR.
                // 1) Siparişi onaylayın.
                // 2) iframe çağırma adımında merchant_oid ve diğer bilgileri veri tabanınıza kayıp edip bu aşamada karşılaştırarak eğer var ise bilgieri çekebilir ve otomatik sipariş tamamlama işlemleri yaptırabilirsiniz.
                // 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapabilirsiniz. Bu işlemide yine iframe çağırma adımında merchant_oid bilgisini kayıt edip bu aşamada sorgulayarak verilere ulaşabilirsiniz.
                // 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
                // değişebilir. Güncel tutarı Request.Form['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
                } else { //Ödemeye Onay Verilmedi
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER
                // 1) Siparişi iptal edin.
                // 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
                // $post['failed_reason_code'] - başarısız hata kodu
                // $post['failed_reason_msg'] - başarısız hata mesajı
                }          
        }
    }
    
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var nodeBase64 = require('nodejs-base64-converter');
    var app = express();
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'MAGAZA_NO';
    var merchant_key = 'XXXXXXXXXXX';
    var merchant_salt = 'YYYYYYYYYYY';
    var basket = JSON.stringify([
        ['Örnek Ürün 1', '50.00', 1], // 1. ürün (Ürün Ad - Birim Fiyat - Adet)
        ['Örnek Ürün 2', '33.25', 2], // 2. ürün (Ürün Ad - Birim Fiyat - Adet)
        ['Örnek Ürün 3', '45.42', 1] // 3. ürün (Ürün Ad - Birim Fiyat - Adet)
    ]);
    var user_basket = basket;
    var merchant_oid = "IN" + microtime.now(); // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    var user_ip = '';
    var email = 'testnon3d@paytr.com'; // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi.
    var payment_amount = '100.99'; // Tahsil edilecek tutar.
    var currency = 'TL';
    var test_mode = '0';
    var user_name = 'PayTR Test';
    var user_address = 'test test test'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi.
    var user_phone = '05555555555';
    // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa. 
    // Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    // Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü ve sayfanın devamında bulunan /callback adımı).
    var merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php';
    // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php';
    var debug_on = 1;
    var client_lang = 'tr'; //Ödeme süreci dil seçeneği tr veya en.
    var payment_type = 'card'; // Ödeme türü
    var non_3d = '0'; //3d'siz işlem
    var card_type = '';  // Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world
    var installment_count = '0'; // Taksit Sayısı
    
    //non3d işlemde, başarısız işlemi test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!)
    var non3d_test_failed = '0';
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${payment_type}${installment_count}${currency}${test_mode}${non_3d}`;
        console.log('HASH STR' + hashSTR);
        var paytr_token = hashSTR + merchant_salt;
        console.log('PAYTR TOKEN' + paytr_token);
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        console.log('TOKEN' + token);
        context = {
            merchant_id,
            user_ip,
            merchant_oid,
            email,
            payment_type,
            payment_amount,
            currency,
            test_mode,
            non_3d,
            merchant_ok_url,
            merchant_fail_url,
            user_name,
            user_address,
            user_phone,
            user_basket,
            debug_on,
            client_lang,
            token,
            non3d_test_failed,
            installment_count,
            card_type,
        };
    
        res.render('index');
    
    });
    
    app.post("/callback", function (req, res) {
    
        // ÖNEMLİ UYARILAR!
        // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        if (callback.status == 'success') {
            // basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');  // Bildirimin alındığını PayTR sistemine bildir.  
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Direkt API 2. Adım örnek kodları[**indirmek için tıklayın.**](/direkt-api/direkt-api-2-adim/PayTR Direkt API 2.ADIM.zip)


---

# Direkt API Test Kart Bilgileri | PayTR


# Direkt API Test Kart Bilgileri

**TEST KART BİLGİLERİ**

Kart bilgileri | Alabileceği değerler | Açıklama  
---|---|---  
Adı Soyadı | PAYTR TEST | Dilediğiniz şekilde gönderebilirsiniz.  
Kart No | 4355 0843 5508 4358 | Bu değer zorunludur.  
Son Kullanma | 12 / 30 | Dilediğiniz şekilde gönderebilirsiniz.  
CVV | 000 | Bu değer zorunludur.  
  
  


Kart bilgileri | Alabileceği değerler | Açıklama  
---|---|---  
Adı Soyadı | PAYTR TEST | Dilediğiniz şekilde gönderebilirsiniz.  
Kart No | 5406 6754 0667 5403 | Bu değer zorunludur.  
Son Kullanma | 12 / 30 | Dilediğiniz şekilde gönderebilirsiniz.  
CVV | 000 | Bu değer zorunludur.  
  
  


Kart bilgileri | Alabileceği değerler | Açıklama  
---|---|---  
Adı Soyadı | PAYTR TEST | Dilediğiniz şekilde gönderebilirsiniz.  
Kart No | 9792 0303 9444 0796 | Bu değer zorunludur.  
Son Kullanma | 12 / 30 | Dilediğiniz şekilde gönderebilirsiniz.  
CVV | 000 | Bu değer zorunludur.  
  
  


Test kart bilgileri direkt API çözümü için geçerlidir. iFrame API ödeme yönteminde test kart bilgileri otomatik olarak gelmektedir. Ek olarak; ad-soyad ve son kullanma tarihini test işleminde istediğiniz değerde gönderebilirsiniz. 


---

# Ön Provizyon Entegrasyonu | PayTR


# Ön Provizyon Entegrasyonu

**Provizyon Nedir?**

Provizyon yapılan kredi kartı harcamasının ön onay sürecini tanımlar. Yapılan harcamaya yönelik işlem güvenliği ve limitinin hesap ekstresine yansımadan provizyon üzerinden kontrol edilebilir. Yapılan ödemeler için ayrılmış olan karşılık bu bekleme sürecinde bankalar tarafından onaylanır ve böylece çalıntı kart, şüpheli işlem, vb. durumlara karşı kredi kartı kullanıcılarının güvenliği sağlanır.

**Kredi Kartı Provizyonu Nedir?**

Kredi kartı provizyonu yapılan harcamanın kullanıcı ve banka onayına sunulduğu ön onay sürecidir. Bu süreçte kullanıcı yaptığı harcamanın miktarını kontrol eder ve herhangi bir problem yaşanması durumunda sürece müdahil olur. Provizyondaki işlemler banka tarafından da incelenir ve onay alması ardından “kredi kartı hareketler” bölümüne yapılmış harcama tutarı olarak yansıtılır.

Ön Provizyon hakkında daha fazla bilgi almak ve entegrasyon dokümanına ulaşmak için [bize ulaşın.](https://www.paytr.com/iletisim)


---

# Havale/EFT iFrame API | PayTR


# Havale/EFT iFrame API

Havale/EFT ödeme çözümü yöntemimizi kullanmak için bizimle iletişime geçmeniz ve gerekli yetkileri mağazanıza tanımlatmanız gerekmektedir. Bizimle PayTR Mağaza Paneli > Destek & Kurulum -> Destek alanından talep oluşturarak iletişime geçebilirsiniz.

**HAVALE / EFT / PTT / ATM**   
Kredi kartı kullanım zorunluluğunu ortadan kaldıran Havale Sistemi, bir çok banka ve PTT entegrasyonu ile hizmetinizde. Düşük komisyon avantajının yanı sıra, 7/24 çalışan operasyon birimimiz yapılan ödeme isteklerini kontrol eder ve onaylanma sürecini en hızlı şekilde tamamlanmasını sağlar.

![](/user/pages/06.havale-eft-iframe-api/havale.png)

**ENTEGRASYON HAKKINDA ÖNEMLİ ÖN BİLGİLENDİRME:**

Entegrasyonda gerekli olan "Mağaza no (merchant_id)" eposta ile şirket yetkilisine gönderilecektir. "Mağaza parolası (merchant_key)" ve "Mağaza gizli anahtarı (merchant_salt)" ise Mağaza Paneli'ne giriş yapılarak Bilgi sayfasında görülebilir.

Entegrasyon 2 aşamalıdır:

  1. PayTR'a arka planda (server-side) istek yapılarak iframe_token alınması ve alınan iframe_token ile iframe içerisinde ödeme bildirim formunun açılması

  2. PayTR sisteminin ödeme sonuçlarını bildireceği, sitenizin bildirim sayfasının(Bildirim URL) hazırlanarak kodlanması





---

# Havale/EFT iFrame API 1. Adım | PayTR


# Havale/EFT iFrame API 1. Adım

Havale/EFT ödeme çözümü yöntemimizi kullanmak için bizimle iletişime geçmeniz ve gerekli yetkileri mağazanıza tanımlatmanız gerekmektedir. Bizimle PayTR Mağaza Paneli > Destek & Kurulum -> Destek alanından talep oluşturarak iletişime geçebilirsiniz.

Entegrasyon ve İşlem akışı:

1) Üye işyeri, PayTR'a iframe_token isteğinde bulunur. Bu istek arka planda (server-side) POST metodu ile gerçekleşir.

**İstek (REQUEST) yapılacak URL: https://www.paytr.com/odeme/api/get-token**

**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet |   
user_ip (string) | Müşteri ip: İstek anında aldığınız müşteri ip numarası(Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | Evet | En fazla 39 karakter (ipv4)  
merchant_oid (string) | Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası.(Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | Evet | En fazla 64 karakter,Alfa numerik  
email (string) | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | Evet | En fazla 100 karakter  
payment_amount(integer) | Ödeme tutarı: Siparişe ait toplam ödeme tutarı | Evet | Ayraç olarak yalnızca nokta(.) gönderilmelidir  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız içinoluşturacağınız değerdir | Evet | Nasıl hesaplanacağı ile ilgili lütfen örnek kodları inceleyin  
user_name | Ad-Soyad: Gönderilmesi durumunda IFrame içerisinde bulunan ödeme bildirim formunda Ad-Soyad bilgisi dolu gelir ve değiştirilemez | Hayır | En fazla 30 karakter  
user_phone | Telefon: Gönderilmesi durumunda IFrame içerisinde bulunan ödeme bildirim formunda Telefon bilgisi dolu gelir ve değiştirilemez | Hayır | 11 karakter, numerik  
payment_type(string) | Ödeme tipi | Evet | ('eft')  
tc_no_last5 | TC No Son 5 hane: Gönderilmesi durumunda IFrame içerisinde bulunan ödeme bildirim formunda TCNo Son 5 hane dolu gelir ve değiştirilemezi | Hayır | 5 karakter numerik  
bank | Banka: Gönderilmesi durumunda IFrame içerisinde banka seçimi yapılamaz, yalnızca gönderilen banka görüntülenir. | Hayır | isbank, akbank, denizbank, finansbank,halkbank, ptt, teb, vakifbank, yapikredi,ziraat seçeneklerinden bir tanesi  
test_mode | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | Hayır | 0 veya 1  
debug_on (int) | Hata döndür: Yanlış veya eksik bilgi iletilmesi durumunda hata mesajı döndürülmesi için 1 gönderilmelidir | Hayır | 0 veya 1  
timeout_limit(int) | Sıfırdan farklı bir değer gönderilmesi durumunda, ödeme işlemi bu süre içerisinde tamamlanmalıdır (Ödeme sırasında sisteminizde fiyat güncellemesi olması durumuna karşı güvenlik amaçlı kullanabilirsiniz) | Hayır | Dakika cinsinden (Gönderilmemesi durumunda 30 dakika olarak tanımlanır)  
  
**Yapılan isteğe geri dönecek yanıt (RESPONSE) JSON formatındadır. Detaylı bilgi için örnek kodu inceleyebilirsiniz.**

Üye İşyeri, başarılı yanıt içerisinde gelen iframe_token ile iframe kullanarak ödeme bildirim formunu açar.

**NOT:** Yukarıda anlatılan işlemlerin tamamlanmasıyla birlikte müşteri tarafından kullanılacak olan ödeme bildirimi formu ekranda belirecektir.

Ödeme işleminde müşterinin etkileşimde bulunacağı adım entegrasyonda böylece tamamlanmış olur. ANCAK; entegrasyonunuz henüz tamamlanmamıştır, 2. adımın tamamlanması ödeme sonucunun (başarılı/başarısız) üye işyerine ulaştırılması için gereklidir.

2) İlk adımda iframe ile açılan formu doldurarak müşteri ödeme bildirimi yaptığında, PayTR operasyon ekibi bildirimi görür ve ödemeyi kontrol eder. Kontrol sonrası, PayTR sistemi tarafından arka planda (server-side) mağaza bildirim sayfasına (Bildirim URL) POST metodu ile kontrolün sonucu gönderilir. Bu bildirime istinaden üye işyeri siparişi onaylar veya iptal eder.

**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı | Açıklama  
---|---  
merchant_oid | Mağaza sipariş no: Satış işlemi için belirlediğiniz sipariş numarası  
status | Ödeme işleminin sonucu(success/failed)  
total_amount | Ödeme tutarı (100 ile çarpılmış hali gönderilir. 34.56 TL => 3456)  
hash | Üye işyerinin, PayTR sisteminden gönderilen değerleri kontrol edebilmesi için güvenlik amaçlı oluşturulan hash  
failed_reason_code | Ödeme bildiriminin onaylanmaması durumunda gönderilir  
failed_reason_msg | Ödeme bildiriminin neden onaylanmadığı mesajını içerir  
test_mode | Mağazanız test modunda iken veya canlı modda yapılan test işlemlerde 1 olarak gönderilir.  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <!doctype html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Örnek Ödeme Sayfası</title>
    </head>
    <body>
    
    <div>
        <h1>Örnek Ödeme Sayfası</h1>
    </div>
    <br><br>
    
    <div style="width: 100%;margin: 0 auto;display: table;">
    
        <?php 
    
    $merchant_id='XXXXXX'; // Mağaza numarası
    $merchant_key='YYYYYYYYYYYYYY'; // Mağaza Parolası - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    $merchant_salt='ZZZZZZZZZZZZZZ'; // Mağaza Gizli Anahtarı - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    ## Kullanıcının IP adresi
    if( isset( $_SERVER["HTTP_CLIENT_IP"] ) ) {
           $ip = $_SERVER["HTTP_CLIENT_IP"];
    } elseif( isset( $_SERVER["HTTP_X_FORWARDED_FOR"] ) ) {
           $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
    } else {
           $ip = $_SERVER["REMOTE_ADDR"];
    }
    
    $user_ip=$ip;  // !!! Eğer bu kodu sunucuda değil local makinanızda çalıştırıyorsanız buraya dış ip adresinizi(https://www.whatismyip.com/) yazmalısınız.
    
    $merchant_oid=time();//sipariş numarası: her işlemde benzersiz olmalıdır! Bu bilgi bildirim sayfanıza yapılacak bildirimde gönderilir.
    $email="musteri@saglayici.com"; // Müşterinizin sitenizde kayıtlı eposta adresi
    $payment_amount="999";//9.99 TL
    $payment_type='eft';
    $debug_on=1;//hata mesajlarını ekrana bas
    
    ## İşlem zaman aşımı süresi - dakika cinsinden
    $timeout_limit = "30";
    
    ## Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir
    $test_mode = 0;
    
    $hash_str=$merchant_id.$user_ip.$merchant_oid.$email.$payment_amount.$payment_type.$test_mode;
    $paytr_token=base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
    
    $post_vals=array(
            'merchant_id'=>$merchant_id,
            'user_ip'=>$user_ip,
            'merchant_oid'=>$merchant_oid,
            'email'=>$email,
            'payment_amount'=>$payment_amount,
            'payment_type'=>$payment_type,
            'paytr_token'=>$paytr_token,
            'debug_on'=>$debug_on,
            'timeout_limit'=>$timeout_limit,
            'test_mode'=>$test_mode
    );
    
    $ch=curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/get-token");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1) ;
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
    curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    
    //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
    //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
    $result = @curl_exec($ch);
    
    if(curl_errno($ch))
    {
        die("PAYTR EFT IFRAME connection error. err:".curl_error($ch));
    }
    curl_close($ch);
    
    $result=json_decode($result,1);
    
    /*
    Başarılı yanıt örneği: (token içerir)
    {"status":"success","token":"28cc613c3d7633cfa4ed0956fdf901e05cf9d9cc0c2ef8db54fa"}
    
    Başarısız yanıt örneği:
    {"status":"failed","reason":"Zorunlu alan degeri gecersiz: merchant_id"}
    */
    
    if($result['status']=='success')
    {
        $token=$result['token'];
    }
    else
    {
        die("PAYTR EFT IFRAME failed. reason:".$result['reason']);
    }
    
        ?>
    
        <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
        <iframe src="https://www.paytr.com/odeme/api/<?php echo $token;?>" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
        <script>iFrameResize({},'#paytriframe');</script>
    
    </div>
    
    <br><br>
    </body>
    </html>
    
    
    # Python 3.6+
    # 1. ADIM için örnek kodlar
    
    import base64
    import hashlib
    import hmac
    import json
    import requests
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'YYYYYYYYYYYYYY'
    merchant_salt = 'ZZZZZZZZZZZZZZ'
    
    # Eğer bu kodu sunucuda değil local makinanızda çalıştırıyorsanız buraya dış ip adresinizi(https://www.whatismyip.com/) yazmalısınız.
    user_ip = ''
    
    # Sipariş numarası: her işlemde benzersiz olmalıdır! Bu bilgi bildirim sayfanıza yapılacak bildirimde gönderilir.
    merchant_oid = ''
    
    # Müşterinizin sitenizde kayıtlı eposta adresi
    email = 'musteri@saglayici.com'
    
    # Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    payment_amount = ''
    
    payment_type = 'eft'
    
    # Hataları ekrana basmak için kullanılır.
    debug_on = '1'
    
    # İşlem zaman aşımı süresi - dakika cinsinden
    timeout_limit = '30'
    
    # Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir
    test_mode = '0'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur
    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + payment_type + test_mode + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'payment_type': payment_type,
        'paytr_token': paytr_token,
        'debug_on': debug_on,
        'timeout_limit': timeout_limit,
        'test_mode': test_mode
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['token'])
    else:
        print('PAYTR EFT IFRAME failed. reason:' + res['reason'])
    
        """
    # Ödeme formunun açılması için gereken HTML kodlar / Başlangıç #
    
    <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
    <iframe src="https://www.paytr.com/odeme/api/{ token }" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
    <script>iFrameResize({},'#paytriframe');</script>
    
    # Ödeme formunun açılması için gereken HTML kodlar / Bitiş #
    """
    
    
    
    // 1. ADIM için örnek kodlar
    
    using Newtonsoft.Json.Linq; // Bu satırda hata alırsanız, site dosyalarınızın olduğu bölümde bin isimli bir klasör oluşturup içerisine Newtonsoft.Json.dll adlı DLL dosyasını kopyalayın.
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Linq;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class iframe_ornek : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "XXXXXX";
                string merchant_key = "YYYYYY";
                string merchant_salt = "ZZZZZZ";
                //
                // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
                string emailstr = "";
                //
                // Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
                int payment_amountstr = 999;
                //
                // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
                string merchant_oid = "";
                //   
                // !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
                // buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
                string user_ip = Request.ServerVariables["HTTP_X_FORWARDED_FOR"];
                if (user_ip == "" || user_ip == null)
                {
                    user_ip = Request.ServerVariables["REMOTE_ADDR"];
                }
                //
                /* ############################################################################################ */
    
                // İşlem zaman aşımı süresi - dakika cinsinden
                string timeout_limit = "30";
                //
                // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
                string debug_on = "1";
                //
                // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
                string test_mode = "0";
                //
                // Ödeme türü eft olarak belirtilmelidir
                string payment_type = "eft";
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["user_ip"] = user_ip;
                data["merchant_oid"] = merchant_oid;
                data["email"] = emailstr;
                data["payment_amount"] = payment_amountstr.ToString();
                data["payment_type"] = payment_type;
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(merchant_id, user_ip, merchant_oid, emailstr, payment_amountstr.ToString(), payment_type, test_mode, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                data["paytr_token"] = Convert.ToBase64String(b);
                //
                data["debug_on"] = debug_on;
                data["test_mode"] = test_mode;
                data["timeout_limit"] = timeout_limit;
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/get-token", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    /*
                        Başarılı yanıt örneği: (token içerir)
                        {"status":"success","token":"28cc613c3d7633cfa4ed0956fdf901e05cf9d9cc0c2ef8db54fa"}
    
                        Başarısız yanıt örneği:
                        {"status":"failed","reason":"Zorunlu alan degeri gecersiz: merchant_id"}
                    */
                    if (json.status == "success")
                    {
                        ViewBag.Src = "https://www.paytr.com/odeme/api/" + json.token + "";
                    }
                    else
                    {
                        Response.Write("PAYTR EFT IFRAME failed. reason:" + json.reason + "");
                    }
                }
    
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'XXXXXX'; // Mağaza numarası.
    var merchant_key = 'YYYYYYYYYYYYYY'; // Mağaza Parolası - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_salt = 'ZZZZZZZZZZZZZZ'; // Mağaza Gizli Anahtarı - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_oid = "IN" + microtime.now(); //sipariş numarası: her işlemde benzersiz olmalıdır! Bu bilgi bildirim sayfanıza yapılacak bildirimde gönderilir.
    
    var user_ip = ''; // Eğer bu kodu sunucuda değil local makinanızda çalıştırıyorsanız buraya dış ip adresinizi(https://www.whatismyip.com/) yazmalısınız.
    var email = 'musteri@saglayici.com'; // Müşterinizin sitenizde kayıtlı eposta adresi
    var payment_amount = 100;
    var payment_type ='eft';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var timeout_limit = 30; // İşlem zaman aşımı süresi - dakika cinsinden.
    var debug_on = 1; //hata mesajlarını ekrana bas.
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${payment_type}${test_mode}`;
        var paytr_token = hashSTR + merchant_salt;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        var options = {
            method: 'POST',
            url: 'https://www.paytr.com/odeme/api/get-token',
            headers:
                { 'content-type': 'application/x-www-form-urlencoded' },
            formData: {
                merchant_id: merchant_id,
                user_ip: user_ip,
                merchant_oid: merchant_oid,
                email: email,
                payment_amount: payment_amount,
                payment_type: payment_type,
                paytr_token: token,
                debug_on: debug_on,
                timeout_limit: timeout_limit, 
                test_mode: test_mode,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.render('layout', { iframetoken: res_data.token });
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        } 
    
        if (callback.status == 'success') {
            //basarili
        } else {
           /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

Havale/EFT iFrame API 1. ADIM örnek kodları[**indirmek için tıklayın.**](/havale-eft-iframe-api/havale-eft-iframe-api-1-adim/PayTR Havale-EFT iFrame API 1. ADIM.zip)


---

# Havale/EFT iFrame API 2. Adım | PayTR


# Havale/EFT iFrame API 2. Adım

**Mağaza bildirim sayfasına (Bildirim URL) yapılacak isteğe Üye işyerinin dönmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**

**Önemli:** OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır. Bildirim URL sayfası, müşterinin göreceği bir sayfa değildir, PayTR ile Mağaza arasında arka planda (server-side) bir iletişimde kullanılır. OK yanıtı alınmayan ödeme işlemleri, Mağaza Paneli'ndeki İşlemler sayfasında “Devam Ediyor” olarak görünür. PayTR sistemi OK cevabını istendiği şekilde almadığı durumda, bildirimin başarısız olduğunu varsayarak bir süre daha tekrar tekrar bildirim göndermeye çalışacaktır.

**Önemli:** PayTR bildirim sistemi, ağ trafik sorunları ve benzeri nedenlerden dolayı aynı ödeme işlemi için birden fazla onay bildirimi gönderebilir. Bu durumda yalnızca ilk bildirim göz önünde bulundurulmalı, sonraki bildirimler için müşteriye tekrar ürün/hizmet sunulmamalı, yalnızca OK yanıtı gönderilerek işlem sonuçlandırılmalıdır. Tekrarlayan bildirimlerin tespiti Mağaza sipariş no (merchant_oid) temel alınarak yapılabilir.

  * Ödeme işleminin başarısız olması durumunda bildirim POST içeriğinde “failed_reason_code” ve “failed_reason_msg” olmak üzere iki alan daha gelir. Bu alanlar hash hesaplamasında kullanılmaz. Bu mesajlar istenirse müşteriyi bilgilendirme amacıyla eposta veya mağaza mesaj sistemi üzerinden müşteriye iletilebilir

failed_reason_code | failed_reason_msg | Açıklama  
---|---|---  
4 | Havale/EFT ödemesi tespit edilemedi. | Ödeme bildirimi formunda müşterinin belirtmiş olduğu bilgiler ile ödemeye ulaşılamamıştır  
5 | Havale/EFT ödeme tutarı yetersiz. Lütfen gönderdiğiniz tutar kadar bildirim yapın. | Müşterinin bankaya gönderdiği tutar, alışveriş tutarından (payment_amount) az olduğundan onay verilmemiştir.  
6 | Müşteri ödeme yapmaktan vazgeçti ve ödeme sayfasından ayrıldı. | Müşteri, kendisine tanınmış olan işlem süresinde (1. ADIM’da tanımlanan timeout_limit değeri) işlemini tamamlamadı veya müşteri ödeme sayfasını kapatarak işlemi sonlandırdı.  
7 | Bildiriminiz alınmadı, lütfen önceki bildiriminizin kontrolünün sonuçlanmasını bekleyin. | Müşteri henüz kontrolü sonuçlanmamış bir ödeme bildirimi bulunurken, tekrar bildirim yaptı.  
41 | Havale/EFT ödemesi ile bildirimdeki Ad Soyadı uyuşmuyor. | Müşterinin bildirim yaparken girdiği Ad Soyadı ile banka kayıtlarındaki Ad Soyadı uyuşmadı.  
42 | Havale/EFT ödemesi ile bildirimdeki TCKN uyuşmuyor. | Müşterinin bildirim yaparken girdiği TCKN ile banka kayıtlarındaki TCKN uyuşmadı.  
43 | Bu Havale/EFT ödemesi daha önce onaylanmış. | Müşterinin bildirimi sonrası yapılan kontrolde, bu ödemenin daha önce bildirilip onay aldığı görüldü.  
44 | Bu Havale/EFT ödemesi iade edilmiş. | Müşterinin bildirimi sonrası yapılan kontrolde, bu ödemenin daha önce iade edildiği görüldü.  
45 | Dekonttaki iki farklı Ad-Soyadından yalnızca birisi yazılmış | Müşterinin bildirimi sonrası yapılan kontrolde,dekontta yazan iki Ad Soyadı bilgisinden yalnızca birisinin girildiği görüldü  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    ## 2. ADIM için örnek kodlar ##
    
    ## ÖNEMLİ UYARILAR ##
    ## 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    ## 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
    ## veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    ## 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
    ## siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
    $post = $_POST;
    
    ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
    #
    ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    $merchant_key   = 'YYYYYYYYYYYYYY';
    $merchant_salt  = 'ZZZZZZZZZZZZZZ';
    ###########################################################################
    
    ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
    #
    ## POST değerleri ile hash oluştur.
    $hash = base64_encode( hash_hmac('sha256', $post['merchant_oid'].$merchant_salt.$post['status'].$post['total_amount'], $merchant_key, true) );
    #
    ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if( $hash != $post['hash'] )
        die('PAYTR notification failed: bad hash');
    ###########################################################################
    
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
    ## 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
    /* Sipariş durum sorgulama örnek
    $durum = SQL
    if($durum == "onay" || $durum == "iptal"){
            echo "OK";
            exit;
    }*/
    
    if( $post['status'] == 'success' ) { ## Ödeme Onaylandı
    
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi onaylayın.
    ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
    ## 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
    ## değişebilir. Güncel tutarı $post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
    } else { ## Ödemeye Onay Verilmedi
    
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi iptal edin.
    ## 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
    ## $post['failed_reason_code'] - başarısız hata kodu
    ## $post['failed_reason_msg'] - başarısız hata mesajı
    
    }
    
    ## Bildirimin alındığını PayTR sistemine bildir.
    echo "OK";
    exit;
    ?>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # 2. ADIM için örnek kodlar
    
    """
    ÖNEMLİ UYARILAR
    1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    """
    
    import base64
    import hashlib
    import hmac
    import json
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'XXXXXXXXXXXXXXXX'
        merchant_salt = 'XXXXXXXXXXXXXXXX'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        """
        BURADA YAPILMASI GEREKENLER
        1) Ödeme durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
        Ödeme durum sorgulama örnek
        durum = SQL
    
        if(durum == 'onay'){
             return HttpResponse(str('OK'))
        """
    
        if post['status'] == 'success':
            """
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi onaylayın.
    ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
    ## 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
    ## değişebilir. Güncel tutarı $post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
            """
        else:
            """
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi iptal edin.
    ## 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
    ## $post['failed_reason_code'] - başarısız hata kodu
    ## $post['failed_reason_msg'] - başarısız hata mesajı
            """
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    // 2. ADIM için örnek kodlar
    
    // ÖNEMLİ UYARILAR!
    // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
    // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
    // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class bildirim_url_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYYYYYYYY";
        string merchant_salt    = "ZZZZZZZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string merchant_oid = Request.Form["merchant_oid"];
            string status = Request.Form["status"];
            string total_amount = Request.Form["total_amount"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(merchant_oid, merchant_salt, status, total_amount);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
                }
    
            //###########################################################################
    
            // BURADA YAPILMASI GEREKENLER
            // 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
            // 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
            if (status == "success") { //Ödeme Onaylandı
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER ONAY İŞLEMLERİDİR.
                // 1) Siparişi onaylayın.
                // 2) iframe çağırma adımında merchant_oid ve diğer bilgileri veri tabanınıza kayıp edip bu aşamada karşılaştırarak eğer var ise bilgieri çekebilir ve otomatik sipariş tamamlama işlemleri yaptırabilirsiniz.
                // 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapabilirsiniz. Bu işlemide yine iframe çağırma adımında merchant_oid bilgisini kayıt edip bu aşamada sorgulayarak verilere ulaşabilirsiniz.
                // 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
                // değişebilir. Güncel tutarı Request.Form['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
                } else { //Ödemeye Onay Verilmedi
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER
                // 1) Siparişi iptal edin.
                // 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
                // $post['failed_reason_code'] - başarısız hata kodu
                // $post['failed_reason_msg'] - başarısız hata mesajı
                }          
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'XXXXXX'; // Mağaza numarası.
    var merchant_key = 'YYYYYYYYYYYYYY'; // Mağaza Parolası - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_salt = 'ZZZZZZZZZZZZZZ'; // Mağaza Gizli Anahtarı - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_oid = "IN" + microtime.now(); //sipariş numarası: her işlemde benzersiz olmalıdır! Bu bilgi bildirim sayfanıza yapılacak bildirimde gönderilir.
    
    var user_ip = ''; // Eğer bu kodu sunucuda değil local makinanızda çalıştırıyorsanız buraya dış ip adresinizi(https://www.whatismyip.com/) yazmalısınız.
    var email = 'musteri@saglayici.com'; // Müşterinizin sitenizde kayıtlı eposta adresi
    var payment_amount = 100;
    var payment_type ='eft';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var timeout_limit = 30; // İşlem zaman aşımı süresi - dakika cinsinden.
    var debug_on = 1; //hata mesajlarını ekrana bas.
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${payment_type}${test_mode}`;
        var paytr_token = hashSTR + merchant_salt;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        var options = {
            method: 'POST',
            url: 'https://www.paytr.com/odeme/api/get-token',
            headers:
                { 'content-type': 'application/x-www-form-urlencoded' },
            formData: {
                merchant_id: merchant_id,
                user_ip: user_ip,
                merchant_oid: merchant_oid,
                email: email,
                payment_amount: payment_amount,
                payment_type: payment_type,
                paytr_token: token,
                debug_on: debug_on,
                timeout_limit: timeout_limit, 
                test_mode: test_mode,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.render('layout', { iframetoken: res_data.token });
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        } 
    
        if (callback.status == 'success') {
            //basarili
        } else {
           /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

**Opsiyonel: Ara bildirimleri alma**

Müşterinizin, IFrame içerisinde bildirim formunu doldurmasıyla birlikte, talep etmeniz halinde PayTR alt yapısı belirteceğiniz “Ara Bildirim URL” adresine bir ara bildirim yapacaktır. Bildirim içeriğinde EFT/Havale isteğinde göndermiş olduğunuz sipariş numarası ve müşterinizin işlem için seçtiği banka bilgisi bulunur. “Ara Bildirim URL” olarak kullanmak istediğiniz URL bilgisini Paytr Mağaza Paneli > Ayarlar bölümünden ekleyebilirsiniz.

Alan Adı | Açıklama  
---|---  
hash | Hash: Bildirimin doğruluğunu belirten hash bilgisi  
status | Durum: Ara bildirim için “info” değeri gelir  
merchant_oid | Sipariş numarası: EFT/Havale bildirimin başlatırken gönderdiğiniz sipariş numarası  
bank | Banka: EFT/Havale bildirimin yapıldığı banka  
  
  
**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    // Ara Bildirim URL için örnek kodlar
    
    $post = $_POST;
    
    ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
    #
    ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    $merchant_key   = 'YYYYYYYYYYYYYY';
    $merchant_salt  = 'ZZZZZZZZZZZZZZ';
    ###########################################################################
    
    ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
    #
    ## POST değerleri ile hash oluştur.
    $hash = base64_encode( hash_hmac('sha256', $post['merchant_oid'].$post['bank'].$merchant_salt,$merchant_key,true));
    
    ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if( $hash != $post['hash'] )
        die('PAYTR notification failed: bad hash');
    ###########################################################################
    
    ## DÖNÜLEN POST DEĞERLERİ
    /*
        $post[merchant_oid]      => Sipariş Numarası
        $post[status]            => "info"
        $post[hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
        ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
        $post[payment_sent_date] => Ödeme Yapılan Tarih
        $post[bank]              => Ödeme Yapılan Banka
        $post[user_name]         => Ödeme Yapan Adı Soyadı
        $post[user_phone]        => Ödeme Yapan Telefon Numarası
        $post[tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
    */
    ###########################################################################
    >
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # 2. ADIM için örnek kodlar
    
    import base64
    import hashlib
    import hmac
    import json
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'XXXXXXXXXXXXXXXX'
        merchant_salt = 'XXXXXXXXXXXXXXXX'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_oid'] + post['bank']+ merchant_salt
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
       ## DÖNÜLEN POST DEĞERLERİ
    /*
        [merchant_oid]      => Sipariş Numarası
        [status]            => "info"
        [hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
        ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
        [payment_sent_date] => Ödeme Yapılan Tarih
        [bank]              => Ödeme Yapılan Banka
        [user_name]         => Ödeme Yapan Adı Soyadı
        [user_phone]        => Ödeme Yapan Telefon Numarası
        [tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
    */
    ###########################################################################
    
    
    // Ara Bildirim URL için örnek kodlar
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class ara_bildirim_url_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYYYYYYYY";
        string merchant_salt    = "ZZZZZZZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string merchant_oid = Request.Form["merchant_oid"];
            string merchant_oid = Request.Form["bank"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(merchant_oid, bank, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
                }
    
            //###########################################################################
    
            //## DÖNÜLEN POST DEĞERLERİ
            /*
             Request.Form[merchant_oid]      => Sipariş Numarası
             Request.Form[status]            => "info"
             Request.Form[hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
             ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
             Request.Form[payment_sent_date] => Ödeme Yapılan Tarih
             Request.Form[bank]              => Ödeme Yapılan Banka
             Request.Form[user_name]         => Ödeme Yapan Adı Soyadı
             Request.Form[user_phone]        => Ödeme Yapan Telefon Numarası
             Request.Form[tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
            */
            //###########################################################################
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_key = 'YYYYYYYYYYYYYY'; // Mağaza Parolası - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_salt = 'ZZZZZZZZZZZZZZ'; // Mağaza Gizli Anahtarı - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + callback.bank + merchant_salt
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        } 
    
            //## DÖNÜLEN POST DEĞERLERİ
            /*
             [merchant_oid]      => Sipariş Numarası
             [status]            => "info"
             [hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
             ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
            [payment_sent_date] => Ödeme Yapılan Tarih
            [bank]              => Ödeme Yapılan Banka
            [user_name]         => Ödeme Yapan Adı Soyadı
            [user_phone]        => Ödeme Yapan Telefon Numarası
            [tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
            */
            //###########################################################################
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

Havale/EFT iFrame API 2. ADIM örnek kodları[**indirmek için tıklayın.**](/havale-eft-iframe-api/havale-eft-iframe-api-2-adim/PayTR Havale-EFT iFrame API 2. ADIM.zip)


---

# Platform Transfer Talebi | PayTR


# Platform Transfer Talebi

**Pazaryeri Çözümü Nedir?** PayTR, 6493 sayılı Ödeme ve menkul Kıymet Mutabakat Sistemleri, Ödeme Hizmetleri ve Elektronik Para Kuruluşları Hakkında Kanun gereğince TCMB lisanslı ödeme kuruluşu olmayı tercih etmeyen pazaryerleri için "Pazaryeri Çözümü" oluşturmuş ve API sistemiyle çalışan ödeme ve transfer teknik entegrasyonu hazırlamıştır.

**Pazaryeri Çözümü Nasıl Çalışır?** Alıcı satın alacağı ürün/hizmet için pazaryerindeki ödeme sayfasında ödemesini başlatır ve ödeme PayTR tarafından işlenir. PayTR ürün/hizmet bedeli olan ödemeyi satıcı hesabına ve komisyon bedelini Pazaryeri hesabına aktarır. Pazaryerine ve satıcıya yapılacak para transferleri PayTR tarafından pazaryerinin isteğiyle ve tercihleri doğrultusunda gerçekleşir.

![](/user/pages/07.platform-transfer-talebi/pazaryeri-cozumu.png)

**PayTR Pazaryeri Çözümü Avantajları** Esnek bir yapıya sahip PayTR Pazaryeri Çözümü ile pazaryeri platformu sahipleri, aynı sepette birden fazla satıcının ürünü olduğu durumlar, parçalı iade yapılması, sipariş tutarının sonradan değişmesi, farklı satıcıya farklı komisyon uygulanması vb. gibi her ihtiyaçlarını özgürce karşılayabilirler.

**PLATFORM TRANSFER TALEBİ 2 AŞAMADAN OLUŞMAKTADIR.**  
1.Transfer talimatının verilmesi bu [**linkten**](/platform-transfer-talebi/transfer-talimatinin-verilmesi) gidebilirsiniz.  
2.Transfer talimatının sonucunun alınması bu [**linkten**](/platform-transfer-talebi/transfer-talimatinin-sonucunun-alinmasi) gidebilirsiniz. 

Direkt API Pazaryeri dokümanı ve tüm servisleri indirmek için [**tıklayın.**](/platform-transfer-talebi/Pazaryeri_ve_Direkt_API.zip)

iFrame API Pazaryeri dokümanı ve tüm servisleri indirmek için [**tıklayın.**](/platform-transfer-talebi/Pazaryeri_ve_iFrame_API.zip)


---

# Geri Dönen Ödemeler Callback | PayTR


# Geri Dönen Ödemeler Callback

Geri dönen ödemelerden oluşturacağınız transfer talebi sonrasında Success yanıtı almanız ile birlikte hesaptan gönderme talebiniz PayTR sistemi tarafından başarılı olarak alınmış olur. PayTR sistemi talebinizi ortalama 5 dakika içerisinde işleme alacak, gönderdiğiniz trans_info içeriğini kontrol ederek transferleri gerçekleştirecektir. Kontrol sırasında hatalı bilgi tespiti halinde ilgili işlem başarısız olarak işaretlenir. Oluşan sonuç JSON formatında PayTR Mağaza Paneli > Destek & Kurulum > Ayarlar > Platform Transfer Sonucu Bildirim URL olarak tanımladığınız adrese POST edilerek bildirilir.

Tanımlayacağınız Bildirim URL’ye POST metodu ile talebinizin sonucu (başarılı veya başarısız) her işlem için ayrı olarak gönderilir. Gelen değerler içerisinde bulunan result değerini ele alarak talep sonucuna göre işlem yapabilirsiniz.

**PayTR sistemince Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı | Açıklama | Değer  
---|---|---  
mode | Sabit olarak cashout değeri ile gelir. | cashout  
hash | Hash kontrolünde kullanılacaktır. | ÖRN: wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=  
trans_id | Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer. | ÖRN: 12345aaabbb  
processed_result | Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler. | ÖRN: [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]  
success_total | Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı) | ÖRN: 1  
failed_total | Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı) | ÖRN: 0  
transfer_total | Başarıyla tranasfer edilen işlemlerin toplam tutarı. | ÖRN: 484.48  
account_balance | Transferler sonrasında kalan alt hesap bakiyeniz. | ÖRN: 75  
  
**Bildirim URL’nize PayTR sistemince yapılacak isteğe dönülmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**
    
    
    Örnek (PHP): echo "OK";
    
    
    Örnek (.NET): Response.Write("OK");
    

**ÖNEMLİ UYARILAR:**

  1. Bildirim URL adresinize üye girişi ve benzeri erişim kısıtlaması yapılmamalıdır. Böylece PayTR sistemi bildirimleri kolayca iletebilecektir.

  2. Bildirim URL’nize gelecek bildirimlere döneceğiniz OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır.

  3. Bildirim URL’niz, müşterinizin ödeme sırasında ulaşacağı bir sayfa değildir, PayTR tarafından arka planda (server-side) ödeme sonucunu bildirmek için kullanılır. Bu nedenle, Bildirim URL’nizde kodlama yaparken oturum (SESSION) değerlerini kullanamazsınız. İşlemlerinizi Mağaza sipariş no (merchant_oid) kullanarak gerçekleştirmelisiniz.

  4. Bildirimin PayTR sisteminden geldiğinden ve ulaşım esnasında değiştirilmediğinden emin olmak için, POST içerisindeki hash değeri ile tarafınızca oluşturulacak hash değerinin aynı olduğunu kontrol etmeniz, güvenlik açısından büyük önem arz etmektedir. Bu kontrolü yapmamanız durumunda maddi kayıplar ile karşılaşabilirsiniz.




  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        #################### POST içerisinde gelen örnek veriler ####################
        #
        // [mode] => cashout
        // -> Sabit bu şekilide gelir
        #
        // [hash] => wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=,
        // -> Kontrolde kullanaılacaktır.
        #
        // [trans_id] => 12345aaabbb
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer.
        #
        // [processed_result] => [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler.
        #
        // [success_total] => 1
        // -> Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı)
        #
        // [failed_total] => 0
        // -> Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı)
        #
        // [transfer_total] => 484.48
        // -> Başarıyla tranasfer edilen işlemlerin toplam tutarı.
        #
        // [account_balance] => 0
        // -> Transferler sonrasında kalan alt hesap bakiyeniz.
        ############################################################################
    
        $post = $_POST;
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        ###########################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        #
        ## POST değerleri ile hash oluştur.
        $hash = base64_encode( hash_hmac('sha256', $post['merchant_id'].$post['trans_id'].$merchant_salt, $merchant_key, true) );
        #
        ## Oluşturulan hash'i, PayTR'dan gelen post içindeki hash ile karşılaştır (isteğin PayTR'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ###########################################################################
    
        ## trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir.
        $processed_result = json_decode($post['processed_result'],1);
        foreach($processed_result as $trans)
        {
            // Burada her işlem için gerekli veri tabanı vb. işlemleri yapabilirsiniz.
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir.
        echo "OK";
        exit;
    ?>
    
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # POST içerisinde gelen örnek veriler
    
    """
    [mode] : cashout
    -> Sabit bu şekilide gelir
    
    [hash] : wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=,
    -> Kontrolde kullanaılacaktır.
    
    [trans_id] : 12345aaabbb
    -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer.
    
    [processed_result] : [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]
    -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler.
    
    [success_total] : 1
    -> Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı)
    
    [failed_total] : 0
    -> Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı)
    
    [transfer_total] : 484.48
    -> Başarıyla tranasfer edilen işlemlerin toplam tutarı.
    
    [account_balance] : 0
    -> Transferler sonrasında kalan alt hesap bakiyeniz.
    """
    
    import base64
    import hashlib
    import hmac
    import json
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'YYYYYYYYYYYYYY'
        merchant_salt = 'ZZZZZZZZZZZZZZ'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_id'] + post['trans_id'] + merchant_salt
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir.
        processed_result = json.loads(post['processed_result'])
    
        for trans in processed_result:
            # Burada her işlem için gerekli veri tabanı vb. işlemleri yapabilirsiniz.
            print(trans)
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    
        //#################### POST içerisinde gelen örnek veriler ####################
        //#
        // [mode] => cashout
        // -> Sabit bu şekilide gelir
        //#
        // [hash] => wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=,
        // -> Kontrolde kullanaılacaktır.
        //#
        // [trans_id] => 12345aaabbb
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer.
        //#
        // [processed_result] => [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler.
        //#
        // [success_total] => 1
        // -> Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı)
        //#
        // [failed_total] => 0
        // -> Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı)
        //#
        // [transfer_total] => 484.48
        // -> Başarıyla tranasfer edilen işlemlerin toplam tutarı.
        //#
        // [account_balance] => 0
        // -> Transferler sonrasında kalan alt hesap bakiyeniz.
        //############################################################################
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using Newtonsoft;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;
    using System.IO;
    
    public partial class paytr_geri_donen_odemeler_callback_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key = "AAAAAA";
        string merchant_salt = "XXXXXXXXXXXXXXXX";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e)
        {
    
            string trans_id = Request.Form["trans_id"];
            string merchant_id = Request.Form["merchant_id"];
            string hash = Request.Form["hash"];
            string processed_result = Request.Form["processed_result"];
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string Birlestir = string.Concat(merchant_id, trans_id, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
            if (hash.ToString() != token)
            {
    
                Response.Write("PAYTR notification failed: bad hash");
                return;
            }
    
            //## trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir.
    
            dynamic dynJson = JsonConvert.DeserializeObject(processed_result);
    
            foreach (var item in dynJson)
            {
                // Burada her işlem için gerekli veri tabanı vb. işlemleri yapabilirsiniz.
            }
            // Bildirimin alındığını PayTR sistemine bildir.
            Response.Write("OK");
        }
    
    }
    
    
    
      var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    //  ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXXXXYYYYYYYY';
    var merchant_salt = 'XXXXXXXXYYYYYYYY';
    
    app.get("/list", function (req, res) {
        //  Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        var start_date = '2020-11-01 00:00:00';
        var end_date = '2020-11-29 23:59:59';
    
        //  ####################### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/geri-donen-transfer',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'start_date': start_date,
                'end_date': end_date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
    
                /*
    
                [ref_no] => 1000001
                [date_detected] => 2020-06-10
                [date_reimbursed] => 2020-06-08
                [transfer_name] => ÖRNEK İSİM
                [transfer_iban] => TR100000000000000000000001
                [transfer_amount] => 35.18
                [transfer_currency] => TL
                [transfer_date] => 2020-06-08
    
                */
                // VT işlemleri vs.
                res.send(res_data);
    
            } else {
    
                // Hata durumu
    
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/send", function (req, res) {
    
        var trans_id = '';
        var trans_info = [{
            'amount': '1283',
            'receiver': 'XYZ LTD ŞTİ',
            'iban': 'TRXXXXXXXXXXXXXXXXXXXXX'
        }];
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + trans_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/hesaptan-gonder',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
    
                'trans_info': JSON.stringify(trans_info),
                'trans_id': trans_id,
                'paytr_token': paytr_token,
                'merchant_id': merchant_id,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(callback.merchant_id + callback.trans_id + merchant_salt).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        var processed_result = JSON.parse(callback.processed_result);
    
        for (const [key, value] of Object.entries(processed_result)) {
            console.log(`${key}: ${value}`);
        }
    
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Geri dönen ödemeler örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/geri-donen-odemeleri-hesaptan-gonder-2/PayTR Geri Donen Odemeler.zip)


---

# Geri Dönen Ödemeleri Hesaptan Gönder | PayTR


# Geri Dönen Ödemeleri Hesaptan Gönder

Bu servis ile transfer talebi yapılmış ancak alıcı hesap hatası nedeniyle geri dönen ödemeler için tekrar ödeme isteği gönderebilirsiniz. Geri dönen ödemeler mağazanıza ait bir alt hesaba bakiye olarak işlenir. Geri dönen bu ödemelerin listesine “Geri Dönen Ödemeler – Listele API” servisi ile ulaşabilirsiniz.

1- Hesaptan ödeme transferi gönderebilmek için tabloda belirtilen bilgileri POST ile ilgili URL’e gönderin: https://www.paytr.com/odeme/hesaptan-gonder

**Token üretiminde kullanılacak veriler:**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet | -  
trans_id(string) | Transfer ID: Transfer işlemi için belirlediğiniz benzersiz işlem numarası. | Evet | En fazla 64 karakter, Alfa numerik  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet | -  
trans_id(string) | Transfer ID: Transfer işlemi için belirlediğiniz **benzersiz** işlem numarası. | Evet | En fazla 64 karakter, Alfa numerik  
trans_info(JSON) | Transfer Bilgisi: Transfer tutarı, alıcı ismi ve IBAN değerlerini içeren JSON formatında içerik. (Nasıl tanımlanacağı için örnek koda bakın) | Evet | -  
paytr_token(string) | PayTR Token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir (Hesaplama için örnek koda bakın) | Evet | -  
  
  


2- Yaptığınız bu isteğe cevap JSON formatında döner.

a. Yapılan istek geçerli ise status değeri **success** ve **trans_id** alanında gönderdiğiniz işlem numarası döner.  
b. Eğer sorguda bir hatanız varsa status değeri **error** döner. Bu durumda hata detayı için **err_msg** içeriğini kontrol etmelisiniz.  


3- Success yanıtı almanız ile birlikte hesaptan gönderme talebiniz PayTR sistemi tarafından başarılı olarak alınmış olur. PayTR sistemi talebinizi ortalama 5 dakika içerisinde işleme alacak, gönderdiğiniz trans_info içeriğini kontrol ederek transferleri gerçekleştirecektir. Kontrol sırasında hatalı bilgi tespiti halinde ilgili işlem başarısız olarak işaretlenir. Oluşan sonuç JSON formatında **PayTR Mağaza Paneli > Ayarlar > Platform Transfer Sonucu Bildirim URL** olarak tanımladığınız adrese POST edilerek bildirilir.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXXXXYYYYYYYY';
        $merchant_salt  = 'XXXXXXXXYYYYYYYY';
    
        ## Gerekli Bilgiler
        #
        $trans_id="PHG".time();
        $trans_info=array();
        //amount 100 ile çarpılarak gönderilir!!
        $trans_info[]=array("amount"=>"1283",
            "receiver"=>"XYZ LTD ŞTİ",
            "iban"=>"TRXXXXXXXXXXXXXXXXXXXXX");
        //...$trans_info[]=...
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token=base64_encode(hash_hmac('sha256',$merchant_id.$trans_id.$merchant_salt, $merchant_key, true));
    
        $post_vals=array('trans_info'=>json_encode($trans_info),
            'trans_id'=>$trans_id,
            'paytr_token'=>$paytr_token,
            'merchant_id'=>$merchant_id
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/hesaptan-gonder");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
        {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        $result_raw=$result;
        $result=json_decode($result,1);
    
        if($result['status']=='success')
        {
            //status ve trans_id içerir
            print_r($result_raw);
        }
        else//status=>error
        {
            //status ve err_no - err_msg içerir
            print_r($result_raw);
        }
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import json
    import requests
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXXXXYYYYYYYY'
    merchant_salt = 'XXXXXXXXYYYYYYYY'
    
    # Gerekli Bilgiler
    trans_id = 'PHG' + random.randint(1, 9999999).__str__()
    trans_info = [
        {
            'amount': '1283',  # amount 100 ile çarpılarak gönderilir!!
            'receiver': 'XYZ LTD ŞTİ',
            'iban': 'TRXXXXXXXXXXXXXXXXXXXXX'
        }
    ]
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + trans_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'trans_info': json.dumps(trans_info),
        'trans_id': trans_id,
        'merchant_id': merchant_id,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/hesaptan-gonder', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        # status ve trans_id içerir
        print(res)
    else:
        # status = error
        # status ve err_no - err_msg içerir
        print(res['err_no'] + ' - ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    
    namespace WebApplication1.Controllers
    {
        class PayTR
        {
            public string amount { get; set; }
            public string receiver { get; set; }
            public string iban { get; set; }
        }
    
        public class paytr_geri_donen_odemeler_hesaptan_gonder_ornekController : Controller
        {
            public ActionResult paytr_geri_donen_odemeler_hesaptan_gonder_ornek()
            {
                List<PayTR> TransferInfo = new List<PayTR>();
                PayTR info = new PayTR();
                info.amount = Convert.ToString(10 * 100); //amount 100 ile çarpılarak gönderilir.
                info.receiver = "XYZ LTD ŞTİ";
                info.iban = "TRXXXXXXXXXXXXXXXXXXXXX";
    
                TransferInfo.Add(info);
    
                string TransInfo = Newtonsoft.Json.JsonConvert.SerializeObject(TransferInfo);
    
                // ####################### #######################
                //
                // 
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                // #######################
                string TransId = "ZZZZZZZ"; 
    
                //  #######################
                string Birlestir = string.Concat(merchant_id, TransId, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // #######################
    
                NameValueCollection data = new NameValueCollection();
                data["trans_info"] = TransInfo;
                data["trans_id"] = TransId;
                data["paytr_token"] = paytr_token;
                data["merchant_id"] = merchant_id;
    
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/hesaptan-gonder", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
                        //status ve trans_id içerir
                        Response.Write(json);
    
                    }
                    else
                    {
                        // Hata durumu
                        //status=>error
                        Response.Write("Error. reason:" + json.err_no + "-" + json.err_msg);
                    }
                }
    
                return View();
            }
        }
    }
    
    
    
      var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    //  ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXXXXYYYYYYYY';
    var merchant_salt = 'XXXXXXXXYYYYYYYY';
    
    app.get("/list", function (req, res) {
        //  Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        var start_date = '2020-11-01 00:00:00';
        var end_date = '2020-11-29 23:59:59';
    
        //  ####################### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/geri-donen-transfer',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'start_date': start_date,
                'end_date': end_date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
    
                /*
    
                [ref_no] => 1000001
                [date_detected] => 2020-06-10
                [date_reimbursed] => 2020-06-08
                [transfer_name] => ÖRNEK İSİM
                [transfer_iban] => TR100000000000000000000001
                [transfer_amount] => 35.18
                [transfer_currency] => TL
                [transfer_date] => 2020-06-08
    
                */
                // VT işlemleri vs.
                res.send(res_data);
    
            } else {
    
                // Hata durumu
    
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/send", function (req, res) {
    
        var trans_id = '';
        var trans_info = [{
            'amount': '1283',
            'receiver': 'XYZ LTD ŞTİ',
            'iban': 'TRXXXXXXXXXXXXXXXXXXXXX'
        }];
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + trans_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/hesaptan-gonder',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
    
                'trans_info': JSON.stringify(trans_info),
                'trans_id': trans_id,
                'paytr_token': paytr_token,
                'merchant_id': merchant_id,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(callback.merchant_id + callback.trans_id + merchant_salt).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        var processed_result = JSON.parse(callback.processed_result);
    
        for (const [key, value] of Object.entries(processed_result)) {
            console.log(`${key}: ${value}`);
        }
    
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Geri dönen ödemeler örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/geri-donen-odemeleri-hesaptan-gonder/PayTR Geri Donen Odemeler.zip)


---

# Geri Dönen Ödemeleri Listele | PayTR


# Geri Dönen Ödemeleri Listele

Bu servis ile transfer talebi yapılmış ancak alıcı hesap hatası nedeniyle geri dönen ödemelerin listesine ulaşabilirsiniz. Geri dönen ödemeler mağazanıza ait bir alt hesaba bakiye olarak işlenir. Geri dönen bu ödemeleri tekrar göndermek için “Geri Dönen Ödemeler – Hesaptan Gönder” servisini kullanabilirsiniz.

1- Geri dönen ödemelerin listesini alabilmek için tabloda belirtilen bilgileri POST ile ilgili URL’e gönderin: https://www.paytr.com/odeme/geri-donen-transfer

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet | -  
start_date(string) | Başlangıç Tarihi Formatı: 2021-01-01 00:00:00 (YYYY-MM-DD hh:mm:ss) | Evet | -  
end_date | Bitiş Tarihi Formatı: 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss) | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
start_date (integer) | Başlangıç Tarihi Formatı: 2021-01-01 00:00:00 (YYYY-MM-DD hh:mm:ss) | Evet | -  
end_date(integer) | Bitiş Tarihi Formatı: 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss) | Evet | -  
dummy(integer) | Dummy veri oluşturmak için kullanılır | Hayır | 1 veya 0 (Dummy veri için 1 gönderilmesi gerekmektedir)  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


2- Yaptığınız bu isteğe cevap JSON formatında döner. a. Verilen tarih aralığında eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner. b. Verilen tarih aralığında eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner. c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.

Status success durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır. Satış ve İade işlemlerinde fark olmaksızın aynı değerler döner.

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
Referans No: İşlemin ayırt edici numarası | ref_no | Örnek: 1000001  
Geri dönen ödemenin tespit edildiği tarih | date_detected | Örnek: 2020-06-08  
Ödemenin geri döndüğü tarih | date_reimbursed | Örnek: 2020-06-08  
Transfer talebinde iletilen alıcı adı soyadı | transfer_name | Örnek: TEST USER  
Transfer talebinde iletilen IBAN | transfer_iban | -  
Transfer talebinde iletilen tutar | transfer_amount | Örnek: 35.18  
Transfer talebinde iletilen para birimi. | transfer_currency | Örnek: TL  
Transfer talebinin iletildiği tarih | transfer_date | Örnek: 2020-06-08  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXXXXYYYYYYYY';
        $merchant_salt  = 'XXXXXXXXYYYYYYYY';
    
        ## Gerekli Bilgiler
        #
        $start_date = "2020-05-20 00:00:00";
        $end_date = "2020-06-16 23:59:59";
        # Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $start_date . $end_date . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'start_date' => $start_date,
            'end_date' => $end_date,
            'paytr_token' => $paytr_token
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/geri-donen-transfer");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        $result = json_decode($result, 1);
    
        /*
          $result değeri içerisinde dönen yanıt örneği;
    
        [ref_no] => 1000001
        [date_detected] => 2020-06-10
        [date_reimbursed] => 2020-06-08
        [transfer_name] => ÖRNEK İSİM
        [transfer_iban] => TR100000000000000000000001
        [transfer_amount] => 35.18
        [transfer_currency] => TL
        [transfer_date] => 2020-06-08
    
        */
    
        if ($result[status] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result[status] == 'failed')
        {
            // sonuç bulunamadı
            echo "ilgili tarih araliginda islem bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result[err_no] . " - " . $result[err_msg];
        }
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import json
    import requests
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXXXXYYYYYYYY'
    merchant_salt = 'XXXXXXXXYYYYYYYY'
    
    # Gerekli Bilgiler
    start_date = '2020-05-20 00:00:00'
    end_date = '2020-06-16 23:59:59'
    # Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + start_date + end_date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'start_date': start_date,
        'end_date': end_date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/geri-donen-transfer', params)
    res = json.loads(result.text)
    
    """
    res değeri içerisinde;
    ['ref_no']              - 1000001
    ['date_detected']       - 2020-06-10
    ['date_reimbursed']     - 2020-06-08
    ['transfer_name']       - ÖRNEK İSİM
    ['transfer_iban']       - TR100000000000000000000001
    ['transfer_amount']     - 35.18
    ['transfer_currency']   - TL
    ['transfer_date']       - 2020-06-08
    bilgileri dönmektedir.
    """
    
    if res['status'] == 'success':
        # VT işlemleri vs.
        print(res)
    elif res['status'] == 'failed':
        print('İlgili tarih araliginda islem bulunamadi')
    else:
        print(res['err_no'] + ' - ' + res['err_msg'])
    
    
    
      // ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
      //  #                                                                                          #
      //  ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
      //  #
      //  ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    using System.Web.Routing;
    
    namespace WebApplication1.Controllers
    {
        public class paytr_geri_donen_odemeler_listele_ornekController : Controller
        {
            public ActionResult paytr_geri_donen_odemeler_listele_ornek()
            {
                // ####################### GEREKLİ BİLGİLER #######################
                //
                // 
    
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
    
                //     #######################
                string start_date = "2021-11-01 00:00:00";
                string end_date = "2021-11-29 23:59:59";
                //  Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
    
                //  ####################### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
                string Birlestir = string.Concat(merchant_id,start_date,end_date,merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // #######################
    
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["start_date"] = start_date;
                data["end_date"] = end_date;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/geri-donen-transfer", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    /*
                      $result değeri içerisinde dönen yanıt örneği;
    
                    [ref_no] => 1000001
                    [date_detected] => 2020-06-10
                    [date_reimbursed] => 2020-06-08
                    [transfer_name] => ÖRNEK İSİM
                    [transfer_iban] => TR100000000000000000000001
                    [transfer_amount] => 35.18
                    [transfer_currency] => TL
                    [transfer_date] => 2020-06-08
    
                    */
    
                    if (json.status == "success")
                    {
                         // VT işlemleri vs.
                        Response.Write(json);
    
                    }
    
                   else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("İlgili tarih araliginda islem bulunamadi");
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
    
                return View();
            }
        }
    }
    
    
    
      var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    //  ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXXXXYYYYYYYY';
    var merchant_salt = 'XXXXXXXXYYYYYYYY';
    
    app.get("/list", function (req, res) {
        //  Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        var start_date = '2020-11-01 00:00:00';
        var end_date = '2020-11-29 23:59:59';
    
        //  ####################### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/geri-donen-transfer',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'start_date': start_date,
                'end_date': end_date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
    
                /*
    
                [ref_no] => 1000001
                [date_detected] => 2020-06-10
                [date_reimbursed] => 2020-06-08
                [transfer_name] => ÖRNEK İSİM
                [transfer_iban] => TR100000000000000000000001
                [transfer_amount] => 35.18
                [transfer_currency] => TL
                [transfer_date] => 2020-06-08
    
                */
                // VT işlemleri vs.
                res.send(res_data);
    
            } else {
    
                // Hata durumu
    
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/send", function (req, res) {
    
        var trans_id = '';
        var trans_info = [{
            'amount': '1283',
            'receiver': 'XYZ LTD ŞTİ',
            'iban': 'TRXXXXXXXXXXXXXXXXXXXXX'
        }];
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + trans_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/hesaptan-gonder',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
    
                'trans_info': JSON.stringify(trans_info),
                'trans_id': trans_id,
                'paytr_token': paytr_token,
                'merchant_id': merchant_id,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(callback.merchant_id + callback.trans_id + merchant_salt).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        var processed_result = JSON.parse(callback.processed_result);
    
        for (const [key, value] of Object.entries(processed_result)) {
            console.log(`${key}: ${value}`);
        }
    
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Geri dönen ödemeler örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/geri-donen-odemeleri-listele/paytr_geri_donen_odemeler.zip)


---

# Platform Transfer Talimatının Verilmesi | PayTR


# Platform Transfer Talimatının Verilmesi

**Mağaza aşağıdaki bilgileri Platform Transfer API’sine gönderir.**

  * İstek (REQUEST) yapılacak URL: https://www.paytr.com/odeme/platform/transfer



**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet |   
merchant_oid (string) | Mağaza sipariş no: Satış işleminde gönderdiğiniz benzersiz sipariş numaranız | Evet | En fazla 64 karakter,Alfa numerik  
trans_id (string) | Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası | Evet | Alfanumerik – En fazla 60 karakter  
submerchant_amount (integer) | Satıcıya yapılacak ödeme tutarı:Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali | Evet | Örn: 34.56 TL için 3456 gönderilmelidir  
total_amount (integer) | Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali | Evet | Örn: 94.56 TL için 9456 gönderilmelidir. (94.56 * 100 = 9456)  
transfer_name (string) | Satıcının banka hesabı için ad soyad/ünvanı | Evet | Örn: Ragıp Adıgüzel  
transfer_iban(int) | Satıcının banka hesabı IBAN numarası | Evet | Örn: TRXX XXXX XXXX XXXX XXXX XXXX XX (26 Karakter)  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet |   
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet |   
  
  


  * POST REQUEST içeriğinde gönderilecek değerler:

Alan adı / tipi | Zorunlu | Token | Açıklama | Kısıtlar  
---|---|---|---|---  
merchant_id(integer) | Evet | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası |   
merchant_oid (string) | Evet | Evet | Mağaza sipariş no: Satış işleminde gönderdiğiniz benzersiz sipariş numaranız | En fazla 64 karakter,Alfa numerik  
trans_id | Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası | Evet | Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası | Alfanumerik – En fazla 60 karakter  
submerchant_amount(integer) | Evet | Evet | Satıcıya yapılacak ödeme tutarı:Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali | Örn: 34.56 TL için 3456 gönderilmelidir  
total_amount(integer) | Evet | Evet | Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali | Örn: 94.56 TL için 9456 gönderilmelidir  
transfer_name (string) | Evet | Evet | Satıcının banka hesabı için ad soyad/ünvanı | Örn: Ragıp Adıgüzel  
transfer_iban | Evet | Evet | Satıcının banka hesabı IBAN numarası | Örn: TRXX XXXX XXXX XXXX XXXX XXXX XX (26 Karakter)  
paytr_token (string) | Evet | Hayır | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Nasıl hesaplanacağı hakkında lütfen örnek kodları inceleyin  
  
  


**STOPAJ BİLGİLENDİRMESİ**

02.08.2024 tarihli Resmi Gazete'de yayınlanan 7524 sayılı Kanun ile 193 sayılı Gelir Vergisi Kanunu ve 5520 sayılı Kurumlar Vergisi Kanunu'nda yapılan değişikliğin ardından pazaryerlerinde yapılan satışların üzerinden stopaj kesintisi uygulamasına yönelik düzenleme 1 Ocak 2025 tarihinde yürürlüğe girmiştir.

Büyüyen e-ticaret pazarında adil vergilendirilme yapılmasına yönelik yeni düzenlemeyle birlikte, 21.12.2024 tarihli ve 9284 sayılı Cumhurbaşkanı kararı ile Gelir Vergisi Kanunu ve Kurumlar Vergisi Kanunu kapsamında hizmet sağlayıcıları ve elektronik ticaret hizmet sağlayıcılarının yapılan satışlar üzerinden %1 oranında stopaj ödemesine karar verilmiştir.

Alt satıcılarına ödemelerini transfer eden pazaryeri üye işyerlerimizin hakedişlerini belirlemek için stopaj tutarını KDV ve vergiler hariç, net satış tutarı üzerinden hesaplamaları gerekmektedir. Tüm detaylara ve örnek hesaplama tablosuna aşağıdaki linkten ulaşabilirsiniz.

Ürün Satış Fiyatı | Kdv Oranı | Kdv Tutarı | Kdv ve Vergiler Düşürüldükten Sonra Net Ürün Fiyatı | Stopaj Tutarı | Pazaryeri Tarafından Belirlenen Alt Satıcı Hakedişi | Stopaj Tutarı Düşürüldükten Sonra Alt Satıcı Yeni Hakedişi  
---|---|---|---|---|---|---  
100 | %20 | 20₺ | 80₺ | 80₺ X 0.01=0.8₺ | 95 | 94.2  
  
**ÖNEMLİ NOTLAR**

1- Mağaza, ödemenin yapılmasını istediği tarihte en geç saat 10:00’a kadar Transfer API’si yoluyla isteği göndermelidir. Daha sonra gönderilen istekler bir sonraki gün işleme alınacaktır.

2- Sipariş ödemesi ile aynı gün transfer talebi oluşturamazsınız. Talebi en erken, ödemeyi takip eden ilk gün oluşturmanız gerekmektedir.

**TRANSFER ÖRNEKLERİ (Değerler gerçek değildir. Sadece örnektir)**

**ÖRNEK 1: ÖDEMEDE TEK ALT SATICI OLMASI DURUMU**

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 100 TL

• Sipariş numarası (merchant_oid): 123ABCD

• Takip numarası (trans_id): 45ABT34

• Satıcı ile olan komisyon oranınıza göre (Örnek: %8) satıcıya aktarılacak (submerchant_amount): 92 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 100 TL Bu bilgilerle ödeme talimatı verdiğinizde;

• Satıcıya 92 TL ödenir,

• Kalan 8 TL içerisinden PayTR ile olan komisyon oranınız (Örnek: %3) düşülerek kalan tutar (örneğe göre 5 TL) firmanızın hesabına aktarılır. Yapılan kesinti tarafınıza faturalandırılır. 

* * *

**ÖRNEK 2: ÖDEMEDE BİRDEN FAZLA ALT SATICI OLMASI DURUMU**

Sipariş ödemesi birden fazla satıcıyı kapsayabilir. Örneğin; Kart hamili alışveriş sepetinde birden fazla satıcıdan ürün / hizmet alıyor olabilir. Siparişin toplam bedelinin 300 TL olduğunu düşünelim. Bu durumda,

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 300 TL

• Sipariş numarası (merchant_oid): 123ABCDE

• Takip numarası (trans_id): 75ZTY39

• Satıcı ile olan komisyon oranınıza göre (Örnek: %8) satıcıya aktarılacak (submerchant_amount): 92 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 100 TL

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 300 TL

• Sipariş numarası (merchant_oid): 123ABCDE

• Takip numarası (trans_id): DF43DFC

• Satıcı ile olan komisyon oranınıza göre (Örnek: %5) satıcıya aktarılacak (submerchant_amount): 47,5 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 50 TL

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 300 TL

• Sipariş numarası (merchant_oid): 123ABCDE

• Takip numarası (trans_id): 98DFVXS

• Satıcı ile olan komisyon oranınıza göre (Örnek: %10) satıcıya aktarılacak (submerchant_amount): 135 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 150 TL şeklinde birden fazla ödeme talimatı verebilirsiniz. 

* * *

**ÖRNEK 3: ÖDEMENİN ALT SATICI İÇİN OLMAMA DURUMU**

Yazılımınız üzerinden geçen diğer ödemeler için (örneğin 50 TL üyelik ücreti, hizmet bedeli, vb.) eğer tutarın tamamını firmanız hesabına almak istiyorsanız,

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 50 TL

• Sipariş numarası (merchant_oid): 1881ABCD

• Takip numarası (trans_id): 18ATT81

• Satıcı ile olan komisyon oranınıza göre (Örnek: %0) satıcıya aktarılacak (submerchant_amount): 0 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 50 TL şeklinde talep oluşturduğunuz durumda tutarın tamamı firmanız hesabına transfer edilecektir.

* * *

**Yapılan isteğe geri dönecek yanıt (RESPONSE) JSON formatındadır. Detaylar için örnek kodları inceleyebilirsiniz.**

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        $merchant_id = 'MAGAZA_NO';
        $merchant_key = 'XXXXXXXXXXX';
        $merchant_salt = 'YYYYYYYYYYY';
    
        // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
        $merchant_oid = "";
    
        // Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası
        $trans_id = time();
    
        // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        $submerchant_amount = "";
    
        // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        $total_amount = "";
    
        // Satıcının banka hesabı için ad soyad/ünvanı
        $transfer_name = "";
    
        // Satıcının banka hesabı IBAN numarası
        $transfer_iban = "";
    
        // İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir
        $hash_str = $merchant_id . $merchant_oid . $trans_id . $submerchant_amount . $total_amount . $transfer_name . $transfer_iban;
        $token = base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
    
        $post_vals=array(
                'merchant_id'=>$merchant_id,
                'merchant_oid'=>$merchant_oid,
                'trans_id'=>$trans_id,
                'submerchant_amount'=>$submerchant_amount,
                'total_amount'=>$total_amount,
                'transfer_name'=>$transfer_name,
                'transfer_iban'=>$transfer_iban,
                'paytr_token'=>$token
            );
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/platform/transfer");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR platform transfer request connection error. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        /*
            Başarılı yanıt örneği:
            {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
            Başarısız yanıt örneği:
            {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
        */
    
        if($result['status']=='success')
        {
            //VT işlemleri vs.
        }
        else
        {
            echo $result['err_no']." - ".$result['err_msg'];
        }
        #########################################################################
    
    ?>
    
    
    # Python 3.6+
    
    import base64
    import hashlib
    import hmac
    import json
    import requests
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'MAGAZA_NO'
    merchant_key = b'XXXXXXXXXXX'
    merchant_salt = 'YYYYYYYYYYY'
    
    # Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
    merchant_oid = ''
    
    # Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası
    trans_id = random.randint(1, 9999999).__str__()
    
    # Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
    submerchant_amount = ''
    
    # Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
    total_amount = ''
    
    # Satıcının banka hesabı için ad soyad/ünvanı
    transfer_name = ''
    
    # Satıcının banka hesabı IBAN numarası
    transfer_iban = ''
    
    # İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir
    hash_str = merchant_id + merchant_oid + trans_id + submerchant_amount + total_amount + transfer_name + transfer_iban + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'trans_id': trans_id,
        'submerchant_amount': submerchant_amount,
        'total_amount': total_amount,
        'transfer_name': transfer_name,
        'transfer_iban': transfer_iban,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/platform/transfer', params)
    res = json.loads(result.text)
    
    """
    Başarılı yanıt örneği:
    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
    Başarısız yanıt örneği:
    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
    """
    
    if res['status'] == 'success':
        # VT işlemleri vs.
        print(res)
    else:
        print(res['err_no'] + ' - ' + res['err_msg'])
    
    
    // 1. ADIM için örnek kodlar
    
    using Newtonsoft.Json.Linq; // Bu satırda hata alırsanız, site dosyalarınızın olduğu bölümde bin isimli bir klasör oluşturup içerisine Newtonsoft.Json.dll adlı DLL dosyasını kopyalayın.
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Linq;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class platform_transfer_talebi_ornek : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
            //
            // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
            string merchant_id      = "XXXXXX";
            string merchant_key     = "YYYYYYYYYYYYYY";
            string merchant_salt    = "ZZZZZZZZZZZZZZ";
            //
            // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası 
            string merchant_oid     = "";
            //
            // Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası 
            string trans_id     = "";
            //
            // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
            string submerchant_amount  = "";
            //
            // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
            string total_amount    = ""; 
            //
            // Satıcının banka hesabı için ad soyad/ünvanı
            string transfer_name    = "";
            //
            // Satıcının banka hesabı IBAN numarası
            string transfer_iban    = "";
            //
    
            // Gönderilecek veriler oluşturuluyor
            NameValueCollection data = new NameValueCollection();
            data["merchant_id"] = merchant_id;
            data["merchant_oid"] = merchant_oid;
            data["trans_id"] = trans_id;
            data["submerchant_amount"] = submerchant_amount.ToString();
            data["total_amount"] = total_amount.ToString();
            data["transfer_name"] = transfer_name;
            data["transfer_iban"] = transfer_iban;
            //
            // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
            string Birlestir = string.Concat(merchant_id, merchant_oid, trans_id, submerchant_amount.ToString(), total_amount.ToString(), transfer_name, transfer_iban, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            data["paytr_token"] = Convert.ToBase64String(b);
            //
    
            using (WebClient client = new WebClient()) {
                client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                byte[] result = client.UploadValues("https://www.paytr.com/odeme/platform/transfer", "POST", data);
                string ResultAuthTicket = Encoding.UTF8.GetString(result);
                dynamic json = JValue.Parse(ResultAuthTicket);
    
                /*
                    Başarılı yanıt örneği:
                    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
                    Başarısız yanıt örneği:
                    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
                */
                if (json.status == "success") {
                    //VT işlemleri vs.
                    Response.Write(json);
                }else{
                    Response.Write("PAYTR platform transfer request failed. reason:" + json.err_msg + "");
                }
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'MAGAZA_NO';
    var merchant_key = 'XXXXXXXXXXX';
    var merchant_salt = 'YYYYYYYYYYY';
    
    app.get("/send", function (req, res) {
    
        // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
        var merchant_oid = '';
        // Eşsiz transfer numarası
        var trans_id = '';
        // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        var submerchant_amount = '';
        // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        var total_amount = '';
        // Satıcının banka hesabı için ad soyad/ünvanı
        var transfer_name = '';
        // Satıcının banka hesabı IBAN numarası
        var transfer_iban = '';
    
        var hash_str = merchant_id + merchant_oid + trans_id + submerchant_amount + total_amount + transfer_name + transfer_iban;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(hash_str + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/platform/transfer',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'merchant_oid': merchant_oid,
                'trans_id': trans_id,
                'submerchant_amount': submerchant_amount,
                'total_amount': total_amount,
                'transfer_name': transfer_name,
                'transfer_iban': transfer_iban,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
    
                /*
                    Başarılı yanıt örneği:
                    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
                    Başarısız yanıt örneği:
                    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
                */
    
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
    
        var callback = req.body;
        var trans_ids = callback.trans_ids;
    
        var trans_ids = trans_ids.replace('\\', '');
    
        // POST değerleri ile hash oluştur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(trans_ids + merchant_salt).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        // ## trans_ids: Daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgilerini içeren JSON 
        // ## (trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir)
        // ## Örn: Burada trans_ids JSON verisini DECODE edip, çıktıdaki her bir trans_id ile veritabanınızdan transfer talebini tespit ederek ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
        var processed_result = JSON.parse(trans_ids);
    
        console.log(processed_result);
    
        // Bildirimin alındığını PayTR sistemine bildir.  
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Transfer talimatının verilmesi örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/transfer-talimatinin-verilmesi/paytr_platform_transfer_talebi.zip)


---

# Transfer Talimatının Sonucunun Alınması (Opsiyonel) | PayTR


# Transfer Talimatının Sonucunun Alınması (Opsiyonel)

PAYTR sistemi, transfer işlemlerinin sonuçlanması sonrası Mağazanın belirlediği URL’e bilgi verir.

**İstek (REQUEST) yapılacak URL: Platform Transfer Sonucu Bildirim URL (Mağaza Paneli > Destek & Kurulum > AYARLAR sayfasına Mağaza tarafından girilmelidir))**

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
trans_id | Transfer talebinde belirttiğiniz trans_id değerlerini içeren JSON string | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Zorunlu | Açıklama | Kısıtlar  
---|---|---|---  
trans_ids (JSON string) | Evet | Transfer talebinde belirttiğiniz trans_id değerlerini içeren JSON string |   
hash (string) | Evet | paytr_token: İsteğin PAYTR’dan geldiğine ve içeriğin değişmediğine emin olmanız için oluşturulan değer | Hesaplama ve kontrol hakkında lütfen örnek kodları inceleyin  
  
  


**Örnek POST:**
    
    
    [hash] => Of0/yvgTii/+lGD3o+J0u8xXriVqlPIrvsZsv4cLhM4=
    [trans_ids] => ["dcbbe0b9fd25154d73c","dc8c509efc6450d30","9310d84d3bf"]

**Yanıt (RESPONSE):**

PAYTR’dan gelen isteğe ekrana OK basarak yanıt vermeniz beklenmektedir. Bu yanıtın alınmadığı durumda istek tekrarlanacaktır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        $post = $_POST;
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        ###########################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        #
        ## POST değerleri ile hash oluştur.
        $post["trans_ids"]=str_replace("\\", "", $post["trans_ids"]);
        $hash = base64_encode( hash_hmac('sha256', $post['trans_ids'].$merchant_salt, $merchant_key, true) );
        #
        ## Oluşturulan hash'i, PayTR'dan gelen post içindeki hash ile karşılaştır (isteğin PayTR'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ###########################################################################
    
        ## $post['trans_ids'] içerisinde daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgileri JSON formatında gelir
        ## trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir
        $trans_ids = json_decode($post['trans_ids'],1);
        foreach($trans_ids as $trans_id)
        {
            ## Örn: Burada $trans_id ile veritabanınızdan transfer talebini tespit edip ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir.
        echo "OK";
        exit;
    ?>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    
    import base64
    import hashlib
    import hmac
    import json
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'YYYYYYYYYYYYYY'
        merchant_salt = 'ZZZZZZZZZZZZZZ'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        post['trans_ids'] = post['trans_ids'].replace('\\', '')
        hash_str = post['trans_ids'] + merchant_salt
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # post['trans_ids'] içerisinde daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgileri JSON formatında gelir
        # trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir
        trans_ids = json.loads(post['trans_ids'])
    
        for ids in trans_ids:
            # Örn: Burada trans_id ile veritabanınızdan transfer talebini tespit edip ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
            print(ids)
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class transfer_sonucu_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYY";
        string merchant_salt    = "ZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string trans_ids = Request.Form["trans_ids"];
            string hash = Request.Form["hash"];
    
            trans_ids = trans_ids.Replace(@"\","");
    
            string Birlestir = string.Concat(trans_ids, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
            }
    
            //###########################################################################
    
            ## trans_ids: Daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgilerini içeren JSON 
            ## (trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir)
            ## Örn: Burada trans_ids JSON verisini DECODE edip, çıktıdaki her bir trans_id ile veritabanınızdan transfer talebini tespit ederek ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
    
            dynamic dynJson = JsonConvert.DeserializeObject(trans_ids);
            foreach (var item in dynJson)
            {
                ## Örn: Burada $trans_id ile veritabanınızdan transfer talebini tespit edip ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
            }
    
            // Bildirimin alındığını PayTR sistemine bildir.  
            Response.Write("OK");    
        }
    }
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'MAGAZA_NO';
    var merchant_key = 'XXXXXXXXXXX';
    var merchant_salt = 'YYYYYYYYYYY';
    
    app.get("/send", function (req, res) {
    
        // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
        var merchant_oid = '';
        // Eşsiz transfer numarası
        var trans_id = '';
        // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        var submerchant_amount = '';
        // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        var total_amount = '';
        // Satıcının banka hesabı için ad soyad/ünvanı
        var transfer_name = '';
        // Satıcının banka hesabı IBAN numarası
        var transfer_iban = '';
    
        var hash_str = merchant_id + merchant_oid + trans_id + submerchant_amount + total_amount + transfer_name + transfer_iban;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(hash_str + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/platform/transfer',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'merchant_oid': merchant_oid,
                'trans_id': trans_id,
                'submerchant_amount': submerchant_amount,
                'total_amount': total_amount,
                'transfer_name': transfer_name,
                'transfer_iban': transfer_iban,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
    
                /*
                    Başarılı yanıt örneği:
                    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
                    Başarısız yanıt örneği:
                    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
                */
    
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
    
        var callback = req.body;
        var trans_ids = callback.trans_ids;
    
        var trans_ids = trans_ids.replace('\\', '');
    
        // POST değerleri ile hash oluştur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(trans_ids + merchant_salt).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        // ## trans_ids: Daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgilerini içeren JSON 
        // ## (trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir)
        // ## Örn: Burada trans_ids JSON verisini DECODE edip, çıktıdaki her bir trans_id ile veritabanınızdan transfer talebini tespit ederek ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
        var processed_result = JSON.parse(trans_ids);
    
        console.log(processed_result);
    
        // Bildirimin alındığını PayTR sistemine bildir.  
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Transfer talimatının sonucunun alınması örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/transfer-talimatinin-sonucunun-alinmasi/PayTR Platform Transfer Talebi.zip)


---

# Durum Sorgu API Entegrasyonu | PayTR


# Durum Sorgu API Entegrasyonu

Durum Sorgu servisi aracılığıyla, mağazanız üzerinde gerçekleştirilen işlemlerin durumunu sorgulayabilirsiniz.

Mağaza Durum Sorgulama ve Pazaryeri Durum Sorgulama olarak iki kategoriye ayrılır. 

1- Aşağıdaki tabloda belirtilen bilgileri https://www.paytr.com/odeme/durum-sorgu adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
merchant_key | Mağaza Parola  
merchant_salt | Mağaza Gizli Anahtar  
merchant_oid | Sipariş Numarası  
  
  
**Mağaza Durum Sorgulama**  
Tablodan gelen değerler ile sipariş numarası sorgulanır. Müşteriye ait ödeme tutarı ve toplam ödeme tutarı para birimi ile birlikte ekrana basılır. Yukarıdaki bilgilerde bir yanlışlık olursa hata mesajıda ekranda gösterilir. Aynı zamanda siparişe ait iadeler var ise bu iadeler ekranda belirtilir.

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Eğer sorguda bir hata yoksa status değeri “success” ve aşağıdaki tabloda bulunan bilgiler döner.  
b. Eğer sorguda bir hatanız varsa status değeri “error” döner. Bu durumda hata detayı için “err_msg” içeriğini kontrol etmelisiniz.

Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Değişkenler | Açıklamalar | Değerler  
---|---|---  
status(string) | Sorgulama sonucu(success veya failed) | success veya error  
net_tutar (string) | Kesinti sonrası kalan tutar | 9.76  
kesinti_tutari (string) | İşlem için kesilen tutar | 0.24  
payment_amount(string) | İlgili siparişe ait tutar bilgisi | 10,8  
payment_total(string) | Müşterinin ilgili sipariş için ödediği tutar | 10,8  
payment_date(integer) | İşlemin gerçekleşme tarihi | 2021-01-01 (YYYY-MM-DD)  
currency(string) | Para birimi | TL(veya TRY), EUR, USD, GBP, RUB  
taksit(string) | Taksit: İşlem taksitli yapıldı ise taksit sayısı | 0,2,3,4,5,6,7,8,9,10,11,12  
kart_marka(string) | İşlem yapılan kartın markası | Örn. WORD, BONUS, vb.  
masked_pan(string) | İşlemin gerçekleşme tarihi | Örn. 455359AAA6747  
odeme_tipi(string) | Ödemenin hangi tipte yapıldığı | KART veya EFT  
test_mode(string) | İşlemin test veya canlı ortamda yapıldığı | 0 veya 1  
returns(Array) | Eğer ilgili sipariş içerisinde iade varsa dönecek değer  
err_no | Hata numarası | 004  
err_msg | Hata mesajı | merchant_oid ile basarili odeme bulunamadi  
  
  


Durum sorgulama örnek kodları: Örnek kodlar içinde nasıl yapılacağı detaylı olarak anlatılmaktadır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    $merchant_id = "XXX";
    $merchant_key = "XXX";
    $merchant_salt = "XXX";
    $merchant_oid = "XXX";
    
    $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $merchant_oid . $merchant_salt, $merchant_key, true));
    
    $post_vals = array('merchant_id' => $merchant_id,
            'merchant_oid' => $merchant_oid,
            'paytr_token' => $paytr_token);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/durum-sorgu");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
    curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 90);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
    //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
    //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
    $result = @curl_exec($ch);
    
    if (curl_errno($ch)) {
           echo curl_error($ch);
           curl_close($ch);
            exit;
    }
    curl_close($ch);
    
    $result = json_decode($result, 1);
    
    if ($result[status] != 'success') {
           echo $result[err_no] . " - " . $result[err_msg];
           exit;
    }
    
    echo $result['payment_amount'] . " " . $result['currency'] . "<br>";
    
    echo $result['payment_total'] . " " . $result['currency'] . "<br>";
    
    echo $result['payment_date'] . "<br>";
    
    foreach ($result['returns'] AS $return_success)
           print_r($return_success);
    ?>
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXXXX'
    merchant_oid = ''
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + merchant_oid + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/durum-sorgu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['payment_amount'] + res['currency'])
        print(res['payment_total'] + res['currency'])
        print(res['payment_date'])
        for return_success in res['returns']:
          print(return_success)
    
    else:
        print(res['err_no'] + ' ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;
    using PayTrTest.Model;
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    
    namespace PayTrTest
    {
        class Program
        {
            private readonly string TRANSFER_URL = "https://www.paytr.com/odeme/durum-sorgu";
            private readonly string MERCHANT_ID = "MERCHANT_ID";
            private readonly string MERCHANT_KEY = "MERCHANT_KEY";
            private readonly string MERCHANT_SALT = "MERCHANT_SALT";
    
            static void Main(string[] args)
            {
                var p = new Program();
                p.Start();
            }
    
            public void Start()
            {
                Dictionary<string, string> testCases = new Dictionary<string, string>
                {
                    { "Geçersiz Merchant OID", "invalid_merchant_oid" } ,
                    { "Başarılı Ödeme", "ffd0c5992212400cb87b88ff40bbcda2" } ,
                    { "Başarısız Ödeme", "fed4b0f2aa33450bab58971ce5da75f0" } ,
                    { "Kısmi Transfer (işlemde) ve Kısmi İade", "dbb5a788734f498e8490333936ec6e11" } ,
                    { "Tamamı Transfer Edilmiş", "5cfbb224a9c44246853818c3082946d8" } ,
                };
    
                foreach(KeyValuePair<string, string> item in testCases)
                {
                    Console.WriteLine($"TESTING '{item.Key}' using Merchant OID: `{item.Value}` {Environment.NewLine}");
                    _DoQuery(item.Value);
                    Console.WriteLine(new string('-',50) + Environment.NewLine);
    
                }
                Console.WriteLine($"{Environment.NewLine}{Environment.NewLine}Cikmak icin bir tusa basin...");
                Console.ReadKey();
            }
    
            private void _DoQuery(string merchantOid)
            {
                PaytrDurumSorguResponse res = _QueryPayment(
                    MERCHANT_ID,
                    MERCHANT_KEY,
                    MERCHANT_SALT,
                    merchantOid
                );
    
                if (res.Status != "success")
                {
                    Console.WriteLine($"  {res.ErrorMessage} - {res.ErrorNo}");
                    return;
                }
    
                Console.WriteLine($"  Sipariş Tutarı : {res.PaymentAmount} {res.Currency}");
    
                Console.WriteLine($"  Müşteri Ödeme Tutarı : {res.PaymentTotal} {res.Currency}");
                if(res.Returns.Count > 0) 
                    Console.WriteLine("  ## IADELER ##");
                foreach (PaytrDurumSorguReturnItem returnItem in res.Returns)
                {
                    Console.WriteLine($"    {returnItem.Amount} - {returnItem.Date} - {returnItem.Type} - {returnItem.DateCompleted} - {returnItem.AuthCode} - {returnItem.RefNum}");
                }
            }
    
            private PaytrDurumSorguResponse _QueryPayment(string merchantId, string merchantKey, string merchantSalt, string merchantOid)
            {
                NameValueCollection data = _GeneratePayTrSorguData(merchantId, merchantKey, merchantSalt, merchantOid);
                ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls;
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
    
                    byte[] result = client.UploadValues(TRANSFER_URL, "POST", data);
    
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    return JsonConvert.DeserializeObject<PaytrDurumSorguResponse>(ResultAuthTicket);
                }
            }
    
            private NameValueCollection _GeneratePayTrSorguData(string merchantId, string merchantKey, string merchantSalt, string merchantOid)
            {
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchantId;
                data["merchant_oid"] = merchantOid;
    
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(merchantId, merchantOid, merchantSalt);
    
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchantKey));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                data["paytr_token"] = Convert.ToBase64String(b);
    
                return data;
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXXXXX';
    var merchant_key = 'XXXXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXXXX';
    
    var merchant_oid = ''; // Benzersiz işlem numarası.
    
    app.get("/", function (req, res) {
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + merchant_oid + merchant_salt).digest('base64');
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/durum-sorgu',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'merchant_oid': merchant_oid,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send(res_data);
    
        } else {
            //hata durumu
            console.log(response.body);
            res.end(response.body);
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Mağaza durum sorgulama örnek kodları[**indirmek için tıklayın.**](/durum-sorgu/paytr_magaza_durum_sorgulama.zip)

1- Aşağıdaki tabloda belirtilen diğer bilgileri https://www.paytr.com/odeme/durum-sorgu adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
merchant_key | Mağaza Parola  
merchant_salt | Mağaza Gizli Anahtar  
merchant_oid | Sipariş Numarası  
  
**Pazaryeri Durum Sorgulama**  
Tablodan gelen değerler ile sipariş numarası sorgulanır. Müşteriye ait ödeme tutarı ve toplam ödeme tutarı para birimi ile birlikte ekrana basılır. Yukarıdaki bilgilerde bir yanlışlık olursa hata mesajıda ekranda gösterilir. Aynı zamanda siparişe ait iadeler var ise bu iadeler ekranda belirtilir.

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Eğer sorguda bir hata yoksa status değeri “success” ve aşağıdaki tabloda bulunan bilgiler döner.  
b. Eğer sorguda bir hatanız varsa status değeri “error” döner. Bu durumda hata detayı için “err_msg” içeriğini kontrol etmelisiniz.

Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Değişkenler | Açıklamalar | Değerler  
---|---|---  
Status(string) | Sorgulama sonucu.(success veya failed) | success veya error  
payment_amount(string) | İlgili siparişe ait tutar bilgisi | 10,8  
payment_total(string) | Müşterinin ilgili sipariş için ödediği tutar | 10,8  
payment_date(integer) | İşlemin gerçekleşme tarihi | 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss)  
currency(string) | Para birimi | TL(veya TRY), EUR, USD, GBP, RUB  
taksit(string) | Taksit: İşlem taksitli yapıldı ise taksit sayısı | 0,2,3,4,5,6,7,8,9,10,11,12  
kart_marka(string) | İşlem yapılan kartın markası | Örn. WORD, BONUS, vb.  
masked_pan(string) | İşlemin gerçekleşme tarihi | Örn. 455359AAA6747  
odeme_tipi(string) | Ödemenin hangi tipte yapıldığı | KART veya EFT  
test_mode(string) | İşlemin test veya canlı ortamda yapıldığı | 0 veya 1  
returns(string) | Eğer ilgili sipariş içerisinde iade varsa dönecek değer |   
reference_no(string) | Referans No: İade talebinde bulunurken gönderildi ise dönen iade referans numarası | 111111111111(maksimum 64 alfanumarik karakter)  
err_no | Hata numarası | 004  
err_msg | Hata mesajı | merchant_oid ile basarili odeme bulunamadi  
submerchant_payments | Platform ödemeleri |   
  
  


Pazar yeri durum sorgulama örnek kodları: Örnek kodlar içinde nasıl yapılacağı detaylı olarak anlatılmaktadır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
        $merchant_id = "XXX";
        $merchant_key = "XXX";
        $merchant_salt = "XXX";
        $merchant_oid = "XXX";
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $merchant_oid . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'merchant_oid' => $merchant_oid,
            'paytr_token' => $paytr_token);
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/durum-sorgu");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
        curl_close($ch);
    
        $result = json_decode($result, 1);
    
        if ($result[status] != 'success') {
            echo $result['err_no'] . " - " . $result['err_msg'];
            exit;
        }
    
        //sipariş tutarı
        echo $result['payment_amount'] . " " . $result['currency'] . "<br>";
    
        //işlem tarihi
        echo $result['payment_date']. "<br>";
    
        //müşteri ödeme tutarı
        echo $result['payment_total'] . " " . $result['currency'] . "<br>";
    
        //siparişteki iadeler (varsa)
    
        /*
    
        Array ( 
        [return_amount] => 1 
        [return_date] => 2021-03-25 23:45:22 
        [return_type] => 
        [date_completed] => 2021-03-25 23:46:02 
        [return_auth_code] =>
        [return_ref_num] => 
        [reference_no] => 111111111111111
        [return_source] => 
        )
    
        */
    
        foreach ($result['returns'] AS $return_success)
            print_r($return_success);
    
        //platform ödemeleri
        foreach ($result['submerchant_payments'] AS $sub_payments)
            print_r($sub_payments);
    ?>
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXXXXX'
    merchant_key = b'XXXXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXXXX'
    merchant_oid = ''
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + merchant_oid + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/durum-sorgu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['payment_amount'] + res['currency'])
        print(res['payment_total'] + res['currency'])
        print(res['payment_date'])
        for return_success in res['returns']:
          print(return_success)
        for sub_payments in res['submerchant_payments']:
          print(sub_payments)
    
    else:
        print(res['err_no'] + ' ' + res['err_msg'])    
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using System.Web.Routing;
    using System.IO;
    
    namespace WebApplication1.Controllers
    {
        public class durum_sorgu_platform_ornekController : Controller
        {
            public ActionResult durum_sorgu_platform_ornek()
            {
                // ####################### #######################
                //
                // 
    
                string merchant_id = "YYYYYY";
                string merchant_key = "YYYYYYYYYYYYYY";
                string merchant_salt = "YYYYYYYYYYYYYY";
                string merchant_oid = "";
                //
    
                //  #######################
                string Birlestir = string.Concat(merchant_id, merchant_oid, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // #######################
    
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["merchant_oid"] = merchant_oid;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/durum-sorgu", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
    
                        Response.Write(json.payment_amount + "-" + json.currency);
                        Response.Write(json.payment_total + "-" + json.currency);
    
                        foreach (var return_success in json.returns)
                        {
                    //Array 
                    //( 
                    //[return_amount] => 1 
                    //[return_date] => 2021-03-25 23:45:22 
                    //[return_type] => 
                    //[date_completed] => 2021-03-25 23:46:02 
                    //[return_auth_code] =>
                    //[return_ref_num] => 
                    //[reference_no] => 111111111111111
                    //[return_source] => 
                    //)
    
                            Response.Write(return_success);
                        }
    
                        foreach (var sub_payments in json.submerchant_payments)
                        {
                            Response.Write(sub_payments);
                        }
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
    
                return View();
            }
        }
    }
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXXXXX';
    var merchant_key = 'XXXXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXXXX';
    
    var merchant_oid = ''; // Benzersiz işlem numarası.
    
    app.get("/", function (req, res) {
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + merchant_oid + merchant_salt).digest('base64');
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/durum-sorgu',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'merchant_oid': merchant_oid,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send(res_data);
    
        } else {
            //hata durumu
            console.log(response.body);
            res.end(response.body);
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Pazaryeri durum sorgulama örnek kodları[**indirmek için tıklayın.**](/durum-sorgu/PayTR Pazaryeri Durum Sorgulama.zip)


---

# İade API Entegrasyonu | PayTR


# İade API Entegrasyonu

Bu servis aracılığıyla, siparişe ait tutarın bir kısmı veya tamamı için iade işlemi gerçekleştirebilirsiniz.

**ÖNEMLİ UYARI:** Yanlış entegrasyon yapmanız hatalı iadelere sebep olabilir ve bu nedenle maddi kayıp yaşayabilirsiniz. Lütfen entegrasyon esnasında çok dikkatli olun! Sorularınız için bize ulaşabilirsiniz.

1- Bu servis ile birlikte iade etmek istediğiniz sipariş için sipariş numarasını ve iade tutarını aşağıda belirtilen gönderilmesi zorunlu olan değerler ile birlikte https://www.paytr.com/odeme/iade adresine POST metodunu kullanarak istek atabilirsiniz.

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu  
---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet  
merchant_oid (string) | Sipariş No: İade işlemini gerçekleştirmek istediğiniz sipariş numarası | Evet  
return_amount(integer) | İade Tutarı: Belirtilen sipariş için iade etmek istediğiniz tutar (Ayraç olarak yalnızca bir nokta (.) gönderilmelidir. Örnek: 10.25) | Evet  
merchant_salt (string) | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet  
merchant_key(integer) | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Açıklama | Zorunlu  
---|---|---  
merchant_id (integer) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet  
merchant_oid (string) | Sipariş No: İade işlemini gerçekleştirmek istediğiniz sipariş numarası | Evet  
return_amount(integer) | İade Tutarı: Belirtilen sipariş için iade etmek istediğiniz tutar (Ayraç olarak yalnızca bir nokta (.) gönderilmelidir. Örnek: 10.25) | Evet  
paytr_token (string) | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir. | Evet  
reference_no | Referans No: İletilmesi durumunda, Durum Sorgu servisinden döner,Alfa numerik | Hayır  
  
  


2- Yapılan isteğe dönecek yanıt JSON formatında olacaktır.  
a. Eğer oluşturulan istek içerisinde belirtilen sipariş numarası yok ise status değeri failed olarak dönecektir.  
b. Eğer oluşturulan istek içerisinde belirtilen sipariş numarası var ise status değeri aşağıdaki tabloda belirtilen değerler ile birlikte success dönecektir.  
c. Eğer gönderdiğiniz isteğin içerisinde bir hata/eksiklik var ise ekranda hata bildirimi belirecektir. Bu durumda hata hakkında detaylı bilgi için err_msg içeriğini kontrol etmeniz gerekecektir.  


**Result değişkeni içinde dönen değerler**

Değişkenler | Açıklamalar  
---|---  
status | İade talebi başarılı ise success döner  
is_test | İade talebi test işlem içinse 1 döner  
merchant_oid | İade talebi yapılan sipariş numarası  
return_amount | İade talebi yapılan tutar  
reference_no | Gönderildi ise referans numarası  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = "XXXXXX";
        $merchant_key   = "YYYYYYYYYYYYYY";
        $merchant_salt  = "ZZZZZZZZZZZZZZ";
        #
        # Sipariş No: İade etmek istediğiniz siparişin numarası.
        $merchant_oid   = "XXXXXX";
        #
        # İade Tutarı: Örneğin işlem 11.97 TL veya 11.97 USD ise.
        $return_amount  = "11.97";
        #
        # Referans Numarası: En fazla 64 karakter, alfa numerik. Zorunlu değil.
        $reference_no  = "XXXXXX11111";
        #
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $paytr_token=base64_encode(hash_hmac('sha256',$merchant_id.$merchant_oid.$return_amount.$merchant_salt,$merchant_key,true));
    
        $post_vals=array('merchant_id'=>$merchant_id,
            'merchant_oid'=>$merchant_oid,
            'return_amount'=>$return_amount,
            'paytr_token'=>$paytr_token);
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/iade");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
        {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        /*
            $result değeri içerisinde;
    
            [status]        - İade talebi başarılı ise success döner.
            [is_test]       - İade talebi test işlem içinse 1 döner.
            [merchant_oid]  - İade talebi yapılan sipariş numarası.
            [return_amount] - İade talebi yapılan tutar.
    
            bilgileri dönmektedir.
        */
    
        if($result['status']=='success')
        {
            // VT işlemleri vs.
        }
        else
        {
            //Örn. $result -> array('status'=>'error', "err_no"=>"006", "err_msg"=>"Toplam iade tutarı odeme tutarindan fazla olamaz")
            echo $result['err_no']." - ".$result['err_msg'];
        }
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXX'
    merchant_key = b'XXX'
    merchant_salt = 'XXX'
    
    # Sipariş Numarası
    merchant_oid = 'XXX'
    
    # İade Tutarı
    return_amount = '11.90' # örn. işlem TL ise on bir lira doksan yedi kuruş
    
    # Referans Numarası: En fazla 64 karakter, alfa numerik. Zorunlu değil.
    reference_no  = 'XXXXXX11111'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + merchant_oid + return_amount + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'return_amount': return_amount,
        'paytr_token': paytr_token,
        'merchant_oid': merchant_oid
    }
    
    result = requests.post('https://www.paytr.com/odeme/iade', params)
    res = json.loads(result.text)
    
    """
    res değeri içerisinde;
    
    ['status']        - İade talebi başarılı ise success döner.
    ['is_test']       - İade talebi test işlem içinse 1 döner.
    ['merchant_oid']  - İade talebi yapılan sipariş numarası.
    ['return_amount'] - İade talebi yapılan tutar.
    
    bilgileri dönmektedir.
    """
    
    if res['status'] == 'success':
       # VT işlemleri vs.
       print(res)
    else:
        """
        Örn.
        ['status']        - error
        ['err_no']        - 006
        ['err_msg']       - Toplam iade tutarı odeme tutarindan fazla olamaz.
        """
        print(res)
    
    
    
    using Newtonsoft.Json.Linq; // Bu satırda hata alırsanız, site dosyalarınızın olduğu bölümde bin isimli bir klasör oluşturup içerisine Newtonsoft.Json.dll adlı DLL dosyasını kopyalayın.
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Linq;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class iade_ornek : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
            //
            // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
            string merchant_id      = "XXXXXX";
            string merchant_key     = "YYYYYYYYYYYYYY";
            string merchant_salt    = "ZZZZZZZZZZZZZZ";
            //
            // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası 
            string merchant_oid     = "";
            //
            // Alıcıya yapılacak olan iade tutarı 
            string return_amount     = "11.97"; //örn. işlem TL ise on bir lira doksan yedi kuruş
            //
            // Referans Numarası: En fazla 64 karakter, alfa numerik. Zorunlu değil.
            string reference_no     = "XXXX1111";
            //
            // Gönderilecek veriler oluşturuluyor
            NameValueCollection data = new NameValueCollection();
            data["merchant_id"] = merchant_id;
            data["merchant_oid"] = merchant_oid;
            data["return_amount"] = return_amount;
            //
            // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
            string Birlestir = string.Concat(merchant_id, merchant_oid, return_amount, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            data["paytr_token"] = Convert.ToBase64String(b);
            //
    
            using (WebClient client = new WebClient()) {
                client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                byte[] result = client.UploadValues("https://www.paytr.com/odeme/iade", "POST", data);
                string ResultAuthTicket = Encoding.UTF8.GetString(result);
                dynamic json = JValue.Parse(ResultAuthTicket);
    
                /*
                    json değeri içerisinde;
    
                    [status]        - İade talebi başarılı ise success döner.
                    [is_test]       - İade talebi test işlem içinse 1 döner.
                    [merchant_oid]  - İade talebi yapılan sipariş numarası.
                    [return_amount] - İade talebi yapılan tutar.
    
                    bilgileri dönmektedir.
                */
    
                if (json.status == "success") {
                    //VT işlemleri vs.
                    Response.Write(json);
                }else{
                    //Örn. $result -> array('status'=>'error', "err_no"=>"006", "err_msg"=>"Toplam iade tutarı odeme tutarindan fazla olamaz")
                    Response.Write("PAYTR payment return failes. reason:" + json.err_msg + "");
                }
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_id = 'XXXXXX';
    var merchant_key = 'YYYYYYYYYYYYYY';
    var merchant_salt = 'ZZZZZZZZZZZZZZ';
    
    var merchant_oid = 'XXXXXX'; // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası 
    var return_amount = '11.97'; // Alıcıya yapılacak olan iade tutarı  
    //örn. işlem TL ise on bir lira doksan yedi kuruş
    var reference_no = "XXXX1111"; // Referans Numarası: En fazla 64 karakter, alfa numerik. Zorunlu değil.
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + merchant_oid + return_amount + merchant_salt).digest('base64');
    
    app.get("/", function (req, res) {
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/iade',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'merchant_oid': merchant_oid,
                'return_amount': return_amount,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                /*
                    [status]        - İade talebi başarılı ise success döner.
                    [is_test]       - İade talebi test işlem içinse 1 döner.
                    [merchant_oid]  - İade talebi yapılan sipariş numarası.
                    [return_amount] - İade talebi yapılan tutar.
                */
                // VT işlemleri vs.
    
                res.send(response.body);
    
            } else {
                //hata durumu
                //Örn. $result -> array('status'=>'error', "err_no"=>"006", "err_msg"=>"Toplam iade tutarı odeme tutarindan fazla olamaz")
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

İade API örnek kodları[**indirmek için tıklayın.**](/iade-api/paytr_iade_api.zip)


---

# PayTR Hata Kodları


# PayTR Hata Kodları

**PayTR servislerinden dönen Hata Kodlarına ait tablolar**

**ÖDEME İŞLEMİ SONRASI BANKAYA GİTMEDEN PAYTR TARAFINDAN BİLDİRİM URL ADRESİNİZE DÖNÜLEN HATA KODLARI VE AÇIKLAMALARI**

failed_reason_code | failed_reason_msg | Açıklama  
---|---|---  
0 | DEĞİŞKEN (AÇIKLAMAYI OKUYUN) | Ödemenin neden onaylanmadığına ilişkin,detaylı hata mesajı (Örneğin: Kartın limiti /bakiyesi yetersiz).  
1 | Kimlik Doğrulama yapılmadı. Lütfen tekrar deneyin ve işlemi tamamlayın. | Müşteri, kimlik doğrulama adımında cep telefonu numarasını girmedi.  
2 | Kimlik Doğrulama başarısız. Lütfen tekrar deneyin ve şifreyi doğru girin. | Müşteri, cep telefonuna gelen şifreyi doğru girmedi.  
3 | Güvenlik kontrolü sonrası onay verilmedi veya kontrol yapılamadı. | Müşterinin işlemi PayTR tarafından güvenlik kontrolünden geçemedi veya kontrol yapılamadı.  
6 | Müşteri ödeme yapmaktan vazgeçti ve ödeme sayfasından ayrıldı. | Müşteri, kendisine tanınmış olan işlem süresinde(1. ADIM’da tanımlanan request_exp_date değeri) işlemini tamamlamadı veya müşteri ödeme sayfasını kapatarak işlemi sonlandırdı.  
8 | Bu karta taksit yapılamamaktadır. | Müşterinin kullanmakta olduğu kart ile seçmiş olduğu taksitli ödeme yöntemi kullanılamaz.  
9 | Bu kart ile işlem yetkisi bulunmamaktadır. | Müşterinin kullanmakta olduğu kart için mağazanızın işlem yetkisi bulunmuyor.  
10 | Bu işlemde 3D Secure kullanılmalıdır. | Müşteri, yapmış olduğu işlemde 3D Secure ile ödeme yapmalıdır.  
11 | Güvenlik uyarısı. İşlem yapan müşterinizi kontrol edin. | Müşterinin işleminde fraud tespiti bulunuyor. Güvenliğiniz için müşterinin işlemlerini kontrol edin.  
99 | İşlem başarısız: Teknik entegrasyon hatası. | Teknik entegrasyon hatası varsa dönülecektir. (debug_on değeri 0 ise)  
  
  
  


**İADE API SERVİSİ ÜZERİNDEN DÖNÜLEN HATA KODLARI VE AÇIKLAMALARI**

err_no | err_msg | Açıklama  
---|---|---  
000 | iade yapilamiyor, daha sonra tekrar deneyin | Ödeme çıkışı esnasında iade servisinin kilitlenmesi durumunda yaşanmaktadır. Bir süre sonra tekrar deneyebilirsiniz.  
001 | Gecersiz istek veya magaza aktif degil | İstekte merchant_id bilgisinin iletilmemesi veya mağazanın aktif olmaması durumunda dönülmektedir.  
002 | Gecersiz merchant_oid | İstekte merchant_oid alanını iletmemeniz durumunda dönülmektedir.  
003 | Gecersiz return_amount | İstekte return_amount alanını iletmemeniz durumunda dönülmektedir.  
004 | paytr_token gonderilmedi veya gecersiz | paytr_token alanının iletilmemesi veya doğru olmaması durumunda dönülmektedir.  
005 | merchant_oid ile basarili odeme bulunamadi | İlettiğiniz sipariş numarası ile başarılı bir ödemenin olmadığı durumda dönülmektedir.  
007 | merchant_oid bulundu ancak odeme henuz siteye bildirilmemis | İlettiğiniz sipariş numarasının bildirim akışının tamamlanmadığını belirtmektedir.  
008 | XYZ odeme tipi iade desteklemiyor | İlettiğiniz ödeme tipi ile iade işlemi yapılmamaktadır.  
009 | Toplam iade tutari odeme tutarindan fazla olamaz | İlettiğiniz iade tutarı işleme ait kalan tutardan fazla olması durumunda dönülmektedir.  
010 | Net bakiyeniz yetersiz | Hesabınızda iade etmek istediğiniz tutar kadar bakiye bulunmaması durumunda döndülmektedir.  
011 | Bir yildan eski islemler icin iade islemi yapilamaz. | Bir yıldan önceki bir işlem için iade işlemi denemeniz durumunda dönülmektedir.  
  
  
  


**DURUM SORGU SERVİSİ ÜZERİNDEN DÖNÜLEN HATA KODLARI VE AÇIKLAMALARI**

err_no | err_msg | Açıklama  
---|---|---  
001 | Gecersiz istek veya magaza aktif degil | İstekte merchant_id bilgisinin iletilmemesi veya mağazanın aktif olmaması durumunda dönülmektedir.  
002 | Gecersiz merchant_oid | İstekte merchant_oid alanını iletmemeniz durumunda dönülmektedir.  
003 | paytr_token gonderilmedi veya gecersiz | paytr_token alanının iletilmemesi veya doğru olmaması durumunda dönülmektedir.  
004 | merchant_oid ile islem bulunamadi | İlettiğiniz sipariş numarasına ait bir işlem bulunamaması durumunda dönülmektedir.  
004 | merchant_oid ile basarili odeme bulunamadi | İlettiğiniz sipariş numarası ile başarılı bir ödemenin olmadığı durumda dönülmektedir.  
  
**PLATFORM TRANSFER TALEBİ SERVİSLERİ ÜZERİNDEN DÖNÜLEN HATA KODLARI VE AÇIKLAMALARI**

err_no | err_msg | Açıklama  
---|---|---  
001 | Gecersiz istek veya magaza aktif degil | İstekte merchant_id bilgisinin iletilmemesi veya mağazanın aktif olmaması durumunda dönülmektedir.  
002 | Bu servis icin yetkiniz yok | Mağazanız türünüz pazaryeri olmaması durumunda bu hata dönülmektedir.  
003 | Gecersiz trans_id | trans_id değeri gönderilmemesi durumunda bu hata yanıtı dönülmektedir.  
004 | paytr_token gonderilmedi veya gecersiz | paytr_token alanının iletilmemesi veya doğru olmaması durumunda dönülmektedir.  
005 | Gecersiz merchant_oid | İstekte merchant_oid alanını iletmemeniz durumunda dönülmektedir.  
006 | merchant_oid ile basarili odeme bulunamadi | İlettiğiniz sipariş numarası ile başarılı bir ödemenin olmadığı durumda dönülmektedir.  
007 | merchant_oid bulundu ancak odeme henuz siteye bildirilmemis | İlettiğiniz sipariş numarasının bildirim akışının tamamlanmadığını belirtmektedir.  
008 | valor tarihi gecmeden transfer yapilamaz, (valör tarihi) sonrasi tekrar deneyin | İşlem için geçerli olan valör tarihinizden önce istekte bulunmanız durumunda dönülmektedir.  
009 | trans_id benzersiz olmalidir, bu trans_id daha once kullanilmis. | Daha önce iletilen bir trans_id değeri iletmeniz durumunda dönülmektedir.  
010 | toplam transfer tutari, kalan tutardan fazla olamaz. | İletmiş olduğunuz transfer tutarı işlem için kalan tutardan fazla olması durumunda dönülmektedir.  
012 | platform komisyonu sifirdan az olamaz | Yapmış olduğunuz istekte PayTR komisyonu kadar tutar kalmaması durumunda dönülmektedir.  
091 | transfer_iban degeri IBAN dogrulamasindan gecemedi, lutfen kontrol edin. | Geçerli bir IBAN numarası girmemeniz durumunda dönülmektedir.  
092 | transfer_iban TR ile baslamalidir, bosluk veya '-' icermemeli ve 26 hane olmalidir, lutfen kontrol edin. | IBAN alanı doğru formatta iletilmemesi nedeniyle dönülmektedir.  
095 | submerchant_amount sifirdan kucuk olamaz. | Alt satıcınıza aktaracağınız tutar 0 dan küçük gönderilmesi nedeniyle dönülmektedir.  
096 | trans_id alfanumerik olmalidir, ozel karakter iceremez | İletilen trans_id alanının alfa numerik olmaması nedeniyle dönülmektedir.  
097 | transfer_iban zorunludur, lutfen kontrol edin | transfer_iban alanının iletilmemesi durumunda dönülmektedir.  
098 | transfer_name zorunludur, lutfen kontrol edin | transfer_name alanının iletilmemesi durumunda dönülmektedir.  
099 | total_amount sifirdan buyuk ve sayisal olmalidir | total_amount alanının doğru formatta iletilmemesi veya 0'dan küçük iletilmesi durumunda dönülmektedir.  
100 | transfer_name icerisinde ad ve soyad arasinda bosluk olmalidir | transfer_name alanının doğru formatta iletilmemesi durumunda dönülmektedir.  
101 | transfer_name icerisinde ad ve soyad en az 2 karakter olmalidir | transfer_name alanının doğru formatta iletilmemesi durumunda dönülmektedir.  
201 | paytr_token gonderilmedi veya gecersiz | paytr_token alanının iletilmemesi veya doğru olmaması durumunda dönülmektedir.  
202 | trans_id alfanumerik olmalidir, ozel karakter iceremez | İletilen trans_id alanının alfa numerik olmaması nedeniyle dönülmektedir.  
203 | trans_id benzersiz olmalidir, bu trans_id daha once kullanilmis. | Daha önce iletilen bir trans_id değeri iletmeniz durumunda dönülmektedir.  
204 | trans_info izin verilenden uzun, daha az kayit ile tekrar deneyin | trans_info alanında beklenenden fazla kayıt iletilmesi durumunda dönülmektedir.  
205 | trans_info en az 2 islem en fazla 2000 islem icermelidir | trans_info alanında beklenenden fazla veya az kayıt iletilmesi durumunda dönülmektedir.  
206 | trans_info gecerli bir JSON string degil | trans_info alanı beklenen formatta iletilmemesi durumunda dönülmektedir.  
301 | paytr_token gonderilmedi veya gecersiz | paytr_token alanının iletilmemesi veya doğru olmaması durumunda dönülmektedir.  
302 | trans_id alfanumerik olmalidir, ozel karakter iceremez | İletilen trans_id alanının alfa numerik olmaması nedeniyle dönülmektedir.  
303 | trans_id benzersiz olmalidir, bu trans_id daha once kullanilmis. | Daha önce iletilen bir trans_id değeri iletmeniz durumunda dönülmektedir.  
305 | merchant_oids en az X islem, en fazla Y islem icermelidir" | İletilen değer merchant_oids alanının alabileceği değerler olmaması durumunda dönülmektedir.  
306 | merchant_oids gecerli bir JSON string degil | merchant_oids alanı beklenen formatta iletilmemesi durumunda dönülmektedir.  
BLK | merchant_oid numarali islemde bloke mevcut, detayli bilgi icin bize ulasin | İletilen sipariş numarasında bloke olması durumunda dönülmektedir.


---

# BKM Express Entegrasyonu | PayTR


# BKM Express Entegrasyonu

BKM Express servisi aracılığıyla, BKM Express sisteminde kayıtlı kartlar aracılığıyla ödeme alabilirsiniz.

BKM Express Entegrasyonu iFrame ödeme yönteminde otomatik olarak ödeme ekranına gelmektedir. Ancak Direkt API çözümünde BKM Express entegrasyonu yaparken $payment_type = "bex" olarak gönderilmesi gerekmektedir. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza no  
merchant_key | Mağaza parola  
merchant_salt | Mağaza gizli anahtar  
merchant_oid | Sipariş numarası  
payment_amount | Siparişe ait toplam Tutar  
user_ip | Kullanıcıdan alınan ip adresi  
email | Kullanıcının email adresi  
payment_type | Bkm Express için bex olarak gönderilmesi gereklidir.  
installment_options | Taksit seçenekleri opsiyoneldir. Göndermediğiniz takdirde müşterinize taksit seçenekleri gösterilmeyecektir. Aşağıda verilen değerler örnektir. Siz komisyon oranlarınıza göre tutarları hesaplayıp aşağıdaki kısmı düzenlemelisiniz.  
  
  


**BKM Express Test Kullanıcı Bilgileri**

Kullanıcı bilgisi | Banka  
---|---  
0010@banka.com | ZİRAAT BANKASI  
0012@banka.com | HALK BANKASI  
0015@banka.com | VAKIFBANK  
0032@banka.com | TEB  
0046@banka.com | AKBANK  
0062@banka.com | GARANTİ  
0064@banka.com | İŞBANK  
0067@banka.com | YAPI KREDİ  
0134@banka.com | DENİZBANK  
0111@banka.com,qnbfinans@bkm.com | FİNANSBANK  
  
  
Tüm kullanıcıların şifreleri 147258'dir.

Bkm Express örnek kodları:

  * PHP


    
    
    <?php
    
    $merchant_id = '';
    $merchant_key = '';
    $merchant_salt = '';
    
    $user_basket = htmlentities(json_encode(array(
        array("Örnek ürün 1", "18.00", 1),
        array("Örnek ürün 2", "33.25", 2),
        array("Örnek ürün 3", "45.42", 1)
    )));
    
    $merchant_oid = $_POST['merchant_oid'];
    
    $test_mode = 1;
    
    if (isset($_SERVER["HTTP_CLIENT_IP"])) {
        $ip = $_SERVER["HTTP_CLIENT_IP"];
    } elseif (isset($_SERVER["HTTP_X_FORWARDED_FOR"])) {
        $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
    } else {
        $ip = $_SERVER["REMOTE_ADDR"];
    }
    $user_ip = $ip;
    
    $email = "testbex@siteniz.com";
    $payment_amount = "15.20";
    
    $installment_count = 0;
    
    $payment_type = "bex";
    
    /* Taksit seçenekleri opsiyoneldir. Göndermediğiniz takdirde müşterinize taksit seçenekleri gösterilmeyecektir. */
    /* Aşağıda verilen değerler örnektir! Siz komisyon oranlarınıza göre tutarları hesaplayıp aşağıdaki kısmı düzenlemelisiniz. */
    /* DİKKAT: Oluşturacağınız JSON tek satır olması ve arasında herhangi bir enter, vb. olmaması gerekmektedir. */
    
    $installment_options = '{"advantage":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"axess":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"bonus":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"combo":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"cardfinans":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"maximum":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"paraf":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"world":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8}}';
    
    $hash_str = $merchant_id . $user_ip . $merchant_oid . $email . $payment_amount . $payment_type . $installment_count . $test_mode . $installment_options;
    $token = base64_encode(hash_hmac('sha256', $hash_str . $merchant_salt, $merchant_key, true));
    
    $post = [
        'merchant_id' => $merchant_id,
        'user_ip' => $user_ip,
        'merchant_oid' => $merchant_oid,
        'email' => $email,
        'payment_type' => $payment_type,
        'payment_amount' => $payment_amount,
        'installment_count' => $installment_count,
        'test_mode' => $test_mode,
        'user_name' => "TEST NAME",
        'user_address' => "USER TEST ADDRESS",
        'user_phone' => "05555555555",
        'user_basket' => $user_basket,
        'debug_on' => 1,
        'paytr_token' => $token,
        'installment_options' => $installment_options
    ];
    
    $ch = curl_init('https://www.paytr.com/odeme');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
    curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 90);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
    //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
    //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
    $response = @curl_exec($ch);
    
    if (curl_errno($ch)) {
        echo curl_error($ch);
        curl_close($ch);
        exit;
    }
    
    curl_close($ch);
    
    exit($response);
    ?>

BKM Express örnek kodları [**indirmek için tıklayın.**](/bkm-express/PayTR BKM Express Örnek.zip)


---

# Satış ve İade İşlem Dökümü Servisi | PayTR


# Satış ve İade İşlem Dökümü Servisi

Bu servisi ile iletilen tarih aralığındaki (en fazla 3 gün) yapılan satış ve iade işlemlerinin dökümünü alabilirsiniz.

1- İşlem detaylarını gerçek istediğiniz tarih / saat ve aşağıdaki tabloda belirtilen diğer bilgileri https://www.paytr.com/rapor/islem-dokumu adresine POST metodu ile gönderin. 

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
start_date(string) | Başlangıç Tarihi Formatı: 2021-01-01 00:00:00 (YYYY-MM-DD hh:mm:ss) | Evet | -  
end_date | Bitiş Tarihi Formatı: 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss) | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
start_date (integer) | Başlangıç Tarihi Formatı: 2021-01-01 00:00:00 (YYYY-MM-DD hh:mm:ss) | Evet | -  
end_date(integer) | Bitiş Tarihi Formatı: 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss) | Evet | -  
dummy(int) | Demo Veri: Servisten dönen verileri simule etmek için kullanılır. Dönen değerler gerçek değildir, test amaçlı gözlem içindir. | Hayır | 0 veya 1  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


2- Yaptığınız bu isteğe cevap JSON formatında döner. a. Verilen tarih aralığında eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner. b. Verilen tarih aralığında eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner. c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.

Status success durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır. Satış ve İade işlemlerinde fark olmaksızın aynı değerler döner.

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
İşlem Tipi: Yapılan işlemin tipi. | islem_tipi (string) | S (satış) veya I (iade)  
Net Tutar: Kesinti sonrası kalan tutar. | net_tutar (string) | Örn. 9.76  
Kesinti Tutarı: İşlem için kesilen tutar. | kesinti_tutari (string) | Örn. 0.24  
Kesinti Oranı: İşlem için kesilen oran. | kesinti_orani (string) | Örn. 2.35  
İşlem Tutarı: Yapılan işlemin tutarı. | islem_tutari (string) | Örn. 10.00  
Ödeme Tutarı: İşlem tutarı üzerinde bir ödeme olması durumunda dönülür. | odeme_tutari (string) | Örn. 10.00  
İşlem Tarihi: İşlemin yapıldığı tarih. | islem_tarihi (string) | Örn. 13.01.2021  
Para Birimi: İşlemin para birimi. | para_birimi (string) | TL, USD, EUR, GBP, RUB  
Taksit: İşlem taksitli yapıldı ise taksit sayısı. | taksit (string) | 0,2,3,4,5,6,7,8,9,10,11,12  
Kart Markası: İşlem yapılan kartın markası. | kart_marka (string) | Örn. WORD, BONUS, vb.  
Kart No: İşlem yapılan maskeli kart numarası. | kart_no (string) | Örn. 455359AAA6747  
Sipariş Numarası: İşlemin sipariş numarası. | siparis_no (string) | Örn. ABC123  
Ödeme Tipi: Ödemenin hangi tipte yapıldığı. | odeme_tipi (string) | KART veya EFT  
  
  


  * PHP
  * Python
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXXYYYYYY';
        $merchant_salt  = 'YYYYYYXXXXXX';
    
        ## Gerekli Bilgiler
        #
        $start_date = "2020-06-02 00:00:00";
        $end_date = "2020-06-04 23:59:59";
        # Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $start_date . $end_date . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'start_date' => $start_date,
            'end_date' => $end_date,
            'paytr_token' => $paytr_token
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/rapor/islem-dokumu");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        $result = json_decode($result, 1);
    
        if ($result['status'] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result['status'] == 'failed')
        {
            // sonuç bulunamadı
            echo "ilgili tarih araliginda islem bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result['err_no'] . " - " . $result['err_msg'];
        }
    
    
    # Python 3.6+
    # İşlem dökümü servisi için kullanılacak örnek kod
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXX'
    merchant_salt = 'XXXXXX'
    
    # Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
    start_date = '2021-02-02 00:00:00'
    end_date = '2021-02-04 23:59:59'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + start_date + end_date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'start_date': start_date,
        'end_date': end_date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/rapor/islem-dokumu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(result.text)
    elif res['status'] == 'failed':
        print('ilgili tarih araliginda islem bulunamadi')
    else:
        print('PAYTR BIN detail request error. Error: ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    using System.Web.Routing;
    
    namespace WebApplication1.Controllers
    {
        public class TransactionDetailController : Controller
        {
            public ActionResult TransactionDetail()
            {
                // ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                string start_date = "2021-01-13 00:00:00";
                string end_date = "2021-01-13 23:59:59";
                // Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
                //
                //   ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
                string Birlestir = string.Concat(merchant_id, start_date, end_date, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
                //
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["start_date"] = start_date;
                data["end_date"] = end_date;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/rapor/islem-dokumu", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
                        // VT işlemleri vs.
                        Response.Write(json);
    
                    }
                    else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("No transaction was found in date duration");
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
                return View();
            }
        }
    }
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    //API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_id = '';
    var merchant_key = '';
    var merchant_salt = '';
    
    app.get("/", function (req, res) {
    
        //Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
        var start_date = '2020-05-01 00:00:00';
        var end_date = '2020-05-01 23:59:59';
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/rapor/islem-dokumu',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'start_date': start_date,
                'end_date': end_date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

İşlem Dökümü Servisi örnek kodlarını [**indirmek için tıklayın.**](/islem-dokumu/paytr_islem_dokumu.zip)


---

# Ödeme Rapor Servisi | PayTR


# Ödeme Rapor Servisi

**Ödeme Özet Servisi**

Bu servis ile iletilen tarih aralığında mağaza hesabına aktarılan ve aktarılacak olan tutarlara ait ödeme özetine ulaşabilirsiniz.

Ödeme özet servisi sayfasına bu [**linkten**](https://dev.paytr.com/odeme-rapor-servisi/odeme-ozeti) gidebilirsiniz.  


**Ödeme Detay Servisi**

Bu servis ile iletilen tarihte yapılan satış işlemlerine ait transfer dökümünü alabilirsiniz. 

Ödeme detay servisi sayfasına bu [**linkten**](https://dev.paytr.com/odeme-rapor-servisi/odeme-detayi) gidebilirsiniz.  



---

# Ödeme Detay Servisi | PayTR


# Ödeme Detay Servisi

Ödeme detay servisi aracılığıyla, iletilen tarihte yapılan satış işlemlerine ait transfer detayı alabilirsiniz.

Mağaza Ödeme Detay ve Pazaryeri Ödeme Detay olarak iki kategoriye ayrılır. 

**Mağaza Ödeme Detay**  


1- Aşağıdaki tabloda belirtilen bilgileri https://www.paytr.com/rapor/odeme-detayi adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
date | Ödeme Detayı İstenen Tarih Formatı: 2022-01-01 (YYYY-MM-DD)  
paytr_token | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
**Mağaza Ödeme Detay**  
Tablodan gelen değerler tarihe göre işlemler sorgulanır. İlgili tarihte yapılan satış işlemlerine ait transfer bilgileri servisten döner.

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Verilen tarihte eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner.   
b. Verilen tarihte eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner.   
c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.  
Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Alan Adı/tipi | Açıklamalar | Değerler  
---|---|---  
merchant_oid | Mağaza sipariş no | Örn. ABC123  
merchant_iban | Mağaza IBAN no | Örn. TR000000000000000000000000000  
merchant_name | Mağaza isim bilgisi | Örn. Test Firma  
payment | İşleme ait tutar | Örn. 18  
currency | İşlemin para birimi | Örn. TL  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    $merchant_id    = 'XXXXX';
        $merchant_key   = 'YYYYYYYYYYYYY';
        $merchant_salt  = 'YYYYYYYYYYYYY';
    
        ## Gerekli Bilgiler
        #
        //$date     = "2022-02-07";
        $date     = "2021-07-01";
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $date . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'date' => $date,
            'paytr_token' => $paytr_token
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/rapor/odeme-detayi/");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        $result = @curl_exec($ch);
        //print_r($result);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        echo "<pre>";
        $result = json_decode($result, 1);
    
        if ($result['status'] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result['status'] == 'failed')
        {
           // sonuç bulunamadı
            echo "ilgili tarihte odeme detayi bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result['err_no'] . " - " . $result['err_msg'];
        }
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    merchant_id = 'XXXXXX'
    merchant_key = 'XXXXXX'
    merchant_salt = 'XXXXXX'
    
    date = '2021-07-01'
    
    hash_str = merchant_id + date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'date': date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/rapor/odeme-detayi', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(result.text)
    elif res['status'] == 'failed':
        print('ilgili tarihte odeme detayi bulunamadi')
    else:
        print('Error: ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    using System.Web.Routing;
    
    namespace WebApplication1.Controllers
    {
        public class TransactionDetailController : Controller
        {
            public ActionResult TransactionDetail()
            {
                // ########################### İŞLEM DETAY ALMAK  İÇİN ÖRNEK KODLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                string date = "2022-02-07";
    
                //
                //   ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
                string Birlestir = string.Concat(merchant_id, date, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
                //
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["date"] = date;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/rapor/odeme-detayi", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
                        // VT işlemleri vs.
                        Response.Write(json);
    
                    }
                    else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("ilgili tarihte odeme detayi bulunamadi");
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
                return View();
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    //API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_id = '';
    var merchant_key = '';
    var merchant_salt = '';
    
    app.get("/", function (req, res) {
    
        var date = '2022-02-07';
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/rapor/odeme-detayi',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'date': date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Mağaza ödeme detay örnek kodları[**indirmek için tıklayın.**](/odeme-rapor-servisi/odeme-detayi/PayTR_Payment_Detail_Service.zip)

**Pazaryeri Ödeme Detay**  


1- Aşağıdaki tabloda belirtilen bilgileri https://www.paytr.com/rapor/odeme-detayi adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
date | Ödeme detay alınmak istenen tarih  
paytr_token | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  


Tablodan gelen değerler tarihe göre işlemler sorgulanır. İlgili tarihte yapılan satış işlemlerine ait transfer bilgileri servisten döner.

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Verilen tarihte eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner.   
b. Verilen tarihte eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner.   
c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.  
Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Alan Adı/tipi | Açıklamalar | Değerler  
---|---|---  
merchant_oid | Mağaza sipariş no | Örn. ABC123  
merchant_iban | Mağaza IBAN no | Örn. TR000000000000000000000000000  
merchant_name | Mağaza isim bilgisi | Örn. Test Firma  
payment | İşleme ait tutar | Örn. 18  
currency | İşlemin para birimi | Örn. TL  
amount | Alt satıcıya aktarılan tutar | Örn. 140  
transfer | Alt satıcı transfer hesap bilgisi | Örn. TR111111111111111111111, TEST SATICI  
currency | İşlemin para birimi | Örn. TL  
  
  


_**Gelen tutar ve aktarılan tutarlar günlük olarak görünmektedir.**_

Ödeme detay örnek kodları: Örnek kodlar içinde nasıl yapılacağı detaylı olarak anlatılmaktadır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    $merchant_id    = 'XXXXX';
        $merchant_key   = 'YYYYYYYYYYYYY';
        $merchant_salt  = 'YYYYYYYYYYYYY';
    
        ## Gerekli Bilgiler
        #
        //$date     = "2022-02-07";
        $date     = "2021-07-01";
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $date . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'date' => $date,
            'paytr_token' => $paytr_token
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/rapor/odeme-detayi/");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        $result = @curl_exec($ch);
        //print_r($result);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        echo "<pre>";
        $result = json_decode($result, 1);
    
        if ($result[status] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result[status] == 'failed')
        {
           // sonuç bulunamadı
            echo "ilgili tarihte odeme detayi bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result[err_no] . " - " . $result[err_msg];
        }
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    merchant_id = 'XXXXXX'
    merchant_key = 'XXXXXX'
    merchant_salt = 'XXXXXX'
    
    date = '2021-07-01'
    
    hash_str = merchant_id + date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'date': date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/rapor/odeme-detayi', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(result.text)
    elif res['status'] == 'failed':
        print('ilgili tarihte odeme detayi bulunamadi')
    else:
        print('Error: ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    using System.Web.Routing;
    
    namespace WebApplication1.Controllers
    {
        public class TransactionDetailController : Controller
        {
            public ActionResult TransactionDetail()
            {
                // ########################### İŞLEM DETAY ALMAK  İÇİN ÖRNEK KODLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                string date = "2022-02-07";
    
                //
                //   ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
                string Birlestir = string.Concat(merchant_id, date, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
                //
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["date"] = date;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/rapor/odeme-detayi", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
                        // VT işlemleri vs.
                        Response.Write(json);
    
                    }
                    else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("ilgili tarihte odeme detayi bulunamadi");
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
                return View();
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    //API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_id = '';
    var merchant_key = '';
    var merchant_salt = '';
    
    app.get("/", function (req, res) {
    
        var date = '2022-02-07';
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/rapor/odeme-detayi',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'date': date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Pazaryeri ödeme detay örnek kodları[**indirmek için tıklayın.**](/odeme-rapor-servisi/odeme-detayi/PayTR_Marketplace_Payment_Detail_Service.zip)


---

# Ödeme Özeti | PayTR


# Ödeme Özeti

Mağaza Ödeme Özeti ve Pazaryeri Ödeme Özeti olarak iki kategoriye ayrılır. 

**Mağaza Ödeme Özeti**  


Ödeme özeti servisi aracılığıyla, iletilen tarih aralığında mağaza hesabına aktarılan ve aktarılacak olan tutarlara ait ödeme özetine ulaşabilirsiniz. 

1- Aşağıdaki tabloda belirtilen bilgileri https://www.paytr.com/rapor/odeme-dokumu adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
start_date | Başlangıç Tarihi Formatı: 2022-01-01 (YYYY-MM-DD)  
end_date | Bitiş Tarihi Formatı: 2022-01-01 (YYYY-MM-DD)  
paytr_token | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  


Tablodan gelen değerler tarih aralığına göre sorgulanır. Tarihe göre hesaba aktarılan ve hesaba aktarılacak olan satış,iade ve net tutar bilgileri servisten döner. 

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Verilen tarihte eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner.   
b. Verilen tarihte eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner.   
c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.  
Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Alan Adı/tipi | Açıklamalar | Değerler  
---|---|---  
date_paid | Ödeme tarihi | Örn. 2022-02-07  
currency | Aktarılan tutarın para birimi | Örn. TL  
sales | Toplam satış tutarı | Örn. 950.95  
return | Toplam iade tutarı | Örn. 12.64  
net | Aktarılan net tutar | Örn. 938.31  
merchant_iban | Mağaza IBAN no | Örn. TR000000000000000000000000000  
TL | Hesaba aktarılacak tutarın para birimi | Örn. TL,USD  
  
Gelecek ödemelerinizi içeren data bloğunu, future_payments ismiyle ele alabilirsiniz. future_payments icerisinde, aşağıda belirtilmiş olan alanlara ek olarak; tarih ve döviz cinsi değerlerine ulaşabilirsiniz.

Alan Adı/tipi | Açıklamalar | Değerler  
---|---|---  
net_amounts | Net tutarı | 500  
sale_amounts | Satış tutarı | 500  
return_amounts | İade tutarı | 150  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    ########################### ÖDEME RAPOR SERVİSİ - ÖZET ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXX';
        $merchant_salt  = 'XXXXXX';
    
        ## Gerekli Bilgiler
        #
        $start_date     = "2022-09-01";
        $end_date       = "2022-09-31";
        # Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $start_date . $end_date . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'start_date' => $start_date,
            'end_date' => $end_date,
            'paytr_token' => $paytr_token
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/rapor/odeme-dokumu/");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        $result = @curl_exec($ch);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        echo "<pre>";
        $result = json_decode($result, 1);
    
        if ($result['status'] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result['status'] == 'failed')
        {
            // sonuç bulunamadı
            echo "ilgili tarih araliginda odeme ozeti bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result['err_no'] . " - " . $result['err_msg'];
        }
    
    
    
    # Python 3.6+
    # ÖDEME RAPOR SERVİSİ - ÖZET ALMAK  İÇİN ÖRNEK KODLAR
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = 'XXXXXX'
    merchant_salt = 'XXXXXX'
    
    start_date = '2022-09-01'
    end_date = '2022-09-31'
    #Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + start_date + end_date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'start_date': start_date,
        'end_date': end_date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/rapor/odeme-dokumu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(result.text)
    elif res['status'] == 'failed':
        print('ilgili tariht aralıgında odeme ozeti bulunamadi')
    else:
        print('Error: ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    using System.Web.Routing;
    
    namespace WebApplication1.Controllers
    {
        public class TransactionDetailController : Controller
        {
            public ActionResult TransactionDetail()
            {
                // ########################### ÖDEME RAPOR SERVİSİ - ÖZET ALMAK  İÇİN ÖRNEK KODLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                string start_date = "2022-09-01";
                string end_date = "2022-09-31";
                // Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
                //
                //   ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
                string Birlestir = string.Concat(merchant_id, start_date, end_date, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
                //
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["start_date"] = start_date;
                data["end_date"] = end_date;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/rapor/odeme-dokumu", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
    
                        Response.Write(json);
    
                    }
                    else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("ilgili tarih araliginde odeme ozeti bulunamadi");
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
                return View();
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = '';
    var merchant_key = '';
    var merchant_salt = '';
    
    app.get("/", function (req, res) {
    
        var start_date = '2022-09-01';
        var end_date = '2022-09-31';
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/rapor/odeme-dokumu',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'start_date': start_date,
                'end_date': end_date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Mağaza ödeme özeti örnek kodları[**indirmek için tıklayın.**](/odeme-rapor-servisi/odeme-ozeti/PayTR_Payment_Statement_Service.zip)

**Pazaryeri Ödeme Özeti**  


Ödeme özeti servisi aracılığıyla, iletilen tarih aralığında mağaza hesabına aktarılan tutarlara ait ödeme özetine ulaşabilirsiniz. 

1- Aşağıdaki tabloda belirtilen bilgileri https://www.paytr.com/rapor/odeme-dokumu adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
start_date | Başlangıç Tarihi Formatı: 2022-01-01 (YYYY-MM-DD)  
end_date | Bitiş Tarihi Formatı: 2022-01-01 (YYYY-MM-DD)  
paytr_token | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  


Tablodan gelen değerler tarih aralığına göre sorgulanır. Tarihe göre hesaba aktarılan satış,iade ve net tutar bilgileri servisten döner. 

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Verilen tarihte eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner.   
b. Verilen tarihte eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner.   
c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.  
Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Alan Adı/tipi | Açıklamalar | Değerler  
---|---|---  
date_paid | Ödeme tarihi | Örn. 2022-02-07  
currency | Aktarılan tutarın para birimi | Örn. TL  
sales | Toplam satış tutarı | Örn. 950.95  
return | Toplam iade tutarı | Örn. 12.64  
net | Aktarılan net tutar | Örn. 938.31  
merchant_iban | Mağaza IBAN no | Örn. TR000000000000000000000000000  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    ########################### ÖDEME RAPOR SERVİSİ - ÖZET ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXX';
        $merchant_salt  = 'XXXXXX';
    
        ## Gerekli Bilgiler
        #
        $start_date     = "2022-09-01";
        $end_date       = "2022-09-31";
        # Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $start_date . $end_date . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'start_date' => $start_date,
            'end_date' => $end_date,
            'paytr_token' => $paytr_token
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/rapor/odeme-dokumu/");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        $result = @curl_exec($ch);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        echo "<pre>";
        $result = json_decode($result, 1);
    
        if ($result[status] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result[status] == 'failed')
        {
            // sonuç bulunamadı
            echo "ilgili tarih araliginda odeme ozeti bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result[err_no] . " - " . $result[err_msg];
        }
    
    
    
    # Python 3.6+
    # ÖDEME RAPOR SERVİSİ - ÖZET ALMAK  İÇİN ÖRNEK KODLAR
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = 'XXXXXX'
    merchant_salt = 'XXXXXX'
    
    start_date = '2022-09-01'
    end_date = '2022-09-31'
    #Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + start_date + end_date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'start_date': start_date,
        'end_date': end_date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/rapor/odeme-dokumu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(result.text)
    elif res['status'] == 'failed':
        print('ilgili tariht aralıgında odeme ozeti bulunamadi')
    else:
        print('Error: ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json.Linq;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using System.Web.Mvc;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    using System.Web.Routing;
    
    namespace WebApplication1.Controllers
    {
        public class TransactionDetailController : Controller
        {
            public ActionResult TransactionDetail()
            {
                // ########################### ÖDEME RAPOR SERVİSİ - ÖZET ALMAK  İÇİN ÖRNEK KODLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                string start_date = "2022-09-01";
                string end_date = "2022-09-31";
                // Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
                //
                //   ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
                string Birlestir = string.Concat(merchant_id, start_date, end_date, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
                //
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["start_date"] = start_date;
                data["end_date"] = end_date;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/rapor/odeme-dokumu", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
    
                        Response.Write(json);
    
                    }
                    else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("ilgili tarih araliginde odeme ozeti bulunamadi");
    
                    }
                    else
                    {
                        // Hata durumu
                        Response.Write(json.err_no + "-" + json.err_msg);
                    }
                }
                return View();
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = '';
    var merchant_key = '';
    var merchant_salt = '';
    
    app.get("/", function (req, res) {
    
        var start_date = '2022-09-01';
        var end_date = '2022-09-31';
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/rapor/odeme-dokumu',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'start_date': start_date,
                'end_date': end_date,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Pazaryeri ödeme özeti örnek kodları[**indirmek için tıklayın.**](/odeme-rapor-servisi/odeme-ozeti/PayTR_Marketplace_Payment_Statement_Service.zip)


---

# Hazır Altyapılar | PayTR


# Hazır Altyapılar

* * *

![1](/user/pages/15.hazir-altyapi/1.png)  
Akakçe, tüketiciyi doğru ürün, doğru satıcı ve doğru fiyatla buluşturan bir alışveriş platformudur. ODTÜ Teknokent'te kurulduğu 2000 yılından bu yana alışverişçilere en ucuz fiyatları sunan Akakçe, Türkiye'de hızla büyüyen e-ticaret sektörünün referans merkezi olarak çalışıyor.   


* * *

![2](/user/pages/15.hazir-altyapi/2.png)  
Akıllı Ticaret, 2005 yılından bu yana kobiler için 360 derece e-ticaret çözümleri üretmektedir. Akıllı Ticaret e-ticaretin öne çıkan tüm aktörleri için çalışma yapmakta, e-ticaret sitesinden pazaryerlerine, onlarca muhasebe entegrasyonundan kargo entegrasyonlarına bir çok dalda entegrasyonları kendi bünyesinde tamamlamış ve müşterilerine kurulum, uyarlama ve destek hizmetlerini bizzat kendi bünyesinde vermektedir.  


* * *

![3](/user/pages/15.hazir-altyapi/3.png)  
Akınsoft yeni Nesil E-Ticaret çözümü ile, E-Ticaret sitenizi kolayca oluşturma ve satışa sunma imkanı sağlamaktadır. İşletmenizin küçük ya da büyük olması, teknolojiye yakın veya uzak olmanız ya da E-Ticaret yapmanıza engel gördüğünüz diğer faktörler gözünüzde büyümesin. AKINSOFT Yeni Nesil E-Ticaret ile, E-Ticaret sitenizi kolayca oluşturabilir ve satışa başlayabilirsiniz.  


* * *

![3](/user/pages/15.hazir-altyapi/62.png)  
Özel veya Hazır SEO altyapılı web sayfaları sunan, Yurtiçi ve Yurtdışı pazarlarda faaliyet gösteren yazılım şirketidir. Paytr Modül entegrasyonları, ve Web Yazılım alanında hizmet vermektedir.  


* * *

![61](/user/pages/15.hazir-altyapi/61.png)  
BilgiKurumsal, 2008 yılında kurulan BO Interactive'in marka haklarının Borusan Holding'e satışının gerçekleşmesinin ardından İstanbul'da kurulmuştur. Kobilerin dijitalleşmelerini sağlayan e-ticaret altyapı sağlayıcısıdır.  


* * *

![5](/user/pages/15.hazir-altyapi/5.png)  
BgrSoft, ağırlıklı olarak e-ticaret yazılımları, özel e-ticaret çözümleri ve tasarım hizmetleri vermek üzere kurulmuştur. BgrSoft, güçlü altyapısı ve 5 yılı aşkın tecrübesi ve uzman personel kadrosu ile müşterilerinin e-ticaret alanındaki rekabetlerini güçlendirmesine yardım etmektedir.  


* * *

![6](/user/pages/15.hazir-altyapi/6.png)  
Bonobo, işinizi geliştirmek için uçtan uca bir çözüm sunmaktadır.  


* * *

![7](/user/pages/15.hazir-altyapi/7.png)  
Epsilos, güncel mimariye sahip kaliteli ve esnek e ticaret yazılımı sunmaktadır. Epsilos ile sektörlere özel, yeni nesil e ticaret sitesine sahip olabilirsiniz.  


* * *

![8](/user/pages/15.hazir-altyapi/8.png)  
Erkan Soft , müşteri odaklı çalışmayı prensip edinmiş, müşterilerinin ihtiyaçları doğrultusunda interaktif çözümler sunan, yeni nesil dijital reklam ajansıdır. Türkiye genelinde 100 den fazla marka ve kuruma hizmet vermektedir.   


* * *

![9](/user/pages/15.hazir-altyapi/9.png)  
Markanıza özel eticaret tasarımı, tedarik entegrasyon, pazaryeri entegrasyon ve ödeme sistemi entegrasyon gibi hizmetleri ile Etic sektörün öncülerinden olmayı kendisine misyon edinmiştir. Kolay kullanım ve yönetim özelliklerine sahip, SEO uyumlu ve anahtar teslim Etic eticaret yazılımı ile siz de e-ticaret dünyasına adım atıp satışlarınızı arttırabilirsiniz.  


* * *

![10](/user/pages/15.hazir-altyapi/10.png)  
Eticea, müşterilerine kaliteli hizmeti; en uygun fiyata ve gelişmiş teknolojiye uygun, akılda kalıcı ve interaktif çözümlerle sunmaktadır.  


* * *

![11](/user/pages/15.hazir-altyapi/11.png)  
Eticsoft, Türkiye'nin önde gelen finansal teknoloji sağlayıcısıdır.  


* * *

![12](/user/pages/15.hazir-altyapi/12.png)  
Eticaretkur, e-ticaret yazılımı olarak ilk çalışmasını 2009 yılında gerçekleştirmiştir. 2011 yılından itibaren ETICARETKUR markasıyla kendi üretim ve tasarımı olan e-ticaret çözümlerini her kesimden müşterilerine sunmaya başlamıştır.  


* * *

![13](/user/pages/15.hazir-altyapi/13.png)  
Softwate Bilişim, 15 yıllık birikim ve deneyimi sonucu yeni bir yapılanma olarak kurulmuştur. 5 yıllık özveri ve azimli çalışma sonucunda sektörün en iyi alt yapısını geliştirmiş olmanın gururu ile 2020 yılının Nisan ayında ilk satışımızı yaparak hızlı bir şekilde sektöre giriş yapmış bulunmaktadır.  


* * *

![14](/user/pages/15.hazir-altyapi/14.png)  
Güçlü SEO uyumu, geliştirilebilir altyapı, trafik sorunu olmayan e-ticaret paketleri, düşük banka komisyonları ve çok daha fazlası ile markanızı dijital dünyaya taşımanıza yardımcı olan Faprika, hedeflerinize en hızlı ve güvenilir bir şekilde ulaşmanızı sağlıyor.  


* * *

![15](/user/pages/15.hazir-altyapi/15.png)  
Fonzip, 2016 yılından beri STK’ların potansiyellerini ortaya çıkartacak en ileri kaynak geliştirme ve STK yönetim araçlarını sunmaktadır.  


* * *

![16](/user/pages/15.hazir-altyapi/16.png)  
Geliştir, bilgi sistemleri mühendisliğinde 10 yıldan fazla deneyime sahip bir kadro tarafından kurulmuştur. İşletmelerin ihtiyaçlarına ve özelliklerine uyarlanan teknolojik ve yenilikçi çözümler sunmaktadır.  


* * *

![17](/user/pages/15.hazir-altyapi/17.png)  
Glycon, sürekli olarak değişen, güncellenen ve yenilenen yazılım dünyası içerisinde bizler de sürekli olarak kendimizi yenilemekte ve müşterilerimize her geçen gün daha iyi, verimli hizmetleri sunmaktadır. Web, mobil, network ve sistem yazılımlarının yanı sıra seo paketleri ile de web sitelerinin yükselmesi için ekstra hizmetler sağlamaktadır.  


* * *

![18](/user/pages/15.hazir-altyapi/18.png)  
Goyomod, e-ticaret sitesi açmak isteyenler için hazırlanmış özel yazılım uygulamasıdır. Sisteme üye olup 3 dakika içinde e-ticaret sitenizi açabilir, hemen ürün ekleyebilir ve satış yapmaya başlayabilirsiniz.  


* * *

![19](/user/pages/15.hazir-altyapi/19.png)  
Hiosis Software Bilişim Medya Danışmanlık Tic. Ltd. Şti. 2017 yılından itibaren yerli ve milli yazılım anlayışı ile ürettiği ürünleri küresel pazarda firmaların kullanımına sunmaktadır.  


* * *

![20](/user/pages/15.hazir-altyapi/20.png)  
IdeaSoft, 15 yıldır Türkiye’nin lider e-ticaret altyapı sağlayıcısı olarak yoluna sağlam adımlarla devam etmektedir. Sektör tecrübesini; doğru bilgi, değişim, işbirliği ve güven ile harmanlayarak e-ticaret ve e-ihracat alanında küresel bir oyuncu olma yolunda ilerlemektedir.  


* * *

![21](/user/pages/15.hazir-altyapi/21.png)  
2010 yılından bu tarafa sürekli kendini yenileyen, dinamik ve son teknoloji ile birleştirilmiş bir iMağaza E-Ticaret alt yapısı ile sizler de işletmenizi sanal mağazalara taşıyabilir ve hemen kazanmaya başlayabilirsiniz.  


* * *

![22](/user/pages/15.hazir-altyapi/64.png)  
ikas, 9000’den fazla kullanıcıya hizmet veren ve girişimcilerin ihtiyaçlarına yönelik olarak geliştirilen yeni nesil bir e-ticaret altyapısıdır.  


* * *

![23](/user/pages/15.hazir-altyapi/23.png)  
Insoplus, online tahsilat yazılımı e-ticaret yazılımı ve pazaryeri API entegrasyonu sunmaktadır.  


* * *

![24](/user/pages/15.hazir-altyapi/24.png)  
Jetteknoloji, 2010 - 2018 arası internet reklam sektöründe ve çeşitli özel yazılım hizmetleri üzerine faaliyet gösterdiği farklı iş kollarından edinmiş olduğu tecrübeler doğrultusunda 2018 yılı başında e-ticaret yazılım sektörüne farklı bir bakış açısı ile katılmış bulunmaktadır.  


* * *

![25](/user/pages/15.hazir-altyapi/25.png)  
Tekrom Teknoloji 2003 yılında kurulmuştur. 15 yılı aşkındır süredir e-ticaret yazılımı sunmaktadır.  


* * *

![26](/user/pages/15.hazir-altyapi/26.png)  
KargoTurk, yurt içi ve yurt dışı kargo taşımacılığı konusunda hizmet vermektedir.  


* * *

![27](/user/pages/15.hazir-altyapi/27.png)  
Kirazsoft, işletmenize özel hazırlanmış karekod, web sitesi ve mobil uygulama sistemleri ile siparişte yaşadığınız tüm sorunları kolay kullanımlı arayüzlerle gidermeyi hedeflemektedir.  


* * *

![28](/user/pages/15.hazir-altyapi/28.png)  
Kobibazaar, 10 yılın verdiği tecrübe ve deneyim ile Türkiye'nin en yenilikçi e-ticaret markaları arasında yer almaktadır.  


* * *

![29](/user/pages/15.hazir-altyapi/29.png)  
Kullanımı en kolay hazır e-ticaret paketi "kolay sipariş" ile E-ticaret sitenizi 1 gün içerisinde açtıktan sonra internetten satış yapmaya hemen başlayabilirsiniz.  


* * *

![30](/user/pages/15.hazir-altyapi/30.1.png)  
Kobinet Yazılım, ileri seviye hazır e-ticaret altyapısı sunmaktadır. Kurulduğu ilk günden itibaren çalışmalarını profesyonel bir şekilde yürütmektedir.   


* * *

![31](/user/pages/15.hazir-altyapi/31.png)  
KUSsoft, 2000 yılından bu yana e-ticaret yazılımları alanında faaliyet göstermektedir.  


* * *

![32](/user/pages/15.hazir-altyapi/32.png)  
LeaderOS, 2016 yılından bu yana geliştirilen ve yüzlerce müşteriye sahip bir Minecraft Web Site scriptidir.  


* * *

![33](/user/pages/15.hazir-altyapi/33.jpg)  
Lebisoft, 2013 yılından günümüze uçtan uca e-ticaret yazılımları sunmaktadır.  


* * *

![34](/user/pages/15.hazir-altyapi/34.png)  
Lidyapos, pazaryeri entegrasyonları içerisinde barındıran mobil uyumlu e-ticaret ve muhabese yazılımları sunmaktadır.  


* * *

![35](/user/pages/15.hazir-altyapi/35.png)  
Müşteri Takip, küçük ve orta ölçekli firmaların ön muhasebe ve müşteri takip işlemlerini kolayca yürütebilecekleri kullanışlı işlevsel ve akıllı bir sistemdir.  


* * *

![36](/user/pages/15.hazir-altyapi/36.png)  
Mysoft,bilişim sektöründe deneyimli bir ekibin bir araya gelmesiyle dijital dönüşüm alanında hizmet vermek üzere 2008 yılında kurulmuştur.Genç ve dinamik ekibiyle şirketlerin iş süreçlerini daha etkin ve verimli kullanmalarını sağlayan çözümler sunmaktadır.  


* * *

![37](/user/pages/15.hazir-altyapi/37.1.png)  
ElinSoft, ihtiyaçlarınıza yönelik hazır yazılımlarıyla sektörünüze ait web sitesini hızlıca oluşturmanızı, yüksek performanslı hosting paketleri ile sorunsuz hizmet vermenizi sağlamayı hedeflemektedir.  


* * *

![38](/user/pages/15.hazir-altyapi/38.png)  
Nirvana Yazılım; yurt içi ve yurt dışı projeleri ile çok sayıda firmaya hizmet vermiş, bir çok web ajansına web tasarım alanında profesyonel destek sağlamıştır.  


* * *

![39](/user/pages/15.hazir-altyapi/39.png)  
Nlksoft, Türkiye E-Ticaret yazılım pazarının hizmet sağlayıcılarındandır. 30’a yakın çalışan kadrosu ve 3 ofisi ile E-Ticaret – E-İhracat Yazılımları, Anaokulu Otomasyonu, Toplu SMS Sistemleri, İçerik Yönetim Sistemi, Online Randevu ve Online Tahsilat Sistemi gibi birçok alanda hizmet veren yazılım şirketidir.  


* * *

![40](/user/pages/15.hazir-altyapi/40.png)  
Odyo Bilişim, 2013 yılında %100 Yerli E-Ticaret Paketleri geliştirerek kolay kullanım, hız , gelişmiş özellikler ve ekonomik fiyatları bir arada sunarak kısa sürede geniş bir kitleye hitap etmeyi başarmıştır.  


* * *

![41](/user/pages/15.hazir-altyapi/41.png)  
Ödemeix, e-ödeme, 21 bankadan tek çekim, 14 bankadan taksitli ve 11 lisanslı ödeme kuruluşlarının sanal poslarının bir arada bulunduğu, internet olan her yerden ve cihazdan, taksitli ve/veya peşin ödeme yapma ve alma imkânı sağlayan, kuruluşunuza özel, yüksek güvenlikli bir alt yapıdır.  


* * *

![42](/user/pages/15.hazir-altyapi/42.png)  
Parantezsoft® web tabanlı yazılım, tasarım ve masaüstü çözümleri sunan, kısacası " İnternet Teknolojisi'nin Tüm Renkleri " ile sizlere hizmet vermeyi ilke edinmiş bir yazılım firmasıdır.  


* * *

![43](/user/pages/15.hazir-altyapi/43.png)  
Platinum E-Ticaret, 2011 yılından günümüze yaklaşık 1500 web sitesine modul,destek ya da tema konusunda destek olmuştur.  


* * *

![44](/user/pages/15.hazir-altyapi/44.png)  
PlatinMarket markasıyla e-ticaret sektörüne giriş yaparak kobilere e-ticaret altyapısı sağlamaktadır. 2004 yılından günümüze kadar Türkiye genelinde 81 il’de 3000 üzerinde firmaya sanal mağaza altyapısı sağlamaktadır.  


* * *

![45](/user/pages/15.hazir-altyapi/45.png)  
ProjeSoft kurulduğu günden bu yana teknolojik yapı kurma odaklı, sistematik olarak e-ticaret sektörüne katalizör olma vizyonuyla hayatına devam etmektedir. Bugüne dek iki bilgisayar mühendisinin kurmuş olduğu ProjeSoft, binlerce farklı e-ticaret sitesine altyapı desteği sağlamıştır.  


* * *

![46](/user/pages/15.hazir-altyapi/46.png)  
Proticaret, bilgi iletişiminin çağdaş, yüksek teknolojilerle bilişim gerçeğini otomasyona geçirecek ETicaret yazılım programlarının arge,üretim,pazarlama ve satışını gerçekleştiren ve kurumların etkin ve yetkin bir biçimde internet web portallarının kullanımlarını sağlamak için kurulmuş bir kurumdur.  


* * *

![47](/user/pages/15.hazir-altyapi/47.png)  
Quka Soft, 2012 yılından bu yana müşterilerine benzersiz e-ticaret çözümleri sunup kurum ve marka kimliklerinin dijital ortamda en iyi şekilde lanse edilmesini sağlamaktadır. Asıl hedefi, e-ticareti baskın olarak pazarlama tekniği ve itici güç olan teknolojinin en iyi şekilde kullanımıdır.  


* * *

![48](/user/pages/15.hazir-altyapi/48.png)  
RGS Yazılım kurulduğu 2005 yılından bu yana e-ticaret yazılımları üzerine faaliyetlerini sürdürmekte ve projeler üretmektedir. Araştırma geliştirme (ar-ge) çalışmalarını tamamen kendi öz kaynakları, bilgi birikimi ve teknolojisiyle gerçekleştirmektedir.  


* * *

![49](/user/pages/15.hazir-altyapi/49.png)  
Sitemia, kısa sürede e-ticaret sitesi açıp, kullanmanızı sağlamaktadır.  


* * *

![50](/user/pages/15.hazir-altyapi/50.png)  
Softtr, 2016 yılında kurulmuştur. Merkez ofis ve ar-ge merkezi olmak üzere iki konumda faaliyet göstermektedir. Bir firmanın e-Ticaret operasyonlarını kendi web sayfası, pazar yeri mağazaları, fiziki mağazaları olmak üzere bir bütün olarak tek panelden yönetmeyi amaçlayan yazılımlar geliştirmektedir.  


* * *

![51](/user/pages/15.hazir-altyapi/51.png)  
Shopinom, e-ticaret (B2C), bayi yönetimi (B2B), e-tahsilat yazılımları geliştirerek işletmelerin e-ticaret dünyasında adım atması ve bu dünyada büyümeleri için yazılımsal ve teknik altyapı hizmetleri sunmaktadır.  


* * *

![52](/user/pages/15.hazir-altyapi/52.png)  
ShopPHP kiralık değil, domain adına lisanslı bir PHP e-ticaret yazılımıdır. Açık kaynak kodlu modüller ve şabon dosyaları ile dilediğiniz gibi kişiselleştirebilir, kendi sunucunuzda ömür boyu kullanabilirsiniz. Üstelik, satın aldığınız ana sürüm boyunca güncel dosyaları ücretsiz alabilir, sürekli güncel kalabilirsiniz.  


* * *

![53](/user/pages/15.hazir-altyapi/53.png)  
2011 Yılında Ankara'da kurulan Tensasoft, başladığı ticaret faaliyetlerini, 2015 yılında Isparta merkezli ofisi ile güçlendirmiştir. Yıllar içinde yaptığı ek yatırımları ve kalite odaklı üretimi sayesinde, Türkiye'de e-ticaret,kurumsal web sitesi,otomasyon vb. teknoloji ürünleri sayesinde rakiplerine karşı üstünlük sağlamış ve en çok tercih edilen markalardan biri haline gelmiştir.  


* * *

![54](/user/pages/15.hazir-altyapi/54.png)  
Ticari Bulut, tüm satışlar tek ekranda yönetebileceğiniz e-ticaret ve muhasebe çözümleri sunmaktadır.  


* * *

![55](/user/pages/15.hazir-altyapi/55.1.png)  
Ticimax, ağırlıklı olarak e-ticaret yazılımları, özel e-ticaret çözümleri ve tasarım hizmetleri vermek üzere kurulmuştur. Ticimax, güçlü altyapısı ve 15 yılı aşkın tecrübesi ve 180+ uzman personeli ile müşterilerinin e-ticaret alanındaki rekabetlerini güçlendirmesine yardım etmektedir.  


* * *

![56](/user/pages/15.hazir-altyapi/56.png)  
Tekrom Teknoloji 2003 yılında kurulmuştur. 15 yılı aşkındır süredir e-ticaret yazılımı sunmaktadır.Türkiye e-ticaret pazarının lider şirketleri arasında yer almaktadır.  


* * *

![57](/user/pages/15.hazir-altyapi/57.png)  
2003 Yılında Us Tasarım adı ile faaliyete başlayan şirket 2008 Yılında Web Tabanlı Yazılımları ön plana çıkarmış ve köklü bir değişim yaşamıştır. Web sitesi, CRM (Müşteri İlişkileri Yönetimi), Elektronik Ticaret, Google Adwords reklamı alanlarında hizmet vermektedir.  


* * *

![58](/user/pages/15.hazir-altyapi/58.png)  
Vesasoft, yazılım sektöründe 2013 yılından bu yana hizmetlerine devam etmektedir. Müşteri memnuniyetini ilke edinmiş Vesasoft, hizmet vermeye başladığı günden bu yana her daim müşterilerinin memnun ve en önemlisi mutlu olabileceği şekilde hizmet vermeyi sürdürmüştür.  


* * *

![59](/user/pages/15.hazir-altyapi/59.png)  
VikaON, 2000'li yılların başında kurulmuştur.ETicaret, Dijital Pazarlama, SEO (Arama Motoru Optimizasyonu) ve SEM (Arama Motoru Pazarlaması) alanlarında 15 yıldan fazla süredir birikime sahip olan ekib, işinizi internete taşıma veya mevcut işletmenizin internet üzerinde daha çok gelir elde etmesi için tüm donanıma sahiptir.  


* * *

![60](/user/pages/15.hazir-altyapi/60.png)  
Zip, hosting, domain ve yazılım sektöründe hizmet veren bir şirkettir. Hizmetini, AHL Teknoloji ve Ticaret Anonim Şirketi çatısı altında yürütmekte olup, firmanın Zip Yazılım, Zip Ticaret, Zip Detector, Zip Mail gibi birçok hizmeti mevcuttur .  


* * *

![66](/user/pages/15.hazir-altyapi/66.png)  
WISECP, web hosting ve diğer tüm dijital hizmetler sunan işletmelere yönelik yeni nesil, akıllı ve gelişmiş bir otomasyon yazılımıdır.  



---

# Shopify Hazır Altyapı | PayTR


# Shopify Hazır Altyapı

![](/user/pages/15.hazir-altyapi/03.shopify/shopify.png)

**Kurulum**

[**Bu bağlantıyı**](https://accounts.shopify.com/store-login?redirect=settings%2Fpayments%2Falternative-providers%2F1058121) kullanarak kurulum işlemini başlatın. Eğer oturumunuz açık değilse Shopify sizi oturum açmanız için yönlendirecektir.  
Daha sonra PayTR Sanal POS uygulamanızı kuracağınız mağazanızı seçebileceğiniz bir ekranla karşılaşacaksınız.  


![1](/user/pages/15.hazir-altyapi/03.shopify/L1.png)

Bu ekrandan mağaza seçiminizi yapın ve ilerleyin. Karşınıza PayTR Sanal POS uygulamasının ekranı çıkacak. Bu ekranın sağ alt köşesinde bulunan **“Bağlan”** butonuna tıklayın.

![2](/user/pages/15.hazir-altyapi/03.shopify/L2.png)

Shopify mağazanıza için PayTR Sanal POS uygulamasını yükleyebileceğiniz bağlantıya yönlendirecek. Bu ekrandan **“Uygulamayı Yükle”** butonuna basarak işlemi tamamlayın.

![3](/user/pages/15.hazir-altyapi/03.shopify/L3.png)

**_Bu adımdan sonra arka planda PayTR Sanal POS Uygulaması mağazanıza yüklenmiştir._**

**Oturum Açma**

Bu adımdan sonra PayTR Mağaza panelinize giriş yapabilmeniz için PayTR oturum açma ekranına yönlendirileceksiniz. Daha önce PayTR tarafından size iletilen PayTR Mağaza Paneli bilgileriniz ile oturum açma işlemini gerçekleştirin. 

![4](/user/pages/15.hazir-altyapi/03.shopify/L4.png)

Oturum Açma ekranında 3 dakikalık oturum süresi vardır. 3 dakikanın ardından aşağıdaki ekranı görürsünüz. Oturum süresi dolduğunda işlemi tekrar başlatmalısınız. 

![5](/user/pages/15.hazir-altyapi/03.shopify/L5.png)

Oturum işlemini tekrar başlatmak için **Shopify Admin sayfası > Ayarlar> Ödemeler> PayTR Sanal POS** uygulamasının detaylarına ulaşın.

![6](/user/pages/15.hazir-altyapi/03.shopify/L6.png)

Bu ekranda sağ alt köşede bulunan **“Yönet”** butonuna tıklayın. Doğrudan oturum açma ekranına yönleneceksiniz.  


Bu ekranda oturum açtıktan sonra Shopify mağazanıza yönlendirileceksiniz.  


Yönlendirildiğiniz sayfada PayTR Sanal POS uygulamasını sağ alt köşedeki buton ile etkinleştirin.

![7](/user/pages/15.hazir-altyapi/03.shopify/L77.png)

Bu adımdan sonra mağazanızdan ödeme alabiliyor olacaksınız. İlk işleminiz **“Test Modunu”** aktifleştirerek test edebilirsiniz. **MağazaNum** bölümünde oturum açarken girdiğiniz mağaza numaranız yazacaktır.   


**Ödeme Sayfası Ayarları**

Shopify, PayTR gibi “Ödeme Yöntemleri” ile yeteri kadar bilgi paylaşmamaktadır. Bu nedenle PayTR Sanal POS ile ödeme alırken sorunla karşılaşmamak için aşağıda önerdiğimiz ayarları uygulamalısınız. Ayar sayfasına **Shopify Admin sayfası > Ayarlar> Ödeme Sayfası** altından ulaşabilirsiniz.  


**1\. Müşteri iletişimi** : Müşteriler ödeme işlemlerini yalnızca e-posta kullanarak yapabilir  
**2\. Form seçenekleri** : Ad ve soyadı gerekli  


Ayarları zorunlu olarak seçilmelidir.  


**Siparişler**

Shopify Mağazanız üzerinden yapılacak alışverişlerin ödemeleri PayTR ortak sayfası üzerinde güvenli bir şekilde gerçekleşecektir. Ödemesi gerçekleşen siparişlerin, Shopify Mağazanızın Admin sayfası> Siparişler adımından ilgili siparişin detayına girerek görebilirsiniz.  


Sipariş detayında bulunan açıklamada **“Test”** işlemleri için **“Test True”** ibaresi görünürken **“Gerçek”** işlemler için hiçbir ibare görünmemektedir. **“Ağ geçidinden bilgiler”** başlığı altındaki bilgi, **PayTR Mağaza Panelinizdeki** işleme ait sipariş numarasıdır. Bu numarayı kopyalayıp **PayTR Mağaza Paneli > İşlemler** sayfasına ulaşın ve **İşlem Numarasıyla Arama** seçeneği kullanarak ilgili işlemi kolayca bulabilirsiniz.

![8](/user/pages/15.hazir-altyapi/03.shopify/L8.png)

PayTR Mağaza Panelinden ilgili işlemin detaylarında;  


**“Ürün/Hizmet Bilgisi”** başlığı altında **“Shopify Alışverişi – 10.00TL – 1 Adet”** gibi bir sabit bilgi bulanacaktır. Shopify sipariş sepet bilgisini paylaşmadığından bu detayları Shopify Sipariş detaylarından kontrol etmelisiniz.  


**“Müşteri Telefonu”** başlığı altında ise sabit olarak “05555555555” telefon numarası göreceksiniz.  
Shopify müşteri bilgilerinden sadece e-posta veya telefonu paylaşmaktadır. PayTR olarak kurulumda eposta adresini kullanmanız gerekmektedir.  


**İade**

İadesini gerçekleştirmek istediğiniz siparişin detayına ulaşın. Yukarıdaki panelde bulunan **“Para İadesi”** butonuna tıklayın.

![9](/user/pages/15.hazir-altyapi/03.shopify/L9.png)

Açılan sayfada sağ bölümde bulunan alandan siparişin iadesini gerçekleştirebilirsiniz. Gerçekleştirdiğiniz iadeleri PayTR Mağaza Paneli> İşlemler sayfası altından ilgili işlemin detayına girerek de görebilirsiniz.

![10](/user/pages/15.hazir-altyapi/03.shopify/L10.png)

PayTR Mağaza Panelinden yapılacak iadeler, şu an için Shopify Mağazanızdaki ilgili siparişe yansıtılmamaktadır. Shopify bu konuyla ilgili özellik getirdiğinde PayTR olarak destekliyor olacağız.

**Bildirim URL’in Kontrolü**

PayTR Mağaza Paneline giriş yapın, Destek & Kurulum menüsünden Ayarlar bağlantısına tıklayarak ayarlar sayfasına ulaşın. Bildirim URL Ayarı (Callback URL) bölümünde "https://arod.paytr.com/notification" adresinin yazılı olduğunu teyit edin. Eğer farklı bir adres görünüyorsa Değiştir butonuna basarak Açılan protokol seçeneğinden https:// seçeneğini seçerek Bildirim URL alanına "https://arod.paytr.com/notification" adresini yazarak kaydedin. 

**Destek**

Bu süreçlerin herhangi birinde bir hata sayfası ile karşılaşırsanız, lütfen hata sayfasında bulunan hata kodu ile **PayTR Mağaza Paneli > Destek** bölümünden iletişime geçiniz.


---

# Wix Hazır Altyapı | PayTR


# Wix Hazır Altyapı

![1](/user/pages/15.hazir-altyapi/02.wix/wix-logo1.png)

**Kurulum**

Wix yönetim paneline giriş yaptıktan sonra:  
• Ayarlar > Ödemeleri Kabul Edin adımlarını takip edin.  
• Sayfanın altında bulunan “Diğer Seçenekleri Görüntüle” linkine tıklayın.  
• PayTR logosu yanında bulunan “Bağla” butonuna tıklayın.  


![2](/user/pages/15.hazir-altyapi/02.wix/Resim1.png)

**Modül Ayarları**

PayTR modülüne ait “Bağla” butonuna bastıktan sonra açılan form sayfasında aşağıdaki alanların doldurulması zorunludur.  
• Merchant ID  
• Merchant Key  
• Merchant Salt  


Bu bilgilere erişmek için PayTR üye bilgileriniz ile birlikte mağaza panelinde bulunan “Bilgi” menü linkine tıklayın (https://www.paytr.com/magaza/bilgi).  


![3](/user/pages/15.hazir-altyapi/02.wix/rsm.png)

Bu bilgileri sırasıyla kopyaladıktan sonra, Wix yönetim panelinize geri dönüş yapıp, PayTR modülündeki form sayfasında bulunan ilgili alanlara yapıştırın ve sayfadaki “Bağla” butonuna tekrar basarak formu kaydedin.  


**Bildirim URL’nin Ayarlanması**

Wix mağazaları için Bildirim URL’ler otomatik olarak tanımlanmaktadır; ancak bu ayarı kontrol etmek için sırasıyla:  
• PayTR mağaza paneline giriş yapın,  
• Destek & Kurulum > Ayarlar linkine tıklayın (https://www.paytr.com/magaza/ayarlar),  
• Bildirim URL (Değiştir) yazısına tıklayın ve Bildirim URL alanında “https://www.paytr.com/wix/notification” linkinin bulunduğuna emin olduktan sona KAYDET butonuna tıklayın.  



---

# Açık Kaynaklı Altyapılar | PayTR


# Açık Kaynaklı Altyapılar

* * *

![1](/user/pages/16.moduller/1.png)

OpenCart bir çevrimiçi mağaza yönetim sistemidir. MySQL veritabanı ve HTML bileşenleri kullanarak PHP tabanlıdır. Farklı diller ve para birimleri için destek sağlanır. GNU Genel Kamu Lisansı altında serbestçe kullanılabilir. Mayıs 2016 itibarıyla 342.000 web sitesi OpenCart kullanmaktadır.  
PayTR Resmi Opencart Eklentisine bu [**linkten**](/moduller/opencart) gidebilirsiniz.  
  


* * *

![2](/user/pages/16.moduller/2.png)

PrestaShop, ücretsiz, açık kaynaklı bir e-ticaret çözümüdür. Yazılım, Açık Yazılım Lisansı altında yayınlanır. MySQL veritabanı yönetim sistemi desteği ile PHP programlama dilinde yazılmıştır. PrestaShop şu anda dünya çapında 300.000 mağaza tarafından kullanılmaktadır ve 60 farklı dilde mevcuttur.  
PayTR Resmi PrestaShop Eklentisine bu [**linkten**](/moduller/prestashop) gidebilirsiniz.  
  


* * *

![3](/user/pages/16.moduller/3.png)

WooCommerce, WordPress'in özgür ve açık kaynak kod kaynaklı E-Ticaret eklentisidir. WooThemes tarafından yapılan ve Automattic tarafından geliştirilen eklenti, kolaylıkla tüm wordpress kullanıcıları tarafından yönetilebilmektedir.  
PayTR Resmi WooCommerce Eklentisine bu [**linkten**](/moduller/wordpress) gidebilirsiniz.  
  


* * *

![4](/user/pages/16.moduller/4.png)

nopCommerce ASP.NET MVC 4.0 tabanlı ve MS SQL Server 2008 Veritabanı kullanan açık-kaynak e-ticaret çözümüdür. nopCommerce resmi olarak Ekim 2008 de küçük ve orta büyüklükteki işletmeler için duyurulan Public License V3 lisansı kullanır.  
PayTR Resmi nopCommerce Eklentisine bu [**linkten**](/moduller/nopcommerce) gidebilirsiniz.  
  


* * *

![5](/user/pages/16.moduller/5.png)

Magento, ücretli ve açık kaynaklı iki sürümü bulunan, toplamda 250.000 aktif müşteri tarafından kullanılan, gelişmiş özellikleri ile bilinen B2B ve B2C online satış platformudur  
PayTR Resmi Magento Eklentisine bu [**linkten**](/moduller/magento) gidebilirsiniz.  
  


* * *

![6](/user/pages/16.moduller/6.png)

Drupal içerik yönetim sistemini güçlendiren açık kaynaklı bir e-ticaret yazılımıdır.  
PayTR Resmi Drupal Commerce Eklentisine bu [**linkten**](/moduller/drupal-commerce) gidebilirsiniz.  
  


* * *

![7](/user/pages/16.moduller/7.png)

XenForo, PHP programlama dilinde yazılan sosyal bir forum script yazılımıdır.XenForo forum yazılımı içerisinde SEO özelliklerini barındırmaktadır  
PayTR Resmi xenForo Eklentisine bu [**linkten**](/moduller/xenforo) gidebilirsiniz.  
  


* * *

![8](/user/pages/16.moduller/8.png)

WHMCS, içerisinde tüm hizmetleri barındıran hazır paket bir web hosting yönetim yazılım otomasyonudur.   
PayTR Resmi WHMCS Eklentisine bu [**linkten**](/moduller/whmcs) gidebilirsiniz.  
  


* * *

![9](/user/pages/16.moduller/9.png)

VirtueMart, en çok tercih edilen CMS sistemlerinden biri olan Joomla üzerine entegre edilerek kullanılan bir modül sistemidir.   
PayTR Resmi VirtueMart Eklentisine bu [**linkten**](/moduller/virtuemart) gidebilirsiniz.  
  


* * *

![10](/user/pages/16.moduller/10.png)

Perfex CRM, Codeigniter tabanlı olarak hazırlanmış ve kendi sunucunuza kurabileceğiniz içerisinde ERP, HRM vb. gibi modülleri olan bir CRM yazılımıdır.   
PayTR Resmi Perfex CRM Eklentisine bu [**linkten**](/moduller/perfex-crm) gidebilirsiniz.  
  


* * *

**DİĞERLERİ**  
  
WHMCSTR WHMCS modül ve entegrasyon için (iFrame API ve Havale/EFT iFrame API Ortak Modül - İndirim Kodu: WHMCSPAYTR)  
[**İş Ortağına Ulaş**](https://www.whmcstr.net/siparis/sanal-pos/paytr-whmcs-modulu/)  
  
BurtiNet WHMCS modül ve entegrasyon için  
[**İş Ortağına Ulaş**](https://www.burtinet.com/whmcs-paytr-sanal-pos-modulu)  
  
Klasik ASP entegrasyonu için  
[**İş Ortağına Ulaş**](https://www.ozguweb.com/classic-asp-paytr-kurulumu/)  
  



---

# Drupal Commerce Açık Kaynaklı Altyapı | PayTR


# Drupal Commerce Açık Kaynaklı Altyapı

![drupal](/user/pages/16.moduller/06.drupal-commerce/dpLogo.png)

**Modül kurulumu için yapılması gerekenler;**

Kurulum

  1. https://www.drupal.org/project/paytr_payment Adresinde bulunan Downloads alanından modülü indiriniz.



![d1](/user/pages/16.moduller/06.drupal-commerce/d1.png)

  2. Drupal yönetici panelinde yer alan Modüller sekmesine ilerleyerek, Yeni eklenti kur bağlantısına tıklayınız. Ardından indirmiş olduğumuz dosyayı yükleyerek ilerleyin.
  3. Drupal yönetici panelinde yer alan Modüller sekmesine ilerleyerek PayTR Sanal Pos iFrame API eklentisini aktif olarak işaretleyerek kurulumu yapın.



![d2](/user/pages/16.moduller/06.drupal-commerce/d2.png)

  4. Drupal yönetici panelinde yer alan, Yapılandırma menüsü altında bulunan Profil türleri bağlantısına tıklayın.



![d3](/user/pages/16.moduller/06.drupal-commerce/d3.png)

  5. Açılan sayfada Customer linkine tıklayın.



![d4](/user/pages/16.moduller/06.drupal-commerce/d4.png)

  6. Daha sonra Alanları Yönet isimli tab’a tıklayın.



![d5](/user/pages/16.moduller/06.drupal-commerce/d5.png)

  7. Daha sonra Alan Ekle bağlantısına tıklayın. Ardından gelen listeden Telefon Numarasını seçerek ilerleyin.



![d6](/user/pages/16.moduller/06.drupal-commerce/d6.png)

  8. Daha sonra görsel de göründüğü gibi bu alanı düzeltin ve kaydedin. Makine tarafından okunabilir ad yazan alanın değeri field_phone olmasına dikkat edin.



![d7](/user/pages/16.moduller/06.drupal-commerce/d7.png)

  9. Son olarak görsel de görüldüğü gibi değerleri girerek kaydet butonuna tıklayınız.



![d8](/user/pages/16.moduller/06.drupal-commerce/d8.png)

Ayarların Yapılması

  1. Görselde görüldüğü gibi yeni bir ödeme yöntemi eklemek için ilgili sayfaya ilerleyin.



![d9](/user/pages/16.moduller/06.drupal-commerce/d9.png)

  2. Yeni bir ödeme yöntemi eklemek için görsel de gösterilen butona basarak ilgili sayfaya gidin.



![d10](/user/pages/16.moduller/06.drupal-commerce/d10.png)

  3. Görsel de yer alan alanları doldurarak modül ayarlarını tamamlayın.



![d11](/user/pages/16.moduller/06.drupal-commerce/d11.png)

Not: Merchant ID, Merchant Key ve Merchant Salt değerlerinizi öğrenmek için https://www.paytr.com/magaza/ayarlar sayfasına gidin.

Taksit Ayarlarının Yapılması

  1. Görsel de gösterildiği gibi Taksit Ayarları sayfasına ilerleyin.



![d12](/user/pages/16.moduller/06.drupal-commerce/d12.png)

  2. İlgili sayfada yer alan kategorilere göre taksit ayarlarınızı yapıp kaydedin.



![d13](/user/pages/16.moduller/06.drupal-commerce/d13.png)

[**Drupal Commerce iFrame API Ödeme Modülü**](https://www.drupal.org/project/paytr_payment)


---

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


---

# Nopcommerce Açık Kaynaklı Altyapı | PayTR


# Nopcommerce Açık Kaynaklı Altyapı

![nopcom](/user/pages/16.moduller/04.nopcommerce/nopcom.png)

**Modül kurulumu için yapılması gerekenler;**

  * Eklenti dosyasını indirin.
  * Yönetici alanı> Yapılandırma> Yerel eklentilere gidin.
  * "Eklenti veya tema yükle" seçeneğini kullanarak eklenti dosyasını yükleyin.
  * Eklenti listesinde yeni yüklediğiniz eklentiyi bulun ve kurmak için "Yükle" düğmesine tıklayın. 



[**nopCommerce iFrame API Ödeme Modülü**](https://www.nopcommerce.com/en/paytr-virtual-pos-iframe-api-turkey)


---

# Opencart Açık Kaynaklı Altyapı | PayTR


# Opencart Açık Kaynaklı Altyapı

![](/images/b/a/1/7/3/ba173db48d3137b107996faf90ece5db653e707e-opencart.png)

“OpenCart modülümüz resmi sürümler üzerinde, en sade haliyle (eklentisiz) geliştirilmiştir. Journal temasını ve Tek Sayfa Ödeme metodunu desteklemektedir.”

**1\. Kurulum**

Otomatik Kurulum Opencart Yönetim Paneline giriş yaptıktan sonra;

  * **Eklentiler > Eklenti Yükle** adımlarını takip edin.



![1](/user/pages/16.moduller/01.opencart/1.PNG)

  * **Yükle** butonuna basın ve indirdiğiniz Opencart sürümünüze uygun **.ocmod.zip** uzantılı dosyayı seçin.



![2](/user/pages/16.moduller/01.opencart/2.PNG)

  * Yükleme işlemi tamamlandığında başarılı mesajı ile karşılaşacaksınız.



![3](/user/pages/16.moduller/01.opencart/3.PNG)

  * Bu adımları tamamladıktan sonra **Eklentiler > Ödeme Metotları** adımlarını takip edin.
  * Listeden **PayTR Sanal POS - iFrame API** modülünü bulun ve **Kur** seçeneği ile kurulum yapın.



![4](/user/pages/16.moduller/01.opencart/4.PNG)

  * Kurulum işlemi tamamlanmıştır. Bundan sonrasını **Ayarların Yapılandırılması** başlığı altından takip edebilirsiniz.



**Manuel Kurulum**

  * İndirdiğiniz Opencart sürümünüze uygun **.ocmod.zip** uzantılı dosyayı klasöre çıkartın.
  * Çıkan **upload** klasörü içerisindeki dosyaları sitenizin olduğu dizine kopyalayın.
  * **Eklentiler > Ödeme Metotları** adımlarını takip edin.
  * Listeden **PayTR Sanal POS - iFrame API** modülünü bulun ve **Kur** seçeneği ile kurulum yapın.
  * Kurulum işlemi tamamlanmıştır. Bundan sonrasını **Ayarların Yapılandırılması** başlığı altından takip edebilirsiniz.



**2\. Ayarların Yapılandırılması**

  * Kurulumu tamamladıktan sonra, **Düzenle** seçeneği ile ayarlar sayfasına ulaşın.



![5](/user/pages/16.moduller/01.opencart/5.PNG)

**Genel Ayarlar**

**Mağaza No, Mağaza Parola ve Mağaza Gizli Anahtar** bilgilerinize https://www.paytr.com/magaza/bilgi adresinden ulaşabilirsiniz. Gerekli bilgileri ilgili alanlara doldurunuz.

**Dil:** Ödeme sayfasının dilinizi ayarlamanıza yardımcı olur. Bu dil seçeneği ayrıca ödeme sayfası üzerinde de bulunur. Toplam: PayTR Ödeme modülünün Ödeme Yöntemleri içerisinde aktif olması için, sepetin ulaşması gereken toplam tutarı bu alana girebilirsiniz.

**Ödeme Sayfası:** Tek Sayfa Ödeme seçeneği sunan temalar veya modüllerde uyumluluğu sağlamak için bu seçeneği kullanabilirsiniz. Standart ve Tek Sayfa olarak 2 seçenek bulunur.

**Not:** Temalar iFrame Ödeme Yöntemi sunan sağlayıcılar için seçenek sunabilmektedir. Aşağıdaki resimde Journal Temasının 3.1 sürümünde gelmiş olan seçeneğini görebilirsiniz. Bu tarz seçenek sunan temalarda, özelliği aktif ederek Standart seçeneğini kullanabilirsiniz. _İlgili sayfaya Opencart Yönetim Paneli > Journal > Skins > Default > Checkout adımlarını takip ederek ulaşabilirsiniz._

![6](/user/pages/16.moduller/01.opencart/6.PNG)

**Durum:** Modül durumunu açık veya kapalı olarak ayarlayabilirsiniz.

**Sıralama:** PayTR Ödeme modülünün Ödeme Yöntemleri içerisindeki sıralamasını belirleyebilirsiniz.

**Sipariş Durumları**

**Başarılı Ödeme:** Ödemenin başarılı olduğu zaman atanacak durumu belirleyebilirsiniz.

**Başarısız Ödeme:** Ödemenin başarısız olduğu zaman atanacak durumu belirleyebilirsiniz.

**Sipariş Notunu Müşteriye Gönder:** Ödeme işlemli sonunda müşteriye sipariş notunun gönderilip gönderilemeyeceğini seçebilirsiniz. Bu seçenek aktif edilirse, doğru çalışması için e-posta ayarlarınızın düzgün yapılandırıldığından emin olun.  


**Vade Farkını Göster:**

**Açık seçeneği** ; sipariş alt toplamına **Vade Farkı** satırı ekler ve **Faturanın Toplam Tutarını** değiştirir.

**Toplam Tutarı Değiştir seçeneği** ; sadece **Faturanın Toplam Tutarını** değiştirir.

**Sipariş Tutarını Değiştir** : Taksitli ödemelerde **Ödenen Toplam Tutarı (vade farkı dahil)** siparişin **Toplam Tutarı** ile değiştirir. Bu seçenek faturayı etkilemez.  


**Taksit Ayarları**

Taksit kısıtlamalarını ayarlayabilirsiniz. Kategori Bazlı taksit seçeneği ile her kategori için taksit seçeneği belirleyebilirsiniz. Sepette bulunan farklı kategorideki ürünler için taksit seçeneği en düşük olan geçerli olur.

**3\. Bildirim URL’in Ayarlanması**

PayTR Mağaza Paneline giriş yapın, menüden **Ayarlar** bağlantısına tıklayarak ayarlar sayfasına ulaşın. **Bildirim URL Ayarı (Callback URL)** bölümünde bulunan **Değiştir** butonuna tıklayın. Açılan ilgili bölümde Opencart sürümünüze uygun olan seçeneklerden bir tanesini seçin ve **Kaydet** butonuna basarak değişiklikleri kaydedin. Eğer sitenizde **SSL** varsa, **Protokol** seçeneğinden **https://** seçeneğini seçin. Eğer **SSL** sertifikanız yoksa, **http://** seçeneğini seçin. Daha sonradan **SSL** kurulumu yaparsanız buradaki **Protokol** ’ü **https://** olarak güncelleyin.

**4\. Kullanmaya Başlama**

Sepetinize ürün ekleyerek ödeme sayfasına kadar ilerleyin.

![7](/user/pages/16.moduller/01.opencart/7.PNG)

Ödeme sayfasına geldiğinizde yukarıdaki ekran ile karşılaşırsınız. Eğer PayTR Mağazanız Canlı durumdaysa yukarıdaki ekran yerine Canlı Mod ekranını göreceksiniz. Test modu ekranı ile karşılaşırsanız, Canlı Moda geçmeden önce 1 veya 2 kere test işlemi yapmanız gerekmektedir. Bu bölüme kadar olan tüm adımları eksiksiz tamamladıktan sonra ödeme almaya başlayabilirsiniz.

**5\. Sipariş Detayları**

PayTR Sanal POS – iFrame API modülü ile başarılı ödeme alınan siparişlerin detayına aşağıdaki gibi not düşülür. Burada sipariş ile ilgili PayTR Mağaza Paneli eşleşen detayları görebilirsiniz.

![8](/user/pages/16.moduller/01.opencart/8.PNG)

Taksitli ödemelerde bu nota ilave olarak **Vade Farkı** da eklenir. Başarısız ödemeler için not aşağıdaki gibidir. 

![9](/user/pages/16.moduller/01.opencart/9.PNG)

Ödeme hatası mesajı alınan hataya göre değişiklik gösterir.

**6\. İade Yapma**

Sipariş detayında bulunan PayTR Sanal POS – iFrame API sekmesinde, başarılı ödeme yapılmış işlemlere iade yapabilirsiniz.

![10](/user/pages/16.moduller/01.opencart/10.PNG)

Taksitli ödemelerde **Toplam Ödenen, Toplam tutardan** farklı olabilmektedir. İade girişine **Toplam** tutarın girilmesi gerekmektedir. Vade farkını girmeniz gerekmez.

**_PayTR Mağaza Panelinden yapılan iadeler, bu sekmeye yansıtılmamaktadır_**

[**OpenCart tüm versiyonları için(Desteklenen Versiyonlar: 1.5.x - 2.x - 3.x - 4.x**](https://www.opencart.com/index.php?route=marketplace%2Fextension%2Finfo&extension_id=38301%2F%3Ftarget%3Dblank)

OpenCart iFrame API Ödeme Modülü Kurulum Dökümanı [**indirmek için tıklayın.**](/moduller/opencart/PayTR_iFrame_API_OpenCart_Modül_Entegrasyonu.zip)


---

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


---

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


---

# Virtuemart Açık Kaynaklı Altyapı | PayTR


# VVirtuemart Açık Kaynaklı Altyapı

## ![](/user/pages/16.moduller/09.virtuemart/vrm.png)

**Kurulum**

  * İndirdiğiniz zip dosyasını açarak sunucunuzun ana dizininde bulunan **plugins/wmpayment** yoluna ilerleyin.  

  * İlgili dizine paytr isimli bir klasör oluşturun.  

  * Zip dosyasından çıkan dosyaları **paytr** klasörü içerisine kopyalayarak yapıştırın.  

  * Joomla yönetici paneline giriş yaptıktan sonra sırasıyla **Uzantılar / Yönetim** sayfasına ilerleyin. Ardından sol menüde yer alan **Keşfet** linkine tıklayarak **PayTR Virtual Pos iFrame API** eklentisini etkinleştirin.



![1](/user/pages/16.moduller/09.virtuemart/1.PNG)

**Ayarların Yapılması**

  * Joomla yönetim paneline giriş yaptıktan sonra üst menüde yer alan **Virtuemart** menüsüne tıklayın. Ardından **ödeme yöntemleri** linkine tıklayın



![2](/user/pages/16.moduller/09.virtuemart/2.PNG)

  * Açılan sayfada **Yeni** linkine tıklayarak gelen sayfadaki formu aşağıdaki ibarelere göre doldurup kaydedin.



![3](/user/pages/16.moduller/09.virtuemart/3.PNG)

  * Kaydetme işleminden sonra **Ayarlar** bölümüne tıklayarak API ayarlarını yapıyoruz.



![4](/user/pages/16.moduller/09.virtuemart/4.PNG)

  * Merchant ID, Merchant Key ve Merchant Salt değerlerinizi öğrenmek için PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfasına gidin.



**Taksit Ayarlarının Yapılması**

  * Görselde yer alan kısımdan kategori bazlı taksit ayarlarınızı yapabilirsiniz.



![5](/user/pages/16.moduller/09.virtuemart/5.PNG)

[**PayTR iFrame API VirtueMart Ödeme Modülü**](https://extensions.joomla.org/extension/vm-payment-paytr-virtual-pos-iframe-api/)

VirtueMart iFrame API Ödeme Modülü Kurulum Dökümanı [**indirmek için tıklayın.**](/moduller/virtuemart/VM_Payment_-_PayTR_Virtual_Pos_iFrame_API_-_Kullanım_Kılavuzu.zip)


---

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


---

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


---

# Xenforo Açık Kaynaklı Altyapı | PayTR


# Xenforo Açık Kaynaklı Altyapı

## ![xenforo](/user/pages/16.moduller/07.xenforo/features-xenforo.png)

**Kurulum**

  * *_xenForo Yönetici paneline_ giriş yapınız.
  * **Eklenti Yönetimi** menüsüne tıklayarak indirmiş olduğunuz **zip** dosyasını yükleyin.



![1](/user/pages/16.moduller/07.xenforo/1.PNG)

  * Tüm adımlar tamamlandığında **PayTR Virtual Pos iFrame API** eklentisini listede görüyorsanız kurulum başarıyla tamamlanmıştır.



**Ayarların Yapılması**

Gerekli API bilgilerine **PayTR Mağaza Paneli > Destek & Kurulum > Bilgi** sayfasından ulaşabilirsiniz.

![2](/user/pages/16.moduller/07.xenforo/2.PNG)

**Bildirim URL (Callback URL) Ayarlarının Yapılması**

  * PayTR Mağaza Paneline giriş yaparak **Ayarlar** sayfasına ilerleyin.
  * **Bildirim URL** alanına site adresinizi yazarak alan adınızın sonunda yer alacak şekilde **“payment_callback.php?_xfProvider=paytr”** değerini ekleyin.



![3](/user/pages/16.moduller/07.xenforo/3.PNG)

[**xenForo Ödeme Modülü**](https://xenforo.com/community/resources/paytr-virtual-pos-iframe-api.8555/)

xenForo iFrame API Ödeme Modülü Kurulum Dökümanı [**indirmek için tıklayın.**](/moduller/xenforo/xenForo_-_PayTR_Sanal_Pos_iFrame_API_Kurulum_ve_Kullanım_Kılavuzu.zip)


---

# NeoPOS Bridge Kurulumu & Entegrasyonu | PayTR


# NeoPOS Bridge Kurulumu & Entegrasyonu

**NeoPOS**   
NFC özellikli Android işletim sistemine sahip akıllı telefon veya tabletinizle, tüm temassız kart ve cihazlar ile ödeme alabilirsiniz.

**PayTR NeoPOS Nasıl Çalışır?**   
PayTR NeoPOS Soft POS teknolojisi altyapısı ile, Mastercard Tap on Phone platformu (Mastercard Acceptance Gateway) üzerinde çalışan mobil ödeme alma özelliği sayesinde, Android işletim sistemine sahip akıllı telefon veya tabletlerden, POS cihazlardan ödeme alır gibi, temassız ödeme almayı sağlar.

**NeoPOS Bridge**  
NeoPOS ana ürünü PayTR Mağaza uygulaması için oluşturulmuş bir ödeme alma yöntemidir. NeoPOS Bridge ise kendi firmanızı ait uygulamanıza bir köprü oluşturarak tüm temassız kart ve cihazlardan (kendi uygulamanız üzerinden) ödeme almanızı sağlar.

NeoPOS Bridge hakkında daha fazla bilgi almak ve entegrasyon dokümanına ulaşmak için [bize ulaşın.](https://www.paytr.com/iletisim)

**NFC özellikli Android işletim sistemine sahip akıllı telefon veya tabletinizle, tüm temassız kart ve cihazlar ile ödeme alabilirsiniz.**   
  


1

![](https://dev.paytr.com/user/pages/16.neopos/images/1.jpg)

2

![](https://dev.paytr.com/user/pages/16.neopos/images/2.jpg)

3

![](https://dev.paytr.com/user/pages/16.neopos/images/3.jpg)

__ __

  



---

# API Servis Test Araçları | PayTR


# API Servis Test Araçları

**Postman**

PayTR tarafından yayınlanmış olan servislerin testlerini daha kolay bir şekilde gerçekleştirmenize imkan tanıyan "Postman" programına ait Collections dosyalarını kullanmaya başlayabilirsiniz.

Collections dosyalarının yer aldığı Postman sayfasına bu [**linkten**](https://dev.paytr.com/servis-test-araclari/postman) gidebilirsiniz.  


**Hash Hesaplama**

Entegrasyon aşamasının ilk adımı olan 1.ADIM içerisinde hash hesaplaması yapılmalı ve istek bloğunun içerisine dahil edilmelidir. İstek bloğunun içerisindeki değerler ile servis üzerinde tekrar hash hesaplaması yapılmaktadır. İletilen hash değeri ile yapılan hesaplama sonucu çıkan hash değeri karşılaştırılmakta ve isteğin doğrudan mağazadan geldiği onaylanmaktadır.

Hash Hesaplama sayfasına bu [**linkten**](/servis-test-araclari/hash-hesaplama) gidebilirsiniz.  


Token hataları genel olarak, listede bulunan nedenlerden ötürü oluşmaktadır;  
1) merchant_key, merchant_salt gibi bilgilerin hatalı kullanımı,  
2) paytr_token hesabında kullanılan verilerin POST içeriğinde farklı değerde olması,  
3) paytr_token hesabında kullanılan verilerin doğru sıra ile uç uca eklenmemesi,  
4) paytr_token hesabında gerekli olan tüm verilerin eklenmemesi veya gerek duyulmayan verilerin hesaba dahil edilmesi.  


_Hash Hesaplama sayfası üzerinden değerlerinizle birlikte doğru hash hesaplaması yapabilirsiniz._

**Servis Yanıt Gözlem**

Entegrasyon aşaması 2.ADIM'da bildirim/callback tarafı bulunmaktadır. PayTR yapısında bulunan bilgilendirme servisleri dışında(örn: durum sorgulama), tüm ödeme gerçekleştirilen API'lerin 2.ADIM'ında ilgili işleme ait detay tanımlı olan Bildirim URL adresinize POST metodu ile gönderilmektedir. PayTR tarafından dönen örnek yanıta Servis Yanıt Gözlem alanından ulaşabilirsiniz. Bildirim URL sayfanıza dönen yanıtlar sayfa üzerinde "PayTR tarafından tanımlı olan Bildirim URL adresinize dönen yanıt" ibaresi altında belirtilmiştir. Sayfa üzerinden "Başarılı" veya "Başarısız" dönen yanıtlara, sayfa üzerinde bulunan form yapısını veya JSON alanını kullanarak ulaşabilirsiniz.

Servis Yanıt Gözlem sayfasına bu [**linkten**](/servis-test-araclari/servis-yanit-gozlem) gidebilirsiniz.  



---

# Hash Hesaplama API Servis Test Aracı | PayTR


# Hash Hesaplama API Servis Test Aracı

iFrame API Direkt API  Link API Havale/EFT Platform Transfer API İade API Durum Sorgu İşlem Dökümü NeoPOS Bridge

### iFrame API

1/3

Tüm alanlar doldurulmalı.

Ürün Ad:  Birim Fiyatı:  Adet: 

Add Field Hash Calculate

Merchant ID: User IP: Merchant OID: Email: Payment Amount: User Basket:  
Sepet içeriği hash hesaplaması için tıklayın No Installment: Max Installment: Currency: Test Mode: Merchant Salt: Merchant Key:


---

# Postman API Servis Test Aracı | PayTR


# Postman API Servis Test Aracı

![postman](/user/pages/18.servis-test-araclari/03.postman/postmanLogo.png)

PayTR API'lerini kullanmak için aşağıdaki bilgilere sahip olmanız gerekmektedir. Bu bilgilere PayTR Mağaza panelindeki Bilgi sayfasından ulaşabilirsiniz.

-PayTR Mağaza No (merchant_id)  
-Mağaza Parola (merchant_key)  
-Mağaza Gizli Anahtar (merchant_salt)  


Not: Bu bilgiler tamamen sizin mağazanıza özeldir, dışarıya paylaşmamalısınız.

**Kurulum ve Kullanım**

Postman tarafında kullanmanız için önceden hazırlanmış olan 2 adet dosya bulunmaktadır. Bunlardan birisi global tanımlamaların bulunduğu **PAYTRENV.postman_environment.json** dosyası, diğeri ise API servislerin bulunduğu **PAYTR APIs.postman_collection.json** dosyasıdır.

**Adım 1 (Environment Dosyasının Kurulumu):**  


-Postman programını açın.  
-Sol menüde bulunan "Environments" butonuna tıklayın.  
-Import butonuna tıklayın.  
-İndirmiş olduğunuz **PAYTRENV.postman_environment.json** adlı dosyayı seçin ve Import edin.  
-Import edilen PAYTRENV adlı environmenti seçtikten sonra **merchant_id** , **merchant_key** , **merchant_salt** , **user_ip** ve **merchant_oid** alanlarındaki XXXXXX değerlerini kendi bilgileriniz ile değiştiriniz.  


**Adım 2 (Collections Dosyasının Kurulumu):**  


-Sol menüde bulunan "Collections" butonuna tıklayın.  
-Import butonuna tıklayın.  
-İndirmiş olduğunuz **PAYTR APIs.postman_collection.json** adlı dosyayı seçin ve Import edin.  
-PAYTR APIs klasör adıyla gelen Collenctions'a tıkladıktan sonra sağ üstte bulunan **No Environment** butonuna tıklayarak, az önce eklemiş olduğumuz **PAYTRENV** adlı environmenti bu Collections'ta kullanabilmek için seçiyoruz.  


**Adım 3 (API Kullanım Örneği):**  


-PayTR APIs adlı Collections içerisinden kullanmak istediğiniz API servisi seçin. (Örneğin: iFrame API)  
-**get-iframe-token** adlı POST Request'e tıkladıktan sonra **Body** butonuna tıklayın.  
-**form-data** kısmında önceden hazırlanmış verilere ek olarak, Environment kısmından gelen bazı global veriler bulumaktadır.  
-Request penceresinde bulunan form alanlarındaki değerleri kendi isteğinize göre değiştirebilir, sonrasında Send butonuna tıklayarak servisi çağırabilirsiniz.  
-Ekranının alt kısmındaki Response panelinde, servisten dönen cevap olarak başarılı/hatalı çıktılar gösterilecektir.  


**Servisler Hakkında Bilgiler**

Aşağıdaki bilgiler, servislerin kısa tanıtımlarıdır. Servisler hakkında daha detaylı bilgiye ve örnek kodlara ulaşmak için [**Buraya Tıklayın**](https://dev.paytr.com/).

**iFrame API**

Bu servis ile iFrame ödeme ekranını açarken kullanılacak olan iframe_token değeri döner.

**Havale/EFT iFrame API**

Bu servis ile Havale/EFT iFrame ödeme ekranını açarken kullanılacak olan iframe_token değeri döner.

**Linkle Ödeme** PayTR Link; entegrasyona gerek olmadan ödemelerinizi tek tık ile almanızı sağlar.

  * Linkle Ödeme (Create) Create servisi ile Hizmet/Ürün veya Fatura/Cari tahsilatlarınız için ödeme linkleri oluşturabilirsiniz.

  * Linkle Ödeme (Delete) Delete servisi ile daha önce oluşturmuş olduğunuz ödeme linklerini silebilirsiniz.

  * Linkle Ödeme (Callback) Oluşturduğunuz ödeme linki üzerinden yalnızca başarılı bir ödeme yapıldığında, Create servisinde link için göndermiş olduğunuz callbak_url’e işlem sonucu bildirilir.




Not: _Eğer Create servisinde callbak_url belirlemediyseniz veya belirlemek istemiyorsanız, bu entegrasyonu yapmanıza gerek yoktur. Bu servis yalnızca "Create" servisinde gönderdiğiniz linkin (varsa) callback _url'sine istek atar._

  * Linkle Ödeme (SMS/Email) Bu servisi kullanarak belirttiğiniz cep telefonu numarasına/email adresine oluşturmuş olduğunuz linkle ödeme sayfasına ait linkin gönderimini sağlayabilirsiniz.



**Direkt API**

iFrame API'ye alternatif olarak kendi ödeme formunuz ile birlikte ödeme almanızı sağlayan servistir. Direkt API çözümünde, kullanılacak olan tüm servislerin mağaza tarafından (siz/yazılımcınız) entegre edilmeli ve test edilmelidir. Direkt API çözümünde güvenlik başta olmak üzere tüm akış mağaza sahibinin sorumluluğundadır. Direkt API çözümünü kullanma talebiniz PayTR ilgili birimlerince incelenmekte ve tanımlanmaktadır. Direkt API çözümü 2 adımlıdır:

  1. ADIMda ödeme/kart bilgileri form aracılığı ile PayTR sistemine aktarılır,
  2. ADIMda ise PayTR'den gelecek olan ödeme sonucuna ait yanıtın aktarılacağı "Bildirim URL" sayfası hazırlanır. Bu sayfada bildirim sonucuna göre (başarılı/başarısız) siparişi onaylamalı veya iptal etmelisiniz. (Bu adımda PayTR tarafından dönecek olan sipariş durumu bilgisi, PayTR Mağaza'nızın ayarlar sayfasında bulunan **Bildirim URL** adresine yönlendirilecektir. Yani 2. adımda kodlama yapacağınız sayfa ile aynı adres olmalıdır.)



**Taksit Oranları Sorgulama**

Direkt API entegrasyonu yapılırken, girilen kart numarasına ait taksit oranlarını çekmek için bu API kullanılmalıdır. Oranlar günlük olarak değişebilir. Bu nedenle bu oranları günlük olarak taksit oranları sorgulama API aracılığıyla çekip veritabanına kaydedebilir, güncelleyebilirsiniz. Bu oranları taksitli işlemlerde ürün fiyatına göre uygulayabilirsiniz.

**BIN Sorgulama Servisi**

BIN sorgulama servisi ile bir BIN numarası (kart numarasının ilk 6 veya 8 hanesini) gönderip kartın detaylı bilgilerine ulaşabilirsiniz.

**Kart Saklama API**

  * Yeni Kart Ekleme Bu servisi kullanarak ödeme esnasında PayTR'de kayıtlı bir kullanıcı ve kullanıcıya ait bir kart oluşturabilirsiniz. Bunun için yapılması gereken süreç:


  1. Direkt API dökümanında belirtildiği şekilde ödeme sayfanızı oluşturun.

  2. Kart bilgilerinin girildiği ödeme formunda "Kartını Kaydet" seçeneği sunacağınız bir onay kutucuğu ekleyin ve bu kutu seçildiyse gerekli bilgileri POST içeriğine ekleyin.

  3. Kullanıcı adına ilk kez bir kart kaydediliyorsa yalnızca "store_card" parametresi gönderilir.

  4. Kullanıcıya ait daha önceden kayıtlı bir kart varsa VE yeni bir kart kaydetmek istiyorsa, POST içerisinde "utoken" ve "store_card" parametreleri birlikte gönderilmelidir.




**Kayıtlı Karttan Ödeme** İzlenecek adımlar:

  1. Ödeme yapacak olan kayıtlı kullanıcıya ait kayıtlı kartlar ekranda listelenir.

  2. Kullanıcı listelenen kayıtlı kartlardan ödeme yapacağı kartı seçer.

  3. Kullanıcın seçtiği karta ait "require_cvv" parametresi değeri "1" ise CVV gireceği input alanı gösterilir.

  4. Kullanıcın seçtiği karta ait "ctoken" bilgisi ve kullanıcının "utoken" bilgisi POST içerisinde gönderilir.



  * **Kayıtlı Kart Listesi** Ödeme formunda, kullanıcıya ait kayıtlı kartları göstermek için daha önceden yeni kart kayıt servisinden elde edilmiş olan "utoken" bilgisi ile bu servise istek atarak o kullanıcıya ait kayıtlı kartları listeleyebilirsiniz.

  * **Kayıtlı Kart Silme** Kullanıcıya ait kayıtlı olan bir kart bilgisini silmek için "utoken, ctoken, merchant_id, paytr_token" bilgilerini bu servise göndererek istek yapmalısınız.

  * **Kayıtlı Karttan Tekrarlayan Ödeme** Kayıtlı Karttan Tekrarlayan Ödeme (Recurring Payment) servisi ile kullanıcıya ait kayıtlı kart bilgileri ile dilediğiniz zaman veya aralıklarla ödeme alabilirsiniz.



  1. Recurring Payment adımında belirtilen değerlerle birlikte ödeme istek bloğunu oluşturun. Ödeme işlemi, kendi oluşturacağınız yapı üzerinden, kayıtlı kart bilgileri ile servise göndereceğiniz istek sonucunda oluşacaktır. Bu sebepten dolayı kullanıcıyla etkileşime girecek form oluşturulmasına gerek bulunmamaktadır.

  2. İşlemler Non3D (Non Secure) olarak gerçekleşecektir. Kullanıcınız herhangi bir ek işlem yapmayacak veya işlem sırasında kendisinden herhangi bir bilgi talep edilmeyecektir (Kullanabilmek için mağazanızda Non3D yetkilerinin açık olması gerekmektedir).

  3. Kayıtlı Kart Listesi servisinden, ödeme gerçekleştirilecek kullanıcıya ait "utoken" verisi kullanarak kayıtlı kartın "ctoken" verisine ulaşmanız gerekmektedir. Daha sonrasında bu ve dökümanda belirtilen diğer tüm alanları POST içerisinde ilgili servise iletmelisiniz.




**Platform Transfer Talebi**

PayTR Pazaryeri Çözümü ile pazaryeri platformu sahipleri, aynı sepette birden fazla satıcının ürünü olduğu durumlar, parçalı iade yapılması, sipariş tutarının sonradan değişmesi, farklı satıcıya farklı komisyon uygulanması vb. gibi her ihtiyaçlarını özgürce karşılayabilirler.

**Transfer Talimatı** İzlenecek adımlar:

**1\. ADIM Platform Transfer Talimatının Verilmesi:** Dökümanda belirtilen bilgiler, ilgili servise gönderilmelidir. 

Not: _Mağaza, ödeme yapılmasını istediği tarihte (aynı gün hariç) en geç saat 10:00'a kadar Transper API'si yoluyla isteği göndermelidir. Daha sonra gönderilen istekler, bir sonraki iş gününde işleme alınacaktır._

**2\. ADIM Transfer Talimatının Sonucunun Alınması (Opsiyonel):** PayTR sistemi, transfer işlemlerin sonuçlanması sonurası PayTR Mağaza Paneli > Destek & Kurulum > Ayarlar sayfasında "Platform Transfer Sonucu Bildirim URL" kısmında belirttiğiniz adrese bilgi verir.

**Geri Dönen Ödemeleri Listele** Bu servis ile transfer talebi yapılmış ancak alıcı hesap hatası nedeniyle geri dönen ödemelerin listesine ulaşabilirsiniz. Geri dönen ödemeler mağazanıza ait bir alt hesaba bakiye olarak işlenir. Geri dönen bu ödemeleri tekrar göndermek için “Geri Dönen Ödemeler – Hesaptan Gönder” servisini kullanabilirsiniz.

**Geri Dönen Ödemeleri Hesaptan Gönder** Bu servis ile transfer talebi yapılmış ancak alıcı hesap hatası nedeniyle geri dönen ödemeler için tekrar ödeme isteği gönderebilirsiniz. Geri dönen bu ödemelerin listesine “Geri Dönen Ödemeler – Listele API” servisi ile ulaşabilirsiniz.

**Geri Dönen Ödemeler Callback** Geri dönen ödemelerden oluşturacağınız transfer talebi sonrasında Success yanıtı almanız ile birlikte hesaptan gönderme talebiniz PayTR sistemi tarafından başarılı olarak alınmış olur. PayTR sistemi talebinizi ortalama 5 dakika içerisinde işleme alacak, gönderdiğiniz trans_info içeriğini kontrol ederek transferleri gerçekleştirecektir. Kontrol sırasında hatalı bilgi tespiti halinde ilgili işlem başarısız olarak işaretlenir. Oluşan sonuç JSON formatında PayTR Mağaza Paneli > Destek & Kurulum > Ayarlar > Platform Transfer Sonucu Bildirim URL olarak tanımladığınız adrese POST edilerek bildirilir.

**İade API**

Bu servis aracılığıyla, siparişe ait tutarın bir kısmı veya tamamı için iade işlemi gerçekleştirebilirsiniz. Bunun için sipariş numarası, iade edilecek tutar VE dökümandaki diğer istenilen bilgilerin ilgili servise POST metodu ile istek atılması gerekmektedir.

**Durum Sorgu API**

Durum Sorgu servisi aracılığıyla, mağazanız üzerinde gerçekleştirilen işlemlerin durumunu sorgulayabilirsiniz. Mağaza Durum Sorgulama ve Pazaryeri Durum Sorgulama olarak iki kategoriye ayrılır.

**BKM Express iFrame API**

BKM Express servisini kullanarak BKM Express sisteminde kayıtlı olan kartlar aracılığıyla ödeme alabilirsiniz. BKM Express Entegrasyonu iFrame ödeme yönteminde otomatik olarak ödeme ekranına gelmektedir. Ancak "Direkt API" çözümünde BKM Express entegrasyonu yaparken $payment_type = "bex" olarak gönderilmesi gerekmektedir.

**işlem Dökümü**

İşlem dökümü servisi ile, iletilen tarih aralığındaki (en fazla 3 gün) yapılan satış ve iade işlemlerinin dökümünü alabilirsiniz.

**Test Kart Bilgileri**

Aşağıdaki test kart bilgileri yalnızca **Direkt API** çözümü için geçerlidir. iFrame API yönteminde test kart bilgileri otomatik olarak gelmektedir.

Kart bilgileri | Alabileceği değerler | Açıklama  
---|---|---  
Adı Soyadı | PAYTR TEST | Dilediğiniz şekilde gönderebilirsiniz.  
Kart No | 4355 0843 5508 4358 | Bu değer zorunludur.  
Son Kullanma | 12 / 30 | Dilediğiniz şekilde gönderebilirsiniz.  
CVV | 000 | Bu değer zorunludur.  
  
  


Kart bilgileri | Alabileceği değerler | Açıklama  
---|---|---  
Adı Soyadı | PAYTR TEST | Dilediğiniz şekilde gönderebilirsiniz.  
Kart No | 5406 6754 0667 5403 | Bu değer zorunludur.  
Son Kullanma | 12 / 30 | Dilediğiniz şekilde gönderebilirsiniz.  
CVV | 000 | Bu değer zorunludur.  
  
  


Kart bilgileri | Alabileceği değerler | Açıklama  
---|---|---  
Adı Soyadı | PAYTR TEST | Dilediğiniz şekilde gönderebilirsiniz.  
Kart No | 9792 0303 9444 0796 | Bu değer zorunludur.  
Son Kullanma | 12 / 30 | Dilediğiniz şekilde gönderebilirsiniz.  
CVV | 000 | Bu değer zorunludur.  
  
  


Postman üzerinde kullanabileceğiniz PayTR Collection ve ENV dosyasına [**link**](/servis-test-araclari/postman/postman_paytr.zip) üzerinden ulaşabilirsiniz.


---

# Servis Yanıt Gözlem API Servis Test Aracı | PayTR


# Servis Yanıt Gözlem API Servis Test Aracı

iFrame API Direkt API  Link API Havale/EFT Platform Transfer API İade API Durum Sorgu İşlem Dökümü

Success Failed

### iFrame API

  
  
  


1/3

Tüm alanlar doldurulmalı.

Ürün Ad:  Birim Fiyatı:  Adet: 

Add Field Hash Calculate

Merchant ID: User IP: Merchant OID: Email: Payment Amount: Total Amount: User Basket:  
Sepet içeriği hash hesaplaması için tıklayın No Installment: Max Installment: Currency: Test Mode: Merchant Salt: Merchant Key:


---

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

---

