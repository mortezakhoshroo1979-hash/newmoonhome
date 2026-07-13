from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from .models import Order


class OrderStatusBulkUpdateForm(forms.Form):
    from_status = forms.ChoiceField(choices=[("", "همه")] + Order.STATUS_CHOICES, required=False, label="از وضعیت")
    to_status = forms.ChoiceField(choices=Order.STATUS_CHOICES, label="به وضعیت")
    province = forms.CharField(required=False, label="استان")
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="از تاریخ")
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="تا تاریخ")
    confirm = forms.BooleanField(required=False, label="اعمال نهایی")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(Column("from_status", css_class="col-md-4"), Column("to_status", css_class="col-md-4"), Column("province", css_class="col-md-4")),
            Row(Column("date_from", css_class="col-md-4"), Column("date_to", css_class="col-md-4"), Column("confirm", css_class="col-md-4")),
            Submit("submit", "پیش‌نمایش / اعمال"),
        )

    def filtered_queryset(self):
        qs = Order.objects.select_related("user", "shipping_method").all()
        if self.cleaned_data.get("from_status"):
            qs = qs.filter(status=self.cleaned_data["from_status"])
        if self.cleaned_data.get("province"):
            qs = qs.filter(province__icontains=self.cleaned_data["province"])
        if self.cleaned_data.get("date_from"):
            qs = qs.filter(created_at__date__gte=self.cleaned_data["date_from"])
        if self.cleaned_data.get("date_to"):
            qs = qs.filter(created_at__date__lte=self.cleaned_data["date_to"])
        return qs
