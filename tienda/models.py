from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    apellido_usuario = models.CharField(max_length=100)
    fecha_nacimiento_usuario = models.DateField(null=True, blank=True)
    genero_usuario = models.CharField(max_length=20,null=True)
    fecharegistro_usuario = models.DateTimeField(null=True)
    activo_usuario = models.BooleanField(default=True,null=True)
    direccion_usuario = models.CharField(max_length=200,null=True)
    telefono_usuario = models.CharField(max_length=10,null=True)
    email_usuario = models.EmailField(unique=True,null=True)

    def __str__(self):
        return f"{self.nombre_usuario} {self.apelllido_usuario}"

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
        ('pedido','pedido'),
        ('cancelado', 'cancelado'),
        ('facturado', 'facturado'),
    ]
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total_pedido = models.DecimalField(max_digits=10,decimal_places=2)
    iva_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    formapago_pedido = models.CharField(max_length=10)
    estado_pedido = models.CharField(max_length=100, choices=ESTADO_PEDIDO, default='borrador')
    
    def __str__(self):
        return f"{self.id_pedido}/{self.usuario.nombre_usuario}"

class Detallepedidos(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id_detalle_pedido


class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre_producto}'
    
    @property
    def subtotal(self):
        return self.producto.precio_producto * self.cantidad