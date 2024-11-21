# sistema_pedidos/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from pedidos import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),  # Redirige la raíz al login o al inicio
    path('inicio/', include('pedidos.urls')),  # Incluye las URLs de la app `pedidos`
    path('productos/', views.productos, name='productos'), # Incluye las URLs de la app `productos`
]