# Preview Safe Base

فایل پایه جدید:
- `preview_base.html`

## هدف
این فایل برای جداسازی کامل preview از templateهای اصلی Django ساخته شده است تا:
- فونت‌ها به‌هم نریزند
- layout با حذف CDNها خراب نشود
- previewها مستقل و پایدار بمانند

## نکته
فایل‌های preview فعلی already standalone هستند، اما این base به‌عنوان مرجع طراحی safe اضافه شده تا اگر بخواهیم نسل بعدی previewها را modular بسازیم، از آن استفاده کنیم.

## پیشنهاد
در preview فقط این فایل‌ها را باز کن:
- `preview_ultra_index.html`
- `preview_ultra_luxury_home.html`
- `preview_ultra_product_list.html`
- `preview_ultra_product_detail.html`
- `preview_ultra_cart.html`
- `preview_ultra_checkout.html`
- `preview_ultra_profile.html`
