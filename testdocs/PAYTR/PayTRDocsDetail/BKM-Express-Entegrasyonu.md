# BKM Express Entegrasyonu | PayTR

# BKM Express Entegrasyonu

BKM Express servisi aracılığıyla, BKM Express sisteminde kayıtlı kartlar aracılığıyla ödeme alabilirsiniz.

BKM Express Entegrasyonu iFrame ödeme yönteminde otomatik olarak ödeme ekranına gelmektedir. Ancak Direkt API çözümünde BKM Express entegrasyonu yaparken $payment_type = "bex" olarak gönderilmesi gerekmektedir. 

Değişkenler | Açıklamalar  
---|---  
merchant_id | Mağaza no  
merchant_key | Mağaza parola  
merchant_salt | Mağaza gizli anahtar  
merchant_oid | Sipariş numarası  
payment_amount | Siparişe ait toplam Tutar  
user_ip | Kullanıcıdan alınan ip adresi  
email | Kullanıcının email adresi  
payment_type | Bkm Express için bex olarak gönderilmesi gereklidir.  
installment_options | Taksit seçenekleri opsiyoneldir. Göndermediğiniz takdirde müşterinize taksit seçenekleri gösterilmeyecektir. Aşağıda verilen değerler örnektir. Siz komisyon oranlarınıza göre tutarları hesaplayıp aşağıdaki kısmı düzenlemelisiniz.  
  
  


**BKM Express Test Kullanıcı Bilgileri**

Kullanıcı bilgisi | Banka  
---|---  
0010@banka.com | ZİRAAT BANKASI  
0012@banka.com | HALK BANKASI  
0015@banka.com | VAKIFBANK  
0032@banka.com | TEB  
0046@banka.com | AKBANK  
0062@banka.com | GARANTİ  
0064@banka.com | İŞBANK  
0067@banka.com | YAPI KREDİ  
0134@banka.com | DENİZBANK  
0111@banka.com,qnbfinans@bkm.com | FİNANSBANK  
  
  
Tüm kullanıcıların şifreleri 147258'dir.

Bkm Express örnek kodları:

  * PHP


    
    
    <?php
    
    $merchant_id = '';
    $merchant_key = '';
    $merchant_salt = '';
    
    $user_basket = htmlentities(json_encode(array(
        array("Örnek ürün 1", "18.00", 1),
        array("Örnek ürün 2", "33.25", 2),
        array("Örnek ürün 3", "45.42", 1)
    )));
    
    $merchant_oid = $_POST['merchant_oid'];
    
    $test_mode = 1;
    
    if (isset($_SERVER["HTTP_CLIENT_IP"])) {
        $ip = $_SERVER["HTTP_CLIENT_IP"];
    } elseif (isset($_SERVER["HTTP_X_FORWARDED_FOR"])) {
        $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
    } else {
        $ip = $_SERVER["REMOTE_ADDR"];
    }
    $user_ip = $ip;
    
    $email = "testbex@siteniz.com";
    $payment_amount = "15.20";
    
    $installment_count = 0;
    
    $payment_type = "bex";
    
    /* Taksit seçenekleri opsiyoneldir. Göndermediğiniz takdirde müşterinize taksit seçenekleri gösterilmeyecektir. */
    /* Aşağıda verilen değerler örnektir! Siz komisyon oranlarınıza göre tutarları hesaplayıp aşağıdaki kısmı düzenlemelisiniz. */
    /* DİKKAT: Oluşturacağınız JSON tek satır olması ve arasında herhangi bir enter, vb. olmaması gerekmektedir. */
    
    $installment_options = '{"advantage":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"axess":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"bonus":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"combo":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"cardfinans":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"maximum":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"paraf":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8},'.
    '"world":{"2":20.2,"3":30.9,"4":40.8,"5":50.4,"6":60.4,"7":70.2,"8":80.1,"9":90.5,"10":100.3,"11":110.2,"12":120.8}}';
    
    $hash_str = $merchant_id . $user_ip . $merchant_oid . $email . $payment_amount . $payment_type . $installment_count . $test_mode . $installment_options;
    $token = base64_encode(hash_hmac('sha256', $hash_str . $merchant_salt, $merchant_key, true));
    
    $post = [
        'merchant_id' => $merchant_id,
        'user_ip' => $user_ip,
        'merchant_oid' => $merchant_oid,
        'email' => $email,
        'payment_type' => $payment_type,
        'payment_amount' => $payment_amount,
        'installment_count' => $installment_count,
        'test_mode' => $test_mode,
        'user_name' => "TEST NAME",
        'user_address' => "USER TEST ADDRESS",
        'user_phone' => "05555555555",
        'user_basket' => $user_basket,
        'debug_on' => 1,
        'paytr_token' => $token,
        'installment_options' => $installment_options
    ];
    
    $ch = curl_init('https://www.paytr.com/odeme');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_vals);
    curl_setopt($ch, CURLOPT_FRESH_CONNECT, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 90);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 90);
    
    //XXX: DİKKAT: lokal makinanızda "SSL certificate problem: unable to get local issuer certificate" uyarısı alırsanız eğer
    //aşağıdaki kodu açıp deneyebilirsiniz. ANCAK, güvenlik nedeniyle sunucunuzda (gerçek ortamınızda) bu kodun kapalı kalması çok önemlidir!
    //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    
    $response = @curl_exec($ch);
    
    if (curl_errno($ch)) {
        echo curl_error($ch);
        curl_close($ch);
        exit;
    }
    
    curl_close($ch);
    
    exit($response);
    ?>

BKM Express örnek kodları [**indirmek için tıklayın.**](/bkm-express/PayTR BKM Express Örnek.zip)
