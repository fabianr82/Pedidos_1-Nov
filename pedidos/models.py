from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Modelo de la portada
class Portada(models.Model):
    imagen = models.ImageField(upload_to='portadas/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Portada {self.id}"

# Modelo de Empresa
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

    item_empresa = models.CharField(max_length=10,primary_key=True, unique=True, default="ID Empresa")
    nit = models.CharField(max_length=15, unique=True, default="NIT Empresa")
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default="Dirección empresa")
    coord_emp = models.CharField(max_length=30, default="Formato: Latitud, Longitud")
    telefono = models.CharField(max_length=15, default="+57 y Teléfono")
    ciudad_emp = models.CharField(max_length=30, choices=CIUDADES, default="BOGOTÁ D.C.")

    def __str__(self):
        return f"{self.nombre} ({self.nit})"

# Modelo de usuario del sistema
class UserSistem(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relación con User
    item_empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    cliente_id = models.CharField(max_length=10, primary_key=True, default="ID Cliente")  # Establecer como llave primaria
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200)
    coordenadas = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    zona = models.CharField(max_length=50, choices=[
        ('Otra', 'Otra'),
        ('NA', 'NA'),
        ('Usaquén', 'Usaquén'),
        ('Chapinero', 'Chapinero'),
        ('Santa Fe', 'Santa Fe'),
        ('San Cristóbal', 'San Cristóbal'),
        ('Usme', 'Usme'),
        ('Tunjuelito', 'Tunjuelito'),
        ('Bosa', 'Bosa'),
        ('Kennedy', 'Kennedy'),
        ('Fontibón', 'Fontibón'),
        ('Engativá', 'Engativá'),
        ('Suba', 'Suba'),
        ('Barrios Unidos', 'Barrios Unidos'),
        ('Teusaquillo', 'Teusaquillo'),
        ('Los Mártires', 'Los Mártires'),
        ('Antonio Nariño', 'Antonio Nariño'),
        ('Puente Aranda', 'Puente Aranda'),
        ('Candelaria', 'Candelaria'),
        ('Rafael Uribe Uribe', 'Rafael Uribe Uribe'),
        ('Ciudad Bolívar', 'Ciudad Bolívar'),
        ('Sumapaz', 'Sumapaz'),
    ], default='Otra')
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    item_producto = models.CharField(max_length=10, primary_key=True)
    UM = models.CharField(max_length=10)
    empresa = models.ForeignKey(Empresa, to_field='item_empresa', on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

class Pedido(models.Model):
    nro_pedido = models.AutoField(primary_key=True)  # Número autoincremental del pedido
    fecha_pedido = models.DateField(default=timezone.now)  # Fecha de creación
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente asociado al pedido
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Solicitado', 'Solicitado'),
            ('Confirmado', 'Confirmado'),
            ('Enviado', 'Enviado'),
            ('Entregado', 'Entregado')
        ],
        default='Solicitado'
    )
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def actualizar_total(self):
        """
        Suma todos los subtotales de los detalles asociados y actualiza el total.
        """
        self.total_pedido = sum(detalle.subtotal for detalle in self.detalles.all())  # Usamos related_name
        self.save()

    def __str__(self):
        return f"Pedido {self.nro_pedido} - Cliente: {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name="detalles"  # Acceso desde Pedido
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    item_pedido = models.PositiveIntegerField(default=1)  # Incremental automático
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        Calcula automáticamente item_pedido, precio_unitario y subtotal antes de guardar.
        """
        if not self.pk:  # Solo se calcula al crear un nuevo detalle
            self.item_pedido = self.pedido.detalles.count() + 1  # Cuenta ítems ya existentes
        self.precio_unitario = self.producto.valor_unitario
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.pedido.actualizar_total()  # Actualiza el total del pedido

    def __str__(self):
        return f"Item {self.item_pedido} - {self.producto.nombre} ({self.cantidad} unidades)"