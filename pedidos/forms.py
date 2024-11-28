from django import forms
from .models import Empresa, UserSistem, Cliente, Producto, Pedido, Portada

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class UserSistemForm(forms.ModelForm):
    class Meta:
        model = UserSistem
        fields = '__all__'

class ClienteForm(forms.ModelForm):

    # Definir las opciones para el campo 'zona'
    ZONA_CHOICES = [
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
    ]

    # Campo zona que usa un Select para elegir entre las opciones de ZONA_CHOICES
    zona = forms.ChoiceField(choices=ZONA_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'cliente_id': 'Nro de Celular 10 Dígitos',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'documento': 'Documento de Identidad',
            'direccion': 'Dirección',
            'coordenadas': 'Coordenadas (Latitud, Longitud)',
            'telefono': 'Teléfono',
            'whatsapp': 'Número de WhatsApp',
            'zona': 'Zona de Ubicación',
            'metodo_pago': 'Método de Pago',
            'item_empresa': 'Empresa Asociada',
        }
        widgets = {
            'cliente_id': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'coordenadas': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'metodo_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'item_empresa': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

# Clase PortadaForm para cargar portadas
class PortadaForm(forms.ModelForm):
    class Meta:
        model = Portada
        fields = ['imagen', 'descripcion']  # Ajusta los campos según tu modelo