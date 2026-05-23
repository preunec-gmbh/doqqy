# Geri Dönen Ödemeleri Listele | PayTR

# Geri Dönen Ödemeleri Listele

Bu servis ile transfer talebi yapılmış ancak alıcı hesap hatası nedeniyle geri dönen ödemelerin listesine ulaşabilirsiniz. Geri dönen ödemeler mağazanıza ait bir alt hesaba bakiye olarak işlenir. Geri dönen bu ödemeleri tekrar göndermek için “Geri Dönen Ödemeler – Hesaptan Gönder” servisini kullanabilirsiniz.

1- Geri dönen ödemelerin listesini alabilmek için tabloda belirtilen bilgileri POST ile ilgili URL’e gönderin: https://www.paytr.com/odeme/geri-donen-transfer

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet | -  
start_date(string) | Başlangıç Tarihi Formatı: 2021-01-01 00:00:00 (YYYY-MM-DD hh:mm:ss) | Evet | -  
end_date | Bitiş Tarihi Formatı: 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss) | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


* **POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id (string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
start_date (integer) | Başlangıç Tarihi Formatı: 2021-01-01 00:00:00 (YYYY-MM-DD hh:mm:ss) | Evet | -  
end_date(integer) | Bitiş Tarihi Formatı: 2021-01-01 23:59:59 (YYYY-MM-DD hh:mm:ss) | Evet | -  
dummy(integer) | Dummy veri oluşturmak için kullanılır | Hayır | 1 veya 0 (Dummy veri için 1 gönderilmesi gerekmektedir)  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


2- Yaptığınız bu isteğe cevap JSON formatında döner. a. Verilen tarih aralığında eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner. b. Verilen tarih aralığında eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner. c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.

Status success durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır. Satış ve İade işlemlerinde fark olmaksızın aynı değerler döner.

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
Referans No: İşlemin ayırt edici numarası | ref_no | Örnek: 1000001  
Geri dönen ödemenin tespit edildiği tarih | date_detected | Örnek: 2020-06-08  
Ödemenin geri döndüğü tarih | date_reimbursed | Örnek: 2020-06-08  
Transfer talebinde iletilen alıcı adı soyadı | transfer_name | Örnek: TEST USER  
Transfer talebinde iletilen IBAN | transfer_iban | -  
Transfer talebinde iletilen tutar | transfer_amount | Örnek: 35.18  
Transfer talebinde iletilen para birimi. | transfer_currency | Örnek: TL  
Transfer talebinin iletildiği tarih | transfer_date | Örnek: 2020-06-08  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXXXXYYYYYYYY';
        $merchant_salt  = 'XXXXXXXXYYYYYYYY';
    
        ## Gerekli Bilgiler
        #
        $start_date = "2020-05-20 00:00:00";
        $end_date = "2020-06-16 23:59:59";
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
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/geri-donen-transfer");
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
    
        /*
          $result değeri içerisinde dönen yanıt örneği;
    
        [ref_no] => 1000001
        [date_detected] => 2020-06-10
        [date_reimbursed] => 2020-06-08
        [transfer_name] => ÖRNEK İSİM
        [transfer_iban] => TR100000000000000000000001
        [transfer_amount] => 35.18
        [transfer_currency] => TL
        [transfer_date] => 2020-06-08
    
        */
    
        if ($result[status] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result[status] == 'failed')
        {
            // sonuç bulunamadı
            echo "ilgili tarih araliginda islem bulunamadi";
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
    import json
    import requests
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXXXXYYYYYYYY'
    merchant_salt = 'XXXXXXXXYYYYYYYY'
    
    # Gerekli Bilgiler
    start_date = '2020-05-20 00:00:00'
    end_date = '2020-06-16 23:59:59'
    # Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + start_date + end_date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'start_date': start_date,
        'end_date': end_date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/geri-donen-transfer', params)
    res = json.loads(result.text)
    
    """
    res değeri içerisinde;
    ['ref_no']              - 1000001
    ['date_detected']       - 2020-06-10
    ['date_reimbursed']     - 2020-06-08
    ['transfer_name']       - ÖRNEK İSİM
    ['transfer_iban']       - TR100000000000000000000001
    ['transfer_amount']     - 35.18
    ['transfer_currency']   - TL
    ['transfer_date']       - 2020-06-08
    bilgileri dönmektedir.
    """
    
    if res['status'] == 'success':
        # VT işlemleri vs.
        print(res)
    elif res['status'] == 'failed':
        print('İlgili tarih araliginda islem bulunamadi')
    else:
        print(res['err_no'] + ' - ' + res['err_msg'])
    
    
    
      // ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
      //  #                                                                                          #
      //  ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
      //  #
      //  ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
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
        public class paytr_geri_donen_odemeler_listele_ornekController : Controller
        {
            public ActionResult paytr_geri_donen_odemeler_listele_ornek()
            {
                // ####################### GEREKLİ BİLGİLER #######################
                //
                // 
    
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
    
                //     #######################
                string start_date = "2021-11-01 00:00:00";
                string end_date = "2021-11-29 23:59:59";
                //  Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
    
                //  ####################### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
                string Birlestir = string.Concat(merchant_id,start_date,end_date,merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // #######################
    
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["start_date"] = start_date;
                data["end_date"] = end_date;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/geri-donen-transfer", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    /*
                      $result değeri içerisinde dönen yanıt örneği;
    
                    [ref_no] => 1000001
                    [date_detected] => 2020-06-10
                    [date_reimbursed] => 2020-06-08
                    [transfer_name] => ÖRNEK İSİM
                    [transfer_iban] => TR100000000000000000000001
                    [transfer_amount] => 35.18
                    [transfer_currency] => TL
                    [transfer_date] => 2020-06-08
    
                    */
    
                    if (json.status == "success")
                    {
                         // VT işlemleri vs.
                        Response.Write(json);
    
                    }
    
                   else if (json.status == "failed")
                    {
                        // sonuç bulunamadı
                        Response.Write("İlgili tarih araliginda islem bulunamadi");
    
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
    
    //  ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXXXXYYYYYYYY';
    var merchant_salt = 'XXXXXXXXYYYYYYYY';
    
    app.get("/list", function (req, res) {
        //  Başlangıç / Bitiş tarihi. En fazla 31 gün aralık tanımlanabilir.
        var start_date = '2020-11-01 00:00:00';
        var end_date = '2020-11-29 23:59:59';
    
        //  ####################### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/geri-donen-transfer',
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
    
                /*
    
                [ref_no] => 1000001
                [date_detected] => 2020-06-10
                [date_reimbursed] => 2020-06-08
                [transfer_name] => ÖRNEK İSİM
                [transfer_iban] => TR100000000000000000000001
                [transfer_amount] => 35.18
                [transfer_currency] => TL
                [transfer_date] => 2020-06-08
    
                */
                // VT işlemleri vs.
                res.send(res_data);
    
            } else {
    
                // Hata durumu
    
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/send", function (req, res) {
    
        var trans_id = '';
        var trans_info = [{
            'amount': '1283',
            'receiver': 'XYZ LTD ŞTİ',
            'iban': 'TRXXXXXXXXXXXXXXXXXXXXX'
        }];
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + trans_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/hesaptan-gonder',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
    
                'trans_info': JSON.stringify(trans_info),
                'trans_id': trans_id,
                'paytr_token': paytr_token,
                'merchant_id': merchant_id,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(callback.merchant_id + callback.trans_id + merchant_salt).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        var processed_result = JSON.parse(callback.processed_result);
    
        for (const [key, value] of Object.entries(processed_result)) {
            console.log(`${key}: ${value}`);
        }
    
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Geri dönen ödemeler örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/geri-donen-odemeleri-listele/paytr_geri_donen_odemeler.zip)
