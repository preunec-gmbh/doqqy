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
