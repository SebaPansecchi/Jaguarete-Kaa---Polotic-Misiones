from django.urls import path
from .views import *
app_name = "tienda"

urlpatterns = [
    path('',index,name="index"),
    path('acercade/',acerca,name="acerca"),
    path('usuarios/login',login_view,name="login"),
    path('usuarios/logout',logout_view,name="logout"),
    path('usuarios/registro',register,name="register"),
    path('producto/buscar',BuscarProductoListView.as_view(),name="buscar"),
    path('producto/nuevo',cargar_producto,name="nuevo"),
    path('producto/modificar/<int:producto_id>',editar_producto,name="editar"),
    path('producto/eliminar/<int:producto_id>',eliminar_producto,name="eliminar"),
    path('producto/ver_producto/<int:producto_id>',ver_producto,name="producto"),
    path('producto/categorias/<int:categoria_id>',producto_categoria,name="categoria"),
    path('carrito',cart_detalle,name="cart_detalle"),
    path('carrito/<int:pk>',cart_remove,name="cart_remove"),
    path('carrito/delete',cart_delete,name="cart_delete"),
]