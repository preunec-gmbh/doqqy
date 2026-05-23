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



