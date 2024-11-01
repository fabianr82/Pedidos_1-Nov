from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmpresaForm, UserSistemForm, ClienteForm, ProductoForm, PedidoForm, PortadaForm
from .models import Empresa, UserSistem, Cliente, Producto, Pedido, Portada

# Vista para la página de inicio
@login_required
def inicio(request):
    portada = Portada.objects.last()  # Obtener la última portada cargada
    return render(request, 'pedidos/inicio.html', {'portada': portada})

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
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/crear_pedido.html', {'form': form})

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