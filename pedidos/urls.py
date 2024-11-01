from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Página de inicio como login
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.logout_view, name='logout'),
    path('cargar_portada/', views.cargar_portada, name='cargar_portada'),
    path('crear_empresa/', views.crear_empresa, name='crear_empresa'),
    path('crear_usuario/', views.crear_user_sist, name='crear_usuario'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('ver_empresas/', views.ver_empresas, name='ver_empresas'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('ver_clientes/', views.ver_clientes, name='ver_clientes'),
    path('ver_productos/', views.ver_productos, name='ver_productos'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
]