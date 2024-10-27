from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistro, FormularioInicioSesion
from .models import Producto, Carrito, CarritoProducto, Pedido
from django.contrib.auth import authenticate

def inicio(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Cliente').exists():
            context['mensaje'] = f"¡Hola, {request.user.username}! Eres un cliente."
            context['url_pedidos'] = 'catalogo_cliente'
            context['boton_texto'] = "Ver catálogo"
    else:
        context['mensaje'] = "¡Bienvenido a Tienda Verde! Explora nuestros productos."
        context['url_pedidos'] = 'catalogo_publico'
        context['boton_texto'] = "Catálogo Público"
        
    return render(request, "tiendaVerde/index.html", context)

@login_required
def catalogo_cliente(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    productos_en_carrito = CarritoProducto.objects.filter(carrito=carrito)
    total = sum(item.producto.precio * item.cantidad for item in productos_en_carrito)
    
    return render(request, 'tiendaVerde/catalogoCliente.html', {
        'productos': productos,
        'productos_en_carrito': productos_en_carrito,
        'total': total,
    })

def catalogo_publico(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'tiendaVerde/catalogo.html', {'productos': productos})

def formulario(request):
    return render(request, "tiendaVerde/formulario.html")

def registrarse(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = FormularioRegistro()
    return render(request, 'tiendaVerde/registrarse.html', {'form': form})

def iniciarSesion(request):
    if request.method == 'POST':
        form = FormularioInicioSesion(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                messages.error(request, "Correo o contraseña incorrectos")
    else:
        form = FormularioInicioSesion()
    return render(request, 'tiendaVerde/inicioSesion.html', {'form': form})

@login_required
def ver_carrito(request):
    try:
        carrito = Carrito.objects.get(user=request.user)
        productos_en_carrito = CarritoProducto.objects.filter(carrito=carrito).select_related('producto')
        total = sum(item.producto.precio * item.cantidad for item in productos_en_carrito)
        total_por_producto = [(item, item.producto.precio * item.cantidad) for item in productos_en_carrito]
        
        # Check for a successful order confirmation message
        pedido_confirmado = request.session.pop('pedido_confirmado', False)  # Use session to store the confirmation flag
    except Carrito.DoesNotExist:
        productos_en_carrito = []
        total = 0
        total_por_producto = []
        pedido_confirmado = False

    return render(request, 'tiendaVerde/ver_carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total': total,
        'total_por_producto': total_por_producto,
        'pedido_confirmado': pedido_confirmado,  # Pass the confirmation flag to the template
    })

@login_required
def agregar_al_carrito(request, producto_id):
    if request.user.groups.filter(name='Cliente').exists():
        try:
            producto = Producto.objects.get(id=producto_id)
            carrito, created = Carrito.objects.get_or_create(user=request.user)
            
            carrito_producto, created = CarritoProducto.objects.get_or_create(
                carrito=carrito, producto=producto,
                defaults={'cantidad': 1}
            )
            
            if not created:
                carrito_producto.cantidad += 1
                carrito_producto.save()
            
            messages.success(request, 'Producto añadido al carrito.')
        except Producto.DoesNotExist:
            messages.error(request, 'El producto no existe.')
    else:
        messages.error(request, 'Debes ser un cliente para agregar productos al carrito.')
    
    return redirect('catalogo_cliente')

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    try:
        carrito_producto = CarritoProducto.objects.get(carrito=carrito, producto__id=producto_id)
        if carrito_producto.cantidad > 1:
            carrito_producto.cantidad -= 1
            carrito_producto.save()
            messages.success(request, 'Se ha disminuido la cantidad del producto en el carrito.')
        else:
            carrito_producto.delete()
            messages.success(request, 'Producto eliminado del carrito.')
    except CarritoProducto.DoesNotExist:
        messages.error(request, 'El producto no está en tu carrito.')

    return redirect('ver_carrito')

@login_required
def confirmar_pedido(request):
    carrito = Carrito.objects.get(user=request.user)
    productos_en_carrito = CarritoProducto.objects.filter(carrito=carrito)

    if request.method == 'POST':
        # Crear el pedido con el estado "Pendiente"
        pedido = Pedido.objects.create(usuario=request.user, estado='Pendiente')

        # Agregar productos al pedido
        for item in productos_en_carrito:
            pedido.productos.add(item.producto)

        # Limpiar el carrito después de confirmar el pedido
        carrito.carritoproducto_set.all().delete()

        # Setear una bandera de sesión para indicar que el pedido ha sido confirmado
        request.session['pedido_confirmado'] = True
        messages.success(request, '¡Tu pedido ha sido confirmado!')

        # Redirigir a la página del carrito para mostrar el mensaje de confirmación
        return redirect('ver_carrito')

    return render(request, 'tiendaVerde/confirmar_pedido.html', {
        'productos_en_carrito': productos_en_carrito,
    })
