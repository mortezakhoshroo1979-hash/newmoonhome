# راه‌اندازی فونت لوکال برای NEWMOON HOME

برای اینکه فونت‌ها بدون اینترنت و در preview داخلی هم درست نمایش داده شوند، باید فایل فونت واقعی داخل پروژه قرار بگیرد.

## فایل‌های پیشنهادی

در این مسیر قرار بده:

```text
static/fonts/
```

مثلاً:

```text
static/fonts/Vazirmatn-Regular.woff2
static/fonts/Vazirmatn-Medium.woff2
static/fonts/Vazirmatn-Bold.woff2
static/fonts/Poppins-Regular.woff2
static/fonts/Poppins-Medium.woff2
static/fonts/Poppins-Bold.woff2
```

## سپس این بلوک را به ابتدای main.css اضافه کن

```css
@font-face {
    font-family: 'VazirmatnLocal';
    src: url('../fonts/Vazirmatn-Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'VazirmatnLocal';
    src: url('../fonts/Vazirmatn-Medium.woff2') format('woff2');
    font-weight: 500;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'VazirmatnLocal';
    src: url('../fonts/Vazirmatn-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'PoppinsLocal';
    src: url('../fonts/Poppins-Regular.woff2') format('woff2');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'PoppinsLocal';
    src: url('../fonts/Poppins-Medium.woff2') format('woff2');
    font-weight: 500;
    font-style: normal;
    font-display: swap;
}

@font-face {
    font-family: 'PoppinsLocal';
    src: url('../fonts/Poppins-Bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
}
```

## و بعد font-family ها را این‌گونه تنظیم کن

```css
font-family: 'VazirmatnLocal', 'Vazirmatn', Tahoma, 'Segoe UI', Arial, sans-serif;
```

و برای بخش‌های لاتین:

```css
font-family: 'PoppinsLocal', 'Poppins', Tahoma, 'Segoe UI', Arial, sans-serif;
```

## نکته

من در حال حاضر چون فایل فونت واقعی در workspace وجود ندارد، fallback امن را فعال کرده‌ام.
اگر فایل‌های فونت را آپلود کنی، من مستقیم آن‌ها را به پروژه متصل می‌کنم.
