from django import forms
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from .models import Brand, Category, Product


class ProductBulkUpdateForm(forms.Form):
    """فرم اکشن‌های گروهی محصولات در پنل مدیریت."""

    ACTION_PERCENT_INCREASE = "percent_increase"
    ACTION_PERCENT_DECREASE = "percent_decrease"
    ACTION_FIXED_INCREASE = "fixed_increase"
    ACTION_FIXED_DECREASE = "fixed_decrease"
    ACTION_SET_PRICE = "set_price"
    ACTION_SET_SPECIAL_DISCOUNT = "set_special_discount"

    ACTION_CHOICES = [
        (ACTION_PERCENT_INCREASE, "افزایش درصدی"),
        (ACTION_PERCENT_DECREASE, "کاهش درصدی"),
        (ACTION_FIXED_INCREASE, "افزایش عدد ثابت"),
        (ACTION_FIXED_DECREASE, "کاهش عدد ثابت"),
        (ACTION_SET_PRICE, "جایگزینی با قیمت جدید"),
        (ACTION_SET_SPECIAL_DISCOUNT, "اعمال تخفیف ویژه"),
    ]

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="دسته‌بندی‌ها",
    )
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        label="برندها",
    )
    min_price = forms.DecimalField(required=False, label="حداقل قیمت")
    max_price = forms.DecimalField(required=False, label="حداکثر قیمت")
    stock_status = forms.ChoiceField(
        required=False,
        choices=[
            ("", "همه"),
            ("in_stock", "موجود"),
            ("out_of_stock", "ناموجود"),
        ],
        label="وضعیت موجودی",
    )
    created_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="از تاریخ")
    created_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="تا تاریخ")

    action_type = forms.ChoiceField(choices=ACTION_CHOICES, label="نوع عملیات")
    value = forms.DecimalField(required=False, label="مقدار عملیات")
    discount_percent = forms.IntegerField(required=False, min_value=0, max_value=100, label="درصد تخفیف ویژه")
    reason = forms.CharField(widget=forms.Textarea, required=False, label="دلیل/توضیحات")
    confirm = forms.BooleanField(required=False, label="اعمال نهایی")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(Column("categories", css_class="col-md-6"), Column("brands", css_class="col-md-6")),
            Row(Column("min_price", css_class="col-md-3"), Column("max_price", css_class="col-md-3"), Column("stock_status", css_class="col-md-3"), Column("action_type", css_class="col-md-3")),
            Row(Column("created_from", css_class="col-md-4"), Column("created_to", css_class="col-md-4"), Column("value", css_class="col-md-4")),
            Row(Column("discount_percent", css_class="col-md-4"), Column("confirm", css_class="col-md-2")),
            "reason",
            Submit("submit", "پیش‌نمایش / اعمال"),
        )

    def filter_queryset(self):
        queryset = Product.objects.select_related("category", "brand").all()
        categories = self.cleaned_data.get("categories")
        brands = self.cleaned_data.get("brands")
        min_price = self.cleaned_data.get("min_price")
        max_price = self.cleaned_data.get("max_price")
        stock_status = self.cleaned_data.get("stock_status")
        created_from = self.cleaned_data.get("created_from")
        created_to = self.cleaned_data.get("created_to")

        if categories:
            queryset = queryset.filter(category__in=categories)
        if brands:
            queryset = queryset.filter(brand__in=brands)
        if min_price is not None:
            queryset = queryset.filter(base_price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(base_price__lte=max_price)
        if stock_status == "in_stock":
            queryset = queryset.filter(stock__gt=0)
        elif stock_status == "out_of_stock":
            queryset = queryset.filter(stock=0)
        if created_from:
            queryset = queryset.filter(created_at__date__gte=created_from)
        if created_to:
            queryset = queryset.filter(created_at__date__lte=created_to)
        return queryset


class ProductQuickEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["base_price", "special_price", "stock", "is_active", "brand", "category"]
