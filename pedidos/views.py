from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from .models import Empresa, UserSistem, Cliente, Producto, Pedido, Portada
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from .forms import EmpresaForm, UserSistemForm, ClienteForm, ProductoForm, PedidoForm, PortadaForm, DetallePedidoForm
from .models import Empresa, UserSistem, Cliente, Producto, Pedido, Portada, DetallePedido
from django.core.exceptions import ValidationError
import json
from django.db.models import Max
from pedidos import models
from django.db import models
from django.views.decorators.csrf import csrf_exempt
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
def editar_empresa(request, item_empresa):
    # Cambia el argumento 'id' por 'item_empresa'
    empresa = get_object_or_404(Empresa, item_empresa=item_empresa)
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
            messages.success(request, "Cliente creado exitosamente.")
            return redirect('ver_clientes')  # Redirige a la vista de clientes después de guardar
        else:
            messages.error(request, "Hubo un error al crear el cliente.")
    else:
        form = ClienteForm()

    # Obtener todas las empresas disponibles
    empresas = Empresa.objects.all()
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
        empresa_item = request.POST.get('item_empresa')

        empresa = get_object_or_404(Empresa, item_empresa=empresa_item)

        Producto.objects.create(
            nombre=nombre,
            marca=marca,
            descripcion=descripcion,
            valor_unitario=valor_unitario,
            fecha_vencimiento=fecha_vencimiento,
            item_producto=item_producto,
            UM=UM,
            empresa=empresa
        )
        
        messages.success(request, "Producto creado exitosamente.")
        return redirect('ver_productos')

    empresas = Empresa.objects.all()
    return render(request, 'pedidos/crear_producto.html', {
        'empresas': empresas
    })

@login_required
def limpiar_productos(request):
    if request.method == 'POST':
        request.session['productos_solicitados'] = []
        messages.success(request, "Productos solicitados eliminados correctamente.")
    
    return redirect('crear_pedido')

@login_required
def guardar_pedido(request):
    if request.method == "POST":
        pedido_id = request.POST.get('pedido_id')  # El nombre correcto del campo enviado
        pedido = get_object_or_404(Pedido, nro_pedido=pedido_id)  # Ajustar a nro_pedido
        pedido.estado = 'Confirmado'  # Cambiar el estado a Confirmado
        pedido.save()  # Guardar cambios
        return JsonResponse({"success": True, "message": "Pedido guardado correctamente."})

# Vistas para listar entidades
@login_required
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'pedidos/ver_productos.html', {'productos': productos})

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
def ver_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente', 'producto', 'item_empresa').all()
    total_pedido = sum(pedido.val_producto for pedido in pedidos)
    return render(request, 'pedidos/ver_pedidos.html', {'pedidos': pedidos, 'total_pedido': total_pedido})

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

def productos(request):        # Acá se toman los productos del catálogo en imágenes
    return render(request, 'pedidos/productos.html')

# Vistas para editar y eliminar productos en un pedido
@login_required
def editar_producto(request, item_producto):
    producto = get_object_or_404(Producto, item_producto=item_producto)
    empresas = Empresa.objects.all()
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.marca = request.POST.get('marca')
        producto.descripcion = request.POST.get('descripcion')
        producto.valor_unitario = request.POST.get('valor_unitario')
        producto.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        producto.UM = request.POST.get('UM')
        empresa_item = request.POST.get('item_empresa')

        empresa = get_object_or_404(Empresa, item_empresa=empresa_item)
        producto.empresa = empresa

        producto.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect('ver_productos')

    return render(request, 'pedidos/editar_producto.html', {
        'producto': producto,
        'empresas': empresas
    })

@login_required
def eliminar_producto(request, producto_index):
    if request.method == 'POST':
        productos_solicitados = request.session.get('productos_solicitados', [])

        if 0 <= producto_index < len(productos_solicitados):
            productos_solicitados.pop(producto_index)
            request.session['productos_solicitados'] = productos_solicitados
            messages.success(request, "Producto eliminado correctamente.")

    return redirect('crear_pedido')

@login_required
def eliminar_empresas(request):
    if request.method == 'POST':
        empresas_a_eliminar = request.POST.getlist('empresas_a_eliminar')
        Empresa.objects.filter(item_empresa__in=empresas_a_eliminar).delete()
        messages.success(request, "Empresas seleccionadas eliminadas exitosamente.")
    return redirect('ver_empresas')

@login_required
def gestionar_empresas(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("action") and "eliminar" in value:
                _, empresa_item = value.split("_")
                empresa = get_object_or_404(Empresa, item_empresa=empresa_item)
                empresa.delete()
                messages.success(request, "Empresa eliminada correctamente.")
    return redirect('ver_empresas')

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, cliente_id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect('ver_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'pedidos/editar_cliente.html', {'form': form, 'cliente': cliente})


@login_required
def eliminar_cliente(request, cliente_id):  # Cambiado 'id' por 'cliente_id'
    cliente = get_object_or_404(Cliente, cliente_id=cliente_id)
    
    # Antes de eliminar, eliminar o desasociar todos los pedidos relacionados
    pedidos_relacionados = Pedido.objects.filter(cliente=cliente)
    if pedidos_relacionados.exists():
        pedidos_relacionados.delete()  # Elimina todos los pedidos relacionados con el cliente

    cliente.delete()  # Luego elimina el cliente
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('ver_clientes')

# Nueva vista para limpiar todos los clientes
@login_required
def limpiar_clientes(request):
    if request.method == 'POST':
        Cliente.objects.all().delete()  # Elimina todos los clientes de la base de datos
        messages.success(request, "Lista de clientes limpiada exitosamente.")
    return redirect('ver_clientes')

@login_required
def eliminar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    detalle.delete()
    return JsonResponse({'success': True})

@csrf_exempt
def agregar_producto(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad"))
        pedido_id = request.POST.get("pedido_id")

        # Obtener el pedido y el producto
        pedido = get_object_or_404(Pedido, nro_pedido=pedido_id)
        producto = get_object_or_404(Producto, item_producto=producto_id)

        # Calcular el item_pedido incremental
        item_pedido_count = DetallePedido.objects.filter(pedido=pedido).count() + 1

        # Crear un nuevo detalle del pedido
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            item_pedido=item_pedido_count,
            cantidad=cantidad,
            precio_unitario=producto.valor_unitario,
            subtotal=cantidad * producto.valor_unitario
        )

        # Actualizar el total del pedido
        pedido.actualizar_total()

        # Renderizar la tabla actualizada
        detalles = pedido.detallepedido_set.all()
        html = render_to_string("pedidos/_tabla_detalles.html", {"detalles": detalles})
        return JsonResponse({
            "success": True,
            "html": html,
            "total_pedido": pedido.total_pedido
        })
    return JsonResponse({"success": False, "error": "Error al agregar producto"})
    
@login_required
def crear_pedido(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Datos del formulario
        cliente_id = request.POST.get("cliente_id")
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))

        # Validación del cliente y producto
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        producto = get_object_or_404(Producto, pk=producto_id)

        # Crear o recuperar el pedido
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, estado="Solicitado")

        # Calcular el item_pedido incremental
        item_pedido_count = DetallePedido.objects.filter(pedido=pedido).count() + 1

        # Crear el detalle del pedido
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            item_pedido=item_pedido_count,
            cantidad=cantidad,
            precio_unitario=producto.valor_unitario,
            subtotal=cantidad * producto.valor_unitario
        )

        # Actualizar el total del pedido
        pedido.actualizar_total()

        # Renderizar la tabla de productos actualizada
        detalles = pedido.detalles.all()
        html = render_to_string("pedidos/_tabla_detalles.html", {"detalles": detalles, "pedido": pedido})

        return JsonResponse({"success": True, "html": html})

    # En caso de GET, cargar los clientes y productos
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, "pedidos/crear_pedido.html", {"clientes": clientes, "productos": productos})

@login_required
def crear_pedido(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Datos del formulario
        cliente_id = request.POST.get("cliente_id")
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))

        # Validación del cliente y producto
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        producto = get_object_or_404(Producto, pk=producto_id)

        # Crear o recuperar el pedido
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, estado="Solicitado")

        # Calcular el item_pedido incremental
        item_pedido_count = DetallePedido.objects.filter(pedido=pedido).count() + 1

        # Crear el detalle del pedido
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            item_pedido=item_pedido_count,
            cantidad=cantidad,
            precio_unitario=producto.valor_unitario,
            subtotal=cantidad * producto.valor_unitario
        )

        # Actualizar el total del pedido
        pedido.actualizar_total()

        # Renderizar la tabla de productos actualizada
        detalles = pedido.detalles.all()
        html = render_to_string("pedidos/_tabla_detalles.html", {"detalles": detalles, "pedido": pedido})

        return JsonResponse({"success": True, "html": html})

    # En caso de GET, cargar los clientes y productos
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, "pedidos/crear_pedido.html", {"clientes": clientes, "productos": productos})
