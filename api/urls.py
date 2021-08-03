from django.urls import path, include
from .views import ProductoList, ProductoDetalle, \
    ClienteList

urlpatterns = [
    path('v1/productos/',ProductoList.as_view(),name='producto_list'),
    path('v1/productos/<str:codigo>',ProductoDetalle.as_view(),name='producto_detalle'),
    path('v1/clientes/',ClienteList.as_view(),name='cliente_list')
]