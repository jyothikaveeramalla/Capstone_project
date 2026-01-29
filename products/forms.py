"""
Product Forms for creating and editing products.
"""

from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing products.
    
    Fields:
    - name: Product name
    - description: Detailed product description
    - category: Product category
    - price: Selling price
    - cost_price: Cost (for artisan tracking)
    - quantity_in_stock: Available quantity
    - image: Main product image
    - material: Material composition
    - dimensions: Product dimensions
    - weight: Product weight
    - is_eco_friendly: Eco-friendly flag
    - sustainability_notes: Notes on sustainability
    - status: Product status (active/inactive/discontinued)
    """
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'price', 'cost_price',
            'quantity_in_stock', 'image', 'material', 'dimensions',
            'weight', 'is_eco_friendly', 'sustainability_notes', 'status'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name',
                'maxlength': '255'
            }),
            
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your product in detail',
                'rows': 5
            }),
            
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Selling price',
                'step': '0.01',
                'min': '0.01'
            }),
            
            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cost price (optional)',
                'step': '0.01',
                'min': '0'
            }),
            
            'quantity_in_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity available',
                'min': '0'
            }),
            
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            
            'material': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Cotton, Silk, Wood',
                'maxlength': '100'
            }),
            
            'dimensions': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30cm x 20cm x 10cm',
                'maxlength': '100'
            }),
            
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in grams',
                'step': '0.1',
                'min': '0'
            }),
            
            'is_eco_friendly': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'sustainability_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Notes about eco-friendly aspects',
                'rows': 3
            }),
            
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def clean_price(self):
        """Validate price is positive."""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price
    
    def clean_quantity_in_stock(self):
        """Validate quantity is non-negative."""
        quantity = self.cleaned_data.get('quantity_in_stock')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity
    
    def clean(self):
        """Additional form validation."""
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        cost_price = cleaned_data.get('cost_price')
        
        # Warn if cost price is higher than selling price
        if cost_price and price and cost_price > price:
            self.add_error(
                'cost_price',
                'Warning: Cost price is higher than selling price.'
            )
        
        return cleaned_data
