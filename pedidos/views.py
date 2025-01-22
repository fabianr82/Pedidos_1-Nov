from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmpresaForm, UserSistemForm, ClienteForm, ProductoForm, PedidoForm, PortadaForm
from .models import Empresa, UserSistem, Cliente, Producto, Pedido, Portada, DetallePedido
from django.core.exceptions import ValidationError
import json
from datetime import datetime
from django.utils import timezone
from django.db import transaction


# Vista para la página de inicio
@login_required
def inicio(request):
    portada = Portada.objects.last()  # Obtener la última portada cargada
    return render(request, 'pedidos/inicio.html', {'portada': portada})

# Vista para cargar una portada
@login_required
def cargar_portada(request):
    if request.method == 'POST':
        form = PortadaForm(request.POST, request.FILES)
        if form.is_valid():
            Portada.objects.all().delete()  # Eliminar portadas existentes si es necesario
            form.save()
            messages.success(request, "Portada cargada exitosamente.")
            return redirect("inicio")
    else:
        form = PortadaForm()
    return render(request, 'pedidos/cargar_portada.html', {'form': form})

# Vista para el login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("inicio")  # Redirige a la página de inicio
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "pedidos/login.html")

# Vista para el logout
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# Vista para crear una empresa
@login_required
def crear_empresa(request):
    if request.method == 'POST':
        item_empresa = request.POST.get('item_empresa')
        nit = request.POST.get('nit')
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        coord_emp = request.POST.get('coord_emp')
        telefono = request.POST.get('telefono')
        ciudad_emp = request.POST.get('ciudad_emp')

        Empresa.objects.create(
            item_empresa=item_empresa,
            nit=nit,
            nombre=nombre,
            direccion=direccion,
            coord_emp=coord_emp,
            telefono=telefono,
            ciudad_emp=ciudad_emp
        )
        messages.success(request, "Empresa creada exitosamente.")
        return redirect('ver_empresas')

    return render(request, 'pedidos/crear_empresa.html')

@login_required
def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa editada exitosamente.")
            return redirect('ver_empresas')
    else:
        form = EmpresaForm(instance=empresa)

    return render(request, 'pedidos/editar_empresa.html', {'form': form})

@login_required
def crear_user_sist(request):
    if request.method == 'POST':
        form = UserSistemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios')
    else:
        form = UserSistemForm()
    return render(request, 'pedidos/crear_user_sist.html', {'form': form})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_clientes')  # Redirige a la vista de clientes después de guardar
    else:
        form = ClienteForm()
    
    empresas = Empresa.objects.all()  # Obtener todas las empresas disponibles
    return render(request, 'pedidos/crear_cliente.html', {'form': form, 'empresas': empresas})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        descripcion = request.POST.get('descripcion')
        valor_unitario = request.POST.get('valor_unitario')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        item_producto = request.POST.get('item_producto')
        UM = request.POST.get('UM')
        empresa_id = request.POST.get('item_empresa')  # Captura el ID de la empresa seleccionada

        empresa = get_object_or_404(Empresa, id=empresa_id)  # Obtener la empresa basada en el ID

        # Crear el producto con la empresa asociada
        Producto.objects.create(
            #empresa=empresa,
            nombre=nombre,
            marca=marca,
            descripcion=descripcion,
            valor_unitario=valor_unitario,
            fecha_vencimiento=fecha_vencimiento,
            item_producto=item_producto,
            UM=UM
        )
        
        return render(request, 'pedidos/crear_producto.html')

    productos = Producto.objects.all()
    empresas = Empresa.objects.all()
    return render(request, 'pedidos/crear_producto.html', {
        'productos': productos,
        'empresas': empresas
    })


@login_required
def crear_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, id=cliente_id)

        # Obtiene el estatus del formulario
        estatus = request.POST.get('EstatusPed', 'Solicitado')  # Valor por defecto es 'Solicitado'

        # Crear el pedido con el estatus seleccionado
        pedido = Pedido(cliente=cliente, EstatusPed=estatus)
        pedido.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')

        with transaction.atomic():
            for producto_id, cantidad in zip(productos, cantidades):
                producto = get_object_or_404(Producto, id=producto_id)
                cantidad = int(cantidad)

                # Crear el detalle del pedido
                detalle = DetallePedido(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad
                )
                detalle.save()

            # Recalcular el total del pedido
            pedido.total = sum(detalle.subtotal for detalle in pedido.detalles.all())
            pedido.save()

        return redirect('detalle_pedido', nro_pedido=pedido.nro_pedido)  # Cambiar la redirección a detalles del pedido

    # Datos para el formulario
    context = {
        'clientes': Cliente.objects.all(),
        'productos': Producto.objects.all(),
    }
    return render(request, 'pedidos/crear_pedido.html', context)



def detalles_pedido(request, nro_pedido):
    pedido = get_object_or_404(Pedido, nro_pedido=nro_pedido)
    detalles = pedido.detalles.all()

    if request.method == 'POST':
        # Obtener el nuevo estado desde el formulario
        nuevo_estatus = request.POST.get('EstatusPed')
        if nuevo_estatus:
            pedido.EstatusPed = nuevo_estatus
            pedido.save()

        # Redirigir a la página de detalles del pedido con el nuevo estado
        return redirect('detalle_pedido', nro_pedido=pedido.nro_pedido)

    context = {
        'pedido': pedido,
        'detalles': detalles,
    }
    return render(request, 'pedidos/detalle_pedido.html', context)

# Vistas para listar entidades
@login_required
def ver_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'pedidos/ver_empresas.html', {'empresas': empresas})

@login_required
def ver_usuarios(request):
    usuarios = UserSistem.objects.all()
    return render(request, 'pedidos/ver_usuarios.html', {'usuarios': usuarios})

@login_required
def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'pedidos/ver_clientes.html', {'clientes': clientes})

@login_required
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'pedidos/ver_productos.html', {'productos': productos})

@login_required
def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'pedidos/ver_pedidos.html', context)
    #return render(request, 'pedidos/ver_pedidos.html', {'pedidos': pedidos})

# Vista para enviar mensajes
@login_required
def enviar_mensajes(request):
    enlaces = []
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        clientes_ids = request.POST.getlist('clientes')
        clientes = Cliente.objects.filter(id__in=clientes_ids)

        for cliente in clientes:
            if cliente.whatsapp:
                enlace = f"https://wa.me/{cliente.whatsapp}?text={mensaje}"
                enlaces.append(enlace)

    clientes = Cliente.objects.all()
    return render(request, 'pedidos/enviar_mensajes.html', {
        'clientes': clientes,
        'enlaces': enlaces
    })

# Vista para la ubicación de clientes en Google Maps
@login_required
def ubicacion_clientes(request):
    pedidos = Pedido.objects.select_related('cliente', 'producto').all()
    clientes_data = []

    for pedido in pedidos:
        clientes_data.append({
            'nombre': f"{pedido.cliente.nombre} {pedido.cliente.apellido}",
            'coordenadas': pedido.cliente.coordenadas,
            'pedido_info': f"Pedido ID: {pedido.id}, Producto: {pedido.producto.nombre}, Cantidad: {pedido.cantidad}",
            'estatus_pedido': pedido.EstatusPed
        })

    context = {
        'clientes_json': json.dumps(clientes_data),
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'pedidos/ubicacion_clientes.html', context)

@login_required
def productos(request):
    return render(request, 'pedidos/productos.html')

# Vistas para editar y eliminar productos en un pedido
@login_required
def editar_producto(request, nro_pedido, item_pedido):
    producto = Pedido.objects.get(nro_pedido=nro_pedido, item_pedido=item_pedido)
    if request.method == 'POST':
        producto.cantidad = request.POST.get('cantidad')
        producto.save()
        return redirect('crear_pedido')

    return render(request, 'pedidos/editar_producto.html', {'producto': producto})

@login_required
def eliminar_producto(request):
    if request.method == 'POST':
        productos_a_eliminar = request.POST.getlist('eliminar[]')
        Producto.objects.filter(id__in=productos_a_eliminar).delete()
    return redirect('ver_productos')

@login_required
def eliminar_empresas(request):
    if request.method == 'POST':
        empresas_a_eliminar = request.POST.getlist('empresas_a_eliminar')
        Empresa.objects.filter(id__in=empresas_a_eliminar).delete()
        messages.success(request, "Empresas seleccionadas eliminadas exitosamente.")
    return redirect('ver_empresas')

@login_required
def gestionar_empresas(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("action") and "eliminar" in value:
                _, empresa_id = value.split("_")
                empresa = get_object_or_404(Empresa, id=empresa_id)
                empresa.delete()
                messages.success(request, "Empresa eliminada correctamente.")
    return redirect('ver_empresas')

@login_required
def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa editada exitosamente.")
            return redirect('ver_empresas')
    else:
        form = EmpresaForm(instance=empresa)

    return render(request, 'pedidos/editar_empresa.html', {'form': form})