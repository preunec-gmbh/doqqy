# Geri Dönen Ödemeleri Hesaptan Gönder | PayTR

# Geri Dönen Ödemeleri Hesaptan Gönder

Bu servis ile transfer talebi yapılmış ancak alıcı hesap hatası nedeniyle geri dönen ödemeler için tekrar ödeme isteği gönderebilirsiniz. Geri dönen ödemeler mağazanıza ait bir alt hesaba bakiye olarak işlenir. Geri dönen bu ödemelerin listesine “Geri Dönen Ödemeler – Listele API” servisi ile ulaşabilirsiniz.

1- Hesaptan ödeme transferi gönderebilmek için tabloda belirtilen bilgileri POST ile ilgili URL’e gönderin: https://www.paytr.com/odeme/hesaptan-gonder

**Token üretiminde kullanılacak veriler:**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet | -  
trans_id(string) | Transfer ID: Transfer işlemi için belirlediğiniz benzersiz işlem numarası. | Evet | En fazla 64 karakter, Alfa numerik  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id(integer) | Mağaza no: PayTR tarafından size verilen Mağaza numarası | Evet | -  
trans_id(string) | Transfer ID: Transfer işlemi için belirlediğiniz **benzersiz** işlem numarası. | Evet | En fazla 64 karakter, Alfa numerik  
trans_info(JSON) | Transfer Bilgisi: Transfer tutarı, alıcı ismi ve IBAN değerlerini içeren JSON formatında içerik. (Nasıl tanımlanacağı için örnek koda bakın) | Evet | -  
paytr_token(string) | PayTR Token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir (Hesaplama için örnek koda bakın) | Evet | -  
  
  


2- Yaptığınız bu isteğe cevap JSON formatında döner.

a. Yapılan istek geçerli ise status değeri **success** ve **trans_id** alanında gönderdiğiniz işlem numarası döner.  
b. Eğer sorguda bir hatanız varsa status değeri **error** döner. Bu durumda hata detayı için **err_msg** içeriğini kontrol etmelisiniz.  


3- Success yanıtı almanız ile birlikte hesaptan gönderme talebiniz PayTR sistemi tarafından başarılı olarak alınmış olur. PayTR sistemi talebinizi ortalama 5 dakika içerisinde işleme alacak, gönderdiğiniz trans_info içeriğini kontrol ederek transferleri gerçekleştirecektir. Kontrol sırasında hatalı bilgi tespiti halinde ilgili işlem başarısız olarak işaretlenir. Oluşan sonuç JSON formatında **PayTR Mağaza Paneli > Ayarlar > Platform Transfer Sonucu Bildirim URL** olarak tanımladığınız adrese POST edilerek bildirilir.

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
        $trans_id="PHG".time();
        $trans_info=array();
        //amount 100 ile çarpılarak gönderilir!!
        $trans_info[]=array("amount"=>"1283",
            "receiver"=>"XYZ LTD ŞTİ",
            "iban"=>"TRXXXXXXXXXXXXXXXXXXXXX");
        //...$trans_info[]=...
        #
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
    
        $paytr_token=base64_encode(hash_hmac('sha256',$merchant_id.$trans_id.$merchant_salt, $merchant_key, true));
    
        $post_vals=array('trans_info'=>json_encode($trans_info),
            'trans_id'=>$trans_id,
            'paytr_token'=>$paytr_token,
            'merchant_id'=>$merchant_id
        );
        #
        ############################################################################################
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/hesaptan-gonder");
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
    
        if(curl_errno($ch))
        {
            echo curl_error($ch);
            curl_close($ch);
            exit;
        }
    
        curl_close($ch);
    
        $result_raw=$result;
        $result=json_decode($result,1);
    
        if($result['status']=='success')
        {
            //status ve trans_id içerir
            print_r($result_raw);
        }
        else//status=>error
        {
            //status ve err_no - err_msg içerir
            print_r($result_raw);
        }
    
    
    # Python 3.6+
    
    import base64
    import hmac
    import hashlib
    import json
    import requests
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'XXXXXXXXYYYYYYYY'
    merchant_salt = 'XXXXXXXXYYYYYYYY'
    
    # Gerekli Bilgiler
    trans_id = 'PHG' + random.randint(1, 9999999).__str__()
    trans_info = [
        {
            'amount': '1283',  # amount 100 ile çarpılarak gönderilir!!
            'receiver': 'XYZ LTD ŞTİ',
            'iban': 'TRXXXXXXXXXXXXXXXXXXXXX'
        }
    ]
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + trans_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'trans_info': json.dumps(trans_info),
        'trans_id': trans_id,
        'merchant_id': merchant_id,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/hesaptan-gonder', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        # status ve trans_id içerir
        print(res)
    else:
        # status = error
        # status ve err_no - err_msg içerir
        print(res['err_no'] + ' - ' + res['err_msg'])
    
    
    
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
    
    namespace WebApplication1.Controllers
    {
        class PayTR
        {
            public string amount { get; set; }
            public string receiver { get; set; }
            public string iban { get; set; }
        }
    
        public class paytr_geri_donen_odemeler_hesaptan_gonder_ornekController : Controller
        {
            public ActionResult paytr_geri_donen_odemeler_hesaptan_gonder_ornek()
            {
                List<PayTR> TransferInfo = new List<PayTR>();
                PayTR info = new PayTR();
                info.amount = Convert.ToString(10 * 100); //amount 100 ile çarpılarak gönderilir.
                info.receiver = "XYZ LTD ŞTİ";
                info.iban = "TRXXXXXXXXXXXXXXXXXXXXX";
    
                TransferInfo.Add(info);
    
                string TransInfo = Newtonsoft.Json.JsonConvert.SerializeObject(TransferInfo);
    
                // ####################### #######################
                //
                // 
                string merchant_id = "AAAAAA";
                string merchant_key = "XXXXXXXXXXXXXXXX";
                string merchant_salt = "XXXXXXXXXXXXXXXX";
                //
                // #######################
                string TransId = "ZZZZZZZ"; 
    
                //  #######################
                string Birlestir = string.Concat(merchant_id, TransId, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // #######################
    
                NameValueCollection data = new NameValueCollection();
                data["trans_info"] = TransInfo;
                data["trans_id"] = TransId;
                data["paytr_token"] = paytr_token;
                data["merchant_id"] = merchant_id;
    
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/hesaptan-gonder", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
    
                    if (json.status == "success")
                    {
                        //status ve trans_id içerir
                        Response.Write(json);
    
                    }
                    else
                    {
                        // Hata durumu
                        //status=>error
                        Response.Write("Error. reason:" + json.err_no + "-" + json.err_msg);
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
    

Geri dönen ödemeler örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/geri-donen-odemeleri-hesaptan-gonder/PayTR Geri Donen Odemeler.zip)
