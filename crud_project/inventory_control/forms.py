from django import forms
from .models import Product, Warehouse, ProductDescription, Customer


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    description = forms.ModelChoiceField(queryset=ProductDescription.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Product
        fields = ['name', 'mfg', 'exp', 'quantity', 'price_per_unit', 'warehouse', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mfg': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exp': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
        }


class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = ProductDescription
        fields = ['description']  # Удаляем или комментируем поле 'product'
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer', 'mail']
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
        }
