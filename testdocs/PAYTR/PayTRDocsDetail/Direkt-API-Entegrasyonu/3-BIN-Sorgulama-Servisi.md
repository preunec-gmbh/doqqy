# BIN Sorgulama Servisi | PayTR

# 4.3 BIN Sorgulama Servisi

BIN sorgulama servisi ile bir BIN numarası gönderip kartın detaylı bilgilerine ulaşabilirsiniz.

1- Detayını sorgulamak istediğiniz kartın BIN numarasını (kart numarasının ilk 6 veya 8 hanesini) ve aşağıdaki tabloda belirtilen diğer bilgileri https://www.paytr.com/odeme/api/bin-detail adresine POST ile gönderin.   


**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
bin_number | BIN Numarası: Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın. | Evet | Maksimum 8 hane olacak şekilde.  
merchant_id | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Zorunlu | Açıklama  
---|---|---  
merchant_id(integer) | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası  
bin_number(string) | Evet | BIN Numarası: Kart numarasının ilk 6 veya 8 hanesi  
paytr_token(string) | Evet | Paytr Token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
  
  
2- Yaptığınız bu isteğe cevap JSON formatında döner.  
a. BIN Numarası tanmlı değilse (Örneğin bir yurtdışı kartı ise) status değeri “failed” olarak döner.  
b. Eğer BIN numarası tanımlı ise status değeri “success” olarak döner ve aşağıdaki tabloda bulunan bilgiler döner.  
c. Eğer sorguda bir hatanız varsa status değeri “error” döner. Bu durumda hata detayı için “err_msg” içeriğini kontrol etmelisiniz.   


Status “success” durumunda dönen diğer bilgiler aşağıdaki tabloda detaylandırılmıştır.   


Alan adı / tipi | Değerler | Açıklama  
---|---|---  
status (string) | success, error veya failed | Status: Sorgulama sonucu  
cardType (string) | credit / debit | Kart Türü: Kartın tipi  
businessCard (string) | y / n | Şirket Kartı: Kartın şirket kartı olup olmadığı bilgisi  
bank (string) | Örnek: Yapı Kredi | Banka: Kartın bankası  
brand (string) | Örnek: axess, bonus,cardfinans, combo,world, paraf, advantage,maximum,saglamkart | Kart Program Ortaklığı İsmi: Kartın program ortaklığı ismi(Kart bir program ortaklığına dahil değil ise değer none olur. Bu durumda ilgili kart ile PayTR üzerinden taksitli işlem yapılamaz.)  
schema (string) | VISA, MASTERCARD, AMEX, TROY, OTHER | Kartın hangi şemaya ait olduğu. (Kartın hangi şemaya ait olduğu bilinmiyorsa OTHER döner.)  
bankCode (int) | Örnek: 0010 | Banka Kodu: Kart bankasının kodu  
allow_non3d (string) | Y(yes) ve N(no) | Non-3D işlem izni sonucu  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ## BIN sorgulama servisi için kullanılacak örnek kod ##
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'XXXXXX';
        $merchant_salt  = 'XXXXXX';
        #
        ## Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
        $bin_number = "";
        #
        ############################################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $hash_str = $bin_number . $merchant_id . $merchant_salt;
        $paytr_token=base64_encode(hash_hmac('sha256', $hash_str, $merchant_key, true));
        $post_vals=array(
            'merchant_id'=>$merchant_id,
            'bin_number'=>$bin_number,
            'paytr_token'=>$paytr_token
        );
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/bin-detail");
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
            die("PAYTR BIN detail request timeout. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die("PAYTR BIN detail request error. Error:".$result['err_msg']);
        elseif($result['status']=='failed')
            die("BIN tanımlı değil. (Örneğin bir yurtdışı kartı)");
        else
            print_r($result);
    
    ?>
    
    
    
    # Python 3.6+
    # BIN sorgulama servisi için kullanılacak örnek kod
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXX'
    merchant_key = b'XXX'
    merchant_salt = 'XXX'
    
    # Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
    bin_number = 'XXXXXX'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = bin_number + merchant_id + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'bin_number': bin_number,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/bin-detail', params)
    res = json.loads(result.text)
    
    if res['status'] == 'error':
        print('PAYTR BIN detail request error. Error: ' + res['err_msg'])
    elif res['status'] == 'failed':
        print('BIN tanımlı değil. (Örneğin bir yurtdışı kartı)')
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
    
    namespace WebApplication1.Controllers
    {
        public class HomeController : Controller
        {
            public ActionResult GetBinDetail()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "XXXXXX";
                string merchant_key = "XXXXXX";
                string merchant_salt = "XXXXXX";
                //
                // Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
                string bin_number = "";
                //
                // ###########################################################################
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(bin_number, merchant_id, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["bin_number"] = bin_number;
                data["paytr_token"] = paytr_token;
                //
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/bin-detail", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "success")
                    {
                        Response.Write(json);
                    }
                                else if (json.status == "failed")
                    {
                        Response.Write("BIN tanımlı değil. (Örneğin bir yurtdışı kartı)");
                    }
                                else if (json.status == "error")
                    {
                        Response.Write("PAYTR BIN detail request error. Error:" + json.err_msg + "");
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
    
    // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'XXXXXX';
    var merchant_salt = 'XXXXXX';
    // Sorgulama yapılmak istenen karta ait kart numarasının ilk 6 veya 8 hanesi. Maksimum doğrulama için 8 hane kullanın.
    var bin_number = 'XXXXXX';
    // Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. //
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(bin_number + merchant_id + merchant_salt).digest('base64');
    
    app.get("/", function (req, res) {
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/api/bin-detail',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'bin_number': bin_number,
            'paytr_token': paytr_token,
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
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

  


BIN Sorgulama örnek kodları[**indirmek için tıklayın.**](/direkt-api/bin-sorgulama-servisi/PayTR_BIN_Sorgulama_Servisi.zip)
