from django.core.exceptions import ValidationError 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Portada(models.Model):
    imagen = models.ImageField(upload_to='portadas/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Portada {self.id}"

class Empresa(models.Model):
<<<<<<< HEAD
    item_empresa = models.CharField(max_length=10, default="ID Empresa")
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default="Dirección no especificada")
    coord_emp = models.CharField(max_length=30, default="Formato: Latitud, Longitud")
    telefono = models.CharField(max_length=15, default="+57 y Teléfono")
    ciudad = models.CharField(max_length=30, default="Ciudad")

    # Agrega otros campos necesarios

=======
    item_empresa = models.CharField(max_length=10, unique=True)  # Nuevo campo con un máximo de 10 caracteres
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default="Dirección no especificada")
    nit = models.CharField(max_length=10, unique=True, default=1)
    coord_emp = models.CharField(max_length=50, default="(lon_x.xxxx,lat_x.xxxx)")  # Para almacenar latitud y longitud
    ciudad_emp = models.CharField(max_length=100, default="Ciudad")
    telefono = models.CharField(max_length=15, default="Sin teléfono")
    
>>>>>>> d3ec3b4c88e179074629feb631a2aa50fa1d88e3
    def __str__(self):
        return self.nombre

class UserSistem(models.Model):
    # Define los campos para el modelo UserSistem
    nombre = models.CharField(max_length=100)
    # Agrega otros campos necesarios

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200)
    coordenadas = models.CharField(max_length=50)  # Para almacenar latitud y longitud
    telefono = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    zona = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    item_empresa = models.ForeignKey(Empresa, to_field="item_empresa", on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField()
    UM = models.CharField(max_length=15, default='UND')  # Permitir valores personalizados
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    item_producto = models.IntegerField(unique=True, default=1)
    
    def clean(self):
        # Verificar si `item_producto` ya existe
        if Producto.objects.filter(item_producto=self.item_producto).exclude(pk=self.pk).exists():
            raise ValidationError({'item_producto': 'El valor de Item Producto ya existe. Por favor, elige un valor diferente.'})

    def save(self, *args, **kwargs):
        # Llamar a `clean` para validar antes de guardar
        self.full_clean()  # Ejecuta todas las validaciones, incluida `clean`
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - Item: {self.item_producto}"

class Pedido(models.Model):
    nro_pedido = models.IntegerField(default=1)  # Campo para el número de pedido
    item_pedido = models.IntegerField(default=1)  # Campo para el número de ítem
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # Cambia `item_empresa` a un campo `ForeignKey` que apunte al modelo `Empresa`
    item_empresa = models.ForeignKey(Empresa, to_field="item_empresa", on_delete=models.SET_NULL, null=True, blank=True)
    EstatusPed = models.CharField(max_length=20, choices=[
        ('Solicitado', 'Solicitado'),
        ('Confirmado', 'Confirmado'),
        ('Entregado', 'Entregado')
    ])
    cantidad = models.IntegerField(default=1)
    fecha_pedido = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ('nro_pedido', 'item_pedido')  # Restringe la unicidad combinada

    def save(self, *args, **kwargs):
        if not self.nro_pedido:
            last_pedido = Pedido.objects.order_by('-nro_pedido').first()
            self.nro_pedido = last_pedido.nro_pedido + 1 if last_pedido else 1

        if not self.item_pedido:
            # Generar un nuevo `item_pedido` basado en el número de ítems en el pedido actual
            max_item = Pedido.objects.filter(nro_pedido=self.nro_pedido).count()
            self.item_pedido = max_item + 1

        super(Pedido, self).save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nombre} {self.cliente.apellido} - Producto: {self.producto.nombre}"
    @property
    def val_producto(self):
        return self.producto.valor_unitario * self.cantidad
    