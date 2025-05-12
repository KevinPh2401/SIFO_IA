from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_orden_compra, name='crear_orden'),
    path('lista/', views.lista_ordenes, name='lista_ordenes'), 
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # CRUD de productos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # CRUD de ordenes de compra
    path('ordenes_compra/', views.lista_ordenes_compra, name='lista_ordenes_compra'),
    path('ordenes_compra/crear/', views.crear_orden_compra_manual, name='crear_orden_compra_manual'),
    path('ordenes_compra/editar/<int:pk>/', views.editar_orden_compra, name='editar_orden_compra'),
    path('ordenes_compra/eliminar/<int:pk>/', views.eliminar_orden_compra, name='eliminar_orden_compra'),

    # CRUD de detalle orden
    path('detalles/', views.lista_detalles, name='lista_detalles'),
    path('detalles/crear/', views.crear_detalle, name='crear_detalle'),
    path('detalles/editar/<int:pk>/', views.editar_detalle, name='editar_detalle'),
    path('detalles/eliminar/<int:pk>/', views.eliminar_detalle, name='eliminar_detalle'),

    # VISTA DEL PANEL
    path('panel/', views.vista_panel, name='vista_panel'),
    

 # vista opcional
]
