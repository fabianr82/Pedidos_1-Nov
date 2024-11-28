from django.urls import path
from . import views

urlpatterns = [
    # Ruta de inicio y autenticación
    path('', views.login_view, name='login'),  # Página de inicio como login
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.logout_view, name='logout'),
    # path('cargar_portada/', views.cargar_portada, name='cargar_portada'),

    # Rutas de Empresa
    path('crear_empresa/', views.crear_empresa, name='crear_empresa'),
    path('ver_empresas/', views.ver_empresas, name='ver_empresas'),
    path('gestionar_empresas/', views.gestionar_empresas, name='gestionar_empresas'),
    path('eliminar_empresas/', views.eliminar_empresas, name='eliminar_empresas'),
    #path('editar_empresa/<int:id>/', views.editar_empresa, name='editar_empresa'),
    path('editar_empresa/<str:item_empresa>/', views.editar_empresa, name='editar_empresa'),


    # Rutas de Usuario y Cliente
    path('crear_usuario/', views.crear_user_sist, name='crear_usuario'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('ver_clientes/', views.ver_clientes, name='ver_clientes'),
    path('editar_cliente/<str:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<str:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('limpiar_clientes/', views.limpiar_clientes, name='limpiar_clientes'),  # Añadir esta línea
    
    # Rutas de Producto
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<str:item_producto>/', views.editar_producto, name='editar_producto'),
    path('ver_productos/', views.ver_productos, name='ver_productos'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),

    # Rutas de Pedido
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    
    # Rutas de Mensajes y Ubicación
    path('enviar_mensajes/', views.enviar_mensajes, name='enviar_mensajes'),
    path('ubicacion_clientes/', views.ubicacion_clientes, name='ubicacion_clientes'),
]