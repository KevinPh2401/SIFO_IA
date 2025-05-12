from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from .models import OrdenCompra, DetalleOrden, Producto, Proveedor
from .forms import OrdenCompraForm, DetalleOrdenForm, ProveedorForm, ProductoForm


def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()  # obtiene todas las órdenes
    return render(request, 'ordenes/lista_ordenes.html', {'ordenes': ordenes})


def crear_orden_compra(request):
    DetalleFormSet = modelformset_factory(DetalleOrden, form=DetalleOrdenForm, extra=1, can_delete=False)

    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST, request.FILES)
        detalle_formset = DetalleFormSet(request.POST)

        if orden_form.is_valid() and detalle_formset.is_valid():
            orden = orden_form.save()

            for form in detalle_formset:
                detalle = form.save(commit=False)
                producto = detalle.producto

                # Validación: cantidad mayor a cero
                if detalle.cantidad <= 0:
                    messages.error(request, f"La cantidad para '{producto}' debe ser mayor a cero.")
                    orden.delete()
                    return redirect('crear_orden')

                # Validación: stock máximo
                if producto.stock + detalle.cantidad > producto.stock_maximo:
                    messages.warning(
                        request,
                        f"Advertencia: '{producto}' sobrepasa el stock máximo al agregar esta orden."
                    )

                detalle.orden = orden
                detalle.save()

            messages.success(request, "Orden de compra creada correctamente.")
            return redirect('lista_ordenes')  # Cambia según tu ruta

        else:
            messages.error(request, "Revisa los errores en el formulario.")
    else:
        orden_form = OrdenCompraForm()
        detalle_formset = DetalleFormSet(queryset=DetalleOrden.objects.none())

    return render(request, 'ordenes/crear_orden.html', {
        'orden_form': orden_form,
        'detalle_formset': detalle_formset
    })


# VISTA PARA LA PARTE DE PROVEEDORES
# LISTA
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})

# CREAR
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/form.html', {'form': form})

# EDITAR
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        return redirect('lista_proveedores')
    return render(request, 'proveedores/form.html', {'form': form})

# ELIMINAR
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'proveedores/confirmar_eliminar.html', {'proveedor': proveedor})

# CIERRE DE LA VISTA PARA LA PARTE DE PROVEEDORES

# VISTA PARA LA PARTE DE PRODUCTOS
# LISTAR
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

# CREAR
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form})

# EDITAR
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('lista_productos')
    return render(request, 'productos/form.html', {'form': form})

# ELIMINAR
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})

# CIERRE DE LA VISTA PARA LA PARTE DE PRODUCTOS



# VISTA PARA LA PARTE DE ORDEN COMPRA
# LISTAR
def lista_ordenes_compra(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'ordenes_compra/lista.html', {'ordenes': ordenes})

# CREAR
def crear_orden_compra_manual(request):
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_ordenes_compra')
    else:
        form = OrdenCompraForm()
    return render(request, 'ordenes_compra/form.html', {'form': form})

# EDITAR
def editar_orden_compra(request, pk):
    orden = get_object_or_404(OrdenCompra, pk=pk)
    form = OrdenCompraForm(request.POST or None, request.FILES or None, instance=orden)
    if form.is_valid():
        form.save()
        return redirect('lista_ordenes_compra')
    return render(request, 'ordenes_compra/form.html', {'form': form})

# ELIMINAR
def eliminar_orden_compra(request, pk):
    orden = get_object_or_404(OrdenCompra, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('lista_ordenes_compra')
    return render(request, 'ordenes_compra/confirmar_eliminar.html', {'orden': orden})

# CIERRE DE LA VISTA PARA LA PARTE DE ORDEN COMPRA



# VISTA PARA LA PARTE DE DETALLE ORDEN
# LISTAR
def lista_detalles(request):
    detalles = DetalleOrden.objects.select_related('orden', 'producto').all()
    return render(request, 'detalles/lista.html', {'detalles': detalles})

# CREAR
def crear_detalle(request):
    if request.method == 'POST':
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_detalles')
    else:
        form = DetalleOrdenForm()
    return render(request, 'detalles/form.html', {'form': form})

# EDITAR
def editar_detalle(request, pk):
    detalle = get_object_or_404(DetalleOrden, pk=pk)
    form = DetalleOrdenForm(request.POST or None, instance=detalle)
    if form.is_valid():
        form.save()
        return redirect('lista_detalles')
    return render(request, 'detalles/form.html', {'form': form})

# ELIMINAR
def eliminar_detalle(request, pk):
    detalle = get_object_or_404(DetalleOrden, pk=pk)
    if request.method == 'POST':
        detalle.delete()
        return redirect('lista_detalles')
    return render(request, 'detalles/confirmar_eliminar.html', {'detalle': detalle})

# CIERRE DE LA VISTA PARA LA PARTE DE DETALLE ORDEN

#  VISTA TIPO PANEL PARA CREAR LA ORDEN COMPLETA
def vista_panel(request):
    mensaje = None

    proveedor_form = ProveedorForm()
    producto_form = ProductoForm()
    orden_form = OrdenCompraForm()
    detalle_form = DetalleOrdenForm()

    if request.method == 'POST':
        if 'guardar_proveedor' in request.POST:
            proveedor_form = ProveedorForm(request.POST)
            if proveedor_form.is_valid():
                proveedor_form.save()
                mensaje = "Proveedor creado exitosamente"

        elif 'guardar_producto' in request.POST:
            producto_form = ProductoForm(request.POST)
            if producto_form.is_valid():
                producto_form.save()
                mensaje = "Producto creado exitosamente"

        elif 'guardar_orden' in request.POST:
            orden_form = OrdenCompraForm(request.POST, request.FILES)
            if orden_form.is_valid():
                orden_form.save()
                mensaje = "Orden de compra creada"

        elif 'guardar_detalle' in request.POST:
            detalle_form = DetalleOrdenForm(request.POST)
            if detalle_form.is_valid():
                detalle_form.save()
                mensaje = "Detalle agregado a la orden"

    contexto = {
        'proveedor_form': proveedor_form,
        'producto_form': producto_form,
        'orden_form': orden_form,
        'detalle_form': detalle_form,
        'mensaje': mensaje,
    }
    return render(request, 'panel_admin.html', contexto)

# CIERRE DE LA VISTA PARA LA PARTE DE CREACION DE ORDEN COMPLETA


#PROTECCION DE LA VISTA DEL PANEL ADMINISTRATIVO

#CIERRE DE LA PROTECCION DE LA VISTA DEL PANEL ADMINISTRATIVO
