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
