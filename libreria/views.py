from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from .forms import UsuarioForm
from .forms import DeditosForm


# Create your views here.
def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/index.html', {'usuarios': usuarios})

def crear(request):
    formulario = UsuarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/crear.html', {'formulario': formulario})

def editar(request, id):
    usuario = Usuario.objects.get(id=id)
    formulario = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/editar.html', {'formulario': formulario})



def eliminar(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('usuarios')


#DEDITOS CALCULADORA
from django.shortcuts import render
from .forms import DeditosForm

def calcular_ingredientes(cantidad, porcentaje_harina=0.4, peso_total_20=400):
    peso_por_dedito = peso_total_20 / 20
    peso_total = peso_por_dedito * cantidad
    harina = peso_total * porcentaje_harina
    queso = peso_total * (1 - porcentaje_harina)
    return harina, queso, peso_total

def calcular_costos(harina_g, queso_g, precio_kg_harina, precio_kg_queso):
    harina_kg = harina_g / 1000
    queso_kg = queso_g / 1000
    costo_harina = harina_kg * precio_kg_harina
    costo_queso = queso_kg * precio_kg_queso
    return round(costo_harina, 2), round(costo_queso, 2), round(costo_harina + costo_queso, 2)

def deditos_view(request):
    resultado = None
    if request.method == 'POST':
        form = DeditosForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            harina, queso, peso_total = calcular_ingredientes(cd['cantidad_deditos'])
            costo_harina, costo_queso, costo_total = calcular_costos(
                harina, queso, cd['precio_harina'], cd['precio_queso']
            )
            resultado = {
                'harina': round(harina, 2),
                'queso': round(queso, 2),
                'peso_total': round(peso_total, 2),
                'costo_harina': costo_harina,
                'costo_queso': costo_queso,
                'costo_total': costo_total
            }
    else:
        form = DeditosForm()
    
    return render(request, 'calculadora_deditos/calculadora.html', {'form': form, 'resultado': resultado})

#CIERRE DE DEDIDOS CALCULADORA


#autenticacion del login para redireccionar a la pagina del panel dashboard


#cierre del autenticador login