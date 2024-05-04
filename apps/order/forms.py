from django import forms

from .models import Cart, Order


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity', 'product')
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'email', 'delivery', 'address')
    
