from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Coupon


class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        widgets = {
            "expires_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "ذخیره"))
