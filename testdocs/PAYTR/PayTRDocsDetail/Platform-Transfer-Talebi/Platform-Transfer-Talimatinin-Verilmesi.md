# Platform Transfer Talimatının Verilmesi | PayTR

# Platform Transfer Talimatının Verilmesi

**Mağaza aşağıdaki bilgileri Platform Transfer API’sine gönderir.**

  * İstek (REQUEST) yapılacak URL: https://www.paytr.com/odeme/platform/transfer



**Token üretiminde kullanılacak veriler**

Alan adı / tipi | Açıklama | Zorunlu | Kısıtlar  
---|---|---|---  
merchant_id | Mağaza No: PayTR tarafından size verilen Mağaza numarası | Evet |   
merchant_oid (string) | Mağaza sipariş no: Satış işleminde gönderdiğiniz benzersiz sipariş numaranız | Evet | En fazla 64 karakter,Alfa numerik  
trans_id (string) | Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası | Evet | Alfanumerik – En fazla 60 karakter  
submerchant_amount (integer) | Satıcıya yapılacak ödeme tutarı:Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali | Evet | Örn: 34.56 TL için 3456 gönderilmelidir  
total_amount (integer) | Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali | Evet | Örn: 94.56 TL için 9456 gönderilmelidir. (94.56 * 100 = 9456)  
transfer_name (string) | Satıcının banka hesabı için ad soyad/ünvanı | Evet | Örn: Ragıp Adıgüzel  
transfer_iban(int) | Satıcının banka hesabı IBAN numarası | Evet | Örn: TRXX XXXX XXXX XXXX XXXX XXXX XX (26 Karakter)  
merchant_salt | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet |   
merchant_key | PayTR Mağaza Paneli > Destek & Kurulum > Entegrasyon Bilgileri sayfası üzerinden ulaşabileceğiniz, mağazanıza özgü değer. | Evet |   
  
  


  * POST REQUEST içeriğinde gönderilecek değerler:

Alan adı / tipi | Zorunlu | Token | Açıklama | Kısıtlar  
---|---|---|---|---  
merchant_id(integer) | Evet | Evet | Mağaza no: PayTR tarafından size verilen Mağaza numarası |   
merchant_oid (string) | Evet | Evet | Mağaza sipariş no: Satış işleminde gönderdiğiniz benzersiz sipariş numaranız | En fazla 64 karakter,Alfa numerik  
trans_id | Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası | Evet | Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası | Alfanumerik – En fazla 60 karakter  
submerchant_amount(integer) | Evet | Evet | Satıcıya yapılacak ödeme tutarı:Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali | Örn: 34.56 TL için 3456 gönderilmelidir  
total_amount(integer) | Evet | Evet | Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali | Örn: 94.56 TL için 9456 gönderilmelidir  
transfer_name (string) | Evet | Evet | Satıcının banka hesabı için ad soyad/ünvanı | Örn: Ragıp Adıgüzel  
transfer_iban | Evet | Evet | Satıcının banka hesabı IBAN numarası | Örn: TRXX XXXX XXXX XXXX XXXX XXXX XX (26 Karakter)  
paytr_token (string) | Evet | Hayır | paytr_token: İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir | Nasıl hesaplanacağı hakkında lütfen örnek kodları inceleyin  
  
  


**STOPAJ BİLGİLENDİRMESİ**

02.08.2024 tarihli Resmi Gazete'de yayınlanan 7524 sayılı Kanun ile 193 sayılı Gelir Vergisi Kanunu ve 5520 sayılı Kurumlar Vergisi Kanunu'nda yapılan değişikliğin ardından pazaryerlerinde yapılan satışların üzerinden stopaj kesintisi uygulamasına yönelik düzenleme 1 Ocak 2025 tarihinde yürürlüğe girmiştir.

Büyüyen e-ticaret pazarında adil vergilendirilme yapılmasına yönelik yeni düzenlemeyle birlikte, 21.12.2024 tarihli ve 9284 sayılı Cumhurbaşkanı kararı ile Gelir Vergisi Kanunu ve Kurumlar Vergisi Kanunu kapsamında hizmet sağlayıcıları ve elektronik ticaret hizmet sağlayıcılarının yapılan satışlar üzerinden %1 oranında stopaj ödemesine karar verilmiştir.

Alt satıcılarına ödemelerini transfer eden pazaryeri üye işyerlerimizin hakedişlerini belirlemek için stopaj tutarını KDV ve vergiler hariç, net satış tutarı üzerinden hesaplamaları gerekmektedir. Tüm detaylara ve örnek hesaplama tablosuna aşağıdaki linkten ulaşabilirsiniz.

Ürün Satış Fiyatı | Kdv Oranı | Kdv Tutarı | Kdv ve Vergiler Düşürüldükten Sonra Net Ürün Fiyatı | Stopaj Tutarı | Pazaryeri Tarafından Belirlenen Alt Satıcı Hakedişi | Stopaj Tutarı Düşürüldükten Sonra Alt Satıcı Yeni Hakedişi  
---|---|---|---|---|---|---  
100 | %20 | 20₺ | 80₺ | 80₺ X 0.01=0.8₺ | 95 | 94.2  
  
**ÖNEMLİ NOTLAR**

1- Mağaza, ödemenin yapılmasını istediği tarihte en geç saat 10:00’a kadar Transfer API’si yoluyla isteği göndermelidir. Daha sonra gönderilen istekler bir sonraki gün işleme alınacaktır.

2- Sipariş ödemesi ile aynı gün transfer talebi oluşturamazsınız. Talebi en erken, ödemeyi takip eden ilk gün oluşturmanız gerekmektedir.

**TRANSFER ÖRNEKLERİ (Değerler gerçek değildir. Sadece örnektir)**

**ÖRNEK 1: ÖDEMEDE TEK ALT SATICI OLMASI DURUMU**

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 100 TL

• Sipariş numarası (merchant_oid): 123ABCD

• Takip numarası (trans_id): 45ABT34

• Satıcı ile olan komisyon oranınıza göre (Örnek: %8) satıcıya aktarılacak (submerchant_amount): 92 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 100 TL Bu bilgilerle ödeme talimatı verdiğinizde;

• Satıcıya 92 TL ödenir,

• Kalan 8 TL içerisinden PayTR ile olan komisyon oranınız (Örnek: %3) düşülerek kalan tutar (örneğe göre 5 TL) firmanızın hesabına aktarılır. Yapılan kesinti tarafınıza faturalandırılır. 

* * *

**ÖRNEK 2: ÖDEMEDE BİRDEN FAZLA ALT SATICI OLMASI DURUMU**

Sipariş ödemesi birden fazla satıcıyı kapsayabilir. Örneğin; Kart hamili alışveriş sepetinde birden fazla satıcıdan ürün / hizmet alıyor olabilir. Siparişin toplam bedelinin 300 TL olduğunu düşünelim. Bu durumda,

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 300 TL

• Sipariş numarası (merchant_oid): 123ABCDE

• Takip numarası (trans_id): 75ZTY39

• Satıcı ile olan komisyon oranınıza göre (Örnek: %8) satıcıya aktarılacak (submerchant_amount): 92 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 100 TL

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 300 TL

• Sipariş numarası (merchant_oid): 123ABCDE

• Takip numarası (trans_id): DF43DFC

• Satıcı ile olan komisyon oranınıza göre (Örnek: %5) satıcıya aktarılacak (submerchant_amount): 47,5 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 50 TL

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 300 TL

• Sipariş numarası (merchant_oid): 123ABCDE

• Takip numarası (trans_id): 98DFVXS

• Satıcı ile olan komisyon oranınıza göre (Örnek: %10) satıcıya aktarılacak (submerchant_amount): 135 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 150 TL şeklinde birden fazla ödeme talimatı verebilirsiniz. 

* * *

**ÖRNEK 3: ÖDEMENİN ALT SATICI İÇİN OLMAMA DURUMU**

Yazılımınız üzerinden geçen diğer ödemeler için (örneğin 50 TL üyelik ücreti, hizmet bedeli, vb.) eğer tutarın tamamını firmanız hesabına almak istiyorsanız,

• Mağaza numarası (merchant_id): 100001

• Sipariş tutarı: 50 TL

• Sipariş numarası (merchant_oid): 1881ABCD

• Takip numarası (trans_id): 18ATT81

• Satıcı ile olan komisyon oranınıza göre (Örnek: %0) satıcıya aktarılacak (submerchant_amount): 0 TL

• Ödemesi yapılacak işlem tutarı (total_amount): 50 TL şeklinde talep oluşturduğunuz durumda tutarın tamamı firmanız hesabına transfer edilecektir.

* * *

**Yapılan isteğe geri dönecek yanıt (RESPONSE) JSON formatındadır. Detaylar için örnek kodları inceleyebilirsiniz.**

  * PHP
  * PYTHON
  * .NET
  * NODEJS


    
    
    <?php
    
        $merchant_id = 'MAGAZA_NO';
        $merchant_key = 'XXXXXXXXXXX';
        $merchant_salt = 'YYYYYYYYYYY';
    
        // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
        $merchant_oid = "";
    
        // Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası
        $trans_id = time();
    
        // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        $submerchant_amount = "";
    
        // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
        $total_amount = "";
    
        // Satıcının banka hesabı için ad soyad/ünvanı
        $transfer_name = "";
    
        // Satıcının banka hesabı IBAN numarası
        $transfer_iban = "";
    
        // İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir
        $hash_str = $merchant_id . $merchant_oid . $trans_id . $submerchant_amount . $total_amount . $transfer_name . $transfer_iban;
        $token = base64_encode(hash_hmac('sha256',$hash_str.$merchant_salt,$merchant_key,true));
    
        $post_vals=array(
                'merchant_id'=>$merchant_id,
                'merchant_oid'=>$merchant_oid,
                'trans_id'=>$trans_id,
                'submerchant_amount'=>$submerchant_amount,
                'total_amount'=>$total_amount,
                'transfer_name'=>$transfer_name,
                'transfer_iban'=>$transfer_iban,
                'paytr_token'=>$token
            );
    
        $ch=curl_init();
        curl_setopt($ch, CURLOPT_URL, "https://www.paytr.com/odeme/platform/transfer");
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
            die("PAYTR platform transfer request connection error. err:".curl_error($ch));
    
        curl_close($ch);
    
        $result=json_decode($result,1);
    
        /*
            Başarılı yanıt örneği:
            {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
            Başarısız yanıt örneği:
            {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
        */
    
        if($result['status']=='success')
        {
            //VT işlemleri vs.
        }
        else
        {
            echo $result['err_no']." - ".$result['err_msg'];
        }
        #########################################################################
    
    ?>
    
    
    # Python 3.6+
    
    import base64
    import hashlib
    import hmac
    import json
    import requests
    import random
    
    # API Entegrasyon Bilgilier - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = 'MAGAZA_NO'
    merchant_key = b'XXXXXXXXXXX'
    merchant_salt = 'YYYYYYYYYYY'
    
    # Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası
    merchant_oid = ''
    
    # Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası
    trans_id = random.randint(1, 9999999).__str__()
    
    # Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
    submerchant_amount = ''
    
    # Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
    total_amount = ''
    
    # Satıcının banka hesabı için ad soyad/ünvanı
    transfer_name = ''
    
    # Satıcının banka hesabı IBAN numarası
    transfer_iban = ''
    
    # İsteğin sizden geldiğine ve içeriğin değişmediğine emin olmamız için oluşturacağınız değerdir
    hash_str = merchant_id + merchant_oid + trans_id + submerchant_amount + total_amount + transfer_name + transfer_iban + merchant_salt
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    
    params = {
        'merchant_id': merchant_id,
        'merchant_oid': merchant_oid,
        'trans_id': trans_id,
        'submerchant_amount': submerchant_amount,
        'total_amount': total_amount,
        'transfer_name': transfer_name,
        'transfer_iban': transfer_iban,
        'paytr_token': paytr_token
    }
    
    result = requests.post('https://www.paytr.com/odeme/platform/transfer', params)
    res = json.loads(result.text)
    
    """
    Başarılı yanıt örneği:
    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
    Başarısız yanıt örneği:
    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
    """
    
    if res['status'] == 'success':
        # VT işlemleri vs.
        print(res)
    else:
        print(res['err_no'] + ' - ' + res['err_msg'])
    
    
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
    
    public partial class platform_transfer_talebi_ornek : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e) {
    
            // ####################### DÜZENLEMESİ ZORUNLU ALANLAR #######################
            //
            // API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
            string merchant_id      = "XXXXXX";
            string merchant_key     = "YYYYYYYYYYYYYY";
            string merchant_salt    = "ZZZZZZZZZZZZZZ";
            //
            // Mağaza sipariş no: Satış işlemi için belirlediğiniz benzersiz sipariş numarası 
            string merchant_oid     = "";
            //
            // Satıcıya yapılacak bu ödemenin takibi için benzersiz takip numarası 
            string trans_id     = "";
            //
            // Satıcıya yapılacak ödeme tutarı: Satıcıya bu sipariş için ödenecek tutarın 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
            string submerchant_amount  = "";
            //
            // Toplam ödeme tutarı: Siparişe ait toplam ödeme tutarının 100 ile çarpılmış hali (Örnek: 50.99 TL için 5099)
            string total_amount    = ""; 
            //
            // Satıcının banka hesabı için ad soyad/ünvanı
            string transfer_name    = "";
            //
            // Satıcının banka hesabı IBAN numarası
            string transfer_iban    = "";
            //
    
            // Gönderilecek veriler oluşturuluyor
            NameValueCollection data = new NameValueCollection();
            data["merchant_id"] = merchant_id;
            data["merchant_oid"] = merchant_oid;
            data["trans_id"] = trans_id;
            data["submerchant_amount"] = submerchant_amount.ToString();
            data["total_amount"] = total_amount.ToString();
            data["transfer_name"] = transfer_name;
            data["transfer_iban"] = transfer_iban;
            //
            // Token oluşturma fonksiyonu, değiştirilmeden kullanılmalıdır.
            string Birlestir = string.Concat(merchant_id, merchant_oid, trans_id, submerchant_amount.ToString(), total_amount.ToString(), transfer_name, transfer_iban, merchant_salt);
            HMACSHA256 hmac = new HMACSHA256(Encoding.UTF8.GetBytes(merchant_key));
            byte[] b = hmac.ComputeHash(Encoding.UTF8.GetBytes(Birlestir));
            data["paytr_token"] = Convert.ToBase64String(b);
            //
    
            using (WebClient client = new WebClient()) {
                client.Headers.Add("Content-Type", "application/x-www-form-urlencoded");
                byte[] result = client.UploadValues("https://www.paytr.com/odeme/platform/transfer", "POST", data);
                string ResultAuthTicket = Encoding.UTF8.GetString(result);
                dynamic json = JValue.Parse(ResultAuthTicket);
    
                /*
                    Başarılı yanıt örneği:
                    {"status":"success", "merchant_amount":"5", "submerchant_amount":"92", "trans_id":"45ABT34", "reference":"12SF45" }
    
                    Başarısız yanıt örneği:
                    {"status":"error", "err_no":"010", "err_msg":"toplam transfer tutarı kalan tutardan fazla olamaz"}
                */
                if (json.status == "success") {
                    //VT işlemleri vs.
                    Response.Write(json);
                }else{
                    Response.Write("PAYTR platform transfer request failed. reason:" + json.err_msg + "");
                }
            }
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
    

Transfer talimatının verilmesi örnek kodları[**indirmek için tıklayın.**](/platform-transfer-talebi/transfer-talimatinin-verilmesi/paytr_platform_transfer_talebi.zip)
