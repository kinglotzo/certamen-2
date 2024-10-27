from django.contrib import admin


from .models import Producto,Pedido

admin.site.register(Producto)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'fecha_creacion')  # Campos a mostrar en la vista de lista
    list_filter = ('estado',)  # Permite filtrar por estado
    search_fields = ('usuario__username',)  # Habilita la búsqueda por nombre de usuario
    ordering = ('fecha_creacion',)  # Ordena por fecha de creación

admin.site.register(Pedido, PedidoAdmin)  # Registro del modelo Pedido con la interfaz personalizada