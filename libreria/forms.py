from django import forms
from .models import Usuario, Empresa
from django.contrib.auth.forms import UserCreationForm



class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    codigo_empresa = forms.CharField(label='Código de Empresa')

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'telefono', 'password', 'codigo_empresa']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_codigo_empresa(self):
        codigo = self.cleaned_data.get('codigo_empresa')
        try:
            empresa = Empresa.objects.get(codigo_empresa=codigo)
        except Empresa.DoesNotExist:
            raise forms.ValidationError("Código de empresa no válido.")
        return empresa  # devuelve la instancia de empresa, no el código

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.empresa = self.cleaned_data['codigo_empresa']  # ya es instancia gracias al clean_codigo_empresa
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