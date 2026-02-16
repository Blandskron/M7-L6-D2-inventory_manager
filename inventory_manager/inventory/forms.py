from django import forms
from .models import Product, Movement

# Formularios basados en ORM
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['product', 'movement_type', 'quantity']