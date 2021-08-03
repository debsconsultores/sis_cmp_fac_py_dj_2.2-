from django.urls import path, include

from .views import ClienteView,ClienteNew,ClienteEdit,clienteInactivar, \
    FacturaView, facturas, \
    ProductoView, \
    borrar_detalle_factura, \
    cliente_add_modify

from .reportes import imprimir_factura_recibo, imprimir_factura_list

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteInactivar, name="cliente_inactivar"),

    path('facturas/',FacturaView.as_view(), name="factura_list"),
    path('facturas/new',facturas, name="factura_new"),
    path('facturas/edit/<int:id>',facturas, name="factura_edit"),
    
    path('facturas/buscar-producto',ProductoView.as_view(), name="factura_producto"),

    path('facturas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),

    path('facturas/imprimir/<int:id>',imprimir_factura_recibo, name="factura_imprimir_one"),

    path('facturas/imprimir-todas/<str:f1>/<str:f2>',imprimir_factura_list, name="factura_imprimir_all"),

    path('facturas/clientes/new/',cliente_add_modify,name="fac_cliente_add"),
    path('facturas/clientes/<int:pk>',cliente_add_modify,name="fac_cliente_mod"),

]