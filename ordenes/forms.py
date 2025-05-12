from django import forms
from .models import OrdenCompra, DetalleOrden
from .models import Proveedor
from .models import Producto
from .models import DetalleOrden


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'fecha_entrega', 'documento']
        widgets = {
            
            'proveedor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_entrega': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'documento': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['orden', 'producto', 'cantidad', 'precio_unitario']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad solicitada'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio por unidad'
            }),
        }
        labels = {
            'orden': 'Orden de Compra',
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del contacto'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'stock', 'stock_minimo', 'stock_maximo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción breve',
                'rows': 3
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad en stock'
            }),

            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad minima en stock'
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad maxima en stock'
            }),
        }