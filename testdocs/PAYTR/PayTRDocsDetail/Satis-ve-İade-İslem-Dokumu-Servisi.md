# Satış ve İade İşlem Dökümü Servisi | PayTR

# Satış ve İade İşlem Dökümü Servisi

Bu servisi ile iletilen tarih aralığındaki (en fazla 3 gün) yapılan satış ve iade işlemlerinin dökümünü alabilirsiniz.

1- İşlem detaylarını gerçek istediğiniz tarih / saat ve aşağıdaki tabloda belirtilen diğer bilgileri https://www.paytr.com/rapor/islem-dokumu adresine POST metodu ile gönderin. 

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(string) | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet | -  
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
dummy(int) | Demo Veri: Servisten dönen verileri simule etmek için kullanılır. Dönen değerler gerçek değildir, test amaçlı gözlem içindir. | Hayır | 0 veya 1  
paytr_token(string) | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Evet | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız.  
  
  
  


2- Yaptığınız bu isteğe cevap JSON formatında döner. a. Verilen tarih aralığında eğer herhangi bir işlem / hareket yoksa status değeri failed olarak döner. b. Verilen tarih aralığında eğer herhangi bir işlem varsa status değeri success ve aşağıdaki tabloda bulunan bilgiler döner. c. Eğer sorguda bir hatanız varsa status değeri error döner. Bu durumda hata detayı için err_msg içeriğini kontrol etmelisiniz.

Status success durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır. Satış ve İade işlemlerinde fark olmaksızın aynı değerler döner.

Açıklama | Alan adı / tipi | Değerler  
---|---|---  
İşlem Tipi: Yapılan işlemin tipi. | islem_tipi (string) | S (satış) veya I (iade)  
Net Tutar: Kesinti sonrası kalan tutar. | net_tutar (string) | Örn. 9.76  
Kesinti Tutarı: İşlem için kesilen tutar. | kesinti_tutari (string) | Örn. 0.24  
Kesinti Oranı: İşlem için kesilen oran. | kesinti_orani (string) | Örn. 2.35  
İşlem Tutarı: Yapılan işlemin tutarı. | islem_tutari (string) | Örn. 10.00  
Ödeme Tutarı: İşlem tutarı üzerinde bir ödeme olması durumunda dönülür. | odeme_tutari (string) | Örn. 10.00  
İşlem Tarihi: İşlemin yapıldığı tarih. | islem_tarihi (string) | Örn. 13.01.2021  
Para Birimi: İşlemin para birimi. | para_birimi (string) | TL, USD, EUR, GBP, RUB  
Taksit: İşlem taksitli yapıldı ise taksit sayısı. | taksit (string) | 0,2,3,4,5,6,7,8,9,10,11,12  
Kart Markası: İşlem yapılan kartın markası. | kart_marka (string) | Örn. WORD, BONUS, vb.  
Kart No: İşlem yapılan maskeli kart numarası. | kart_no (string) | Örn. 455359AAA6747  
Sipariş Numarası: İşlemin sipariş numarası. | siparis_no (string) | Örn. ABC123  
Ödeme Tipi: Ödemenin hangi tipte yapıldığı. | odeme_tipi (string) | KART veya EFT  
  
  


  * PHP
  * Python
  * .NET
  * NODEJS


    
    
    <?php
    
        ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR ##########################
        #                                                                                          #
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXXYYYYYY';
        $merchant_salt  = 'YYYYYYXXXXXX';
    
        ## Gerekli Bilgiler
        #
        $start_date = "2020-06-02 00:00:00";
        $end_date = "2020-06-04 23:59:59";
        # Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
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
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/rapor/islem-dokumu");
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
    
        if ($result['status'] == 'success')
        {
            // VT işlemleri vs.
            print_r($result);
        }
        elseif ($result['status'] == 'failed')
        {
            // sonuç bulunamadı
            echo "ilgili tarih araliginda islem bulunamadi";
        }
        else
        {
            // Hata durumu
            echo $result['err_no'] . " - " . $result['err_msg'];
        }
    
    
    # Python 3.6+
    # İşlem dökümü servisi için kullanılacak örnek kod
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXX'
    merchant_salt = 'XXXXXX'
    
    # Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
    start_date = '2021-02-02 00:00:00'
    end_date = '2021-02-04 23:59:59'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + start_date + end_date + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'start_date': start_date,
        'end_date': end_date,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/rapor/islem-dokumu', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(result.text)
    elif res['status'] == 'failed':
        print('ilgili tarih araliginda islem bulunamadi')
    else:
        print('PAYTR BIN detail request error. Error: ' + res['err_msg'])
    
    
    
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
                // ########################### İŞLEM DÖKÜMÜ ALMAK  İÇİN ÖRNEK KODLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                string start_date = "2021-01-13 00:00:00";
                string end_date = "2021-01-13 23:59:59";
                // Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
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
                    byte[] result = client.UploadValues("https://www.paytr.com/rapor/islem-dokumu", "POST", data);
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
                        Response.Write("No transaction was found in date duration");
    
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
    
        //Başlangıç / Bitiş tarihi. En fazla 3 gün aralık tanımlanabilir.
        var start_date = '2020-05-01 00:00:00';
        var end_date = '2020-05-01 23:59:59';
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(merchant_id + start_date + end_date + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/rapor/islem-dokumu',
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
    

İşlem Dökümü Servisi örnek kodlarını [**indirmek için tıklayın.**](/islem-dokumu/paytr_islem_dokumu.zip)
