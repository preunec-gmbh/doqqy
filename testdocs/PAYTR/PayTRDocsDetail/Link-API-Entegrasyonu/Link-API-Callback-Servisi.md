# Link API Callback Servisi | PayTR

# Link API Callback Servisi

Oluşturduğunuz ödeme linki üzerinden yalnızca başarılı bir ödeme yapıldığında, Create servisinde o link için göndermiş olduğunuz callbak_url’e işlem sonucu bildirilir.

BİLGİ: Eğer Create servisinde callbak_url belirlemediyseniz veya belirlemek istemiyorsanız, bu entegrasyonu yapmanız gerek yoktur.

DİKKAT: Bu servis yalnızca Create servisinde gönderdiğiniz linkin eğer varsa callback_url’ine istek atar. Mağaza Paneli içerisinde Bildirim URL kısmı ile hiçbir bağlantısı bulunmamaktadır.

**PayTR sistemince link için tanımladığınız Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**

Alan Adı | Açıklama  
---|---  
hash | PayTR sisteminden gönderilen değerlerin doğruluğunu kontrol etmeniz için güvenlik amaçlı oluşturulan hash değeri (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
merchant_oid | PayTR tarafından oluşturulan sipariş referans numarası.  
status | Başarılı ödeme sonucunda success değeri döner (Link API'de başarısız ödemeler için bildirim yapılmaz).  
total_amount | Müşteriden tahsil edilen toplam tutar. (100 ile çarpılmış hali gönderilir. 34.56 => 3456) (Not: Müşteri vade farklı taksit seçtiği vb. durumlarda, 1. ADIM’da gönderdiğiniz “payment_amount” değerinden daha yüksek olabilir)  
payment_amount | Sipariş tutarı: 1. ADIM’da gönderdiğiniz “payment_amount” değeridir. (100 ile çarpılmış hali gönderilir. 34.56 => 3456)  
payment_type | Müşterinin hangi ödeme şekli ile ödemesini tamamladığını belirtir. Örn. card, bex vb. değerleri alır.  
currency | Para birimi: Ödemenin hangi para birimi üzerinden yapıldığını belirtir. TL, USD, EUR, GBP, RUB değerlerinden birini alır.  
callback_id | Link oluşturmada (create) ilettiğiniz callbak_id bilgisi.  
merchant_id | PayTR mağaza numaranız.  
test_mode | Mağazanız test modunda iken veya canlı modda yapılan test işlemlerde 1 olarak gönderilir  
  
**Bildirim URL’nize PayTR sistemince yapılacak isteğe dönülmesi gereken yanıt (RESPONSE) text (düz yazı) formatında ve yalnızca OK değeri olmalıdır.**   

    
    
    Örnek (PHP): echo "OK";
    
    
    
    Örnek (.NET): Response.Write("OK");

**ÖNEMLİ UYARILAR:**

  1. Bildirim URL adresinize üye girişi ve benzeri erişim kısıtlaması yapılmamalıdır. Böylece PayTR sistemi bildirimleri kolayca iletebilecektir.

  2. Bildirim URL’nize gelecek bildirimlere döneceğiniz OK yanıtının öncesinde veya sonrasında HTML veya herhangi başka bir içerik ekrana basılmamalıdır.

  3. Bildirim URL’niz, müşterinizin ödeme sırasında ulaşacağı bir sayfa değildir, PayTR tarafından arka planda (server-side) ödeme sonucunu bildirmek için kullanılır. Bu nedenle, Bildirim URL’nizde kodlama yaparken oturum (SESSION) değerlerini kullanamazsınız. İşlemlerinizi Mağaza sipariş no (merchant_oid) kullanarak gerçekleştirmelisiniz.

  4. OK yanıtı alınmayan bildirimlerde, ilgili sipariş Mağaza Paneli'ndeki İşlemler sayfasında “Devam Ediyor” olarak görünecektir.

  5. PayTR sistemi, Bildirim URL’nizden OK cevabını istendiği şekilde almadığı durumda, bildirimin başarısız olduğunu varsayar. Ağ trafik sorunları, sitenizdeki anlık yoğunluklar ve benzeri nedenlerden dolayı aynı ödeme işlemi için birden fazla bildirim ulaşabilir. Bu nedenle, bildirimin birden fazla geldiği durumlarda, yalnızca ilk bildirim göz önünde bulundurulmalı, sonraki bildirimler için müşteriye tekrar ürün/hizmet sunulmamalıdır. Tekrarlayan bildirimlerde yalnızca OK yanıtı ile süreç sonlandırılmalıdır. Tekrarlayan bildirimlerin tespiti Mağaza sipariş no (merchant_oid) temel alınarak yapılmalıdır.

  6. Bildirimin PayTR sisteminden geldiğinden ve ulaşım esnasında değiştirilmediğinden emin olmak için, **POST içerisindeki hash** değeri ile tarafınızca **oluşturulacak hash** değerinin aynı olduğunu kontrol etmeniz, güvenlik açısından büyük önem arz etmektedir. Bu kontrolü yapmamanız durumunda maddi kayıplar ile karşılaşabilirsiniz.




Yukarıdaki açıklamalara uygun olarak Bildirim URL’nizi hazırladıysanız, kontrol için bir adet test ödemesi gerçekleştirmelisiniz. Eğer yaptığınız test işlem PayTR Mağaza Paneli’nizdeki İşlemler sayfasında “Başarılı” olarak görünürse PayTR entegrasyonunuz tümüyle tamamlanmıştır.

Eğer işlemin durumu “Devam Ediyor” olarak görünüyorsa Bildirim URL’nizden “OK” yanıtı alınamıyor demektir. İşlemler sayfasında yaptığınız test işleminin satırında “Detay” linkine tıklayıp, Bildirim URL’nizden hangi yanıt geldiğini kontrol edin.

**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Destek & Kurulum > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        ############################# ÖDEME LİNKİ BİLDİRİM ÖRNEK KODLAR ############################
        #                                                                                          #
        $post = $_POST;
    
        ################################ DÜZENLEMESİ ZORUNLU ALANLAR ###############################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_key   = 'XXXXXXXXXXXXXXXX';
        $merchant_salt  = 'XXXXXXXXXXXXXXXX';
        ############################################################################################
    
        ################ Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. ################
        #
        ## POST değerleri ile hash oluştur.
        $hash = base64_encode( hash_hmac('sha256', $post['callback_id'].$post['merchant_oid'].$merchant_salt.$post['status'].$post['total_amount'], $merchant_key, true) );
        #
        ## Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        ## Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if( $hash != $post['hash'] )
            die('PAYTR notification failed: bad hash');
        ############################################################################################
        #
        ## BURADA YAPILMASI GEREKENLER
        ## 1) Ödeme durumunu $post['callback_id'] değerini kullanarak veri tabanınızdan sorgulayın.
        ## 2) Eğer ödeme zaten daha önceden onaylandıysa (callback size ulaştıysa) sadece echo "OK"; exit; yaparak akışı sonlandırın.
        /* Ödeme durum sorgulama örnek
           $durum = SQL
           if($durum == "onay"){
                echo "OK";
                exit;
            }
         */
    
        if( $post['status'] == 'success' ) { ## Ödeme Onaylandı
            ## BURADA YAPILMASI GEREKENLER
            ## 1) Veri tabanınızda ödemeyi onaylayın.
            ## 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            ## 3) $post['total_amount'] müşterinin yaptığı ödemenin toplam tutarıdır. Muhasebe işlemlerinizde
            ## bu tutraı kullanmanız gerekmektedir.
        } else {
            ## Link API'de başarısız ödemeler için callback yapılmamaktadır.
            ## Dolayısıyla kod akışında buraya erişim olmayacaktır. Ancak ileride Link API'de yapılabilecek geliştirmeler
            ## için dilerseniz buraya bir handler yazabilirsiniz.
        }
    
        ## Bildirimin alındığını PayTR sistemine bildir. OK yanıtını bu alandan kaldırmayın.
        echo "OK";
        exit;
    
    
    # Python 3.6+
    # Django Web Framework referans alınarak hazırlanmıştır
    # ÖDEME LİNKİ BİLDİRİM ÖRNEK KODLAR
    
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
        hash_str = post['callback_id'] + post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        """
        BURADA YAPILMASI GEREKENLER
        1) Ödeme durumunu post['callback_id'] değerini kullanarak veri tabanınızdan sorgulayın.
        2) Eğer ödeme zaten daha önceden onaylandıysa (callback size ulaştıysa) sadece 'OK' yaparak akışı sonlandırın.
        Ödeme durum sorgulama örnek
        durum = SQL
    
        if(durum == 'onay'){
             return HttpResponse(str('OK'))
        """
    
        if post['status'] == 'success':
            """
            BURADA YAPILMASI GEREKENLER
            1) Veri tabanınızda ödemeyi onaylayın.
            2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            3) post['total_amount'] müşterinin yaptığı ödemenin toplam tutarıdır. Muhasebe işlemlerinizde
            bu tutraı kullanmanız gerekmektedir.
            """
        else:
            """
            Link API'de başarısız ödemeler için callback yapılmamaktadır.
            Dolayısıyla kod akışında buraya erişim olmayacaktır. Ancak ileride Link API'de yapılabilecek geliştirmeler
            """
    
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
    
    public partial class paytr_link_api_callback : System.Web.UI.Page
    {
        // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        //
        // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        string merchant_key = "XXXXXXXXXXXXXXXXXXXXXXXXXX";
        string merchant_salt = "YYYYYYYYYYYYYYYYYYYYYYYYY";
        // ###########################################################################
    
        protected void Page_Load(object sender, EventArgs e)
        {
            // ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
            // 
            // POST değerleri ile hash oluştur.
            string callback_id = Request.Form["callback_id"];
            string merchant_oid = Request.Form["merchant_oid"];
            string status = Request.Form["status"];
            string total_amount = Request.Form["total_amount"];
            string hash = Request.Form["hash"];
    
            string Birlestir = string.Concat(callback_id, merchant_oid, merchant_salt, status, total_amount);
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
    
            ////////////////////////////////////////////////////////////////////////////////////////////
            //
            //
            ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
            // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
            // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
            // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
            // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
            // [payment_amount]  => Ödeme tutarı.
            // [payment_type]    => Ödeme yöntemi.
            // [currency]        => Ödeme para birimi.
            // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
            // [merchant_id]     => PayTR mağaza numaranınz.
    
            // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
            ////////////////////////////////////////////////////////////////////////////////////////////
            //
    
            // BURADA YAPILMASI GEREKENLER
            // 1) Ödeme durumunu ['callback_id'] değerini kullanarak veri tabanınızdan sorgulayın.
            // 2) Eğer ödeme zaten daha önceden onaylandıysa (callback size ulaştıysa) sadece echo "OK"; exit; yaparak akışı sonlandırın.
    
            /* Ödeme durum sorgulama örnek
            status = SQL
            if(status == "confirm"){
                 Response.Write("OK");
            }
            */
    
            if (status == "success")
            { //Ödeme Onaylandı
    
                // BURADA YAPILMASI GEREKENLER ONAY İŞLEMLERİDİR.
                // 1) Veri tabanınızda ödemeyi onaylayın.
                // 2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapabilirsiniz. Bu işlemide yine iframe çağırma adımında merchant_oid bilgisini kayıt edip bu aşamada sorgulayarak verilere ulaşabilirsiniz.
                // 3) ['total_amount'] müşterinin yaptığı ödemenin toplam tutarıdır. Muhasebe işlemlerinizde bu tutarı kullanmanız gerekmektedir.
            }
            else
            { //Ödemeye Onay Verilmedi
    
                // BURADA YAPILMASI GEREKENLER
                // 1) Link API'de başarısız ödemeler için callback yapılmamaktadır.
                // 2) Dolayısıyla kod akışında buraya erişim olmayacaktır. Ancak ileride Link API'de yapılabilecek geliştirmeler
                // için dilerseniz buraya bir handler yazabilirsiniz.
                // ['failed_reason_msg'] - başarısız hata mesajı
            }
            // Bildirimin alındığını PayTR sistemine bildir. OK yanıtını bu alandan kaldırmayın.
            Response.Write("OK");
        }
    }
    
    
    var crypto = require('crypto');
    var express = require('express');
    var app = express();
    var request = require('request');
    
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    var merchant_id = 'AAAAAA';
    var merchant_key = 'XXXXXXXXXXXXXXXX';
    var merchant_salt = 'XXXXXXXXXXXXXXXX';
    
    app.get("/create", function (req, res) {
    
        var name = 'Örnek Ürün / Hizmet Adı';  // Ürün / Hizmetin açıklaması. En az 4 en fazla 200 karakter.
        var price = '1445'; // 14.45 TL için 14.45 * 100 = 1445 (100 ile çarpılmış ve integer olarak gönderilmelidir.)
        var currency = 'TL';  //TL - USD - EUR - GBP gönderilebilir.
        var max_installment = '12'; // 2 - 12 arası gönderilebilir. 1 gönderilirse bireysel kartlar taksit yapılamaz.
    
        //collection (fatura/cari tahsilat) veya product (ürün/hizmet satışı) gönderilebilir.
        //collection ise email (ödeme yapan tarafın eposta adresi olmalı).
        //product ise min_count (satın alma adet alt limiti) gereklidir.
    
        var link_type = 'product';
        var lang = 'tr'; //tr veya en gönderilebilir.
        var required = name + price + currency + max_installment + link_type + lang;
        var email = '';
        var min_count = '';
        if (link_type == 'product') {
            min_count = '1';
            // Alt adet limiti.
            required += min_count;
        } else {
            (link_type == 'collection')
            email = 'test@example.com';
            // Ödeme yapan kullanıcının eposta adresi.
            required += email;
        }
    
        var max_count = '1';
    
        // Opsiyonel bilgiler, gönderilmesi zorunlu değildir.
    
        var expiry_date = '2021-06-23 17:00:00';
    
        // Link'in son kullanma tarihi. Gönderilmezse, sürekli açık kalır.
        // Örnek format: 2021-05-31 17:00:00
    
        //Link ile yapılan ödemenin sonucunun gönderileceği URL. En fazla 400 kararkter.
        //http:// ya da https:// ile başlamalı, localhost olmamalı ve port içermemelidir.
        //callback_id gönderildiğinde bu alan zorunlu olmaktadır.
    
        var callback_link = '';
    
        // Bildirimde dönülecek bildirim ID'si. Alfanumerik ve en fazla 64 karakter olabilir.
        //callback_link gönderildiğinde bu alan zorunlu olmaktadır.
        var callback_id = '';
    
        var debug_on = '1'; //Entegrasyon hatalarını alabilmek için 1 olarak bırakın.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(required + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/create',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'name': name,
                'price': price,
                'currency': currency,
                'max_installment': max_installment,
                'link_type': link_type,
                'lang': lang,
                'min_count': min_count,
                'email': email,
                'expiry_date': expiry_date,
                'max_count': max_count,
                'callback_link': callback_link,
                'callback_id': callback_id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(body);
            } else {
    
                res.end(body);
            }
    
        });
    
    });
    
    app.get("/delete", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/delete',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
                /* Başarılı yanıt içerik örneği
                [status]  => success
                */
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendsms", function (req, res) {
    
        var id = 'XXXX';  // Link ID - create metodunda dönülen değerdir.
        var cell_phone = '05555555555'; // SMS gönderilecek numara. 05 ile başlamalı ve 11 hane olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + cell_phone + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-sms',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'cell_phone': cell_phone,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.get("/sendmail", function (req, res) {
    
        var id = 'XXXX'; // Link ID - create metodunda dönülen değerdir.
        var email = ''; // Eposta gönderilecek adres. Standart email adresi formatına uygun olmalıdır.
        var debug_on = '1'; // Hataları ekrana basmak için kullanılır.
    
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(id + merchant_id + email + merchant_salt).digest('base64');
    
        var options = {
            'method': 'POST',
            'url': 'https://www.paytr.com/odeme/api/link/send-email',
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            form: {
                'merchant_id': merchant_id,
                'id': id,
                'email': email,
                'debug_on': debug_on,
                'paytr_token': paytr_token,
            }
        };
    
        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            var res_data = JSON.parse(body);
    
            if (res_data.status == 'success') {
                res.send(response.body);
    
            } else {
                console.log(response.body);
                res.end(response.body);
            }
    
        });
    
    });
    
    app.post("/callback", function (req, res) {
        var callback = req.body;
    
        token = callback.id + callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var paytr_token = crypto.createHmac('sha256', merchant_key).update(token).digest('base64');
    
        if (paytr_token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        ////////////////////////////// POST İÇERİSİNDE DÖNEN DEĞERLER //////////////////////////////
        // [hash]            => Doğrulama yapmak için kullanılacak hash bilgisi.
        // [merchant_oid]    => PayTR tarafından oluşturulan sipariş referans numarası.
        // [status]          => Ödemenin başarılı durumunda success değeri alır(Link API'de başarısız ödemeler için callback yapılmamaktadır).
        // [total_amount]    => Toplam ödeme tutarı(Örneğin taksitli ödeme ise vade farklı toplam tutar).
    
        // [payment_amount]  => Ödeme tutarı.
        // [payment_type]    => Ödeme yöntemi.
        // [currency]        => Ödeme para birimi.
        // [callback_id]     => Link oluşturmada(create) ilettiğiniz callbak_id bilgisi.
    
        // [merchant_id]     => PayTR mağaza numaranınz.
    
        // [test_mode]       => Eğer mağazanız test modunda ise 1 döner.
        ////////////////////////////////////////////////////////////////////////////////////////////
    
        if (callback.status == 'success') {
    
            //basarili
        } else {
            /// basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3200;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });
    

Link API CallBack Servisi örnek kodlarını[**indirmek için tıklayın.**](/link-api/linkle-api-callback/PayTR Link API - Callback \(Optional\).zip)
