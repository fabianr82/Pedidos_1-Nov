from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmpresaForm, UserSistemForm, ClienteForm, ProductoForm, PedidoForm, PortadaForm
from .models import Empresa, UserSistem, Cliente, Producto, Pedido, Portada
import json
from datetime import datetime

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

# Vistas para la creación de entidades
@login_required
def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'pedidos/crear_empresa.html', {'form': form})

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
            return redirect('ver_clientes')
    else:
        form = ClienteForm()
    return render(request, 'pedidos/crear_cliente.html', {'form': form})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_productos')
    else:
        form = ProductoForm()
    return render(request, 'pedidos/crear_producto.html', {'form': form})

@login_required
def crear_pedido(request):
    productos_solicitados = request.session.get('productos_solicitados', [])
    total_pedido = sum(producto['val_producto'] for producto in productos_solicitados)

    if request.method == 'POST':
        if 'limpiar_productos' in request.POST:
            request.session['productos_solicitados'] = []
            messages.success(request, "Productos solicitados eliminados correctamente.")
            return redirect('crear_pedido')

        if 'eliminar_productos_seleccionados' in request.POST:
            # Recibir los índices de las filas seleccionadas para eliminar
            indices_a_eliminar = request.POST.getlist('eliminar_fila')
            if indices_a_eliminar:
                # Convertir los índices a enteros y eliminar en orden inverso para evitar problemas
                indices_a_eliminar = sorted([int(i) for i in indices_a_eliminar], reverse=True)
                for index in indices_a_eliminar:
                    if 0 <= index < len(productos_solicitados):
                        productos_solicitados.pop(index)
                request.session['productos_solicitados'] = productos_solicitados
                messages.success(request, "Productos seleccionados eliminados correctamente.")
            
            # Recalcular el total después de la eliminación
            total_pedido = sum(producto['val_producto'] for producto in productos_solicitados)

        elif 'agregar_producto' in request.POST:
            producto_id = request.POST.get('producto')
            cantidad = int(request.POST.get('cantidad', 1))

            if producto_id and cantidad > 0:
                producto = Producto.objects.get(id=producto_id)
                val_producto = float(producto.valor_unitario) * cantidad

                nro_pedido = request.session.get('nro_pedido', 1)
                item_pedido = len(productos_solicitados) + 1

                productos_solicitados.append({
                    'id': producto.id,
                    'nro_pedido': nro_pedido,
                    'item_pedido': item_pedido,
                    'nombre': producto.nombre,
                    'marca': producto.marca,
                    'descripcion': producto.descripcion,
                    'valor_unitario': float(producto.valor_unitario),
                    'cantidad': cantidad,
                    'val_producto': val_producto,
                    'fecha_pedido': datetime.now().strftime('%Y-%m-%d')
                })
                request.session['productos_solicitados'] = productos_solicitados
                messages.success(request, "Producto agregado a la lista.")

            total_pedido = sum(producto['val_producto'] for producto in productos_solicitados)

        elif 'guardar_pedido' in request.POST:
            cliente_id = request.POST.get('cliente')
            estatus_pedido = request.POST.get('EstatusPed')
            fecha_pedido = datetime.now().strftime('%Y-%m-%d')

            if cliente_id and productos_solicitados:
                cliente = Cliente.objects.get(id=cliente_id)

                for producto_data in productos_solicitados:
                    producto = Producto.objects.get(id=producto_data['id'])
                    
                    ultimo_pedido = Pedido.objects.filter(nro_pedido=producto_data['nro_pedido']).order_by('-item_pedido').first()
                    item_pedido = (ultimo_pedido.item_pedido + 1) if ultimo_pedido else 1

                    Pedido.objects.create(
                        nro_pedido=producto_data['nro_pedido'],
                        cliente=cliente,
                        producto=producto,
                        EstatusPed=estatus_pedido,
                        cantidad=producto_data['cantidad'],
                        fecha_pedido=fecha_pedido,
                        item_pedido=item_pedido
                    )

                request.session['productos_solicitados'] = []
                messages.success(request, "Pedido guardado correctamente.")
                return redirect('inicio')

    productos = Producto.objects.all()
    clientes = Cliente.objects.all()
    cliente_id = request.POST.get('cliente') if request.method == 'POST' else None
    cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None

    return render(request, 'pedidos/crear_pedido.html', {
        'productos': productos,
        'clientes': clientes,
        'productos_solicitados': productos_solicitados,
        'total_pedido': total_pedido,
        'cliente_seleccionado': cliente
    })

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
    return render(request, 'pedidos/ver_pedidos.html', {'pedidos': pedidos})

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
def eliminar_producto(request, nro_pedido, item_pedido):
    producto = Pedido.objects.get(nro_pedido=nro_pedido, item_pedido=item_pedido)
    producto.delete()
    return redirect('crear_pedido')