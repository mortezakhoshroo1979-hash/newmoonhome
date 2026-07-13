from django import forms
from .models import Product, SiteSetting, CustomOrder, Category

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ProductForm(forms.ModelForm):
    gallery_images = forms.FileField(widget=MultipleFileInput(attrs={'class': 'form-control'}), required=False, label="آلبوم تصاویر گالری")
    class Meta:
        model = Product
        fields = [
            "name_fa", "name_en", "name_ar", "category", "price", "price_usd", 
            "old_price", "stock", "image", "background_image", "description_fa", 
            "is_active", "is_featured"
        ]
        widgets = {
            'name_fa': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_usd': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description_fa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = "__all__"