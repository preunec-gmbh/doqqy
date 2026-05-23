# Transfer Talimatının Sonucunun Alınması (Opsiyonel) | PayTR

# Transfer Talimatının Sonucunun Alınması (Opsiyonel)

PAYTR sistemi, transfer işlemlerinin sonuçlanması sonrası Mağazanın belirlediği URL’e bilgi verir.

**İstek (REQUEST) yapılacak URL: Platform Transfer Sonucu Bildirim URL (Mağaza Paneli > Destek & Kurulum > AYARLAR sayfasına Mağaza tarafından girilmelidir))**

**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
trans_id | Transfer talebinde belirttiğiniz trans_id değerlerini içeren JSON string | Evet | -  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet | -  
  
  


**POST REQUEST içeriğinde gönderilecek değerler:**

Alan adı / tipi | Zorunlu | Açıklama | Kısıtlar  
---|---|---|---  
trans_ids (JSON string) | Evet | Transfer talebinde belirttiğiniz trans_id değerlerini içeren JSON string |   
hash (string) | Evet | paytr_token: İsteğin PAYTR’dan geldiğine ve içeriğin değişmediğine emin olmanız için oluşturulan değer | Hesaplama ve kontrol hakkında lütfen örnek kodları inceleyin  
  
  


**Örnek POST:**
    
    
    [hash] => Of0/yvgTii/+lGD3o+J0u8xXriVqlPIrvsZsv4cLhM4=
    [trans_ids] => ["dcbbe0b9fd25154d73c","dc8c509efc6450d30","9310d84d3bf"]

**Yanıt (RESPONSE):**

PAYTR’dan gelen isteğe ekrana OK basarak yanıt vermeniz beklenmektedir. Bu yanıtın alınmadığı durumda istek tekrarlanacaktır.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        $post = $_POST;
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        ###########################################################################
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        #
        ## POST değerleri ile hash oluştur.
        $post["trans_ids"]=str_replace("\\", "", $post["trans_ids"]);
        $hash = base64_encode( hash_hmac('sha256', $post['trans_ids'].$merchant_salt, $merchant_key, true) );
        #
        ## Oluşturulan hash'i, PayTR'dan gelen post içindeki hash ile karşılaştır (isteğin PayTR'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ###########################################################################
    
        ## $post['trans_ids'] içerisinde daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgileri JSON formatında gelir
        ## trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir
        $trans_ids = json_decode($post['trans_ids'],1);
        foreach($trans_ids as $trans_id)
        {
            ## Örn: Burada $trans_id ile veritabanınızdan transfer talebini tespit edip ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir.
        echo "OK";
        exit;
    ?>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    
    import base64
    import hashlib
    import hmac
    import json
    
    from django.shortcuts import render, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    
    @csrf_exempt
    def callback(request):
        if request.method != 'POST':
            return HttpResponse(str(''))
    
        post = request.POST
    
        # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        merchant_key = b'YYYYYYYYYYYYYY'
        merchant_salt = 'ZZZZZZZZZZZZZZ'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        post['trans_ids'] = post['trans_ids'].replace('\\', '')
        hash_str = post['trans_ids'] + merchant_salt
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # post['trans_ids'] içerisinde daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgileri JSON formatında gelir
        # trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir
        trans_ids = json.loads(post['trans_ids'])
    
        for ids in trans_ids:
            # Örn: Burada trans_id ile veritabanınızdan transfer talebini tespit edip ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
            print(ids)
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class transfer_sonucu_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYY";
        string merchant_salt    = "ZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string trans_ids = Request.Form["trans_ids"];
            string hash = Request.Form["hash"];
    
            trans_ids = trans_ids.Replace(@"\","");
    
            string Birlestir = string.Concat(trans_ids, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
            }
    
            //###########################################################################
    
            ## trans_ids: Daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgilerini içeren JSON 
            ## (trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir)
            ## Örn: Burada trans_ids JSON verisini DECODE edip, çıktıdaki her bir trans_id ile veritabanınızdan transfer talebini tespit ederek ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
    
            dynamic dynJson = JsonConvert.DeserializeObject(trans_ids);
            foreach (var item in dynJson)
            {
                ## Örn: Burada $trans_id ile veritabanınızdan transfer talebini tespit edip ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
            }
    
            // Bildirimin alındığını PayTR sistemine bildir.  
            Response.Write("OK");    
        }
    }
    
    
    var request = require('request');
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'MAGAZA_NO';
    var merchant_key = 'XXXXXXXXXXX';
    var merchant_salt = 'YYYYYYYYYYY';
    
    app.get("/send", function (req, res) {
    
        // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
        var merchant_oid = '';
        // Eşsiz transfer numarası
        var trans_id = '';
        // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        var submerchant_amount = '';
        // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        var total_amount = '';
        // Satıcının banka hesabı için ad soyad/ünvanı
        var transfer_name = '';
        // Satıcının banka hesabı IBAN numarası
        var transfer_iban = '';
    
        var hash_str = merchant_id + merchant_oid + trans_id + submerchant_amount + total_amount + transfer_name + transfer_iban;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(hash_str + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/platform/transfer',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'merchant_oid': merchant_oid,
                'trans_id': trans_id,
                'submerchant_amount': submerchant_amount,
                'total_amount': total_amount,
                'transfer_name': transfer_name,
                'transfer_iban': transfer_iban,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
    
                /*
                    Başarılı yanıt örneği:
                    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
                    Başarısız yanıt örneği:
                    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
                */
    
                res.send(res_data);
    
            } else {
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
    
        var callback = req.body;
        var trans_ids = callback.trans_ids;
    
        var trans_ids = trans_ids.replace('\\', '');
    
        // POST değerleri ile hash oluştur.
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(trans_ids + merchant_salt).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        // ## trans_ids: Daha önce PayTR'a ilettiğiniz transfer taleplerinden tamamlanan transferlerin trans_id bilgilerini içeren JSON 
        // ## (trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir)
        // ## Örn: Burada trans_ids JSON verisini DECODE edip, çıktıdaki her bir trans_id ile veritabanınızdan transfer talebini tespit ederek ilgili kullanıcınıza bilgilendirme gönderebilirsiniz (email, sms vb.)
        var processed_result = JSON.parse(trans_ids);
    
        console.log(processed_result);
    
        // Bildirimin alındığını PayTR sistemine bildir.  
        res.send("OK");
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Transfer talimatının sonucunun alınması örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/transfer-talimatinin-sonucunun-alinmasi/PayTR Platform Transfer Talebi.zip)
