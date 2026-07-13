from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from .models import CustomerRank, User


class UserFilterEmailForm(forms.Form):
    is_verified = forms.NullBooleanField(required=False, label="وضعیت تایید")
    rank = forms.ModelChoiceField(queryset=CustomerRank.objects.all(), required=False, label="رتبه")
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="از تاریخ")
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="تا تاریخ")
    min_score = forms.IntegerField(required=False, label="حداقل امتیاز")
    subject = forms.CharField(required=False, label="موضوع ایمیل")
    message = forms.CharField(required=False, widget=forms.Textarea, label="متن ایمیل")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(Column("is_verified", css_class="col-md-3"), Column("rank", css_class="col-md-3"), Column("min_score", css_class="col-md-3")),
            Row(Column("date_from", css_class="col-md-3"), Column("date_to", css_class="col-md-3")),
            "subject",
            "message",
            Submit("submit", "ارسال / پیش‌نمایش"),
        )

    def filtered_queryset(self):
        qs = User.objects.select_related("profile").all()
        is_verified = self.cleaned_data.get("is_verified")
        rank = self.cleaned_data.get("rank")
        date_from = self.cleaned_data.get("date_from")
        date_to = self.cleaned_data.get("date_to")
        min_score = self.cleaned_data.get("min_score")

        if is_verified is not None:
            qs = qs.filter(is_verified=is_verified)
        if rank:
            qs = qs.filter(profile__rank=rank)
        if date_from:
            qs = qs.filter(date_joined__date__gte=date_from)
        if date_to:
            qs = qs.filter(date_joined__date__lte=date_to)
        if min_score is not None:
            qs = qs.filter(profile__score__gte=min_score)
        return qs
