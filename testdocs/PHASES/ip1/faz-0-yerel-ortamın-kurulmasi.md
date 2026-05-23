# Geliştirici: 

* EMİRHAN KURU

## Yeni Tenant (Müşteri) Kurulum Adımları

Yeni bir veritabanı (tenant) açmak ve sistemi hazırlamak için sırasıyla aşağıdaki adımları izleyin:

1. `.env` dosyası içerisindeki `DATABASE_URL` değişkenine yeni veritabanı adını (hedef DB adını) yazın.
2. PostgreSQL'de ilgili veritabanını oluşturmak için şu komutu çalıştırın:
   ```bash
   npx ts-node prisma/create-tenant-db.ts
   ```
3. Bağımlılıkları temiz bir şekilde kurun:
   ```bash
   npm ci
   ```
4. Prisma istemcisini güncelleyin:
   ```bash
   npx prisma generate
   ```
5. Veritabanı tablolarını yeni oluşturulan veritabanına basın:
   ```bash
   npx prisma migrate deploy
   ```
6. Varsayılan admin hesabını (seed) içeri aktarın:
   ```bash
   npx prisma db seed
   ```