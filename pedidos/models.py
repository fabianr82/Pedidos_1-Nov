from typing import Self
from django.core.exceptions import ValidationError 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import pedidos

class Portada(models.Model):
    imagen = models.ImageField(upload_to='portadas/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Portada {self.id}"

class Empresa(models.Model):
    CIUDADES = [
        ("BOGOTÁ D.C.", "BOGOTÁ D.C."),
        ("MANTA", "MANTA"),
        ("TUNJA", "TUNJA"),
        ("BELÉN", "BELÉN"),
        ("MEDELLÍN", "MEDELLÍN"),
        ("CALI", "CALI"),
        ("BARRANQUILLA", "BARRANQUILLA"),
        ("CARTAGENA", "CARTAGENA"),
        ("BUCARAMANGA", "BUCARAMANGA"),
        ("MANIZALES", "MANIZALES"),
        ("PEREIRA", "PEREIRA"),
        ("IBAGUÉ", "IBAGUÉ"),
        ("SANTA MARTA", "SANTA MARTA"),
    ]
    item_empresa = models.CharField(max_length=10, unique=True, default="ID Empresa")
    nit = models.CharField(max_length=15, unique=True, default="NIT Empresa")
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default="Dirección empresa")
    coord_emp = models.CharField(max_length=30, default="Formato: Latitud, Longitud")
    telefono = models.CharField(max_length=15, default="+57 y Teléfono")
    ciudad_emp = models.CharField(
        max_length=30,
        choices=CIUDADES,
        default="BOGOTÁ D.C."  # Valor predeterminado
    )

    # Agrega otros campos necesarios

    def __str__(self):
        return f"{self.nombre} ({self.nit}) ({self.item_empresa})"

class UserSistem(models.Model):
    # Define los campos para el modelo UserSistem
    nombre = models.CharField(max_length=100)
    # Agrega otros campos necesarios

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    item_empresa = models.ForeignKey(
        'Empresa',  # Referencia al modelo Empresa
        on_delete=models.CASCADE,
        default=1  # ID predeterminado de una Empresa existente
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200)  # Dirección seleccionada de Google Places
    
    #coordenadas = models.CharField(max_length=50)  # Para almacenar latitud y longitud
    coordenadas = models.CharField(max_length=50, blank=True, null=True)  # Guardar latitud y longitud
       
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
    # Mantén el campo 'id' como clave primaria
    id = models.AutoField(primary_key=True)
    
    # Cambiar 'nro_pedido' para que sea autoincrementable y único
    nro_pedido = models.IntegerField(unique=True, editable=False)  # No editable por el usuario
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    item_empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    
    EstatusPed = models.CharField(max_length=20, choices=[
        ('Solicitado', 'Solicitado'),
        ('Pagado', 'Pagado'),
        ('Entregado', 'Entregado'),
        ('Pagado', 'Pagado')
    ])
    
    fecha_pedido = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-nro_pedido']

    def save(self, *args, **kwargs):
        # Si 'nro_pedido' no está asignado, lo generamos automáticamente
        if not self.nro_pedido:
            # Obtener el máximo nro_pedido actual (si hay registros previos)
            max_nro_pedido = Pedido.objects.aggregate(models.Max('nro_pedido'))['nro_pedido__max']
            
            # Si no hay pedidos previos, max_nro_pedido será None, por lo que asignamos 1
            self.nro_pedido = (max_nro_pedido or 0) + 1  # Si max_nro_pedido es None, se asigna 1
        
        # El cálculo del total sigue existiendo
        if self.pk:  # Solo calcula el total si el pedido ya tiene un id (es decir, ya existe)
            self.total = sum(detalle.subtotal for detalle in self.detalles.all())

        super(Pedido, self).save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.nro_pedido} - Cliente: {self.cliente.nombre} {self.cliente.apellido}"


    
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # Relación con el pedido
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de producto
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario del producto
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Subtotal (cantidad * precio_unitario)

    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.precio_unitario = self.producto.valor_unitario
        self.subtotal = self.cantidad * self.precio_unitario
        super(DetallePedido, self).save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de Pedido {self.pedido.nro_pedido} - Producto: {self.producto.nombre}"