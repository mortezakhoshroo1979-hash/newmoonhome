from django import forms
from .models import CustomOrder

class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = ['full_name', 'phone', 'width', 'height', 'depth', 'color_scheme', 'customer_image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }