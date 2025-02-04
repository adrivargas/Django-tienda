from django.db import models
from django.contrib.auth.models import User
from django import forms


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    apellido_usuario = models.CharField(max_length=100)
    fecha_nacimiento_usuario = models.DateField(null=True, blank=True)
    genero_usuario = models.CharField(max_length=20, null=True)
    fecharegistro_usuario = models.DateTimeField(null=True)
    activo_usuario = models.BooleanField(default=True, null=True)
    direccion_usuario = models.CharField(max_length=200, null=True)
    telefono_usuario = models.CharField(max_length=10, null=True)
    email_usuario = models.EmailField(unique=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Usar OneToOneField en lugar de ForeignKey

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido_usuario}"

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'apellido_usuario', 'direccion_usuario', 'telefono_usuario', 'fecha_nacimiento_usuario', 'genero_usuario']
        widgets = {
            'fecha_nacimiento_usuario': forms.DateInput(attrs={'type': 'date'}),
        }

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    rol_perfil = models.CharField(max_length=50)
    permisos_perfil = models.TextField()

    def __str__(self):
        return super().__str__()

class CategoriaProducto(models.Model):
    id_categoria_producto = models.AutoField(primary_key=True)
    nombre_categoria_producto = models.CharField(max_length=100)
    descripcion_categoria_producto = models.TextField()

    def __str__(self):
        return self.nombre_categoria_producto

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=50)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    stock_producto = models.IntegerField()
    descripcion_producto = models.TextField()
    foto_producto = models.ImageField(upload_to='productos/')
    id_categoria_producto = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_producto
class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('borrador', 'Borrador'),
        ('pedido', 'Pedido'),
        ('cancelado', 'Cancelado'),
        ('facturado', 'Facturado'),
    ]
    
    FORMAS_PAGO = [
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
    ]
    
    FORMAS_ENTREGA = [
        ('domicilio', 'A domicilio'),
        ('retirar', 'Retirar en la empresa'),
    ]

    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    iva_pedido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    formapago_pedido = models.CharField(max_length=10, choices=FORMAS_PAGO)
    estado_pedido = models.CharField(max_length=100, choices=ESTADO_PEDIDO, default='borrador')
    forma_entrega = models.CharField(max_length=20, choices=FORMAS_ENTREGA, default='retirar')  # Valor por defecto
    id_pedido = models.AutoField(primary_key=True)
    

    def __str__(self):
        return f"Pedido {self.id} - {self.id_usuario}"
    
    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.get_estado_pedido_display()}"


    def total_con_iva(self):
        """Método para obtener el total con IVA incluido"""
        if not self.iva_pedido:
            self.iva_pedido = self.total_pedido * 0.12
        return self.total_pedido + self.iva_pedido





class Detallepedidos(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)  # Permitir null temporalmente
    cantidad = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id_detalle_pedido} - Pedido {self.id_pedido.id_pedido if self.id_pedido else 'Sin Pedido'}"



class Carrito(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre_producto}'
    
    @property
    def subtotal(self):
        return self.producto.precio_producto * self.cantidad
