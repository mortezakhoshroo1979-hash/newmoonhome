# store/price_utils.py
# ابزار پردازش قیمت: پارس ارقام فارسی/عربی، جداکننده هزارگان، رند کردن.

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS  = "٠١٢٣٤٥٦٧٨٩"
ASCII_DIGITS   = "0123456789"

_TRANS = str.maketrans(
    PERSIAN_DIGITS + ARABIC_DIGITS,
    ASCII_DIGITS + ASCII_DIGITS,
)


def normalize_digits(s):
    """ارقام فارسی/عربی → ASCII."""
    if s is None:
        return ""
    return str(s).translate(_TRANS)


def parse_number(value):
    """
    ورودی: '۱٬۲۵۰٬۰۰۰' یا '1,250,000' یا '  1250000 ' یا int
    خروجی: int
    خطا: ValueError اگه چیز عددی نبود.
    """
    if value is None or value == "":
        raise ValueError("empty")
    if isinstance(value, (int,)):
        return int(value)
    if isinstance(value, float):
        return int(value)
    s = normalize_digits(value)
    # حذف کاما، فاصله، جداکننده هزارگان فارسی، تومان/ريال
    for ch in [",", "،", "٬", " ", "\u200c", "\t"]:
        s = s.replace(ch, "")
    s = s.replace("تومان", "").replace("ريال", "").replace("ریال", "")
    s = s.strip()
    if s.startswith("+"):
        s = s[1:]
    return int(float(s))


def format_thousands(n):
    """1250000 → '1,250,000'  (None → '')"""
    if n is None or n == "":
        return ""
    try:
        n = int(n)
    except (ValueError, TypeError):
        return str(n)
    return f"{n:,}"


def round_to_base(n, base, mode="nearest"):
    """
    رند کردن n به مضربی از base.
    mode: 'nearest' | 'up' | 'down'
    """
    if not base or base <= 0:
        return n
    n = int(n)
    base = int(base)
    if mode == "up":
        return ((n + base - 1) // base) * base
    if mode == "down":
        return (n // base) * base
    # nearest
    q, r = divmod(n, base)
    if r * 2 >= base:
        return (q + 1) * base
    return q * base


def apply_price_op(current_price, op, value):
    """
    محاسبه قیمت جدید بر اساس عملیات.
    op: inc_percent | dec_percent | inc_amount | dec_amount | set_exact
    value: عدد
    """
    p = int(current_price or 0)
    v = int(value or 0)
    if op == "inc_percent":
        return p + (p * v) // 100
    if op == "dec_percent":
        return p - (p * v) // 100
    if op == "inc_amount":
        return p + v
    if op == "dec_amount":
        return max(0, p - v)
    if op == "set_exact":
        return v
    return p
