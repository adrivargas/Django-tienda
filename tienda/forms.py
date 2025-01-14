from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'stock_producto', 'precio_producto','tipo_producto', 'id_categoria_producto']
