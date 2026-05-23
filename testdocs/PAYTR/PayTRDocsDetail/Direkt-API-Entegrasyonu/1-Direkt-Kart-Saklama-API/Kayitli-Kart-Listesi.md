# Kayıtlı Kart Listesi | PayTR

# Kayıtlı Kart Listesi

**KULLANICININ KAYITLI KART LİSTESİNİ ALMA (CAPI LIST)**  
1) Bir kullanıcı ödeme işlemine başlarken kullanıcıya PayTR’da kayıtlı olan kartları listelemek için https://www.paytr.com/odeme/capi/list adresine aşağıdaki parametreler ile istek yapın.  


**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
utoken | Kart kayıt sonrası ödeme bildiriminde tarafınıza PayTR sisteminden bildirilen kullanıcıya özel token | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Zorunlu | Açıklama  
---|---|---  
merchant_id (integer) | Evet | Mağaza No: PayTR tarafından size verilen Mağaza numarası  
utoken (string) | Evet | User Token: Kart kayıt sonrası ödeme bildiriminde tarafınıza PayTR sisteminden bildirilen kullanıcıya özel token  
paytr_token (string) | Evet | Paytr Token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
  
  
2) Yapılan isteğe aşağıdaki tabloda bulunan değerler JSON formatında dönecektir. Gönderdiğiniz bilgiler ile herhangi bir eşleşme bulunamadığında cevap boş JSON olarak döner.  


Alan adı / tipi | Zorunlu | Olası/Örnek Değerler  
---|---|---  
status (string) | Status: Hata durumunda error olarak döner, işlem başarılı olduğunda döndürülmez | error  
err_msg (string) | Error Message: İstek başarısız olduğu durumlarda err_msg’de hata nedeni döndürülür | Örnek: Bağlantı hatası oluştu  
ctoken (string) | Card Token: Kullanıcının kayıtlı kartını tanımlayan token |   
last_4 (string) | Son 4: Kayıtlı kartın son 4 hanesi |   
require_cvv (string) | CVV gerekli: Bu kayıtlı kart ile ödeme yapmak için CVV gerekip gerekmediği | 0 veya 1 (Bir kart için 1 dönerse, kart ile ödeme yapılabilmesi için kullanıcıdan CVV bilgisini almanız gerekmektedir)  
month (string) | Ay: Kartının son kullanma tarihinin ay bilgisi | Örnek: 05  
year (string) | Yılı: Kartının son kullanma tarihinin yıl bilgisi | Örnek: 28  
c_bank (string) | Banka: Kartının bankası | Örnek: Yapı Kredi  
c_name | Adı Soyadı: Kullanıcının kart kayıt sırasında girdiği ad soyadı |   
c_brand (string) | Kart Program Ortaklığı İsmi | Örnek: maximum, bonus,world vb.  
c_type (string) | Kart Tipi: Kredi kartı veya banka kartı / ön ödemeli kart | credit veya debit  
businessCard (string) | Şirket Kartı: Kartın şirket kartı olup olmadığı bilgisi | y / n  
initial (string) | Kart Şeması: 2 ve 5 MasterCard, 3 Amex, 4 VISA, 9 TROY | 2,3,4,5,9  
schema (string) | Kartın şeması: Kartın hangi şemaya ait olduğu bilinmiyorsa OTHER döner. | VISA, MASTERCARD, AMEX, TROY, vb.  
  
  
3) Dönen kart bilgileri alınarak kullanıcıya seçebileceği kayıtlı kartlarını listeleyin.  
4) Seçilen kayıtlı kartın ctoken bilgisi ve kullanıcıya ait utoken bilgisini kullanarak ödeme başlatın (Eğer seçilen kart için require_cvv değeri 1 ise kullanıcıya CVV gireceği bir alan sunmalısınız ve ödeme isteğinde CVV'yi göndermelisiniz).

Bu işlem sonunda kayıtlı kart listesi JSON formatında döner.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ## utoken ile kayıtlı kartların listesi alındığında 1nci adım dokümanında ki zorunlu alanları tamamlayamıyoruz.
        ## Kayıtlı bir kart ile ödeme işlemini tamamlama adımını tarif edebilir misiniz?
    
        ## Kullanıcı kart listesi için örnek kodlar ##
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        #
        ## Kart kayıt sonrası ödeme bildiriminde tarafınıza PAYTR sisteminden bildirilen kullanıcıya özel token
        $utoken = "";
        #
        ############################################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $hash_str = $utoken . $merchant_salt;
        $paytr_token=base64_encode(hash_hmac('sha256', $hash_str, $merchant_key, true));
        $post_vals=array(
            'merchant_id'=>$merchant_id,
            'utoken'=>$utoken,
            'paytr_token'=>$paytr_token
        );
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/capi/list");
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
            die("PAYTR CAPI List connection error. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='error')
            die("PAYTR CAPI list failed. Error:".$result['err_msg']);
        else
            print_r($result);
    
    ?>
    
    
    
    # Python 3.6+
    # Kullanıcı kart listesi için örnek kodlar
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'YYYYYYYYYYYYYY'
    merchant_salt = 'ZZZZZZZZZZZZZZ'
    
    # Kart kayıt sonrası ödeme bildiriminde tarafınıza PAYTR sisteminden bildirilen kullanıcıya özel token
    utoken = ''
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = utoken + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'utoken': utoken,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/capi/list', params)
    res = json.loads(result.text)
    
    print(res)
    
    # if res['status'] == 'error':
    #     print('PAYTR CAPI list failed. Error: ' + res['err_msg'])
    # else:
    #     print(res)
    
    
    
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
            public ActionResult List()
            {
                // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
                //
                // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
                string merchant_id = "XXXXXX";
                string merchant_key = "XXXXXX";
                string merchant_salt = "XXXXXX";
                //
    
                // Kart kayıt sonrası ödeme bildiriminde tarafınıza PAYTR sisteminden bildirilen kullanıcıya özel token
                string utoken = "";
                //
    
                //
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(utoken, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["utoken"] = utoken;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/capi/list", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "error")
                    {
                        Response.Write("PAYTR CAPI list failed. Error:" + json.err_msg + "");
                    }
                    else
                    {
                        Response.Write(json);
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
    
    // Kart kayıt sonrası ödeme bildiriminde tarafınıza PAYTR sisteminden bildirilen kullanıcıya özel token.
    var utoken = '';
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(utoken + merchant_salt ).digest('base64');
    
    app.get("/", function (req, res) {
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/capi/list',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'utoken': utoken,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        console.log(res_data);
        console.log(body);
        console.log(response.body);
        if (res_data.status == 'success') {
            res.send(response.body);
    
        } else {
            console.log(response.body);
            res.end(response.body);
        }
    
    });
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

List Card Servisi örnek kodlarını[**indirmek için tıklayın.**](/direkt-api/kart-saklama-api/kayitli-kart-listesi/PayTR List Card.zip)
