from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from app.core.forms.supplier import SupplierForm
from app.core.models import Supplier
from app.security.mixins.mixins import (
    CreateViewMixin,
    DeleteViewMixin,
    ListViewMixin,
    PermissionMixin,
    UpdateViewMixin,
)
from app.security.instance.menu_module import MenuModule

class SupplierListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/suppliers/list.html'
    model = Supplier
    context_object_name = 'suppliers'
    permission_required = 'view_supplier'
    query = Q()
    suppliers = Supplier.objects.all()  # Obtén todos los proveedores
    context = {
        'suppliers': suppliers
    }

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(name__icontains=q1), Q.OR)
            self.query.add(Q(ruc__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:supplier_create')
        return context

class SupplierCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Supplier
    template_name = 'core/suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'add_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Proveedor'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        supplier = self.object
        messages.success(self.request, f"Éxito al crear al proveedor {supplier.name}.")
        return response
    
class SupplierUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Supplier
    template_name = 'core/suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'change_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Proveedor'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        supplier = self.object
        messages.success(self.request, f"Éxito al actualizar el proveedor {supplier.name}.")
        return response
    
class SupplierDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Supplier
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'delete_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Proveedor'
        context['description'] = f"¿Desea Eliminar al Proveedor: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente al proveedor {self.object.name}."
        messages.success(self.request, success_message)
        self.object.deleted = True
        self.object.save()
        
        return super().delete(request, *args, **kwargs)
