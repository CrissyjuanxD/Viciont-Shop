import json
import json
from django.http import JsonResponse
from django.views import View
from django.db.models import Sum
from django.utils.dateparse import parse_date
from app.sales.models import Invoice, InvoiceDetail
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Product
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice, InvoiceDetail
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q,F
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.staticfiles import finders

from django.http import HttpResponseRedirect


from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required
from django.views import View
from django.utils.decorators import method_decorator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch


from proy_sales.utils import custom_serializer, save_audit


class SaleListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'
    query = Q()  # Inicializa la consulta vacía

    def get_queryset(self):
        q1 = self.request.GET.get('q')  # Obtiene el término de búsqueda
        if q1:
            self.query.add(Q(id__icontains=q1), Q.OR)  # Busca por ID de factura
            self.query.add(Q(customer__first_name__icontains=q1), Q.OR)  # Busca por nombre del cliente
            self.query.add(Q(customer__last_name__icontains=q1), Q.OR)  # Busca por apellido del cliente
            self.query.add(Q(payment_method__icontains=q1), Q.OR)  # Busca por método de pago
            self.query.add(Q(state__icontains=q1), Q.OR)  # Busca por estado de la factura
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['permission_add'] = context['permissions'].get('add_supplier','')
        # context['create_url'] = reverse_lazy('core:supplier_create')
        return context

class SaleCreateView(PermissionMixin,CreateViewMixin, CreateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'add_invoice' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id','description','price','stock','iva__value')
        context['detail_sales'] =[]
        context['save_url'] = reverse_lazy('sales:sales_create') 
        print(context['products'])
        
        return context
    
    def post(self, request, *args, **kwargs):
        print("POST request received")
        form = self.get_form()
        print(request.POST)
        if not form.is_valid():
            messages.success(self.request, f"Error al grabar la venta!!!: {form.errors}.")
            return JsonResponse({"msg":form.errors},status=400)
        data = request.POST
        try:
            with transaction.atomic():
                sale = Invoice.objects.create(
                    customer_id=int(data['customer']),
                    payment_method_id=int(data['payment_method']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    discount=Decimal(data['discount']),
                    iva= Decimal(data['iva']),
                    total=Decimal(data['total']),
                    payment=Decimal(data['payment']),
                    change=Decimal(data['change']),
                    state='F'
                )
                details = json.loads(request.POST['detail'])
                print(details) #[{'id':'1','price':'2'},{}]
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "A")
                messages.success(self.request, f"Éxito al registrar la venta F#{sale.id}")
                return JsonResponse({"msg":"Éxito al registrar la venta Factura"},status=200)
        except Exception as ex:
              return JsonResponse({"msg":ex},status=400)


class SaleUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'change_invoice' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id','description','price','stock','iva__value')
        detail_sale =list(InvoiceDetail.objects.filter(invoice_id=self.object.id).values(
             "product","product__description","quantity","price","subtotal","iva"))
        print("detalle")
        detail_sale=json.dumps(detail_sale,default=custom_serializer)
        context['detail_sales']=detail_sale  #[{'id':1,'precio':2},{},{}]
        context['save_url'] = reverse_lazy('sales:sales_update',kwargs={"pk":self.object.id})
        print(detail_sale)
        return context
    
    def post(self, request, *args, **kwargs):
        print("POST request update")
        form = self.get_form()
        print(request.POST)
        if not form.is_valid():
            messages.success(self.request, f"Error al actualizar la venta!!!: {form.errors}.")
            return JsonResponse({"msg":form.errors},status=400)
        data = request.POST
        try:
            print("facturaId: ")
            print(self.kwargs.get('pk'))
            sale= Invoice.objects.get(id=self.kwargs.get('pk'))
           
            with transaction.atomic():
                sale.customer_id=int(data['customer'])
                sale.payment_method_id=int(data['payment_method'])
                sale.issue_date=data['issue_date']
                sale.subtotal=Decimal(data['subtotal'])
                sale.discount=Decimal(data['discount'])
                sale.iva= Decimal(data['iva'])
                sale.total=Decimal(data['total'])
                sale.payment=Decimal(data['payment'])
                sale.change=Decimal(data['change'])
                sale.state='M'
                sale.save()
                details = json.loads(request.POST['detail'])
                print(details)
                detdelete=InvoiceDetail.objects.filter(invoice_id=sale.id)
                for det in detdelete:
                    det.product.stock+= int(det.quantity)
                    det.product.save()
                detdelete.delete()
               
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantify']),
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),  
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantify']))
                save_audit(request, sale, "M")
                messages.success(self.request, f"Éxito al Modificar la venta F#{sale.id}")
                return JsonResponse({"msg":"Éxito al Modificar la venta Factura"},status=200)
        except Exception as ex:
              return JsonResponse({"msg":ex},status=400)
        

class SaleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Invoice
    template_name = 'sales/invoices/delete.html'
    success_url = reverse_lazy('sales:sales_list')
    permission_required = 'delete_invoice'

    def form_valid(self, form):
        print("Iniciando form_valid")
        self.object = self.get_object()
        print(f"Objeto a eliminar: Invoice {self.object.id}")
        
        try:
            with transaction.atomic():
                print("Iniciando transacción atómica")
                details = InvoiceDetail.objects.filter(invoice_id=self.object.id)
                print(f"Detalles encontrados: {details.count()}")
                
                for detail in details:
                    print(f"Procesando detalle: {detail.id}")
                    print(f"Producto: {detail.product}, Stock actual: {detail.product.stock}")
                    print(f"Cantidad a devolver: {detail.quantity}")
                    
                    detail.product.stock += int(detail.quantity)
                    detail.product.save()
                    
                    print(f"Nuevo stock del producto: {detail.product.stock}")
                
                print("Eliminando detalles de la factura")
                details.delete()
                
                print(f"Eliminando factura {self.object.id}")
                self.object.delete()
                
                print("Factura eliminada exitosamente")
                messages.success(self.request, f"Éxito al eliminar la venta F#{self.object.id}")
                return HttpResponseRedirect(self.get_success_url())
        except Exception as ex:
            print(f"Error durante la eliminación: {str(ex)}")
            messages.error(self.request, f"Error al eliminar la venta: {str(ex)}")
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        print("Obteniendo contexto de datos")
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        """
        Llamamos a form_valid directamente para mantener nuestra lógica personalizada.
        """
        return self.form_valid(None)
    





class AnularFacturaView(View):  
    @method_decorator(require_POST)  
    @method_decorator(permission_required('change_invoice'))  
    def post(self, request, invoice_id):  
        try:  
            with transaction.atomic():  
                invoice = Invoice.objects.get(id=invoice_id)  

                if invoice.state == 'A':  
                    return JsonResponse({'success': False, 'error': 'La factura ya está anulada'})  

                invoice.state = 'A'  
                invoice.save()  

                details = InvoiceDetail.objects.filter(invoice_id=invoice.id)  
                for detail in details:  
                    detail.product.stock += int(detail.quantity)  
                    detail.product.save()  

                return JsonResponse({'success': True})  
        except Invoice.DoesNotExist:  
            return JsonResponse({'success': False, 'error': 'Factura no encontrada'})  
        except Exception as e:  
            return JsonResponse({'success': False, 'error': str(e)})  

def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    details = InvoiceDetail.objects.filter(invoice_id=invoice_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{invoice.id}.pdf"'

    pdf_canvas = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    logo_path = finders.find('img/cucho_logof.png')
    pdf_canvas.drawImage(logo_path, (width - 100) / 2, height - 70, width=100, height=50)

    pdf_canvas.setFillColor(colors.HexColor("#800080"))  # Color morado
    pdf_canvas.setFont("Helvetica-Bold", 24)
    pdf_canvas.drawCentredString(width / 2, height - 100, "VIBES STORE")  # Bajamos el título
    pdf_canvas.setFont("Helvetica", 10)

    # Detalles del cliente y factura en formato de tabla
    customer_data = [
        ["Cliente:", invoice.customer.get_full_name],
        ["Dirección:", "LOS TRONCOS, Milagro, Ecuador"],
        ["Fecha:", invoice.issue_date.strftime('%d/%m/%Y')],
        ["Vencimiento:", (invoice.issue_date + timedelta(days=30)).strftime('%d/%m/%Y')],
        ["Factura #:", invoice.id]
    ]
    customer_table = Table(customer_data, colWidths=[100, 350])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#800080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#800080"))
    ]))
    customer_table.wrapOn(pdf_canvas, width, height)
    customer_table.drawOn(pdf_canvas, (width - 450) / 2, height - 230)  # Bajamos la tabla

    total_subtotal = sum(detail.quantity * detail.price for detail in details)
    total_iva = sum(detail.iva for detail in details)
    total_total = total_subtotal + total_iva
   # Datos de la sección de productos
    product_data = [["PRODUCTO", "PRECIO", "UNIDADES", "SUBTOTAL", "IVA", "TOTAL"]]
    for detail in details:
        subtotal = detail.quantity * detail.price
        total = subtotal + detail.iva
        product_data.append([
            detail.product.description,
            f"{detail.price:.2f}$",
            f"{detail.quantity:.2f}",
            f"{subtotal:.2f}$",
            f"{detail.iva:.2f}$",
            f"{total:.2f}$"
        ])

    product_table = Table(product_data, colWidths=[170, 60, 60, 60, 60, 60])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#800080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#800080")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
    ]))
    product_table.wrapOn(pdf_canvas, width, height)
    product_table.drawOn(pdf_canvas, (width - 480) / 2, height - 430)  # Bajamos la tabla de productos

    # Totales al final de la sección de productos
    pdf_canvas.setFillColor(colors.HexColor("#800080"))
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(30, height - 450, "TOTAL")  # No centramos los totales
    pdf_canvas.setFillColor(colors.black)
    pdf_canvas.setFont("Helvetica", 10)
    pdf_canvas.drawString(340, height - 450, f"{total_subtotal:.2f}$")
    pdf_canvas.drawString(410, height - 450, f"{total_iva:.2f}$")
    pdf_canvas.drawString(470, height - 450, f"{total_total:.2f}$")

    # Método de pago y estado
    pdf_canvas.setFont("Helvetica", 10)
    pdf_canvas.drawString(30, height - 470, f"Método de Pago: {invoice.payment_method}")  # No centramos estos elementos
    pdf_canvas.drawString(30, height - 485, f"Estado: {invoice.get_state_display()}")  # No centramos estos elementos

    pdf_canvas.save()
    return response



class SalesGraphView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Filtrar facturas del año 2024
            invoices = Invoice.objects.filter(issue_date__year=2024)

            # Agregar los datos de ventas por cliente
            sales_by_customer = invoices.values('customer__full_name').annotate(
                total_sales=Sum('total')
            ).order_by('-total_sales')

            # Preparar los datos para el gráfico
            chart_data = {
                'labels': [item['customer__full_name'] for item in sales_by_customer],
                'data': [item['total_sales'] for item in sales_by_customer]
            }

            return JsonResponse(chart_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)