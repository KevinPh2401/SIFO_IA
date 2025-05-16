from django import forms
from .models import Usuario, Empresa
from django.contrib.auth.forms import UserCreationForm
import re
from django.forms.widgets import DateInput


class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    codigo_empresa = forms.CharField(label='Código de Empresa')

    fecha_nacimiento = forms.DateField(
    widget=DateInput(attrs={'type': 'date'}),
    label="Fecha de Nacimiento",
    required=False
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento',
            'tipo_documento', 'numero_documento', 'imagen', 'descripcion'
        ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise forms.ValidationError("La contraseña debe contener letras y números.")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este email.")
        return email

    def clean_numero_documento(self):
        numero = self.cleaned_data.get('numero_documento')
        if numero and Usuario.objects.filter(numero_documento=numero).exists():
            raise forms.ValidationError("Ya existe un usuario con este número de documento.")
        return numero

    def clean_codigo_empresa(self):
        codigo = self.cleaned_data.get('codigo_empresa')
        try:
            empresa = Empresa.objects.get(codigo_empresa=codigo)
        except Empresa.DoesNotExist:
            raise forms.ValidationError("Código de empresa no válido.")
        return empresa

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.empresa = self.cleaned_data['codigo_empresa']  # Instancia de empresa
        if commit:
            usuario.save()
        return usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

class DeditosForm(forms.Form):
    cantidad_deditos = forms.IntegerField(label="Cantidad de deditos", min_value=1)
    precio_harina = forms.FloatField(label="Precio del kilo de harina", min_value=0)
    precio_queso = forms.FloatField(label="Precio del kilo de queso", min_value=0)