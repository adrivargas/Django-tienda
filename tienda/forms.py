from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'stock_producto', 'precio_producto', 'id_categoria_producto']

    def __init__(self, *args, **kwargs):
        super(ProductoForm,self).__init__(*args,**kwargs)
        self.fields['nombre_producto'].widget.attrs = {'class':'single-input-item','placeholder':'Nombre Producto'}
