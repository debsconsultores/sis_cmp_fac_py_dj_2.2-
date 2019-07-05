from django.urls import path, include

from .views import ClienteView

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name="cliente_list"),

]