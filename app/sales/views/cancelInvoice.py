from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Product
from app.sales.forms.invoice import InvoiceForm
from app.sales.models import Invoice
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q,F

class SaleListView(PermissionMixin,ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(id = q1), Q.OR) 
            self.query.add(Q(customer__first_name__icontains=q1), Q.OR) 
            self.query.add(Q(customer__last_name__icontains=q1), Q.OR) 
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
        print(context['products'])
        # context['grabar'] = 'Grabar Proveedor'
        # context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        invoice = self.object
        messages.success(self.request, f"Éxito al registrar la ventar {invoice.id}.")
        return response

class SaleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:sales_list')
    permission_required = 'change_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        invoice = self.object
        messages.success(self.request, f"Éxito al actualizar la venta {invoice.id}.")
        return response

class SaleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Invoice
    template_name = 'sales/invoices/confirm_delete.html'
    success_url = reverse_lazy('sales:sales_list')
    context_object_name = 'invoice'
    permission_required = 'delete_invoice'

    def delete(self, request, *args, **kwargs):
        invoice = self.get_object()
        messages.success(self.request, f"Éxito al eliminar la venta {invoice.id}.")
        return super().delete(request, *args, **kwargs)



