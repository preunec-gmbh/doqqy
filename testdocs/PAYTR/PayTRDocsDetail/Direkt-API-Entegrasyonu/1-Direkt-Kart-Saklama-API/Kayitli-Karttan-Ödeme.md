# Kayıtlı Karttan Ödeme | PayTR

# Kayıtlı Karttan Ödeme

**CAPI LIST servisinden dönen require_cvv, utoken ve ctoken değerlerinin kullanımı.**   
1- Ödeme işlemini yapan kullanıcının kayıtlı kart listesi alınarak kullanıcının önüne listelenlir.   
2-Kullanıcı listelenen kartlar arasından ödeme yapacağı kartı seçer.  
3-Kullanıcının seçtiği karta ait require_cvv parametresi kontrol edilip eğer 1 ise CVV gireceği alan gösterilir.   
4-Kullanıcının seçtiği kartın ctoken bilgisi ve kullanıcının utoken bilgisi ödeme isteğinde gönderilir. 

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (integer) | Mağaza No: PayTR tarafından size verilen Mağaza numarası |  |   
user_ip (string) | Müşteri ip: İstek anında aldığınız müşteri ip numarası(Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | Evet | En fazla 39 karakter (ipv4)  
merchant_oid (string) | Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası.(Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | Evet | En fazla 64 karakter,Alfa numerik  
email (string) | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | Evet | En fazla 100 karakter  
payment_amount(integer) | Ödeme tutarı: Siparişe ait toplam ödeme tutarı | Evet | Ayraç olarak yalnızca nokta(.) gönderilmelidir  
payment_type(string) | Ödeme tipi | Evet | ('card')  
installment_count(int) | Taksit sayısı | Evet | 0, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12  
currency(string) | Para birimi | Hayır | TL, EUR, USD, GBP, RUB(Boş ise TL kabul edilir)  
test_mode | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | Hayır | 0 veya 1  
non_3d | Non 3D işlem yapabilmek için 1 gönderilebilir | Evet | 0 veya 1  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet  
paytr_token (string) | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız  
user_ip (string) | Müşteri ip: İstek anında aldığınız müşteri ip numarası (Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | Evet | En fazla 39 karakter (ipv4)  
merchant_oid (string) | Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası. (Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | Evet | En fazla 64 karakter, Alfa numerik  
email (string) | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | Evet | En fazla 100 karakter  
payment_type(string) | Ödeme tipi | Evet | ('card')  
require_cvv | Kullanıcının seçtiği karta ait require_cvv parametresi kontrol edilip eğer 1 ise CVV gireceği alan gösterilir | Evet(Açıklama dikkatli okunmalı.) | -  
payment_amount (double), ondalık olarak nokta (.) ve noktadan sonra iki hane | Ödeme tutarı: Siparişe ait toplam ödeme tutarı | Evet | Örn: 100.99 veya 150 veya 1500.35  
installment_count(int) | Taksit sayısı | Evet | 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12  
card_type(string) | Kart tipi (Taksitli işlemlerde kullanmak üzere) | Hayır | advantage, axess, combo, bonus, cardfinans, maximum, paraf, world  
currency(string) | Para birimi | Hayır | TL(veya TRY), EUR, USD (Boş ise TL kabul edilir)  
client_lang(string) | Ödeme sürecinde kullanılacak dil | Hayır | Türkçe için tr veya İngilizce için en (Boş gönderilirse tr geçerli olur)  
test_mode | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | Hayır | 0 veya 1  
non_3d | Non 3D işlem yapabilmek için 1 gönderilebilir | Evet | 0 veya 1  
non3d_test_failed | Non 3D işlemde, başarısız işlem durumunu test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!) | Hayır | 0 veya 1  
merchant_ok_url(string) | Müşterinin başarılı ödeme sonrası yönledirileceği sayfa (Örn.Siparişlerim takip sayfası)(Uyarı: Müşteri bu sayfaya ulaştığında henüz sipariş onaylanmış olmaz) | Evet | En fazla 400 karakter Uyarı: Tam URL olmalıdır  
merchant_fail_url(string) | Müşterinin ödemesi sırasında beklenmeyen bir hatada yönlendirileceği sayfa | Evet | En fazla 400 karakter Uyarı: Tam URL olmalıdır  
user_name (string) | Müşteri adı ve soyadı: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız adı ve soyadı | Evet | En fazla 60 karakter  
user_address (string) | Müşteri adresi: Müşterinin sipariş sırasında ilettiği adresi | Evet | En fazla 400 karakter  
user_phone (string) | Müşteri telefon numarası: Müşterinin sipariş sırasında ilettiği telefon numarası | Evet | En fazla 20 karakter  
user_basket (string) | Sepet içeriği: Müşterinin siparişindeki ürün/hizmet bilgilerini içermelidir | Evet | JSON tipinde(Örnek kodları inceleyin)  
debug_on (int) | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | Hayır | 0 veya 1(Entegrasyon ve test sürecinde hataları tespit etmek için mutlaka 1  
utoken | Kullanıcıya ait kartı kaydederken servisten tarafınıza dönen ve sizin sistemininiz üzerinden kullacınızla eşleştirdiğiniz değer | Evet  
ctoken | CAPI LIST servisinden dönen kullanıcının kayıtlı kartına ait ctoken değeri | Evet  
  
  


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
    
        ## Kullanıcının ödeme yaparken kayıtlı kartını kullanması için örnek kodlar ##
    
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
    
            //      $card_type = "bonus";       // Alabileceği değerler; advantage, axess, bonus, cardfinans, maximum, paraf, world
            //      $installment_count = "5";
    
            $post_url = "https://www.paytr.com/odeme";
    
            $hash_str = $merchant_id . $user_ip . $merchant_oid . $email . $payment_amount . $payment_type . $installment_count. $currency. $test_mode. $non_3d;
            $token = base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
    
            ## CAPI LIST servisinden dönen require_cvv, utoken ve ctoken değerlerinin kullanımı ##
            ## Ödeme işlemini yapan kullanıcının kayıtlı kart listesi alınarak kullanıcının önüne listelenlir. ##
            ## Kullanıcı listelenen kartlar arasından ödeme yapacağı kartı seçer ##
            ## Kullanıcının seçtiği karta ait require_cvv parametresi kontrol edilip eğer 1 ise CVV gireceği alan gösterilir ##
            ## Kullanıcının seçtiği kartın ctoken bilgisi ve kullanıcının utoken bilgisi ödeme isteğinde gönderilir. ##
            $utoken = "";
            $ctoken = "";       
            $require_cvv = ""; 
    
        ?>
    
        <body>
            <form action="<?php echo $post_url;?>" method="post">
              <!-- CVV gereklilik kontrolü yapılıyor -->
              <?php if($require_cvv == 1) { ?>
                Kart Güvenlik Kodu: <input type="text" name="cvv" value=""><br>
              <?php } ?>
              <input type="hidden" name="merchant_id" value="<?php echo $merchant_id;?>">
              <input type="hidden" name="user_ip" value="<?php echo $user_ip;?>">
              <input type="hidden" name="merchant_oid" value="<?php echo $merchant_oid;?>">
              <input type="hidden" name="email" value="<?php echo $email;?>">
              <input type="hidden" name="payment_type" value="<?php echo $payment_type;?>">
              <input type="hidden" name="payment_amount" value="<?php echo $payment_amount;?>">
              <input type="hidden" name="installment_count" value="0">
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
              <input type="hidden" name="paytr_token" value="<?php echo $token; ?>">
              <input type="hidden" name="non3d_test_failed" value="<?php echo $non3d_test_failed; ?>">
              <input type="hidden" name="installment_count" value="<?php echo $installment_count; ?>">
              <input type="hidden" name="card_type" value="<?php echo $card_type; ?>">
              <input type="hidden" name="utoken" value="<?php echo $utoken; ?>">
              <input type="hidden" name="ctoken" value="<?php echo $ctoken; ?>">
              <br />
              <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # Tek başına bir bütün değildir, capi_payment_stored_card.html ile birlikte çalışmaktadır.
    # Kullanıcının ödeme yaparken kayıtlı kartını kullanması için örnek kodlar
    
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
    
        # Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world
        card_type = 'bonus'
        installment_count = '5'
    
        hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + payment_type + installment_count + currency + test_mode + non_3d
        paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    
        """
        CAPI LIST servisinden dönen require_cvv, utoken ve ctoken değerlerinin kullanımı
        Ödeme işlemini yapan kullanıcının kayıtlı kart listesi alınarak kullanıcının önüne listelenlir.
        Kullanıcı listelenen kartlar arasından ödeme yapacağı kartı seçer
        Kullanıcının seçtiği karta ait require_cvv parametresi kontrol edilip eğer 1 ise CVV gireceği alan gösterilir
        Kullanıcının seçtiği kartın ctoken bilgisi ve kullanıcının utoken bilgisi ödeme isteğinde gönderilir.
        """
        utoken = ''
        ctoken = ''
        require_cvv = ''
    
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
            'card_type': card_type,
            'utoken': utoken,
            'ctoken': ctoken,
            'require_cvv': require_cvv
        }
    
        return render(request, 'capi_payment_stored_card.html', context)
    
    
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
            public ActionResult StoredCard()
            {
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
                // Tahsil edilecek tutar. 100.99
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
                string merchant_ok_url = "http://siteniz.com/success";
                //
                // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
                // !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
                // !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
                string merchant_fail_url = "http://siteniz.com/failed";
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
    
                // İşlem zaman aşımı süresi - dakika cinsinden
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
    
                // CAPI LIST servisinden dönen require_cvv, utoken ve ctoken değerlerinin kullanımı ##
                // Ödeme işlemini yapan kullanıcının kayıtlı kart listesi alınarak kullanıcının önüne listelenlir. ##
                // Kullanıcı listelenen kartlar arasından ödeme yapacağı kartı seçer ##
                //# Kullanıcının seçtiği karta ait require_cvv parametresi kontrol edilip eğer 1 ise CVV gireceği alan gösterilir ##
                // Kullanıcının seçtiği kartın ctoken bilgisi ve kullanıcının utoken bilgisi ödeme isteğinde gönderilir. ##
                string utoken = "";
                string ctoken = "";
                string require_cvv = "";
    
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
                ViewBag.uToken = utoken;
                ViewBag.cToken = ctoken;
                ViewBag.RequireCvv = require_cvv;
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
    
    // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXX';
    var merchant_salt = 'XXXXXX';
    
    // Sepet içerği oluşturma fonksiyonu, değiştirilmeden kullanılabilir.
    var basket = JSON.stringify([['Örnek Ürün 1', '50.00', 1], ['Örnek Ürün 2', '50.00', 1]]);
    var user_basket = basket;
    var merchant_oid = "IN" + microtime.now(); // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    var user_ip = '';
    var email = ''; // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi.
    var payment_amount = '100.99'; // Tahsil edilecek tutar. 100.99
    var currency = 'TL';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var user_name = 'PayTR Test'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi.
    var user_address = 'test test test'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi.
    var user_phone = '05555555555'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi.
    // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php';
    // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php';
    var debug_on = 1; // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    var client_lang = 'tr';
    var payment_type = 'card';
    var installment_count = '0';
    var non_3d = '0'; // 3D'siz işlem.
    var card_type = '';
    var non3d_test_failed = '0'; // Non3d Test Failed.
    
    // CAPI LIST servisinden dönen require_cvv, utoken ve ctoken değerlerinin kullanımı ##
    // Ödeme işlemini yapan kullanıcının kayıtlı kart listesi alınarak kullanıcının önüne listelenlir. ##
    // Kullanıcı listelenen kartlar arasından ödeme yapacağı kartı seçer ##
    //# Kullanıcının seçtiği karta ait require_cvv parametresi kontrol edilip eğer 1 ise CVV gireceği alan gösterilir ##
    // Kullanıcının seçtiği kartın ctoken bilgisi ve kullanıcının utoken bilgisi ödeme isteğinde gönderilir. ##
    
    var utoken = "";
    var ctoken = "";
    var require_cvv = "0";
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${payment_type}${installment_count}${currency}${test_mode}${non_3d}`;
        var paytr_token = hashSTR + merchant_salt;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
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
            utoken,
            ctoken,
            require_cvv
        };
    
        res.render('index');
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Stored Card Servisi örnek kodlarını[**indirmek için tıklayın.**](/direkt-api/kart-saklama-api/kayitli-karttan-odeme/PayTR Stored Card API.zip)
