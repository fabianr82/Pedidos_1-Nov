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
    item_producto = models.CharField(max_length=10, primary_key=True, unique=True)
    UM = models.CharField(max_length=10)
    empresa = models.ForeignKey(Empresa, to_field='item_empresa', on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

# Modelo Pedido
class Pedido(models.Model):
    nro_pedido = models.IntegerField(default=1, primary_key=True)
    item_pedido = models.IntegerField(default=1)

    # Relacionar con cliente usando el campo cliente_id
    cliente = models.ForeignKey(
        Cliente,
        to_field='cliente_id',  # Usar el campo 'cliente_id' para la relación
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    # Relacionar el pedido con la empresa correspondiente
    item_empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)

    EstatusPed = models.CharField(max_length=20, choices=[
        ('Solicitado', 'Solicitado'),
        ('Confirmado', 'Confirmado'),
        ('Entregado', 'Entregado')
    ])

    cantidad = models.PositiveIntegerField(default=1)
    fecha_pedido = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('nro_pedido', 'item_pedido')

    def save(self, *args, **kwargs):
        if not self.nro_pedido:
            last_pedido = Pedido.objects.order_by('-nro_pedido').first()
            self.nro_pedido = last_pedido.nro_pedido + 1 if last_pedido else 1

        if not self.item_pedido:
            max_item = Pedido.objects.filter(nro_pedido=self.nro_pedido).count()
            self.item_pedido = max_item + 1

        super(Pedido, self).save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nombre} {self.cliente.apellido} - Producto: {self.producto.nombre}"

    @property
    def val_producto(self):
        return self.producto.valor_unitario * self.cantidad