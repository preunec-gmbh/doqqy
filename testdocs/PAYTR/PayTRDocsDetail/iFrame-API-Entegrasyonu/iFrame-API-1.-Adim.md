# iFrame API 1. Adım | PayTR

# iFrame API 1. Adım

1- iFrame Token istediğinde bulunabilmek için tabloda belirtilen bilgileri POST ile ilgili URL’e gönderin: https://www.paytr.com/odeme/api/get-token   
Bu istek arka planda (server-side) POST metodu ile gerçekleşir.

**POST REQUEST içeriğinde gönderilecek değerler:**   
  


Alan adı / tipi | Zorunlu | Token | Açıklama | Kısıtlar  
---|---|---|---|---  
merchant_id(string) | Evet | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası |   
user_ip (string) | Evet | Evet | Müşteri ip: İstek anında aldığınız müşteri ip numarası(Önemli: Lokal makinenizde yapacağınız denemelerde mutlaka dış IP adresini gönderdiğinizden emin olun) | En fazla 39 karakter (ipv4)  
merchant_oid(string) | Evet | Evet | Mağaza sipariş no: Satış işlemi içinbelirlediğiniz benzersiz sipariş numarası.(Not: Sipariş no ödeme sonuç bildirimi esnasında geri dönen değerler arasındadır) | En fazla 64 karakter,Alfa numerik  
email (string) | Evet | Evet | Müşteri eposta adresi: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız eposta adresi | En fazla 100 karakter  
payment_amount(integer) | Evet | Evet | Ödeme tutarı: Siparişe ait toplam ödeme tutarı.(Tutarı 100 ile çarparak göndermelisiniz) | Örn: 34.56 için 3456gönderilmelidir.(34.56 * 100 = 3456)  
currency(string) | Evet | Evet | Para birimi | TL(veya TRY), EUR, USD, GBP,RUB (Boş ise TL kabul edilir)  
user_basket(string) | Evet | Evet | Sepet içeriği: Müşterinin siparişindeki ürün/hizmet bilgilerini içermelidir | Nasıl bir yapıda olacağı ile ilgili olarak örnek kodlara bakmalısınız  
no_installment(int) | Evet | Evet | Taksit görüntülenmesin: Eğer 1 olarak gönderilirse taksit seçenekleri gösterilmez(Örn. cep telefonu için taksit yasağı vardır) | 0 veya 1  
max_installment(int) | Evet | Evet | En fazla taksit sayısı: Gösterilecek en fazlataksit sayısını belirler (Örn. kuyum harcamalarında en fazla 4 taksit uygulamasıvardır) | 0,2,3,4,5,6,7,8,9,10,11,12 Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur  
paytr_token(string) | Evet | Hayır | paytr_token: İsteğin sizden geldiğine veiçeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Hesaplama ile ilgili olarak örnek kodlara bakmalısınız  
user_name(string) | Evet | Hayır | Müşteri adı ve soyadı: Müşterinin sisteminizde kayıtlı olan veya form aracılığıyla aldığınız adı ve soyadı | En fazla 60 karakter  
user_address(string) | Evet | Hayır | Müşteri adresi: Müşterinin sipariş sırasında ilettiği adresi | En fazla 400 karakter  
user_phone(string) | Evet | Hayır | Müşteri telefon numarası: Müşterinin sipariş sırasında ilettiği telefon numarası | En fazla 20 karakter  
merchant_ok_url | Evet | Hayır | Müşterinin başarılı ödeme sonrası yönlendirileceği sayfa (Örn. Siparişlerim takip sayfası) | En fazla 400 karakter  
merchant_fail_url | Evet | Hayır | Müşterinin ödemesi sırasında beklenmeyen bir hatada yönlendirileceği sayfa | En fazla 400 karakter  
test_mode | Hayır | Evet | Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir | 0 veya 1  
debug_on (int) | Hayır | Hayır | Hata döndür: PayTR’a yanlış veya eksik bilgi iletilmesi durumunda sistemden hata mesajı döndürülmesi için 1 gönderilmelidir | 0 veya 1  
timeout_limit(int) | Hayır | Hayır | Sıfırdan farklı bir değer gönderilmesi durumunda, ödeme işlemi bu süre içerisinde tamamlanmalıdır. (Ödeme sırasındasisteminizde fiyat güncellemesi olmasıdurumuna karşı güvenlik amaçlı kullanabilirsiniz) | Dakika cinsinden(Gönderilmemesi durumunda 30 dakika olarak tanımlanır)  
lang(string) | Hayır | Hayır | Ödeme sürecinde sayfalarda kullanılacak dil | Türkçe için tr veya İngilizce içinen(Boş gönderilirse tr geçerli olur)  
  
  
  


* **iframe_token** isteğine verilen yanıt (RESPONSE) JSON formatındadır:
    
    
    - Başarılı yanıt örneği: (token içerir)
    {"status":"success","token":"28cc613c3d7633cfa4ed0956fdf901e05cf9d9cc0c2ef8db54fa"}
    
    
    - Başarısız yanıt örneğı:
    {"status":"failed","reason":"Zorunlu alan degeri gecersiz: merchant_id"}

Üye İşyeri, başarılı yanıt içerisinde gelen **iframe_token** ile iframe TAG’ı kullanarak ödeme formunu açar. Aşağıdaki HTML kod, gelen **iframe_token** değeri yerleştirilerek kullanılmalıdır. 
    
    
    <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
    <iframe src="https://www.paytr.com/odeme/guvenli/iframe_token" id="paytriframe" frameborder="0"
    scrolling="no" style="width: 100%;"></iframe>
    <script>iFrameResize({},'#paytriframe');</script>

Yukarıda anlatılan aşamaların tamamlanmasıyla birlikte, müşteri tarafından kullanılacak olan ödeme formu ekranda belirecektir. Ödeme işleminde müşterinin etkileşimde bulunacağı kısım entegrasyonda böylece tamamlanmış olur. _ANCAK; entegrasyonunuz henüz tamamlanmamıştır_ , 2. ADIM ödeme sonucunu (başarılı/başarısız) almanız ve siparişi onaylamanız / iptal etmeniz için gereklidir

**ÖNEMLİ UYARI:** PayTR ödeme alt yapısı asenkron olarak çalışmaktadır. Bu nedenle ödeme tamamlandığında müşteri merchant_ok_url'e yönlendirilirken, ödemenin kesin sonucu (Başarılı ya da Başarısız sonucu) Bildirim URL'ye POST ile gönderilmektedir. merchant_ok_url'e herhangi bir veri POST edilmemektedir, bu nedenle merchant_ok_url olarak belirttiğiniz sayfada sipariş onay/iptal gibi işlem yapmamalısınız. 

![](/user/pages/02.iframe-api/iframe-api-1-adim/odeme.png)

  * PHP
  * Python
  * .NET
  * NODEJS


    
    
    <!doctype html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Örnek Ödeme Sayfası</title>
    </head>
    <body>
    
    <div>
        <h1>Örnek Ödeme Sayfası</h1>
        <p>1. ADIM için örnek kodlar</p>
    </div>
    <br><br>
    
    <div style="width: 100%;margin: 0 auto;display: table;">
    
        <?php
    
        ## 1. ADIM için örnek kodlar ##
    
        ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
        #
        ## API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
        $merchant_id    = 'XXXXXX';
        $merchant_key   = 'YYYYYYYYYYYYYY';
        $merchant_salt  = 'ZZZZZZZZZZZZZZ';
        #
        ## Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
        $email = "XXXXXXXX";
        #
        ## Tahsil edilecek tutar.
        $payment_amount = ""; //9.99 için 9.99 * 100 = 999 gönderilmelidir.
        #
        ## Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
        $merchant_oid = "";
        #
        ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
        $user_name = "";
        #
        ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
        $user_address = "";
        #
        ## Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
        $user_phone = "";
        #
        ## Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
        ## !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
        ## !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
        $merchant_ok_url = "http://www.siteniz.com/odeme_basarili.php";
        #
        ## Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
        ## !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
        ## !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
        $merchant_fail_url = "http://www.siteniz.com/odeme_hata.php";
        #
        ## Müşterinin sepet/sipariş içeriği
        $user_basket = "";
        #
        /* ÖRNEK $user_basket oluşturma - Ürün adedine göre array'leri çoğaltabilirsiniz
        $user_basket = base64_encode(json_encode(array(
            array("Örnek ürün 1", "18.00", 1), // 1. ürün (Ürün Ad - Birim Fiyat - Adet )
            array("Örnek ürün 2", "33.25", 2), // 2. ürün (Ürün Ad - Birim Fiyat - Adet )
            array("Örnek ürün 3", "45.42", 1)  // 3. ürün (Ürün Ad - Birim Fiyat - Adet )
        )));
        */
        ############################################################################################
    
        ## Kullanıcının IP adresi
        if( isset( $_SERVER["HTTP_CLIENT_IP"] ) ) {
            $ip = $_SERVER["HTTP_CLIENT_IP"];
        } elseif( isset( $_SERVER["HTTP_X_FORWARDED_FOR"] ) ) {
            $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
        } else {
            $ip = $_SERVER["REMOTE_ADDR"];
        }
    
        ## !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
        ## buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
        $user_ip=$ip;
        ##
    
        ## İşlem zaman aşımı süresi - dakika cinsinden
        $timeout_limit = "30";
    
        ## Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
        $debug_on = 1;
    
        ## Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
        $test_mode = 0;
    
        $no_installment = 0; // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
    
        ## Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
        ## Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
        $max_installment = 0;
    
        $currency = "TL";
    
        ####### Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur. #######
        $hash_str = $merchant_id .$user_ip .$merchant_oid .$email .$payment_amount .$user_basket.$no_installment.$max_installment.$currency.$test_mode;
        $paytr_token=base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
        $post_vals=array(
                'merchant_id'=>$merchant_id,
                'user_ip'=>$user_ip,
                'merchant_oid'=>$merchant_oid,
                'email'=>$email,
                'payment_amount'=>$payment_amount,
                'paytr_token'=>$paytr_token,
                'user_basket'=>$user_basket,
                'debug_on'=>$debug_on,
                'no_installment'=>$no_installment,
                'max_installment'=>$max_installment,
                'user_name'=>$user_name,
                'user_address'=>$user_address,
                'user_phone'=>$user_phone,
                'merchant_ok_url'=>$merchant_ok_url,
                'merchant_fail_url'=>$merchant_fail_url,
                'timeout_limit'=>$timeout_limit,
                'currency'=>$currency,
                'test_mode'=>$test_mode
            );
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/api/get-token");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1) ;
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    
         // XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
         // aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
         // curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
        $result = @curl_exec($ch);
    
        if(curl_errno($ch))
            die("PAYTR IFRAME connection error. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        if($result['status']=='success')
            $token=$result['token'];
        else
            die("PAYTR IFRAME failed. reason:".$result['reason']);
        #########################################################################
    
        ?>
    
        <!-- Ödeme formunun açılması için gereken HTML kodlar / Başlangıç -->
        <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
        <iframe src="https://www.paytr.com/odeme/guvenli/<?php echo $token;?>" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
        <script>iFrameResize({},'#paytriframe');</script>
        <!-- Ödeme formunun açılması için gereken HTML kodlar / Bitiş -->
    
    </div>
    
    <br><br>
    </body>
    </html>
    
    
    
    # Python 3.6+
    # 1. ADIM için örnek kodlar
    
    import base64
    import hmac
    import hashlib
    import requests
    import json
    
    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'XXXXXX'
    merchant_key = b'YYYYYYYYYYYYYY'
    merchant_salt = b'ZZZZZZZZZZZZZZ'
    
    # Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
    email = 'XXXXXXXX'
    
    # Tahsil edilecek tutar.
    payment_amount = '' # 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    
    # Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
    merchant_oid = ''
    
    # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
    user_name = ''
    
    # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
    user_address = ''
    
    # Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
    user_phone = ''
    
    # Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
    # !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    # !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
    merchant_ok_url = 'http://www.siteniz.com/odeme_basarili.php'
    
    # Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
    # !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
    # !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
    merchant_fail_url = 'http://www.siteniz.com/odeme_hata.php'
    
    # Müşterinin sepet/sipariş içeriği
    user_basket = ''
    
    # ÖRNEK $user_basket oluşturma - Ürün adedine göre array'leri çoğaltabilirsiniz
    """
    user_basket = base64.b64encode(json.dumps([['Örnek ürün 1', '18.00', 1],
                   ['Örnek ürün 2', '33.25', 2],
                   ['Örnek ürün 3', '45.42', 1]]).encode())
    """
    
    # !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
    # buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
    user_ip = ''
    
    # İşlem zaman aşımı süresi - dakika cinsinden
    timeout_limit = '30'
    
    # Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
    debug_on = '1'
    
    # Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    test_mode = '1'
    
    no_installment = '0' # Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
    
    # Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
    # Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
    max_installment = '0'
    
    currency = 'TL'
    
    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + user_basket.decode() + no_installment + max_installment + currency + test_mode
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': paytr_token,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }
    
    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)
    
    if res['status'] == 'success':
        print(res['token'])
    
        """
        context = {
            'token': res['token']
        }
        """
    else:
        print(result.text)
    
    """
    # Ödeme formunun açılması için gereken HTML kodlar / Başlangıç #
    
    <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
    <iframe src="https://www.paytr.com/odeme/guvenli/{ token }" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
    <script>iFrameResize({},'#paytriframe');</script>
    
    # Ödeme formunun açılması için gereken HTML kodlar / Bitiş #
    """
    
    
    // 1. ADIM için örnek kodlar
    
    using Newtonsoft.Json.Linq; // Bu satırda hata alırsanız, site dosyalarınızın olduğu bölümde bin isimli bir klasör oluşturup içerisine Newtonsoft.Json.dll adlı DLL dosyasını kopyalayın.
    using System;
    using System.Collections.Generic;
    using System.Collections.Specialized;
    using System.Linq;
    using System.Net;
    using System.Security.Cryptography;
    using System.Text;
    using System.Web;
    using System.Web.Script.Serialization;
    using System.Web.UI;
    using System.Web.UI.WebControls;
    
    namespace WebApplication3
    {
        public partial class _Default : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
            //
            // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
            string merchant_id = "XXXXXX";
            string merchant_key = "YYYYYYYYYYYYYY";
            string merchant_salt = "ZZZZZZZZZZZZZZ";
            //
            // Müşterinizin sitenizde kayıtlı veya form vasıtasıyla aldığınız eposta adresi
            string emailstr = "ZZZZZZZZZZZZZZ";
            //
            // Tahsil edilecek tutar. 9.99 için 9.99 * 100 = 999 gönderilmelidir.
            int payment_amountstr = ;
            //
            // Sipariş numarası: Her işlemde benzersiz olmalıdır!! Bu bilgi bildirim sayfanıza yapılacak bildirimde geri gönderilir.
            string merchant_oid = "";
            //
            // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız ad ve soyad bilgisi
            string user_namestr = "";
            //
            // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız adres bilgisi
            string user_addressstr = "";
            //
            // Müşterinizin sitenizde kayıtlı veya form aracılığıyla aldığınız telefon bilgisi
            string user_phonestr = "";
            //
            // Başarılı ödeme sonrası müşterinizin yönlendirileceği sayfa
            // !!! Bu sayfa siparişi onaylayacağınız sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
            // !!! Siparişi onaylayacağız sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
            string merchant_ok_url = "http://www.siteniz.com/basarili";
            //
            // Ödeme sürecinde beklenmedik bir hata oluşması durumunda müşterinizin yönlendirileceği sayfa
            // !!! Bu sayfa siparişi iptal edeceğiniz sayfa değildir! Yalnızca müşterinizi bilgilendireceğiniz sayfadır!
            // !!! Siparişi iptal edeceğiniz sayfa "Bildirim URL" sayfasıdır (Bakınız: 2.ADIM Klasörü).
            string merchant_fail_url = "http://www.siteniz.com/basarisiz";
            //        
            // !!! Eğer bu örnek kodu sunucuda değil local makinanızda çalıştırıyorsanız
            // buraya dış ip adresinizi (https://www.whatismyip.com/) yazmalısınız. Aksi halde geçersiz paytr_token hatası alırsınız.
            string user_ip = Request.ServerVariables["HTTP_X_FORWARDED_FOR"];
            if (user_ip == "" || user_ip == null)
            {
                user_ip = Request.ServerVariables["REMOTE_ADDR"];
            }
            //
            // ÖRNEK user_basket oluşturma - Ürün adedine göre object'leri çoğaltabilirsiniz
            object[][] user_basket = {
                new object[] {"Örnek ürün 1", "18.00", 1}, // 1. ürün (Ürün Ad - Birim Fiyat - Adet)
                new object[] {"Örnek ürün 2", "33.25", 2}, // 2. ürün (Ürün Ad - Birim Fiyat - Adet)
                new object[] {"Örnek ürün 3", "45.42", 1}, // 3. ürün (Ürün Ad - Birim Fiyat - Adet)
                };
            /* ############################################################################################ */
    
            // İşlem zaman aşımı süresi - dakika cinsinden
            string timeout_limit = "30";
            //
            // Hata mesajlarının ekrana basılması için entegrasyon ve test sürecinde 1 olarak bırakın. Daha sonra 0 yapabilirsiniz.
            string debug_on = "1";
            //
            // Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
            string test_mode = "1";
            //
            // Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
            string no_installment = "0";
            //
            // Sayfada görüntülenecek taksit adedini sınırlamak istiyorsanız uygun şekilde değiştirin.
            // Sıfır (0) gönderilmesi durumunda yürürlükteki en fazla izin verilen taksit geçerli olur.
            string max_installment = "0";
            //
            // Para birimi olarak TL, EUR, USD gönderilebilir. USD ve EUR kullanmak için kurumsal@paytr.com 
            // üzerinden bilgi almanız gerekmektedir. Boş gönderilirse TL geçerli olur.
            string currency = "TL";
            //
            // Türkçe için tr veya İngilizce için en gönderilebilir. Boş gönderilirse tr geçerli olur.
            string lang = "";
    
            // Gönderilecek veriler oluşturuluyor
            NameValueCollection data = new NameValueCollection();
            data["merchant_id"] = merchant_id;
            data["user_ip"] = user_ip;
            data["merchant_oid"] = merchant_oid;
            data["email"] = emailstr;
            data["payment_amount"] = payment_amountstr.ToString();
            //
            // Sepet içerği oluşturma fonksiyonu, değiştirilmeden kullanılabilir.
            JavaScriptSerializer ser = new JavaScriptSerializer();
            string user_basket_json = ser.Serialize(user_basket);
            string user_basketstr = Convert.ToBase64String(Encoding.UTF8.GetBytes(user_basket_json));
            data["user_basket"] = user_basketstr;
            //
            // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
            string Birlestir = string.Concat(merchant_id, user_ip, merchant_oid, emailstr, payment_amountstr.ToString(), user_basketstr, no_installment, max_installment, currency, test_mode, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            data["paytr_token"] = Convert.ToBase64String(b);
            //
            data["debug_on"] = debug_on;
            data["test_mode"] = test_mode;
            data["no_installment"] = no_installment;
            data["max_installment"] = max_installment;
            data["user_name"] = user_namestr;
            data["user_address"] = user_addressstr;
            data["user_phone"] = user_phonestr;
            data["merchant_ok_url"] = merchant_ok_url;
            data["merchant_fail_url"] = merchant_fail_url;
            data["timeout_limit"] = timeout_limit;
            data["currency"] = currency;
            data["lang"] = lang;
    
            using (WebClient client = new WebClient())
            {
                client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                byte[] result = client.UploadValues("https://www.paytr.com/odeme/api/get-token", "POST", data);
                string ResultAuthTicket = Encoding.UTF8.GetString(result);
                dynamic json = JValue.Parse(ResultAuthTicket);
    
                if (json.status == "success")
                { 
                    paytriframe.Attributes["src"] = "https://www.paytr.com/odeme/guvenli/" + json.token;
                    paytriframe.Visible = true;
                }
                else
                {
                    Response.Write("PAYTR IFRAME failed. reason:" + json.reason + "");
                }
            }
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

  


iFrame API 1. Adım örnek kodları[**indirmek için tıklayın.**](/iframe-api/iframe-api-1-adim/PayTR iFrame API 1.ADIM.zip)
