from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Portada(models.Model):
    imagen = models.ImageField(upload_to='portadas/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Portada {self.id}"

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default="Dirección no especificada")
    telefono = models.CharField(max_length=15, default="Sin teléfono")
    # Agrega otros campos necesarios

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
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()    

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    fecha_pedido = models.DateField(default=timezone.now)  # Establece la fecha actual como valor predeterminado
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    EstatusPed = models.CharField(max_length=20, choices=[
        ('Solicitado', 'Solicitado'),
        ('Confirmado', 'Confirmado'),
        ('Entregado', 'Entregado')
    ])
    cantidad = models.IntegerField(default=1)  # Define un valor predeterminado


    def __str__(self):
        return f"Pedido {self.id} - {self.estatus_pedido}"
