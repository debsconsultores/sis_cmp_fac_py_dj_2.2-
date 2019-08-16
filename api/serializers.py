from rest_framework import serializers

from inv.models import Producto

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Producto
        fields='__all__'