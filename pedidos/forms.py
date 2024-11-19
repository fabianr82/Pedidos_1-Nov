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
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
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