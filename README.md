<div dir="rtl">

# 🛍️ LiaraShop

### فروشگاه اینترنتی مدرن و ماژولار مبتنی بر Django

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-5.1.6-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge" alt="License" />
</p>

<p align="center">
  یک پروژه فروشگاهی کامل با تمرکز بر تجربه کاربری، مدیریت محتوا، سبد خرید، حساب کاربری و فرآیند سفارش
</p>

---

## 📌 معرفی پروژه

**LiaraShop** یک فروشگاه اینترنتی توسعه‌یافته با **Django** است که با معماری ماژولار طراحی شده تا بخش‌های مختلف یک فروشگاه آنلاین را از مدیریت محصولات و کاربران تا سبد خرید، سفارش‌ها و داشبورد مشتری پوشش دهد.

در این پروژه تلاش شده است علاوه بر پیاده‌سازی قابلیت‌های اصلی فروشگاه، مواردی مانند **مدیریت محتوای داینامیک، آدرس‌های کاربر، علاقه‌مندی‌ها، اعلان‌ها، نظرات محصولات، فیلتر و صفحه‌بندی محصولات و سبد خرید مبتنی بر Session** نیز در نظر گرفته شود.

> 🎯 هدف اصلی پروژه: ساخت یک هسته قابل توسعه برای فروشگاه اینترنتی با ساختار تمیز، ماژولار و قابل نگهداری.

---

## ✨ قابلیت‌های اصلی

### 🛒 فروشگاه و محصولات

- نمایش محصولات و دسته‌بندی‌ها
- صفحه اختصاصی جزئیات محصول
- نمایش ویژگی‌ها و توضیحات محصول
- سیستم نظرات محصولات
- فیلتر محصولات بر اساس قیمت و دسته‌بندی
- Pagination برای لیست محصولات
- مدیریت محصولات از طریق پنل مدیریت Django
- نمایش بنرهای داینامیک
- مدیریت محتوای صفحات عمومی

### 🧺 سبد خرید

- افزودن محصول به سبد خرید
- حذف محصول از سبد خرید
- تغییر تعداد محصولات
- محاسبه تعداد و مبلغ سبد خرید
- نگهداری سبد خرید کاربران مهمان با **Session**
- امکان مدیریت سبد خرید در حساب کاربری

### 👤 حساب کاربری

- ثبت‌نام و ورود کاربران
- سیستم احراز هویت اختصاصی
- پروفایل کاربر
- ویرایش اطلاعات حساب
- تغییر رمز عبور
- مدیریت سفارش‌ها
- مدیریت علاقه‌مندی‌ها
- مدیریت آدرس‌های ارسال
- انتخاب آدرس پیش‌فرض
- مدیریت اعلان‌ها
- مدیریت نظرات ثبت‌شده

### 📍 مدیریت آدرس

- ثبت چند آدرس برای کاربر
- محدودیت تعداد آدرس‌های ذخیره‌شده
- انتخاب یک آدرس به عنوان آدرس پیش‌فرض
- استفاده از آدرس پیش‌فرض در فرآیند ارسال سفارش

### 🔔 اعلان‌ها و ارتباط با کاربر

- ایجاد اعلان از سمت مدیریت
- تاریخ ایجاد و انقضای اعلان
- نمایش اعلان‌ها در داشبورد کاربر
- صفحه تماس با ما بدون نیاز به احراز هویت

### 📝 مدیریت محتوا

- صفحه «درباره ما» با قابلیت ویرایش از پنل مدیریت
- استفاده از **CKEditor 5** برای مدیریت محتوای Rich Text
- مدیریت بنرها و تنظیمات عمومی سایت
- پشتیبانی از محتوای فارسی و تاریخ شمسی

---

## 🧩 ساختار ماژول‌ها

پروژه به چند اپلیکیشن مستقل تقسیم شده است تا مسئولیت هر بخش مشخص و قابل توسعه باشد:

```text
Liara-Shop-django/
│
├── Shop/                  # تنظیمات اصلی پروژه و URL Configuration
├── Products/              # محصولات و دسته‌بندی‌ها
├── Cart/                  # منطق سبد خرید و Session Cart
├── account/               # کاربران، احراز هویت و پروفایل
├── Dashbord/              # داشبورد مشتری
├── order/                 # سفارش‌ها
├── pyment/                # بخش پرداخت
├── Social/                # امکانات مرتبط با تعاملات اجتماعی
├── core/                  # تنظیمات و قابلیت‌های عمومی پروژه
├── context_processors/    # داده‌های مشترک Templateها
├── templates/             # Templateهای پروژه
├── statics/               # فایل‌های Static
├── media/                 # فایل‌های Media
├── docs/                  # مستندات و تصاویر پروژه
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🏗️ معماری کلی

```text
                        ┌─────────────────────┐
                        │      Browser        │
                        │   Customer / Admin  │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │       Django       │
                        │    Web Framework   │
                        └──────────┬──────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
   │   Products   │        │     Cart     │        │   Account    │
   └──────────────┘        └──────────────┘        └──────────────┘
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   ▼
                         ┌───────────────────┐
                         │    Orders /       │
                         │     Payment       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      SQLite       │
                         │     Database      │
                         └───────────────────┘
```

---

## 🛠️ تکنولوژی‌های استفاده‌شده

| تکنولوژی | کاربرد |
|---|---|
| **Python** | زبان اصلی توسعه |
| **Django 5.1.6** | Backend و Web Framework |
| **SQLite** | دیتابیس فعلی پروژه |
| **Django Templates** | لایه نمایش |
| **CKEditor 5** | مدیریت محتوای Rich Text |
| **Pillow** | پردازش تصاویر |
| **django-jalali / jdatetime** | تاریخ و محتوای شمسی |
| **django-widget-tweaks** | کنترل و شخصی‌سازی فرم‌ها |
| **django-colorfield** | مدیریت رنگ‌ها در پنل مدیریت |
| **python-decouple** | مدیریت تنظیمات و Environment Variables |
| **ghasedak** | زیرساخت ارسال SMS |

---

## 🚀 راه‌اندازی پروژه

### 1. Clone کردن Repository

```bash
git clone https://github.com/mzulfikari/Liara-Shop-django.git
cd Liara-Shop-django
```

### 2. ساخت Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 4. تنظیم Environment Variables

اطلاعات حساس پروژه نباید مستقیماً داخل کد قرار بگیرند. یک فایل `.env` در ریشه پروژه ایجاد کرده و مقادیر موردنیاز را متناسب با محیط خود تنظیم کنید.

نمونه:

```env
SECRET_KEY=your-secret-key
DEBUG=True

# در صورت استفاده از سرویس‌های خارجی
SMS_API_KEY=your-api-key
PAYMENT_API_KEY=your-payment-key
```

> ⚠️ فایل `.env` را در Repository عمومی قرار ندهید و Secretهای واقعی را در Git commit نکنید.

### 5. اجرای Migrationها

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. ساخت Superuser

```bash
python manage.py createsuperuser
```

### 7. اجرای سرور توسعه

```bash
python manage.py runserver
```

سپس پروژه را در آدرس زیر باز کنید:

```text
http://127.0.0.1:8000/
```

پنل مدیریت Django نیز از مسیر زیر در دسترس است:

```text
http://127.0.0.1:8000/admin/
```

---

## ⚙️ تنظیمات مهم

برخی از تنظیمات اصلی پروژه در `Shop/settings.py` قرار دارند، از جمله:

- Custom User Model
- Authentication Backends
- Static & Media Files
- CKEditor 5
- Jalali Date
- Context Processors
- Session Configuration
- Database Configuration

در محیط Production پیشنهاد می‌شود مقادیر زیر حتماً از Environment Variables خوانده شوند:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- اطلاعات Database
- API Keyهای سرویس SMS
- اطلاعات درگاه پرداخت

---

## 🖼️ تصاویر پروژه

تصاویر و مستندات بصری پروژه در مسیر زیر قرار دارند:

```text
docs/image/
```

### صفحه اصلی

![LiaraShop Home](docs/image/Screenshot%202025-09-17%20020448.png)

### فروشگاه و محصولات

![LiaraShop Products](docs/image/Screenshot%202025-09-17%20020602.png)

### جزئیات محصول

![LiaraShop Product Detail](docs/image/Screenshot%202025-09-17%20020624.png)

### داشبورد کاربر

![LiaraShop Dashboard](docs/image/Screenshot%202025-09-17%20020645.png)

---

## 🔐 نکات امنیتی

برای استفاده از پروژه در محیط Production، موارد زیر باید قبل از Deployment بررسی و اصلاح شوند:

- `DEBUG=False`
- تعریف دقیق `ALLOWED_HOSTS`
- انتقال `SECRET_KEY` به Environment Variables
- عدم Commit کردن `.env` و اطلاعات حساس
- استفاده از HTTPS
- تنظیم صحیح Cookieهای امن
- بررسی CSRF و Session Security
- استفاده از دیتابیس Production مناسب در صورت نیاز
- تنظیم صحیح Static و Media Storage
- مدیریت امن کلیدهای سرویس SMS و Payment Gateway

---

## 📈 مسیر توسعه پیشنهادی

برخی قابلیت‌هایی که می‌توانند در نسخه‌های بعدی به پروژه اضافه شوند:

- [ ] REST API با Django REST Framework
- [ ] JWT Authentication
- [ ] اتصال کامل درگاه پرداخت Production
- [ ] سیستم تخفیف و Coupon
- [ ] سیستم امتیازدهی پیشرفته محصولات
- [ ] جستجوی پیشرفته و Full-Text Search
- [ ] Wishlist پیشرفته
- [ ] سیستم مدیریت موجودی و Inventory
- [ ] تست‌های Unit و Integration
- [ ] Docker و Docker Compose
- [ ] Redis و Celery برای Taskهای پس‌زمینه
- [ ] CI/CD با GitHub Actions
- [ ] Logging و Monitoring

---

## 👨‍💻 تیم توسعه

### Backend

**مرتضی ذوالفقاری**

- GitHub: [@mzulfikari](https://github.com/mzulfikari)
- Telegram: [@mzulfiqari](https://t.me/mzulfiqari)

### Frontend

**اکرام تاجیک**

- GitHub: [@ekramtajik](https://github.com/ekramtajik)

---

## 📄 License

این پروژه برای اهداف توسعه و نمونه‌کار ایجاد شده است. در صورت استفاده مجدد از کد یا توسعه آن، رعایت حقوق صاحبان پروژه و مستندات مربوطه توصیه می‌شود.

---

<p align="center">
  Made with ❤️ and Django
</p>

</div>
