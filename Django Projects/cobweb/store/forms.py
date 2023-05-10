from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'manufacturer', 'category', 'price', 'img', 'model', 'caliber', 'weight', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom attributes to form fields if needed
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter description'})
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter manufacturer'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter category'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter price'})
        self.fields['img'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter image URL'})
        self.fields['model'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter model'})
        self.fields['caliber'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter caliber'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter weight'})
        self.fields['capacity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter capacity'})