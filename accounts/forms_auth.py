from django import forms
from django.contrib.auth import authenticate
from accounts.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند.')
        return cleaned_data


class LoginForm(forms.Form):
    identifier = forms.CharField(label='ایمیل یا موبایل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')
        user = User.objects.filter(email=identifier).first() or User.objects.filter(phone=identifier).first() or User.objects.filter(username=identifier).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                cleaned_data['user'] = auth_user
                return cleaned_data
        raise forms.ValidationError('اطلاعات ورود نامعتبر است.')


class OTPVerifyForm(forms.Form):
    code = forms.CharField(max_length=6, label='کد تایید')


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='ایمیل')
