from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProductoSerializer,ClienteSerializer
from inv.models import Producto
from fac.models import Cliente

from django.db.models import Q

class ProductoList(APIView):
    def get(self,request):
        prod = Producto.objects.all()
        data = ProductoSerializer(prod,many=True).data
        return Response(data)


class ProductoDetalle(APIView):
    def get(self,request, codigo):
        prod = get_object_or_404(Producto,Q(codigo=codigo)|Q(codigo_barra=codigo))
        data = ProductoSerializer(prod).data
        return Response(data)


class ClienteList(APIView):
    def get(self,request):
        obj = Cliente.objects.all()
        data = ClienteSerializer(obj,many=True).data
        return Response(data)