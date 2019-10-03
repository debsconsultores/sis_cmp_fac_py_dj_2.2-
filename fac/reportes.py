from django.shortcuts import render

from .models import FacturaEnc,FacturaDet

def imprimir_factura_recibo(request,id):
    template_name="fac/factura_one.html"

    enc = FacturaEnc.objects.get(id=id)
    det = FacturaDet.objects.filter(factura=id)

    context={
        'request':request,
        'enc':enc,
        'detalle':det
    }

    return render(request,template_name,context)