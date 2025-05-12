from django import forms
from .models import Usuario

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