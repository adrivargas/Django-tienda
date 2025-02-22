"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tienda.views import *

urlpatterns = [
    path('', home, name='home'),
    path('hola/', hola_mundo),
    path('admin/', admin.site.urls),
    path('productos/', lista_producto, name='lista_productos'),
    path('productos/crear', crear_producto, name='crear_producto'),
    path('productos/editar/<int:id_prod>', editar_producto, name='editar_producto'),
    path('registrar/', registrar, name='registrar'),
    path('iniciar/', iniciar, name='iniciar'),
    path('salir/',cerrar_sesion, name='salir'),
    path('agregar_al_carrito/<int:id_prod>/',agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', carrito, name='carrito'),
    path('carrito/eliminar/<int:id_prod>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('eliminar-una-unidad/<int:id_prod>/',eliminar_una_unidad, name='eliminar_una_unidad'),
    path('actualizar_cantidad_carrito/<int:id_prod>/<int:nueva_cantidad>/', actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('pedidos/', pedidos, name='pedidos'),
    path('finalizar_compra/',finalizar_compra, name='finalizar_compra'),
    path('mis_pedidos/',mis_pedidos, name='mis_pedidos'),
    path('cambiar_estado_pedido/<int:pedido_id>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
]
