## Tanoor back-end

یک API مبتنی بر جنگو برای لیست کردن غذاها، ثبت‌نام/ورود کاربران و مدیریت سبد خرید.

### ویژگی‌ها

- ثبت‌نام و ورود کاربران (احراز هویت JWT)
- نمایش لیست غذاها با تصاویر و جزئیات
- افزودن، کاهش و پاک کردن سبد خرید (مبتنی بر سشن)
- مدل کاربری سفارشی (ورود مبتنی بر شماره تلفن)

### پیش‌نیازها

- Python 3.8+
- Django 4.x
- djangorestframework
- djangorestframework-simplejwt
- Pillow
- drf-yasg (برای مستندات Swagger)

### دستورالعمل‌های راه‌اندازی

1. **کلون کردن مخزن:**
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **ایجاد و فعال‌سازی محیط مجازی:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **نصب وابستگی‌ها:**
   ```bash
   pip install -r requirements.txt
   ```

4. **اعمال مهاجرت‌ها:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **ایجاد سوپریوزر:**
   ```bash
   python manage.py createsuperuser
   ```

6. **اجرای سرور توسعه:**
   ```bash
   python manage.py runserver
   ```

7. **دسترسی به API:**
   - لیست غذاها: `GET /foods/`
   - ثبت‌نام: `POST /register/`
   - ورود: `POST /login/`
   - افزودن به سبد: `GET /add-to-basket/<id>/`
   - کاهش سبد: `GET /decrease_basket/<id>/`
   - پاک کردن سبد: `GET /clear_basket/`
   - مستندات API (Swagger): `GET /swagger/`

### نکات

- برای آپلود تصاویر، اطمینان حاصل کنید که `MEDIA_ROOT` و `MEDIA_URL` در `settings.py` تنظیم شده‌اند.
- از ابزارهایی مانند Postman برای تست نقاط پایانی API استفاده کنید.
- مستندات API از طریق Swagger در آدرس `/swagger/` قابل دسترسی است.
- توکن‌های JWT برای احراز هویت استفاده می‌شوند (به جز نقاط پایانی سبد خرید).

---

**توسعه‌دهنده: [نام شما]**

لطفاً `<your-repo-url>`، `<project-folder>` و `[نام شما]` را با اطلاعات مناسب جایگزین کنید.