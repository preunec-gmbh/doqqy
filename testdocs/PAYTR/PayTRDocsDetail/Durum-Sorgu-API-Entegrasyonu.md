# Durum Sorgu API Entegrasyonu | PayTR

# Durum Sorgu API Entegrasyonu

Durum Sorgu servisi aracılığıyla, mağazanız üzerinde gerçekleştirilen işlemlerin durumunu sorgulayabilirsiniz.

Mağaza Durum Sorgulama ve Pazaryeri Durum Sorgulama olarak iki kategoriye ayrılır. 

1- Aşağıdaki tabloda belirtilen bilgileri https://www.paytr.com/odeme/durum-sorgu adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
merchant_key | Mağaza Parola  
merchant_salt | Mağaza Gizli Anahtar  
merchant_oid | Sipariş Numarası  
  
  
**Mağaza Durum Sorgulama**  
Tablodan gelen değerler ile sipariş numarası sorgulanır. Müşteriye ait ödeme tutarı ve toplam ödeme tutarı para birimi ile birlikte ekrana basılır. Yukarıdaki bilgilerde bir yanlışlık olursa hata mesajıda ekranda gösterilir. Aynı zamanda siparişe ait iadeler var ise bu iadeler ekranda belirtilir.

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Eğer sorguda bir hata yoksa status değeri “success” ve aşağıdaki tabloda bulunan bilgiler döner.  
b. Eğer sorguda bir hatanız varsa status değeri “error” döner. Bu durumda hata detayı için “err_msg” içeriğini kontrol etmelisiniz.

Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Değişkenler | Açıklamalar | Değerler  
---|---|---  
status(string) | Sorgulama sonucu(success veya failed) | success veya error  
net_tutar (string) | Kesinti sonrası kalan tutar | 9.76  
kesinti_tutari (string) | İşlem için kesilen tutar | 0.24  
payment_amount(string) | İlgili siparişe ait tutar bilgisi | 10,8  
payment_total(string) | Müşterinin ilgili sipariş için ödediği tutar | 10,8  
payment_date(integer) | İşlemin gerçekleşme tarihi | 2021-01-01 (YYYY-MM-DD)  
currency(string) | Para birimi | TL(veya TRY), EUR, USD, GBP, RUB  
taksit(string) | Taksit: İşlem taksitli yapıldı ise taksit sayısı | 0,2,3,4,5,6,7,8,9,10,11,12  
kart_marka(string) | İşlem yapılan kartın markası | Örn. WORD, BONUS, vb.  
masked_pan(string) | İşlemin gerçekleşme tarihi | Örn. 455359AAA6747  
odeme_tipi(string) | Ödemenin hangi tipte yapıldığı | KART veya EFT  
test_mode(string) | İşlemin test veya canlı ortamda yapıldığı | 0 veya 1  
returns(Array) | Eğer ilgili sipariş içerisinde iade varsa dönecek değer  
err_no | Hata numarası | 004  
err_msg | Hata mesajı | merchant_oid ile basarili odeme bulunamadi  
  
  


Durum sorgulama örnek kodları: Örnek kodlar içinde nasıl yapılacağı detaylı olarak anlatılmaktadır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    $merchant_id = "XXX";
    $merchant_key = "XXX";
    $merchant_salt = "XXX";
    $merchant_oid = "XXX";
    
    $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $merchant_oid . $merchant_salt, $merchant_key, true));
    
    $post_vals = array('merchant_id' => $merchant_id,
            'merchant_oid' => $merchant_oid,
            'paytr_token' => $paytr_token);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/durum-sorgu");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
    curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 90);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
    //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
    //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
    $result = @curl_exec($ch);
    
    if (curl_errno($ch)) {
           echo curl_error($ch);
           curl_close($ch);
            exit;
    }
    curl_close($ch);
    
    $result = json_decode($result, 1);
    
    if ($result[status] != 'success') {
           echo $result[err_no] . " - " . $result[err_msg];
           exit;
    }
    
    echo $result['payment_amount'] . " " . $result['currency'] . "<br>";
    
    echo $result['payment_total'] . " " . $result['currency'] . "<br>";
    
    echo $result['payment_date'] . "<br>";
    
    foreach ($result['returns'] AS $return_success)
           print_r($return_success);
    ?>
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXXXX'
    merchant_oid = ''
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + merchant_oid + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/durum-sorgu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['payment_amount'] + res['currency'])
        print(res['payment_total'] + res['currency'])
        print(res['payment_date'])
        for return_success in res['returns']:
          print(return_success)
    
    else:
        print(res['err_no'] + ' ' + res['err_msg'])
    
    
    
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;
    using PayTrTest.Model;
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    
    namespace PayTrTest
    {
        class Program
        {
            private readonly string TRANSFER_URL = "https://www.paytr.com/odeme/durum-sorgu";
            private readonly string MERCHANT_ID = "MERCHANT_ID";
            private readonly string MERCHANT_KEY = "MERCHANT_KEY";
            private readonly string MERCHANT_SALT = "MERCHANT_SALT";
    
            static void Main(string[] args)
            {
                var p = new Program();
                p.Start();
            }
    
            public void Start()
            {
                Dictionary<string, string> testCases = new Dictionary<string, string>
                {
                    { "Geçersiz Merchant OID", "invalid_merchant_oid" } ,
                    { "Başarılı Ödeme", "ffd0c5992212400cb87b88ff40bbcda2" } ,
                    { "Başarısız Ödeme", "fed4b0f2aa33450bab58971ce5da75f0" } ,
                    { "Kısmi Transfer (işlemde) ve Kısmi İade", "dbb5a788734f498e8490333936ec6e11" } ,
                    { "Tamamı Transfer Edilmiş", "5cfbb224a9c44246853818c3082946d8" } ,
                };
    
                foreach(KeyValuePair<string, string> item in testCases)
                {
                    Console.WriteLine($"TESTING '{item.Key}' using Merchant OID: `{item.Value}` {Environment.NewLine}");
                    _DoQuery(item.Value);
                    Console.WriteLine(new string('-',50) + Environment.NewLine);
    
                }
                Console.WriteLine($"{Environment.NewLine}{Environment.NewLine}Cikmak icin bir tusa basin...");
                Console.ReadKey();
            }
    
            private void _DoQuery(string merchantOid)
            {
                PaytrDurumSorguResponse res = _QueryPayment(
                    MERCHANT_ID,
                    MERCHANT_KEY,
                    MERCHANT_SALT,
                    merchantOid
                );
    
                if (res.Status != "success")
                {
                    Console.WriteLine($"  {res.ErrorMessage} - {res.ErrorNo}");
                    return;
                }
    
                Console.WriteLine($"  Sipariş Tutarı : {res.PaymentAmount} {res.Currency}");
    
                Console.WriteLine($"  Müşteri Ödeme Tutarı : {res.PaymentTotal} {res.Currency}");
                if(res.Returns.Count > 0) 
                    Console.WriteLine("  ## IADELER ##");
                foreach (PaytrDurumSorguReturnItem returnItem in res.Returns)
                {
                    Console.WriteLine($"    {returnItem.Amount} - {returnItem.Date} - {returnItem.Type} - {returnItem.DateCompleted} - {returnItem.AuthCode} - {returnItem.RefNum}");
                }
            }
    
            private PaytrDurumSorguResponse _QueryPayment(string merchantId, string merchantKey, string merchantSalt, string merchantOid)
            {
                NameValueCollection data = _GeneratePayTrSorguData(merchantId, merchantKey, merchantSalt, merchantOid);
                ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls;
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
    
                    byte[] result = client.UploadValues(TRANSFER_URL, "POST", data);
    
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    return JsonConvert.DeserializeObject<PaytrDurumSorguResponse>(ResultAuthTicket);
                }
            }
    
            private NameValueCollection _GeneratePayTrSorguData(string merchantId, string merchantKey, string merchantSalt, string merchantOid)
            {
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchantId;
                data["merchant_oid"] = merchantOid;
    
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(merchantId, merchantOid, merchantSalt);
    
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchantKey));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                data["paytr_token"] = Convert.ToBase64String(b);
    
                return data;
            }
        }
    }
    
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXXXXX';
    var merchant_key = 'XXXXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXXXX';
    
    var merchant_oid = ''; // Benzersiz işlem numarası.
    
    app.get("/", function (req, res) {
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + merchant_oid + merchant_salt).digest('base64');
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/durum-sorgu',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'merchant_oid': merchant_oid,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send(res_data);
    
        } else {
            //hata durumu
            console.log(response.body);
            res.end(response.body);
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Mağaza durum sorgulama örnek kodları[**indirmek için tıklayın.**](/durum-sorgu/paytr_magaza_durum_sorgulama.zip)

1- Aşağıdaki tabloda belirtilen diğer bilgileri https://www.paytr.com/odeme/durum-sorgu adresine POST ile gönderin. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza No  
merchant_key | Mağaza Parola  
merchant_salt | Mağaza Gizli Anahtar  
merchant_oid | Sipariş Numarası  
  
**Pazaryeri Durum Sorgulama**  
Tablodan gelen değerler ile sipariş numarası sorgulanır. Müşteriye ait ödeme tutarı ve toplam ödeme tutarı para birimi ile birlikte ekrana basılır. Yukarıdaki bilgilerde bir yanlışlık olursa hata mesajıda ekranda gösterilir. Aynı zamanda siparişe ait iadeler var ise bu iadeler ekranda belirtilir.

2- Yaptığınız bu isteğe cevap JSON formatında döner.   
a. Eğer sorguda bir hata yoksa status değeri “success” ve aşağıdaki tabloda bulunan bilgiler döner.  
b. Eğer sorguda bir hatanız varsa status değeri “error” döner. Bu durumda hata detayı için “err_msg” içeriğini kontrol etmelisiniz.

Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.

Değişkenler | Açıklamalar | Değerler  
---|---|---  
Status(string) | Sorgulama sonucu.(success veya failed) | success veya error  
payment_amount(string) | İlgili siparişe ait tutar bilgisi | 10,8  
payment_total(string) | Müşterinin ilgili sipariş için ödediği tutar | 10,8  
payment_date(integer) | İşlemin gerçekleşme tarihi | 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss)  
currency(string) | Para birimi | TL(veya TRY), EUR, USD, GBP, RUB  
taksit(string) | Taksit: İşlem taksitli yapıldı ise taksit sayısı | 0,2,3,4,5,6,7,8,9,10,11,12  
kart_marka(string) | İşlem yapılan kartın markası | Örn. WORD, BONUS, vb.  
masked_pan(string) | İşlemin gerçekleşme tarihi | Örn. 455359AAA6747  
odeme_tipi(string) | Ödemenin hangi tipte yapıldığı | KART veya EFT  
test_mode(string) | İşlemin test veya canlı ortamda yapıldığı | 0 veya 1  
returns(string) | Eğer ilgili sipariş içerisinde iade varsa dönecek değer |   
reference_no(string) | Referans No: İade talebinde bulunurken gönderildi ise dönen iade referans numarası | 111111111111(maksimum 64 alfanumarik karakter)  
err_no | Hata numarası | 004  
err_msg | Hata mesajı | merchant_oid ile basarili odeme bulunamadi  
submerchant_payments | Platform ödemeleri |   
  
  


Pazar yeri durum sorgulama örnek kodları: Örnek kodlar içinde nasıl yapılacağı detaylı olarak anlatılmaktadır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
        $merchant_id = "XXX";
        $merchant_key = "XXX";
        $merchant_salt = "XXX";
        $merchant_oid = "XXX";
    
        $paytr_token = base64_encode(hash_hmac('sha256', $merchant_id . $merchant_oid . $merchant_salt, $merchant_key, true));
    
        $post_vals = array('merchant_id' => $merchant_id,
            'merchant_oid' => $merchant_oid,
            'paytr_token' => $paytr_token);
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/durum-sorgu");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 90);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
        //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
        //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
        //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if (curl_errno($ch)) {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
        curl_close($ch);
    
        $result = json_decode($result, 1);
    
        if ($result[status] != 'success') {
            echo $result['err_no'] . " - " . $result['err_msg'];
            exit;
        }
    
        //sipariş tutarı
        echo $result['payment_amount'] . " " . $result['currency'] . "<br>";
    
        //işlem tarihi
        echo $result['payment_date']. "<br>";
    
        //müşteri ödeme tutarı
        echo $result['payment_total'] . " " . $result['currency'] . "<br>";
    
        //siparişteki iadeler (varsa)
    
        /*
    
        Array ( 
        [return_amount] => 1 
        [return_date] => 2021-03-25 23:45:22 
        [return_type] => 
        [date_completed] => 2021-03-25 23:46:02 
        [return_auth_code] =>
        [return_ref_num] => 
        [reference_no] => 111111111111111
        [return_source] => 
        )
    
        */
    
        foreach ($result['returns'] AS $return_success)
            print_r($return_success);
    
        //platform ödemeleri
        foreach ($result['submerchant_payments'] AS $sub_payments)
            print_r($sub_payments);
    ?>
    
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXXXXX'
    merchant_key = b'XXXXXXXXXXXXXXXXXX'
    merchant_salt = 'XXXXXXXXXXXXXXXXXX'
    merchant_oid = ''
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + merchant_oid + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/durum-sorgu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['payment_amount'] + res['currency'])
        print(res['payment_total'] + res['currency'])
        print(res['payment_date'])
        for return_success in res['returns']:
          print(return_success)
        for sub_payments in res['submerchant_payments']:
          print(sub_payments)
    
    else:
        print(res['err_no'] + ' ' + res['err_msg'])    
    
    
    
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
    using System.IO;
    
    namespace WebApplication1.Controllers
    {
        public class durum_sorgu_platform_ornekController : Controller
        {
            public ActionResult durum_sorgu_platform_ornek()
            {
                // ####################### #######################
                //
                // 
    
                string merchant_id = "YYYYYY";
                string merchant_key = "YYYYYYYYYYYYYY";
                string merchant_salt = "YYYYYYYYYYYYYY";
                string merchant_oid = "";
                //
    
                //  #######################
                string Birlestir = string.Concat(merchant_id, merchant_oid, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // #######################
    
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["merchant_oid"] = merchant_oid;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/durum-sorgu", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
    
                        Response.Write(json.payment_amount + "-" + json.currency);
                        Response.Write(json.payment_total + "-" + json.currency);
    
                        foreach (var return_success in json.returns)
                        {
                    //Array 
                    //( 
                    //[return_amount] => 1 
                    //[return_date] => 2021-03-25 23:45:22 
                    //[return_type] => 
                    //[date_completed] => 2021-03-25 23:46:02 
                    //[return_auth_code] =>
                    //[return_ref_num] => 
                    //[reference_no] => 111111111111111
                    //[return_source] => 
                    //)
    
                            Response.Write(return_success);
                        }
    
                        foreach (var sub_payments in json.submerchant_payments)
                        {
                            Response.Write(sub_payments);
                        }
    
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
    
    // API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXXXXX';
    var merchant_key = 'XXXXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXXXX';
    
    var merchant_oid = ''; // Benzersiz işlem numarası.
    
    app.get("/", function (req, res) {
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + merchant_oid + merchant_salt).digest('base64');
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/durum-sorgu',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'merchant_oid': merchant_oid,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send(res_data);
    
        } else {
            //hata durumu
            console.log(response.body);
            res.end(response.body);
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Pazaryeri durum sorgulama örnek kodları[**indirmek için tıklayın.**](/durum-sorgu/PayTR Pazaryeri Durum Sorgulama.zip)
