# Kayıtlı Kart Silme | PayTR

# Kayıtlı Kart Silme

**KULLANICI KARTINI SİLME (CAPI DELETE)**  


1- Bir kullanıcının kayıtlı kartları arasından bir kart silmek için https://www.paytr.com/odeme/capi/delete adresine aşağıdaki parametreleri göndererek istek yapın.  


**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
utoken | Kart kayıt sonrası ödeme bildiriminde tarafınıza PayTR sisteminden bildirilen kullanıcıya özel token | Evet | -  
ctoken | CAPI LIST servisinden kullanıcınıza ait karta token bilgisi | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Zorunlu | Açıklama  
---|---|---  
merchant_id (integer) | Evet | Mağaza No: PayTR tarafından size verilen Mağaza numarası  
utoken (string) | Evet | User Token: Kart kayıt sonrası ödeme bildiriminde tarafınıza PayTR sisteminden bildirilen kullanıcıya özel token  
paytr_token (string) | Evet | PayTR Token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
ctoken (string) | Evet | Card Token: Kullanıcının kayıtlı kartını tanımlayan token.  
  
  


2- Yapılan isteğe aşağıdaki tabloda bulunan değerler JSON formatında dönecektir. Dönen cevaba göre kullanıcınızı bilgilendirebilirsiniz.  


Alan adı / tipi | Zorunlu | Olası/Örnek Değerler  
---|---|---  
status (string) | Status: Yapılan kart silme isteğinin başarılı ya da başarısız olduğunu belirtir | success veya error  
err_msg (string) | Error Message: İstek başarısız olduğu durumlarda err_msg’de hata nedeni döndürülür | Örnek: Kart yok veya daha önce silinmiş  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
        <?php
    
        ## Kart silmek için örnek kodlar ##
    
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
        ## Kullanıcının kayıtlı kartını tanımlayan token (Kullanıcı kayıtlı kart listesini alma sonucunda dönen yanıtta bulunur)
        $ctoken = "";
        #
        ############################################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $hash_str = $ctoken . $utoken . $merchant_salt;
        $paytr_token=base64_encode(hash_hmac('sha256', $hash_str, $merchant_key, true));
        $post_vals=array(
            'merchant_id'=>$merchant_id,
            'ctoken'=>$ctoken,
            'utoken'=>$utoken,
            'paytr_token'=>$paytr_token
        );
        ############################################################################################
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/capi/delete");
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
            die("PAYTR CAPI Delete connection error. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='success')
            echo "Kart silindi!";
        else
            die("PAYTR CAPI Delete failed. Error:".$result['err_msg']);
    
        ?>
    
    
    
        # Python 3.6+
    # Kart silmek için örnek kodlar
    
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
    
    # Kullanıcının kayıtlı kartını tanımlayan token (Kullanıcı kayıtlı kart listesini alma sonucunda dönen yanıtta bulunur)
    ctoken = ''
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = ctoken + utoken + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'ctoken': ctoken,
        'utoken': utoken,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/capi/delete', params)
    res = json.loads(result.text)
    
    print(res)
    
    # if res['status'] == 'success':
    #     print('Kart silindi!')
    # else:
    #     print('PAYTR CAPI Delete failed. Error:' + res['err_msg'])
    
    
    
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
            public ActionResult Delete()
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
                // Kullanıcının kayıtlı kartını tanımlayan token (Kullanıcı kayıtlı kart listesini alma sonucunda dönen yanıtta bulunur)
                string ctoken = "";
                //
    
                //
                // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
                string Birlestir = string.Concat(ctoken, utoken, merchant_salt);
                HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
                byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
                string paytr_token = Convert.ToBase64String(b);
    
                // Gönderilecek veriler oluşturuluyor
                NameValueCollection data = new NameValueCollection();
                data["merchant_id"] = merchant_id;
                data["ctoken"] = ctoken;
                data["utoken"] = utoken;
                data["paytr_token"] = paytr_token;
                //
    
                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                    byte[] result = client.UploadValues("https://www.paytr.com/odeme/capi/delete", "POST", data);
                    string ResultAuthTicket = Encoding.UTF8.GetString(result);
                    dynamic json = JValue.Parse(ResultAuthTicket);
                    if (json.status == "success")
                    {
                        Response.Write("Kart başarıyla silindi!");
                    }
                    else
                    {
                        Response.Write("PAYTR CAPI Delete failed. reason:" + json.err_msg + "");
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
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'YYYYYYYYYYYYYY';
    var merchant_salt = 'ZZZZZZZZZZZZZZ';
    
    //Kart kayıt sonrası ödeme bildiriminde tarafınıza PAYTR sisteminden bildirilen kullanıcıya özel token
    var utoken = '';
    
    //Kullanıcının kayıtlı kartını tanımlayan token (Kullanıcı kayıtlı kart listesini alma sonucunda dönen yanıtta bulunur)
    var ctoken = '';
    
    var paytr_token = crypto.createHmac('sha256', merchant_key).update(ctoken + utoken + merchant_salt).digest('base64');
    
    app.get("/", function (req, res) {
    
    var options = {
        'method': 'POST',
        'url': 'https://www.paytr.com/odeme/capi/delete',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'merchant_id': merchant_id,
            'ctoken': ctoken,
            'utoken': utoken,
            'paytr_token': paytr_token,
        }
    };
    
    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        var res_data = JSON.parse(body);
    
        if (res_data.status == 'success') {
            res.send('Kart bilgisi basarili sekilde silindi.');
    
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
    

Delete Card Servisi örnek kodlarını[**indirmek için tıklayın.**](/direkt-api/kart-saklama-api/kayitli-kart-silme/PayTR Delete Card API.zip)
