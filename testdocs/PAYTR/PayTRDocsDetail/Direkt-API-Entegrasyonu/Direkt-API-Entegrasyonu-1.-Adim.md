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
