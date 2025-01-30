from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Producto, Carrito
from .forms import ProductoForm,CustomUserCreationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

# Create your views here.
def hola_mundo(request):
    html="""
    <strong>
        <h1 style="font-size:110px; color: #0000FF;">
            Hola Mundo
        </h1>
   </strong>
    """
    return HttpResponse(html)

    # Usuarios
    #     nombre
    #     apellido
    #     fechanacimiento
    #     genero
    #     fecharegistro
    #     activo
    #     direccion
    #     telefono
    #     email
    # Perfiles
    #     rol
    #     permiso
    # Productos
    #     nombre
    #     tipo
    #     precio
    #     stock
    #     descripcion
    #     foto
    #     categoria
    # Categoriaproducto
    #     nombre
    #     descripcion
    # Pedidos
    #     fecha
    #     id
    #     forma de entrega
    #     total
    #     iva
    #     forma de Pago
    # detallepedido
    #     id
    #     idproducto
    #     idpedido
    #     cantidad
    #     valorproducto
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Producto
from .forms import ProductoForm, CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

# Registrar usuario
def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return render(request, 'home.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Iniciar sesión
def iniciar(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['clave']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return render(request, 'home.html')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

# Página principal
def home(request):
    carrito_count = Carrito.objects.filter(usuario=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'home.html', {'carrito_count': carrito_count})

# Listar productos
def lista_producto(request):
    producto = Producto.objects.all()
    return render(request, 'lista_productos.html', {'prod': producto})

# Crear producto (Solo "adrivargas")
@login_required
def crear_producto(request):
    if request.user.username != "adrivargas":
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(lista_producto)
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

# Editar producto (Solo "adrivargas")
@login_required
def editar_producto(request, id_prod):
    if request.user.username != "adrivargas":
        return HttpResponseForbidden("No tienes permisos para acceder a esta página.")

    prod = Producto.objects.get(id_producto=id_prod)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=prod)
    return render(request, 'editar_producto.html', {'form': form, 'producto': prod})


@login_required
def agregar_al_carrito(request, id_prod):
    producto = get_object_or_404(Producto, id_producto=id_prod)

    # Buscar si el producto ya está en el carrito del usuario
    carrito_item, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto)

    if not created:
        carrito_item.cantidad += 1  # Si ya existe, aumentar cantidad
        carrito_item.save()

    print(f"Producto agregado: {producto.nombre_producto}, Cantidad: {carrito_item.cantidad}")

    return redirect('carrito')  # Redirigir a la vista del carrito

def carrito(request):
    """ Muestra el carrito con productos y total de la compra """
    if request.user.is_authenticated:
        carrito_items = Carrito.objects.filter(usuario=request.user)
        print(f"Usuario autenticado: {request.user}")
        print(f"Productos en carrito: {carrito_items}")  # Depuración

        total = sum(item.subtotal for item in carrito_items)  # Calcular total de la compra
        return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})
    else:
        return redirect('iniciar')  # Redirigir al login si el usuario no está autenticado


def finalizar_compra(request):
    if request.user.is_authenticated:
        carrito_items = Carrito.objects.filter(usuario=request.user)
        total = sum(item.subtotal for item in carrito_items)

        # Aquí puedes agregar lógica para crear un pedido y vaciar el carrito
        # Ejemplo:
        # Pedido.objects.create(usuario=request.user, total=total, ...)
        carrito_items.delete()  # Eliminar los items del carrito

        return render(request, 'compra_finalizada.html', {'total': total})
    else:
        return redirect('iniciar')
    
@login_required
def eliminar_del_carrito(request, id_prod):
    """ Elimina un producto del carrito del usuario autenticado """
    usuario = request.user  # Obtiene el usuario autenticado
    producto = get_object_or_404(Producto, id_producto=id_prod)

    # Buscar si el producto está en el carrito del usuario
    item_carrito = Carrito.objects.filter(usuario=usuario, producto=producto).first()

    if item_carrito:
        item_carrito.delete()  # Eliminar el producto de la base de datos

    return redirect('carrito')  # Redirigir a la vista del carrito


@login_required
def actualizar_cantidad_carrito(request, id_prod, nueva_cantidad):
    """ Actualiza la cantidad de un producto en el carrito del usuario """
    usuario = request.user  # Obtiene el usuario autenticado
    producto = get_object_or_404(Producto, id_producto=id_prod)

    # Buscar si el producto está en el carrito del usuario
    item_carrito = Carrito.objects.filter(usuario=usuario, producto=producto).first()

    if item_carrito:
        if nueva_cantidad > 0:
            item_carrito.cantidad = nueva_cantidad  # Actualizar cantidad
            item_carrito.save()
        else:
            item_carrito.delete()  # Eliminar el producto si la cantidad es 0

    return redirect('carrito')  # Redirigir a la vista del carrito

@login_required
def eliminar_una_unidad(request, id_prod):
    """ Elimina una unidad de un producto en el carrito del usuario autenticado """
    usuario = request.user  # Obtiene el usuario autenticado
    producto = get_object_or_404(Producto, id_producto=id_prod)  # Obtiene el producto

    # Busca si el producto está en el carrito del usuario
    item_carrito = Carrito.objects.filter(usuario=usuario, producto=producto).first()

    if item_carrito:
        if item_carrito.cantidad > 1:
            item_carrito.cantidad -= 1  # Disminuir en 1 la cantidad
            item_carrito.save()
        else:
            item_carrito.delete()  # Eliminar si la cantidad llega a 0

    return redirect('carrito')  # Redirigir a la vista del carrito
