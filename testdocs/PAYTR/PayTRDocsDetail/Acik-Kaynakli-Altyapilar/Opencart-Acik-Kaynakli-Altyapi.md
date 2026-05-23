# Opencart Açık Kaynaklı Altyapı | PayTR

# Opencart Açık Kaynaklı Altyapı

![](/images/b/a/1/7/3/ba173db48d3137b107996faf90ece5db653e707e-opencart.png)

“OpenCart modülümüz resmi sürümler üzerinde, en sade haliyle (eklentisiz) geliştirilmiştir. Journal temasını ve Tek Sayfa Ödeme metodunu desteklemektedir.”

**1\. Kurulum**

Otomatik Kurulum Opencart Yönetim Paneline giriş yaptıktan sonra;

  * **Eklentiler > Eklenti Yükle** adımlarını takip edin.



![1](/user/pages/16.moduller/01.opencart/1.PNG)

  * **Yükle** butonuna basın ve indirdiğiniz Opencart sürümünüze uygun **.ocmod.zip** uzantılı dosyayı seçin.



![2](/user/pages/16.moduller/01.opencart/2.PNG)

  * Yükleme işlemi tamamlandığında başarılı mesajı ile karşılaşacaksınız.



![3](/user/pages/16.moduller/01.opencart/3.PNG)

  * Bu adımları tamamladıktan sonra **Eklentiler > Ödeme Metotları** adımlarını takip edin.
  * Listeden **PayTR Sanal POS - iFrame API** modülünü bulun ve **Kur** seçeneği ile kurulum yapın.



![4](/user/pages/16.moduller/01.opencart/4.PNG)

  * Kurulum işlemi tamamlanmıştır. Bundan sonrasını **Ayarların Yapılandırılması** başlığı altından takip edebilirsiniz.



**Manuel Kurulum**

  * İndirdiğiniz Opencart sürümünüze uygun **.ocmod.zip** uzantılı dosyayı klasöre çıkartın.
  * Çıkan **upload** klasörü içerisindeki dosyaları sitenizin olduğu dizine kopyalayın.
  * **Eklentiler > Ödeme Metotları** adımlarını takip edin.
  * Listeden **PayTR Sanal POS - iFrame API** modülünü bulun ve **Kur** seçeneği ile kurulum yapın.
  * Kurulum işlemi tamamlanmıştır. Bundan sonrasını **Ayarların Yapılandırılması** başlığı altından takip edebilirsiniz.



**2\. Ayarların Yapılandırılması**

  * Kurulumu tamamladıktan sonra, **Düzenle** seçeneği ile ayarlar sayfasına ulaşın.



![5](/user/pages/16.moduller/01.opencart/5.PNG)

**Genel Ayarlar**

**Mağaza No, Mağaza Parola ve Mağaza Gizli Anahtar** bilgilerinize https://www.paytr.com/magaza/bilgi adresinden ulaşabilirsiniz. Gerekli bilgileri ilgili alanlara doldurunuz.

**Dil:** Ödeme sayfasının dilinizi ayarlamanıza yardımcı olur. Bu dil seçeneği ayrıca ödeme sayfası üzerinde de bulunur. Toplam: PayTR Ödeme modülünün Ödeme Yöntemleri içerisinde aktif olması için, sepetin ulaşması gereken toplam tutarı bu alana girebilirsiniz.

**Ödeme Sayfası:** Tek Sayfa Ödeme seçeneği sunan temalar veya modüllerde uyumluluğu sağlamak için bu seçeneği kullanabilirsiniz. Standart ve Tek Sayfa olarak 2 seçenek bulunur.

**Not:** Temalar iFrame Ödeme Yöntemi sunan sağlayıcılar için seçenek sunabilmektedir. Aşağıdaki resimde Journal Temasının 3.1 sürümünde gelmiş olan seçeneğini görebilirsiniz. Bu tarz seçenek sunan temalarda, özelliği aktif ederek Standart seçeneğini kullanabilirsiniz. _İlgili sayfaya Opencart Yönetim Paneli > Journal > Skins > Default > Checkout adımlarını takip ederek ulaşabilirsiniz._

![6](/user/pages/16.moduller/01.opencart/6.PNG)

**Durum:** Modül durumunu açık veya kapalı olarak ayarlayabilirsiniz.

**Sıralama:** PayTR Ödeme modülünün Ödeme Yöntemleri içerisindeki sıralamasını belirleyebilirsiniz.

**Sipariş Durumları**

**Başarılı Ödeme:** Ödemenin başarılı olduğu zaman atanacak durumu belirleyebilirsiniz.

**Başarısız Ödeme:** Ödemenin başarısız olduğu zaman atanacak durumu belirleyebilirsiniz.

**Sipariş Notunu Müşteriye Gönder:** Ödeme işlemli sonunda müşteriye sipariş notunun gönderilip gönderilemeyeceğini seçebilirsiniz. Bu seçenek aktif edilirse, doğru çalışması için e-posta ayarlarınızın düzgün yapılandırıldığından emin olun.  


**Vade Farkını Göster:**

**Açık seçeneği** ; sipariş alt toplamına **Vade Farkı** satırı ekler ve **Faturanın Toplam Tutarını** değiştirir.

**Toplam Tutarı Değiştir seçeneği** ; sadece **Faturanın Toplam Tutarını** değiştirir.

**Sipariş Tutarını Değiştir** : Taksitli ödemelerde **Ödenen Toplam Tutarı (vade farkı dahil)** siparişin **Toplam Tutarı** ile değiştirir. Bu seçenek faturayı etkilemez.  


**Taksit Ayarları**

Taksit kısıtlamalarını ayarlayabilirsiniz. Kategori Bazlı taksit seçeneği ile her kategori için taksit seçeneği belirleyebilirsiniz. Sepette bulunan farklı kategorideki ürünler için taksit seçeneği en düşük olan geçerli olur.

**3\. Bildirim URL’in Ayarlanması**

PayTR Mağaza Paneline giriş yapın, menüden **Ayarlar** bağlantısına tıklayarak ayarlar sayfasına ulaşın. **Bildirim URL Ayarı (Callback URL)** bölümünde bulunan **Değiştir** butonuna tıklayın. Açılan ilgili bölümde Opencart sürümünüze uygun olan seçeneklerden bir tanesini seçin ve **Kaydet** butonuna basarak değişiklikleri kaydedin. Eğer sitenizde **SSL** varsa, **Protokol** seçeneğinden **https://** seçeneğini seçin. Eğer **SSL** sertifikanız yoksa, **http://** seçeneğini seçin. Daha sonradan **SSL** kurulumu yaparsanız buradaki **Protokol** ’ü **https://** olarak güncelleyin.

**4\. Kullanmaya Başlama**

Sepetinize ürün ekleyerek ödeme sayfasına kadar ilerleyin.

![7](/user/pages/16.moduller/01.opencart/7.PNG)

Ödeme sayfasına geldiğinizde yukarıdaki ekran ile karşılaşırsınız. Eğer PayTR Mağazanız Canlı durumdaysa yukarıdaki ekran yerine Canlı Mod ekranını göreceksiniz. Test modu ekranı ile karşılaşırsanız, Canlı Moda geçmeden önce 1 veya 2 kere test işlemi yapmanız gerekmektedir. Bu bölüme kadar olan tüm adımları eksiksiz tamamladıktan sonra ödeme almaya başlayabilirsiniz.

**5\. Sipariş Detayları**

PayTR Sanal POS – iFrame API modülü ile başarılı ödeme alınan siparişlerin detayına aşağıdaki gibi not düşülür. Burada sipariş ile ilgili PayTR Mağaza Paneli eşleşen detayları görebilirsiniz.

![8](/user/pages/16.moduller/01.opencart/8.PNG)

Taksitli ödemelerde bu nota ilave olarak **Vade Farkı** da eklenir. Başarısız ödemeler için not aşağıdaki gibidir. 

![9](/user/pages/16.moduller/01.opencart/9.PNG)

Ödeme hatası mesajı alınan hataya göre değişiklik gösterir.

**6\. İade Yapma**

Sipariş detayında bulunan PayTR Sanal POS – iFrame API sekmesinde, başarılı ödeme yapılmış işlemlere iade yapabilirsiniz.

![10](/user/pages/16.moduller/01.opencart/10.PNG)

Taksitli ödemelerde **Toplam Ödenen, Toplam tutardan** farklı olabilmektedir. İade girişine **Toplam** tutarın girilmesi gerekmektedir. Vade farkını girmeniz gerekmez.

**_PayTR Mağaza Panelinden yapılan iadeler, bu sekmeye yansıtılmamaktadır_**

[**OpenCart tüm versiyonları için(Desteklenen Versiyonlar: 1.5.x - 2.x - 3.x - 4.x**](https://www.opencart.com/index.php?route=marketplace%2Fextension%2Finfo&extension_id=38301%2F%3Ftarget%3Dblank)

OpenCart iFrame API Ödeme Modülü Kurulum Dökümanı [**indirmek için tıklayın.**](/moduller/opencart/PayTR_iFrame_API_OpenCart_Modül_Entegrasyonu.zip)
