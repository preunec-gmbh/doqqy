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
