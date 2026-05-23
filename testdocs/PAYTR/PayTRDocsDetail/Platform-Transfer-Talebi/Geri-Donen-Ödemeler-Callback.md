# Geri Dönen Ödemeler Callback | PayTR

# Geri Dönen Ödemeler Callback

Geri dönen ödemelerden oluşturacağınız transfer talebi sonrasında Success yanıtı almanız ile birlikte hesaptan gönderme talebiniz PayTR sistemi tarafından başarılı olarak alınmış olur. PayTR sistemi talebinizi ortalama 5 dakika içerisinde işleme alacak, gönderdiğiniz trans_info içeriğini kontrol ederek transferleri gerçekleştirecektir. Kontrol sırasında hatalı bilgi tespiti halinde ilgili işlem başarısız olarak işaretlenir. Oluşan sonuç JSON formatında PayTR Mağaza Paneli > Destek & Kurulum > Ayarlar > Platform Transfer Sonucu Bildirim URL olarak tanımladığınız adrese POST edilerek bildirilir.

Tanımlayacağınız Bildirim URL’ye POST metodu ile talebinizin sonucu (başarılı veya başarısız) her işlem için ayrı olarak gönderilir. Gelen değerler içerisinde bulunan result değerini ele alarak talep sonucuna göre işlem yapabilirsiniz.

**PayTR sistemince Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**   


Alan adı | Açıklama | Değer  
---|---|---  
mode | Sabit olarak cashout değeri ile gelir. | cashout  
hash | Hash kontrolünde kullanılacaktır. | ÖRN: wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=  
trans_id | Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer. | ÖRN: 12345aaabbb  
processed_result | Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler. | ÖRN: [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]  
success_total | Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı) | ÖRN: 1  
failed_total | Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı) | ÖRN: 0  
transfer_total | Başarıyla tranasfer edilen işlemlerin toplam tutarı. | ÖRN: 484.48  
account_balance | Transferler sonrasında kalan alt hesap bakiyeniz. | ÖRN: 75  
  
**Bildirim URL’nize PayTR sistemince yapılacak isteğe dönülmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**
    
    
    Örnek (PHP): echo "OK";
    
    
    Örnek (.NET): Response.Write("OK");
    

**ÖNEMLİ UYARILAR:**

  1. Bildirim URL adresinize üye girişi ve benzeri erişim kısıtlaması yapılmamalıdır. Böylece PayTR sistemi bildirimleri kolayca iletebilecektir.

  2. Bildirim URL’nize gelecek bildirimlere döneceğiniz OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır.

  3. Bildirim URL’niz, müşterinizin ödeme sırasında ulaşacağı bir sayfa değildir, PayTR tarafından arka planda (server-side) ödeme sonucunu bildirmek için kullanılır. Bu nedenle, Bildirim URL’nizde kodlama yaparken oturum (SESSION) değerlerini kullanamazsınız. İşlemlerinizi Mağaza sipariş no (merchant_oid) kullanarak gerçekleştirmelisiniz.

  4. Bildirimin PayTR sisteminden geldiğinden ve ulaşım esnasında değiştirilmediğinden emin olmak için, POST içerisindeki hash değeri ile tarafınızca oluşturulacak hash değerinin aynı olduğunu kontrol etmeniz, güvenlik açısından büyük önem arz etmektedir. Bu kontrolü yapmamanız durumunda maddi kayıplar ile karşılaşabilirsiniz.




  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        #################### POST içerisinde gelen örnek veriler ####################
        #
        // [mode] => cashout
        // -> Sabit bu şekilide gelir
        #
        // [hash] => wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=,
        // -> Kontrolde kullanaılacaktır.
        #
        // [trans_id] => 12345aaabbb
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer.
        #
        // [processed_result] => [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler.
        #
        // [success_total] => 1
        // -> Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı)
        #
        // [failed_total] => 0
        // -> Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı)
        #
        // [transfer_total] => 484.48
        // -> Başarıyla tranasfer edilen işlemlerin toplam tutarı.
        #
        // [account_balance] => 0
        // -> Transferler sonrasında kalan alt hesap bakiyeniz.
        ############################################################################
    
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
        $hash = base64_encode( hash_hmac('sha256', $post['merchant_id'].$post['trans_id'].$merchant_salt, $merchant_key, true) );
        #
        ## Oluşturulan hash'i, PayTR'dan gelen post içindeki hash ile karşılaştır (isteğin PayTR'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ###########################################################################
    
        ## trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir.
        $processed_result = json_decode($post['processed_result'],1);
        foreach($processed_result as $trans)
        {
            // Burada her işlem için gerekli veri tabanı vb. işlemleri yapabilirsiniz.
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir.
        echo "OK";
        exit;
    ?>
    
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # POST içerisinde gelen örnek veriler
    
    """
    [mode] : cashout
    -> Sabit bu şekilide gelir
    
    [hash] : wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=,
    -> Kontrolde kullanaılacaktır.
    
    [trans_id] : 12345aaabbb
    -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer.
    
    [processed_result] : [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]
    -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler.
    
    [success_total] : 1
    -> Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı)
    
    [failed_total] : 0
    -> Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı)
    
    [transfer_total] : 484.48
    -> Başarıyla tranasfer edilen işlemlerin toplam tutarı.
    
    [account_balance] : 0
    -> Transferler sonrasında kalan alt hesap bakiyeniz.
    """
    
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
        hash_str = post['merchant_id'] + post['trans_id'] + merchant_salt
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi güvenlik nedeniyle mutlaka yapmanız gerekiyor.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir.
        processed_result = json.loads(post['processed_result'])
    
        for trans in processed_result:
            # Burada her işlem için gerekli veri tabanı vb. işlemleri yapabilirsiniz.
            print(trans)
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    
        //#################### POST içerisinde gelen örnek veriler ####################
        //#
        // [mode] => cashout
        // -> Sabit bu şekilide gelir
        //#
        // [hash] => wszlFsC7nrfCPvP77kdEzzE4smGdV4FWvDibKlXIpRM=,
        // -> Kontrolde kullanaılacaktır.
        //#
        // [trans_id] => 12345aaabbb
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz eşsiz değer.
        //#
        // [processed_result] => [{\"amount\":484.48,\"receiver\":\"XYZ LTD STI\",\"iban\":\"TRXXXXXXXXXXXXXXXXXX\",\"result\":\"success\"}]
        // -> Geri dönen ödeme hesaptan gönderme talebi yaparken PayTR'a gönderdiğiniz değerler.
        //#
        // [success_total] => 1
        // -> Başarıyla transfer edilen işlem sayısı (processed_result içerisinde, result:success olanların sayısı)
        //#
        // [failed_total] => 0
        // -> Hata alan işlem sayısı (processed_result içerisinde, result:failed olanların sayısı)
        //#
        // [transfer_total] => 484.48
        // -> Başarıyla tranasfer edilen işlemlerin toplam tutarı.
        //#
        // [account_balance] => 0
        // -> Transferler sonrasında kalan alt hesap bakiyeniz.
        //############################################################################
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    using Newtonsoft;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;
    using System.IO;
    
    public partial class paytr_geri_donen_odemeler_callback_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key = "AAAAAA";
        string merchant_salt = "XXXXXXXXXXXXXXXX";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e)
        {
    
            string trans_id = Request.Form["trans_id"];
            string merchant_id = Request.Form["merchant_id"];
            string hash = Request.Form["hash"];
            string processed_result = Request.Form["processed_result"];
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string Birlestir = string.Concat(merchant_id, trans_id, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
            if (hash.ToString() != token)
            {
    
                Response.Write("PAYTR notification failed: bad hash");
                return;
            }
    
            //## trans_id bilgisi transfer talebi yaparken PayTR'a gönderdiğiniz her işlem için eşsiz değerdir.
    
            dynamic dynJson = JsonConvert.DeserializeObject(processed_result);
    
            foreach (var item in dynJson)
            {
                // Burada her işlem için gerekli veri tabanı vb. işlemleri yapabilirsiniz.
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
    

Geri dönen ödemeler örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/geri-donen-odemeleri-hesaptan-gonder-2/PayTR Geri Donen Odemeler.zip)
