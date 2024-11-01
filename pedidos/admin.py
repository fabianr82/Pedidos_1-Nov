from django.contrib import admin
from .models import UserSistem, Empresa, Cliente, Producto, Pedido

admin.site.register(UserSistem)
admin.site.register(Empresa)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)