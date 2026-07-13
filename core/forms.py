from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Banner, ContactMessage, SiteSetting, Slider


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = "__all__"
        widgets = {
            "site_description": forms.Textarea(attrs={"rows": 4}),
        }


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = "__all__"


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"
