# API Servis Test Araçları | PayTR

# API Servis Test Araçları

**Postman**

PayTR tarafından yayınlanmış olan servislerin testlerini daha kolay bir şekilde gerçekleştirmenize imkan tanıyan "Postman" programına ait Collections dosyalarını kullanmaya başlayabilirsiniz.

Collections dosyalarının yer aldığı Postman sayfasına bu [**linkten**](https://dev.paytr.com/servis-test-araclari/postman) gidebilirsiniz.  


**Hash Hesaplama**

Entegrasyon aşamasının ilk adımı olan 1.ADIM içerisinde hash hesaplaması yapılmalı ve istek bloğunun içerisine dahil edilmelidir. İstek bloğunun içerisindeki değerler ile servis üzerinde tekrar hash hesaplaması yapılmaktadır. İletilen hash değeri ile yapılan hesaplama sonucu çıkan hash değeri karşılaştırılmakta ve isteğin doğrudan mağazadan geldiği onaylanmaktadır.

Hash Hesaplama sayfasına bu [**linkten**](/servis-test-araclari/hash-hesaplama) gidebilirsiniz.  


Token hataları genel olarak, listede bulunan nedenlerden ötürü oluşmaktadır;  
1) merchant_key, merchant_salt gibi bilgilerin hatalı kullanımı,  
2) paytr_token hesabında kullanılan verilerin POST içeriğinde farklı değerde olması,  
3) paytr_token hesabında kullanılan verilerin doğru sıra ile uç uca eklenmemesi,  
4) paytr_token hesabında gerekli olan tüm verilerin eklenmemesi veya gerek duyulmayan verilerin hesaba dahil edilmesi.  


_Hash Hesaplama sayfası üzerinden değerlerinizle birlikte doğru hash hesaplaması yapabilirsiniz._

**Servis Yanıt Gözlem**

Entegrasyon aşaması 2.ADIM'da bildirim/callback tarafı bulunmaktadır. PayTR yapısında bulunan bilgilendirme servisleri dışında(örn: durum sorgulama), tüm ödeme gerçekleştirilen API'lerin 2.ADIM'ında ilgili işleme ait detay tanımlı olan Bildirim URL adresinize POST metodu ile gönderilmektedir. PayTR tarafından dönen örnek yanıta Servis Yanıt Gözlem alanından ulaşabilirsiniz. Bildirim URL sayfanıza dönen yanıtlar sayfa üzerinde "PayTR tarafından tanımlı olan Bildirim URL adresinize dönen yanıt" ibaresi altında belirtilmiştir. Sayfa üzerinden "Başarılı" veya "Başarısız" dönen yanıtlara, sayfa üzerinde bulunan form yapısını veya JSON alanını kullanarak ulaşabilirsiniz.

Servis Yanıt Gözlem sayfasına bu [**linkten**](/servis-test-araclari/servis-yanit-gozlem) gidebilirsiniz.  

