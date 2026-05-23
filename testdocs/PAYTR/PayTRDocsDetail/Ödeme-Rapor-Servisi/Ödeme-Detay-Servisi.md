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
