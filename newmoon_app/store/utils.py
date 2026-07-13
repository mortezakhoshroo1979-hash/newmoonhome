"""توابع کمکی برای پنل مدیریت NEWMOON HOME."""

PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def normalize_digits(value):
    text = str(value or "")
    return text.translate(PERSIAN_DIGITS).translate(ARABIC_DIGITS)


def parse_price(value):
    text = normalize_digits(value)
    text = text.replace(",", "").replace("،", "").replace(" ", "")
    if text in ("", None):
        return 0
    return int(text)


def format_price(value):
    try:
        value = int(value or 0)
    except Exception:
        value = 0
    return f"{value:,}"


def round_to_base(value, base, mode="nearest"):
    value = int(value)
    base = int(base or 0)
    if base <= 0:
        return max(value, 0)
    if mode == "up":
        result = ((value + base - 1) // base) * base
    elif mode == "down":
        result = (value // base) * base
    else:
        result = round(value / base) * base
    return max(int(result), 0)


def compute_new_price(current_price, operation, value=0, round_base=0, round_mode="nearest"):
    current_price = int(current_price or 0)
    if operation == "inc_percent":
        new_price = current_price * (100 + float(value)) / 100
    elif operation == "dec_percent":
        new_price = current_price * (100 - float(value)) / 100
    elif operation == "inc_amount":
        new_price = current_price + int(value)
    elif operation == "dec_amount":
        new_price = current_price - int(value)
    elif operation == "set_exact":
        new_price = int(value)
    else:
        new_price = current_price
    new_price = max(int(round(new_price)), 0)
    return round_to_base(new_price, round_base, round_mode)
