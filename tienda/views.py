from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Producto, Carrito, Pedido, Detallepedidos,Usuario, UsuarioForm
from .forms import ProductoForm,CustomUserCreationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test



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


# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

# Registrar usuario
# Registrar usuario
def registrar(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guardar el usuario de Django
            user = form.save()

            # Crear un perfil de Usuario
            Usuario.objects.create(
                user=user,
                nombre_usuario='',  # O agregar un campo vacío por ahora
                apellido_usuario='',  # Lo mismo con apellido
                fecharegistro_usuario=timezone.now(),  # Usar la fecha de registro
                # Aquí puedes agregar más campos según sea necesario
            )
            
            # Iniciar sesión automáticamente
            login(request, user)
            return render(request, 'home.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})


def completar_perfil(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.user = request.user  # Asociar el perfil con el usuario autenticado
            usuario.save()
            return redirect('home')  # O donde desees redirigir al usuario después de completar su perfil
    else:
        form = UsuarioForm()
    return render(request, 'completar_perfil.html', {'form': form})


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

def es_superusuario(user):
    return user.is_superuser

# Página principal
def home(request):
    carrito_count = Carrito.objects.filter(usuario=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'home.html', {'carrito_count': carrito_count})

# Listar productos
def lista_producto(request):
    producto = Producto.objects.all()
    return render(request, 'lista_productos.html', {'prod': producto})

# Crear producto (Solo "adrivargas")

def crear_producto(request):

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(lista_producto)
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

# Editar producto (Solo "adrivargas")

def editar_producto(request, id_prod):
    prod = Producto.objects.get(id_producto=id_prod)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=prod)
    return render(request, 'editar_producto.html', {'form': form, 'producto': prod})



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
    if request.user.is_authenticated:
        carrito_items = Carrito.objects.filter(usuario=request.user)
        # print(f"Usuario autenticado: {request.user}")
        # print(f"Productos en carrito: {carrito_items}")  # Depuración

        total = sum(item.subtotal for item in carrito_items)  # Calcular total de la compra
        return render(request, 'carrito.html', {'carrito_items': carrito_items, 'total': total})
    else:
        return redirect('iniciar')  # Redirigir al login si el usuario no está autenticado

def finalizar_compra(request):
    if request.method == 'POST':
        forma_pago = request.POST.get('forma_pago')
        forma_entrega = request.POST.get('forma_entrega')

        if not forma_pago or not forma_entrega:
            return render(request, 'finalizar_compra.html', {'error': 'Todos los campos son obligatorios'})

        # Obtener los productos del carrito del usuario logueado
        carrito_items = Carrito.objects.filter(usuario=request.user)  # Usamos `usuario` y no `id_usuario`

        total = Decimal('0.00')  # Inicializamos el total como un Decimal
        for item in carrito_items:
            total += item.subtotal  # Utilizamos la propiedad `subtotal`

        iva = total * Decimal('0.15')  # Aseguramos que el IVA sea un Decimal
        total_con_iva = total + iva  # Total con IVA

        usuario = Usuario.objects.get(user=request.user)

        messages.success(request, '¡Tu pedido ha sido realizado correctamente!')

        # Crear el pedido
        pedido = Pedido.objects.create(
            id_usuario=usuario,
            formapago_pedido=forma_pago,
            forma_entrega=forma_entrega,
            iva_pedido=iva,
            total_pedido=total_con_iva, 
            estado_pedido='pedido',
        )
        carrito_items.delete()

        # Redirigir a la página de confirmación de la compra
        return redirect('home')

    else:
        # Si no es un POST, mostrar el formulario con los detalles del carrito
        carrito_items = Carrito.objects.filter(usuario=request.user)  # Usamos `usuario`
        
        total = Decimal('0.00')  # Inicializamos el total como un Decimal
        for item in carrito_items:
            total += item.subtotal  # Utilizamos la propiedad `subtotal`

        iva = total * Decimal('0.15')  # Aseguramos que el IVA sea un Decimal
        total_con_iva = total + iva  # Total con IVA

        return render(request, 'finalizar_compra.html', {
            'carrito_items': carrito_items,
            'total': total,
            'iva': iva,
            'total_con_iva': total_con_iva,
        })



def eliminar_del_carrito(request, id_prod):
    """ Elimina un producto del carrito del usuario autenticado """
    usuario = request.user  # Obtiene el usuario autenticado
    producto = get_object_or_404(Producto, id_producto=id_prod)

    # Buscar si el producto está en el carrito del usuario
    item_carrito = Carrito.objects.filter(usuario=usuario, producto=producto).first()

    if item_carrito:
        item_carrito.delete()  # Eliminar el producto de la base de datos

    return redirect('carrito')  # Redirigir a la vista del carrito



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

def pedidos(request):
    if request.user.is_superuser:
        pedidos = Pedido.objects.all() 
    else:
        pedidos = Pedido.objects.filter(id_usuario=request.user.usuario)  
    
    return render(request, 'pedidos.html', {'pedidos': pedidos})

def cambiar_estado_pedido(request, pedido_id):
    
    if request.user.is_superuser: 
        pedido = get_object_or_404(Pedido, id_pedido=pedido_id)

        if pedido.estado_pedido == 'pedido':
            if 'cancelar' in request.POST:
                pedido.estado_pedido = 'cancelado'
            elif 'facturar' in request.POST:
                pedido.estado_pedido = 'facturado'
        
        # Guarda los cambios en el pedido
        pedido.save()

        # Redirige al listado de pedidos
        return redirect('pedidos')  # Cambia a la URL que deseas, por ejemplo 'mis_pedidos'
    else:
        # Redirige si no es superusuario
        return redirect('home')  # Puedes redirigir a una página que indique que no tienen permisos

def mis_pedidos(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Filtra los pedidos por el usuario asociado al modelo Usuario
        pedidos = Pedido.objects.filter(id_usuario=request.user.usuario)  # Asumiendo que 'usuario' es la relación a Usuario
        return render(request, 'mis_pedidos.html', {'pedidos': pedidos})
    else:
        return redirect('login')  # Redirige al login si el usuario no está autenticado
