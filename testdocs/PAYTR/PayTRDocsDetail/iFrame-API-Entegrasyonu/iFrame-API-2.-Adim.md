# iFrame API 2. Adım | PayTR

# iFrame API 2. Adım

iFrame ile açılan ödeme formunu kullanarak müşteriniz ödeme yaptığında, PayTR sistemi ödeme sonucunu yazılımınıza bildirmelidir ve yazılımınızdan bildirimin alındığına dair cevap almalıdır. Aksi halde, ödeme işlemi tamamlanmaz ve tarafınıza ödeme aktarılmaz.

PayTR sistemince ödeme sonuç bildiriminin yapılacağı sayfa (Bildirim URL) tarafınızca belirlenmeli ve Mağaza Paneli Destek & Kurulum alanındaki AYARLAR sayfasında tanımlanmalıdır.

Tanımlayacağınız Bildirim URL’ye POST metodu ile ödemenin sonucu (başarılı veya başarısız) her işlem için ayrı olarak gönderilir. Bu bildirime istinaden Bildirim URL’nizde yapacağınız kodlama ile yazılımınızda siparişi onaylamalı veya iptal etmelisiniz, ekrana OK basarak PayTR sistemine cevap vermelisiniz.

**PayTR sistemince Bildirim URL’nize POST REQUEST içeriğinde gönderilecek değerler:**   


Alan Adı | Zorunlu | Token | Açıklama  
---|---|---|---  
merchant_oid | Evet | Evet | Mağaza sipariş no: Satış işlemi için belirlediğiniz ve 1. ADIM’da gönderdiğiniz sipariş numarası  
status | Evet | Evet | Ödeme işleminin sonucu (success veya failed)  
total_amount | Evet | Evet | Müşteriden tahsil edilen toplam tutar (100 ile çarpılmış hali gönderilir. 34.56 => 3456)(Not: Müşteri vade farklı taksit seçtiği vb. durumlarda, 1. ADIM’da gönderdiğiniz “payment_amount” değerinden daha yüksek olabilir)  
hash | Evet | Evet | PayTR sisteminden gönderilen değerlerin doğruluğunu kontrol etmeniz için güvenlik amaçlı oluşturulan hash değeri (Hesaplama ile ilgili olarak örnek kodlara bakmalısınız)  
failed_reason_code | Hayır | Evet | Ödemenin onaylanmaması durumunda gönderilir (Bkz: 2. Adım İçin Hata Kodları ve Açıklamaları Tablosu)  
failed_reason_msg | Hayır | Evet | Ödemenin neden onaylanmadığı mesajını içerir (Bkz: 2. Adım İçin Hata Kodları ve Açıklamaları Tablosu)  
test_mode | Hayır | Hayır | Mağazanız test modunda iken veya canlı modda yapılan test işlemlerde 1 olarak gönderilir  
payment_type | Evet | Evet | Ödeme şekli: Müşterinin hangi ödeme şekli ile ödemesini tamamladığını belirtir.'card' veya 'eft' değerlerini alır.  
currency | Evet | Hayır | Para birimi: Ödemenin hangi para birimi üzerinden yapıldığını belirtir. ‘TL’, ‘USD’,‘EUR’, ‘GBP’, ‘RUB’ değerlerinden birini alır  
payment_amount | Evet | Hayır | Sipariş tutarı: 1. ADIM’da gönderdiğiniz “payment_amount” değeridir.(100 ile çarpılmış hali gönderilir. 34.56 => 3456)  
  
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




**2\. Adım İçin Hata Kodları ve Açıklamaları**

failed_reason_code | failed_reason_msg | Açıklama  
---|---|---  
0 | DEĞİŞKEN (AÇIKLAMAYI OKUYUN) | Ödemenin neden onaylanmadığına ilişkin, detaylı hata mesajı (Örneğin: Kartın limiti / bakiyesi yetersiz).  
1 | Kimlik Doğrulama yapılmadı. Lütfen tekrar deneyin ve işlemi tamamlayın. | Müşteri, kimlik doğrulama adımında cep telefonu numarasını girmedi.  
2 | Kimlik Doğrulama başarısız. Lütfen tekrar deneyin ve şifreyi doğru girin. | Müşteri, cep telefonuna gelen şifreyi doğru girmedi.  
3 | Güvenlik kontrolü sonrası onay verilmedi veya kontrol yapılamadı. | Müşterinin işlemi PayTR tarafından güvenlik kontrolünden geçemedi veya kontrol yapılamadı.  
6 | Müşteri ödeme yapmaktan vazgeçti ve ödeme sayfasından ayrıldı. | Müşteri, kendisine tanınmış olan işlem süresinde (1.ADIM’da tanımlanan timeout_limit değeri) işlemini tamamlamadı veya müşteri ödeme sayfasını kapatarak işlemi sonlandırdı.  
8 | Bu karta taksit yapılamamaktadır. | Müşterinin kullanmakta olduğu kart ile seçmiş olduğu taksitli ödeme yöntemi kullanılamaz.  
9 | Bu kart ile işlem yetkisi bulunmamaktadır. | Müşterinin kullanmakta olduğu kart için mağazanızın işlem yetkisi bulunmuyor.  
10 | Bu işlemde 3D Secure kullanılmalıdır. | Müşteri, yapmış olduğu işlemde 3D Secure ile ödeme yapmalıdır.  
11 | Güvenlik uyarısı. İşlem yapan müşterinizi kontrol edin. | Müşterinin işleminde fraud tespiti bulunuyor. Güvenliğiniz için müşterinin işlemlerini kontrol edin.  
99 | İşlem başarısız: Teknik entegrasyon hatası. | Teknik entegrasyon hatası varsa dönülecektir. (debug_on değeri 0 ise)  
  
  
Yukarıdaki açıklamalara uygun olarak Bildirim URL’nizi hazırladıysanız, kontrol için bir adet test ödemesi gerçekleştirmelisiniz. Eğer yaptığınız test işlem PayTR Mağaza Paneli’nizdeki İşlemler sayfasında “Başarılı” olarak görünürse PayTR entegrasyonunuz tümüyle tamamlanmıştır.

Eğer işlemin durumu “Devam Ediyor” olarak görünüyorsa Bildirim URL’nizden “OK” yanıtı alınamıyor demektir. İşlemler sayfasında yaptığınız test işleminin satırında “Detay” linkine tıklayıp, Bildirim URL’nizden hangi yanıt geldiğini kontrol edin.

**ÖNEMLİ UYARI:** Bildirim URL’iniz Paytr Mağaza Paneli > Destek & Kurulum > Ayarlar > Bildirim URL Ayarları kısmından, eğer sitenizde SSL var ise Bildirim URL protokolünü HTTPS olarak ayarlamanız gerekmektedir. SSL sertifikanız yok ise, kesinlikle HTTPS’li link kullanmayın. Eğer sitenizde Paytr entegrasyonundan sonra SSL kurulumu yaptıysanız, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTPS olarak değiştirerek kaydedin. Eğer kurulumdan sonra sitenizdeki SSL sertifikasını iptal ederseniz, Bildirim URL Ayarları bölümüne giderek, buradan protokolü HTTP olarak değiştirerek kaydedin.

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
            }
         */
    
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
        hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
        hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
        # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
        # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
        if hash != post['hash']:
            return HttpResponse(str('PAYTR notification failed: bad hash'))
    
        # BURADA YAPILMASI GEREKENLER
        # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
        # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.
    
        if post['status'] == 'success':  # Ödeme Onaylandı
            """
            BURADA YAPILMASI GEREKENLER
            1) Siparişi onaylayın.
            2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
            3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
            Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
            """
            print(request)
        else:  # Ödemeye Onay Verilmedi
            """
            BURADA YAPILMASI GEREKENLER
            1) Siparişi iptal edin.
            2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
            post['failed_reason_code'] - başarısız hata kodu
            post['failed_reason_msg'] - başarısız hata mesajı
            """
            print(request)
    
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
    
    var merchant_id = 'XXXXXX';
    var merchant_key = 'YYYYYYYYYYYYYY';
    var merchant_salt = 'ZZZZZZZZZZZZZZ';
    var basket = JSON.stringify([
        ['Örnek Ürün 1', '18.00', 1],
        ['Örnek Ürün 2', '33.25', 2],
        ['Örnek Ürün 3', '45.42', 1]
    ]);
    var user_basket = nodeBase64.encode(basket);
    var merchant_oid = "IN" + microtime.now(); // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    // Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    // Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    var max_installment = '0';
    var no_installment = '0'  // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın.
    var user_ip = '';
    var email = 'XXXXXXXX'; // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi.
    var payment_amount = 100; // Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    var currency = 'TL';
    var test_mode = '0'; // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    var user_name = ''; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
    var user_address = ''; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
    var user_phone = '05555555555'; // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
    
    // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php';
    // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    // Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    var merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php';
    var timeout_limit = 30; // İşlem zaman aşımı süresi - dakika cinsinden
    var debug_on = 1; // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    var lang = 'tr'; // Türkçe için tr veya İngilizce için en gönderilebilir. Boş gönderilirse tr geçerli olur.
    
    app.get("/", function (req, res) {
    
        var hashSTR = `${merchant_id}${user_ip}${merchant_oid}${email}${payment_amount}${user_basket}${no_installment}${max_installment}${currency}${test_mode}`;
    
        var paytr_token = hashSTR + merchant_salt;
    
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        var options = {
            method: 'POST',
            url: 'https://www.paytr.com/odeme/api/get-token',
            headers:
                { 'content-type': 'application/x-www-form-urlencoded' },
            formData: {
                merchant_id: merchant_id,
                merchant_key: merchant_key,
                merchant_salt: merchant_salt,
                email: email,
                payment_amount: payment_amount,
                merchant_oid: merchant_oid,
                user_name: user_name,
                user_address: user_address,
                user_phone: user_phone,
                merchant_ok_url: merchant_ok_url,
                merchant_fail_url: merchant_fail_url,
                user_basket: user_basket,
                user_ip: user_ip,
                timeout_limit: timeout_limit,
                debug_on: debug_on,
                test_mode: test_mode,
                lang: lang,
                no_installment: no_installment,
                max_installment: max_installment,
                currency: currency,
                paytr_token: token,
    
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
    
        // ÖNEMLİ UYARILAR!
        // 1) Bu sayfaya oturum (SESSION) ile veri taşıyamazsınız. Çünkü bu sayfa müşterilerin yönlendirildiği bir sayfa değildir.
        // 2) Entegrasyonun 1. ADIM'ında gönderdiğniz merchant_oid değeri bu sayfaya POST ile gelir. Bu değeri kullanarak
        // veri tabanınızdan ilgili siparişi tespit edip onaylamalı veya iptal etmelisiniz.
        // 3) Aynı sipariş için birden fazla bildirim ulaşabilir (Ağ bağlantı sorunları vb. nedeniyle). Bu nedenle öncelikle
        // siparişin durumunu veri tabanınızdan kontrol edin, eğer onaylandıysa tekrar işlem yapmayın. Örneği aşağıda bulunmaktadır.
    
        var callback = req.body;
    
        // POST değerleri ile hash oluştur.
        paytr_token = callback.merchant_oid + merchant_salt + callback.status + callback.total_amount;
        var token = crypto.createHmac('sha256', merchant_key).update(paytr_token).digest('base64');
    
        // Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
        // Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    
        if (token != callback.hash) {
            throw new Error("PAYTR notification failed: bad hash");
        }
    
        if (callback.status == 'success') {
            //basarili
        } else {
            //basarisiz
        }
    
        res.send('OK');
    
    });
    
    var port = 3000;
    app.listen(port, function () {
        console.log("Server is running. Port:" + port);
    });

iFrame API 2. Adım örnek kodları[**indirmek için tıklayın.**](/iframe-api/iframe-api-2-adim/PayTR iFrame API 2.ADIM.zip)
