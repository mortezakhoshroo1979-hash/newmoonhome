# store/templatetags/manager_extras.py
from django import template
from ..price_utils import format_thousands as _fmt

register = template.Library()


@register.filter(name="thousands")
def thousands(value):
    """{{ product.price|thousands }} → 1,250,000"""
    return _fmt(value)


@register.filter(name="toman")
def toman(value):
    """{{ product.price|toman }} → 1,250,000 تومان"""
    s = _fmt(value)
    if not s:
        return ""
    return f"{s} تومان"
