from django.db import models
from django.contrib.auth.models import User
class Producto(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion=models.TextField()
    precio=models.IntegerField()
    imagen=models.ImageField(upload_to='static/tiendaVerde/imagenes/')
    def __str__(self):
        return self.nombre
class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    # Se pueden agregar más campos si es necesario

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  # Relación con Carrito
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con Producto
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad del producto en el carrito

class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        ENVIADO = 'Enviado', 'Enviado'
        CANCELADO = 'Cancelado', 'Cancelado'  # Otros estados que quieras añadir

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario que hizo el pedido
    productos = models.ManyToManyField(Producto)  # Productos incluidos en el pedido
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)  # Estado del pedido
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username}'  # Representación del pedido