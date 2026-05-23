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
  
  

