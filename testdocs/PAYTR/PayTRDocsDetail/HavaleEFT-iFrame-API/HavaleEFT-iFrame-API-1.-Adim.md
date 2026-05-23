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
