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
