# Havale/EFT iFrame API 2. Adım | PayTR

# Havale/EFT iFrame API 2. Adım

**Mağaza bildirim sayfasına (Bildirim URL) yapılacak isteğe Üye işyerinin dönmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**

**Önemli:** OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır. Bildirim URL sayfası, müşterinin göreceği bir sayfa değildir, PayTR ile Mağaza arasında arka planda (server-side) bir iletişimde kullanılır. OK yanıtı alınmayan ödeme işlemleri, Mağaza Paneli'ndeki İşlemler sayfasında “Devam Ediyor” olarak görünür. PayTR sistemi OK cevabını istendiği şekilde almadığı durumda, bildirimin başarısız olduğunu varsayarak bir süre daha tekrar tekrar bildirim göndermeye çalışacaktır.

**Önemli:** PayTR bildirim sistemi, ağ trafik sorunları ve benzeri nedenlerden dolayı aynı ödeme işlemi için birden fazla onay bildirimi gönderebilir. Bu durumda yalnızca ilk bildirim göz önünde bulundurulmalı, sonraki bildirimler için müşteriye tekrar ürün/hizmet sunulmamalı, yalnızca OK yanıtı gönderilerek işlem sonuçlandırılmalıdır. Tekrarlayan bildirimlerin tespiti Mağaza sipariş no (merchant_oid) temel alınarak yapılabilir.

  * Ödeme işleminin başarısız olması durumunda bildirim POST içeriğinde “failed_reason_code” ve “failed_reason_msg” olmak üzere iki alan daha gelir. Bu alanlar hash hesaplamasında kullanılmaz. Bu mesajlar istenirse müşteriyi bilgilendirme amacıyla eposta veya mağaza mesaj sistemi üzerinden müşteriye iletilebilir

failed_reason_code | failed_reason_msg | Açıklama  
---|---|---  
4 | Havale/EFT ödemesi tespit edilemedi. | Ödeme bildirimi formunda müşterinin belirtmiş olduğu bilgiler ile ödemeye ulaşılamamıştır  
5 | Havale/EFT ödeme tutarı yetersiz. Lütfen gönderdiğiniz tutar kadar bildirim yapın. | Müşterinin bankaya gönderdiği tutar, alışveriş tutarından (payment_amount) az olduğundan onay verilmemiştir.  
6 | Müşteri ödeme yapmaktan vazgeçti ve ödeme sayfasından ayrıldı. | Müşteri, kendisine tanınmış olan işlem süresinde (1. ADIM’da tanımlanan timeout_limit değeri) işlemini tamamlamadı veya müşteri ödeme sayfasını kapatarak işlemi sonlandırdı.  
7 | Bildiriminiz alınmadı, lütfen önceki bildiriminizin kontrolünün sonuçlanmasını bekleyin. | Müşteri henüz kontrolü sonuçlanmamış bir ödeme bildirimi bulunurken, tekrar bildirim yaptı.  
41 | Havale/EFT ödemesi ile bildirimdeki Ad Soyadı uyuşmuyor. | Müşterinin bildirim yaparken girdiği Ad Soyadı ile banka kayıtlarındaki Ad Soyadı uyuşmadı.  
42 | Havale/EFT ödemesi ile bildirimdeki TCKN uyuşmuyor. | Müşterinin bildirim yaparken girdiği TCKN ile banka kayıtlarındaki TCKN uyuşmadı.  
43 | Bu Havale/EFT ödemesi daha önce onaylanmış. | Müşterinin bildirimi sonrası yapılan kontrolde, bu ödemenin daha önce bildirilip onay aldığı görüldü.  
44 | Bu Havale/EFT ödemesi iade edilmiş. | Müşterinin bildirimi sonrası yapılan kontrolde, bu ödemenin daha önce iade edildiği görüldü.  
45 | Dekonttaki iki farklı Ad-Soyadından yalnızca birisi yazılmış | Müşterinin bildirimi sonrası yapılan kontrolde,dekontta yazan iki Ad Soyadı bilgisinden yalnızca birisinin girildiği görüldü  
  
  


  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
    ## 2. ADIM için örnek kodlar ##
    
    ## ÖNEMLİ UYARILAR ##
    ## 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    ## 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
    ## veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    ## 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
    ## siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
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
    $hash = base64_encode( hash_hmac('sha256', $post['merchant_oid'].$merchant_salt.$post['status'].$post['total_amount'], $merchant_key, true) );
    #
    ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if( $hash != $post['hash'] )
        die('PAYTR notification failed: bad hash');
    ###########################################################################
    
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
    ## 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
    /* Sipariş durum sorgulama örnek
    $durum = SQL
    if($durum == "onay" || $durum == "iptal"){
            echo "OK";
            exit;
    }*/
    
    if( $post['status'] == 'success' ) { ## Ödeme Onaylandı
    
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi onaylayın.
    ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
    ## 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
    ## değişebilir. Güncel tutarı $post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
    } else { ## Ödemeye Onay Verilmedi
    
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi iptal edin.
    ## 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
    ## $post['failed_reason_code'] - başarısız hata kodu
    ## $post['failed_reason_msg'] - başarısız hata mesajı
    
    }
    
    ## Bildirimin alındığını PayTR sistemine bildir.
    echo "OK";
    exit;
    ?>
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # 2. ADIM için örnek kodlar
    
    """
    ÖNEMLİ UYARILAR
    1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
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
        merchant_key = b'XXXXXXXXXXXXXXXX'
        merchant_salt = 'XXXXXXXXXXXXXXXX'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        """
        BURADA YAPILMASI GEREKENLER
        1) Ödeme durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
        Ödeme durum sorgulama örnek
        durum = SQL
    
        if(durum == 'onay'){
             return HttpResponse(str('OK'))
        """
    
        if post['status'] == 'success':
            """
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi onaylayın.
    ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
    ## 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
    ## değişebilir. Güncel tutarı $post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
            """
        else:
            """
    ## BURADA YAPILMASI GEREKENLER
    ## 1) Siparişi iptal edin.
    ## 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
    ## $post['failed_reason_code'] - başarısız hata kodu
    ## $post['failed_reason_msg'] - başarısız hata mesajı
            """
    
        # Bildirimin alındığını PayTR sistemine bildir.
        return HttpResponse(str('OK'))
    
    
    // 2. ADIM için örnek kodlar
    
    // ÖNEMLİ UYARILAR!
    // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
    // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
    // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
    // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
    // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class bildirim_url_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYYYYYYYY";
        string merchant_salt    = "ZZZZZZZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string merchant_oid = Request.Form["merchant_oid"];
            string status = Request.Form["status"];
            string total_amount = Request.Form["total_amount"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(merchant_oid, merchant_salt, status, total_amount);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
                }
    
            //###########################################################################
    
            // BURADA YAPILMASI GEREKENLER
            // 1) Siparişin durumunu $post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
            // 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse  echo "OK"; exit; yaparak sonlandırın.
    
            if (status == "success") { //Ödeme Onaylandı
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER ONAY İŞLEMLERİDİR.
                // 1) Siparişi onaylayın.
                // 2) iframe çağırma adımında merchant_oid ve diğer bilgileri veri tabanınıza kayıp edip bu aşamada karşılaştırarak eğer var ise bilgieri çekebilir ve otomatik sipariş tamamlama işlemleri yaptırabilirsiniz.
                // 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapabilirsiniz. Bu işlemide yine iframe çağırma adımında merchant_oid bilgisini kayıt edip bu aşamada sorgulayarak verilere ulaşabilirsiniz.
                // 3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda
                // değişebilir. Güncel tutarı Request.Form['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
    
                } else { //Ödemeye Onay Verilmedi
    
                // Bildirimin alındığını PayTR sistemine bildir.  
                Response.Write("OK");
    
                // BURADA YAPILMASI GEREKENLER
                // 1) Siparişi iptal edin.
                // 2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
                // $post['failed_reason_code'] - başarısız hata kodu
                // $post['failed_reason_msg'] - başarısız hata mesajı
                }          
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'XXXXXX'; // Mağaza numarası.
    var merchant_key = 'YYYYYYYYYYYYYY'; // Mağaza Parolası - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_salt = 'ZZZZZZZZZZZZZZ'; // Mağaza Gizli Anahtarı - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_oid = "IN" + microtime.now(); //sipariş numarası: her işlemde benzersiz olmalıdır! Bu bilgi bildirim sayfanıza yapılacak bildirimde gönderilir.
    
    var user_ip = ''; // Eğer bu kodu sunucuda değil local makinanızda çalıştırıyorsanız buraya dış ip adresinizi(https://www.whatismyip.com/) yazmalısınız.
    var email = 'musteri@saglayici.com'; // Müşterinizin sitenizde kayıtlı eposta adresi
    var payment_amount = 100;
    var payment_type ='eft';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var timeout_limit = 30; // İşlem zaman aşımı süresi - dakika cinsinden.
    var debug_on = 1; //hata mesajlarını ekrana bas.
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${payment_type}${test_mode}`;
        var paytr_token = hashSTR + merchant_salt;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        var options = {
            method: 'POST',
            url: 'https://www.paytr.com/odeme/api/get-token',
            headers:
                { 'content-type': 'application/x-www-form-urlencoded' },
            formData: {
                merchant_id: merchant_id,
                user_ip: user_ip,
                merchant_oid: merchant_oid,
                email: email,
                payment_amount: payment_amount,
                payment_type: payment_type,
                paytr_token: token,
                debug_on: debug_on,
                timeout_limit: timeout_limit, 
                test_mode: test_mode,
    
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.render('layout', { iframetoken: res_data.token });
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        } 
    
        if (callback.status == 'success') {
            //basarili
        } else {
           /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

**Opsiyonel: Ara bildirimleri alma**

Müşterinizin, IFrame içerisinde bildirim formunu doldurmasıyla birlikte, talep etmeniz halinde PayTR alt yapısı belirteceğiniz “Ara Bildirim URL” adresine bir ara bildirim yapacaktır. Bildirim içeriğinde EFT/Havale isteğinde göndermiş olduğunuz sipariş numarası ve müşterinizin işlem için seçtiği banka bilgisi bulunur. “Ara Bildirim URL” olarak kullanmak istediğiniz URL bilgisini Paytr Mağaza Paneli > Ayarlar bölümünden ekleyebilirsiniz.

Alan Adı | Açıklama  
---|---  
hash | Hash: Bildirimin doğruluğunu belirten hash bilgisi  
status | Durum: Ara bildirim için “info” değeri gelir  
merchant_oid | Sipariş numarası: EFT/Havale bildirimin başlatırken gönderdiğiniz sipariş numarası  
bank | Banka: EFT/Havale bildirimin yapıldığı banka  
  
  
**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    // Ara Bildirim URL için örnek kodlar
    
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
    $hash = base64_encode( hash_hmac('sha256', $post['merchant_oid'].$post['bank'].$merchant_salt,$merchant_key,true));
    
    ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if( $hash != $post['hash'] )
        die('PAYTR notification failed: bad hash');
    ###########################################################################
    
    ## DÖNÜLEN POST DEĞERLERİ
    /*
        $post[merchant_oid]      => Sipariş Numarası
        $post[status]            => "info"
        $post[hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
        ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
        $post[payment_sent_date] => Ödeme Yapılan Tarih
        $post[bank]              => Ödeme Yapılan Banka
        $post[user_name]         => Ödeme Yapan Adı Soyadı
        $post[user_phone]        => Ödeme Yapan Telefon Numarası
        $post[tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
    */
    ###########################################################################
    >
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # 2. ADIM için örnek kodlar
    
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
        merchant_key = b'XXXXXXXXXXXXXXXX'
        merchant_salt = 'XXXXXXXXXXXXXXXX'
    
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
        # POST değerleri ile hash oluştur.
        hash_str = post['merchant_oid'] + post['bank']+ merchant_salt
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
       ## DÖNÜLEN POST DEĞERLERİ
    /*
        [merchant_oid]      => Sipariş Numarası
        [status]            => "info"
        [hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
        ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
        [payment_sent_date] => Ödeme Yapılan Tarih
        [bank]              => Ödeme Yapılan Banka
        [user_name]         => Ödeme Yapan Adı Soyadı
        [user_phone]        => Ödeme Yapan Telefon Numarası
        [tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
    */
    ###########################################################################
    
    
    // Ara Bildirim URL için örnek kodlar
    
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Net.Mail;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    public partial class ara_bildirim_url_ornek : System.Web.UI.Page {
    
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key     = "YYYYYYYYYYYYYY";
        string merchant_salt    = "ZZZZZZZZZZZZZZ";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string merchant_oid = Request.Form["merchant_oid"];
            string merchant_oid = Request.Form["bank"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(merchant_oid, bank, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            string token = Convert.ToBase64String(b);
    
            //
            // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
            // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
            if (hash.ToString() != token) {
                Response.Write("PAYTR notification failed: bad hash");
                return;
                }
    
            //###########################################################################
    
            //## DÖNÜLEN POST DEĞERLERİ
            /*
             Request.Form[merchant_oid]      => Sipariş Numarası
             Request.Form[status]            => "info"
             Request.Form[hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
             ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
             Request.Form[payment_sent_date] => Ödeme Yapılan Tarih
             Request.Form[bank]              => Ödeme Yapılan Banka
             Request.Form[user_name]         => Ödeme Yapan Adı Soyadı
             Request.Form[user_phone]        => Ödeme Yapan Telefon Numarası
             Request.Form[tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
            */
            //###########################################################################
        }
    }
    
    
    var express = require('express');
    var ejsLayouts = require('express-ejs-layouts');
    var microtime = require('microtime');
    var crypto = require('crypto');
    var app = express();
    var nodeBase64 = require('nodejs-base64-converter');
    var request = require('request');
    var path = require('path');
    
    app.set('views', path.join(__dirname, '/app_server/views'));
    
    app.set('view engine', 'ejs');
    app.use(ejsLayouts);
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_key = 'YYYYYYYYYYYYYY'; // Mağaza Parolası - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    var merchant_salt = 'ZZZZZZZZZZZZZZ'; // Mağaza Gizli Anahtarı - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        paytr_token = callback.merchant_oid + callback.bank + merchant_salt
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        } 
    
            //## DÖNÜLEN POST DEĞERLERİ
            /*
             [merchant_oid]      => Sipariş Numarası
             [status]            => "info"
             [hash]              => PayTR Tarafından Hesaplanan Hash Değeri
    
             ## AŞAĞIDAKİLER MÜŞTERİNİN FORMA GİRDİĞİ BİLGİLERDİR ##
            [payment_sent_date] => Ödeme Yapılan Tarih
            [bank]              => Ödeme Yapılan Banka
            [user_name]         => Ödeme Yapan Adı Soyadı
            [user_phone]        => Ödeme Yapan Telefon Numarası
            [tc_no_last5]       => T.C. Kimlik Numarası Son 5 Hanesi
            */
            //###########################################################################
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

Havale/EFT iFrame API 2. ADIM örnek kodları[**indirmek için tıklayın.**](/havale-eft-iframe-api/havale-eft-iframe-api-2-adim/PayTR Havale-EFT iFrame API 2. ADIM.zip)
