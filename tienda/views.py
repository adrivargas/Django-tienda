from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Producto
from .forms import ProductoForm,CustomUserCreationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return render(request, 'home.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html',{'form':form})

def iniciar(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['clave']
        usuario = authenticate(request, username=username,password=password)
        if usuario is not None:
            login(request, usuario)
            return render(request,'home.html')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def lista_producto(request):
    producto = Producto.objects.all()
    return render(request, 'lista_productos.html', {'prod' : producto})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(lista_producto)
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

@permission_required('tienda.puede_ver_productos', raise_exception=True)
def editar_producto(request, id_prod):
    prod = Producto.objects.get(id_producto=id_prod)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=prod)
    return render(request, 'editar_producto.html', {'form':form, 'producto':prod})



