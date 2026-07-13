# Standalone Ultra Preview Notes

نسخه modular برای این محیط پایدار نبود، چون فایل CSS مشترک در preview همیشه به‌درستی لود نمی‌شد.

## راه‌حل نهایی
بازگشت به فایل‌های self-contained:
- هر فایل preview شامل CSS داخلی خودش است
- بدون وابستگی به CSS جداگانه
- بدون وابستگی به CDN

## فایل شروع
- `preview_ultra_index.html`

## نتیجه
این ساختار برای محیط محدود preview پایدارتر است.
