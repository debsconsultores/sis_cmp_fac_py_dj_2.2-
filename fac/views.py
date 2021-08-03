from django.shortcuts import render,redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate

from bases.views import SinPrivilegios

from .models import Cliente, FacturaEnc, FacturaDet
from .forms import ClienteForm
import inv.views as inv
from inv.models import Producto

class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "fac/cliente_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_cliente"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.add_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get")
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})


class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get en editar")

        print(request)
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        print(form_class,form,context)
        return self.render_to_response(context)


@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "fac/factura_list.html"
    context_object_name = "obj"
    permission_required="fac.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs


@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request,id=None):
    template_name='fac/facturas.html'

    detalle = {}
    clientes = Cliente.objects.filter(estado=True)
    
    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first()
        if id:
            if not enc:
                messages.error(request,'Factura No Existe')
                return redirect("fac:factura_list")

            usr = request.user
            if not usr.is_superuser:
                if enc.uc != usr:
                    messages.error(request,'Factura no fue creada por usuario')
                    return redirect("fac:factura_list")

        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0.00,
                'descuento':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total
            }

        detalle=FacturaDet.objects.filter(factura=enc)
        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes}
        return render(request,template_name,contexto)
    
    if request.method == "POST":
        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        cli=Cliente.objects.get(pk=cliente)

        if not id:
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = cli
                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("fac:factura_list")
        
        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")

        prod = Producto.objects.get(codigo=codigo)
        det = FacturaDet(
            factura = enc,
            producto = prod,
            cantidad = cantidad,
            precio = precio,
            sub_total = s_total,
            descuento = descuento,
            total = total
        )
        
        if det:
            det.save()
        
        return redirect("fac:factura_edit",id=id)

    return render(request,template_name,contexto)


class ProductoView(inv.ProductoView):
    template_name="fac/buscar_producto.html" 


def borrar_detalle_factura(request, id):
    template_name = "fac/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)


@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def cliente_add_modify(request,pk=None):
    template_name="fac/cliente_form.html"
    context = {}

    if request.method=="GET":
        context["t"]="fc"
        if not pk:
            form = ClienteForm()
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            form = ClienteForm(instance=cliente)
            context["obj"]=cliente
        context["form"] = form
    else:
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        celular = request.POST.get("celular")
        tipo = request.POST.get("tipo")
        usr = request.user

        if not pk:
            cliente = Cliente.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                celular = celular,
                tipo = tipo,
                uc=usr,
            )
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            cliente.nombres=nombres
            cliente.apellidos=apellidos
            cliente.celular = celular
            cliente.tipo = tipo
            cliente.um=usr.id

        cliente.save()
        if not cliente:
            return HttpResponse("No pude Guardar/Crear Cliente")
        
        id = cliente.id
        return HttpResponse(id)
    
    return render(request,template_name,context)
    