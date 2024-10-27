from django.contrib import admin
from django.urls import path
from tiendaVerde import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("formulario/", views.formulario, name="formulario"),
    path("registrarse/", views.registrarse, name="registrarse"),
    path("login/", auth_views.LoginView.as_view(template_name="tiendaVerde/inicioSesion.html"), name="inicioSesion"),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(next_page='inicio'), name='cerrarSesion'),
    path('catalogo/', views.catalogo_publico, name='catalogo_publico'),  # Para usuarios no autenticados
    path('catalogo_cliente/', views.catalogo_cliente, name='catalogo_cliente'),  # Para clientes autenticados
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),  # Para ver el carrito
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
]
